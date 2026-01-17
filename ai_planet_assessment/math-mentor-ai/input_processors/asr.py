"""
ASR Processor for Math Mentor AI

This module handles audio-to-text conversion for math problems.
Uses Google Gemini for audio transcription (primary) with Whisper as fallback.
It transcribes audio with confidence scoring, normalizes math phrases, and triggers HITL.
"""

import re
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile
import os
import base64

# Lazy imports to avoid loading heavy models until needed
_whisper_model = None


def get_whisper_model(model_size: str = "base"):
    """Lazy load the Whisper model (fallback)."""
    global _whisper_model
    if _whisper_model is None:
        try:
            import whisper
            print(f"Loading Whisper model ({model_size})...")
            _whisper_model = whisper.load_model(model_size)
            print("Whisper loaded successfully.")
        except ImportError:
            print("Whisper not available. Using Gemini-only mode.")
            return None
        except Exception as e:
            print(f"Whisper failed to load: {e}")
            return None
    return _whisper_model


class ASRProcessor:
    """
    ASR Processor: Transcribe audio of math problems.
    
    Uses OpenAI Whisper for speech-to-text with math phrase normalization.
    Triggers HITL when transcript is uncertain.
    """
    
    # Math phrase normalizations (speech to symbols)
    MATH_PHRASES = {
        # Basic operations
        r'\bplus\b': '+',
        r'\bminus\b': '-',
        r'\btimes\b': '×',
        r'\bmultiplied by\b': '×',
        r'\bdivided by\b': '÷',
        r'\bover\b': '/',
        r'\bequals\b': '=',
        r'\bis equal to\b': '=',
        
        # Powers
        r'\bsquared\b': '²',
        r'\bcubed\b': '³',
        r'\bto the power of (\d+)\b': '^\\1',
        r'\braised to\b': '^',
        
        # Roots
        r'\bsquare root of\b': '√',
        r'\bcube root of\b': '∛',
        r'\broot of\b': '√',
        
        # Trig functions
        r'\bsine of\b': 'sin(',
        r'\bcosine of\b': 'cos(',
        r'\btangent of\b': 'tan(',
        r'\bsine\b': 'sin',
        r'\bcosine\b': 'cos',
        r'\btangent\b': 'tan',
        r'\binverse sine\b': 'sin⁻¹',
        r'\binverse cosine\b': 'cos⁻¹',
        r'\binverse tangent\b': 'tan⁻¹',
        r'\barcsin\b': 'sin⁻¹',
        r'\barccos\b': 'cos⁻¹',
        r'\barctan\b': 'tan⁻¹',
        
        # Other functions
        r'\blogarithm of\b': 'log(',
        r'\blog of\b': 'log(',
        r'\bnatural log of\b': 'ln(',
        r'\bln of\b': 'ln(',
        r'\bexponential of\b': 'exp(',
        r'\be to the\b': 'e^',
        
        # Constants
        r'\bpi\b': 'π',
        r'\binfinity\b': '∞',
        r'\btheta\b': 'θ',
        r'\balpha\b': 'α',
        r'\bbeta\b': 'β',
        r'\bgamma\b': 'γ',
        r'\bdelta\b': 'δ',
        
        # Comparisons
        r'\bless than or equal to\b': '≤',
        r'\bgreater than or equal to\b': '≥',
        r'\bless than\b': '<',
        r'\bgreater than\b': '>',
        r'\bnot equal to\b': '≠',
        
        # Calculus
        r'\bintegral of\b': '∫',
        r'\bderivative of\b': 'd/dx(',
        r'\bd by dx of\b': 'd/dx(',
        r'\blimit as\b': 'lim',
        r'\bsummation of\b': 'Σ',
        r'\bsum of\b': 'Σ',
        
        # Variables (spoken)
        r'\bx squared\b': 'x²',
        r'\bx cubed\b': 'x³',
        r'\by squared\b': 'y²',
        r'\by cubed\b': 'y³',
    }
    
    def __init__(
        self,
        model_size: str = "base",
        confidence_threshold: float = 0.75
    ):
        """
        Initialize the ASR Processor.
        
        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
            confidence_threshold: Minimum confidence to avoid HITL
        """
        self.model_size = model_size
        self.confidence_threshold = confidence_threshold
        self._model = None
    
    @property
    def model(self):
        """Lazy-load the Whisper model (fallback)."""
        if self._model is None:
            self._model = get_whisper_model(self.model_size)
        return self._model
    
    def _transcribe_with_gemini(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Transcribe audio using Google Gemini's audio capabilities.
        
        Args:
            audio_bytes: Audio file bytes
            
        Returns:
            Dictionary with transcript and confidence
        """
        try:
            from utils.llm_client import LLMClient
            import google.generativeai as genai
            import os
            from dotenv import load_dotenv
            
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
            
            if not api_key:
                return {"success": False, "error": "No API key"}
            
            genai.configure(api_key=api_key)
            
            # Create a temp file to save audio
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_file.write(audio_bytes)
            temp_file.close()
            
            try:
                # Upload file to Gemini
                audio_file = genai.upload_file(temp_file.name)
                
                # Use Gemini to transcribe
                model = genai.GenerativeModel("gemini-2.0-flash")
                
                prompt = """Listen to this audio carefully and transcribe it exactly.
The audio contains a math problem being spoken. Convert any spoken math to proper notation:
- "squared" → ²
- "cubed" → ³  
- "divided by" → ÷
- "times" → ×
- "plus" → +
- "minus" → -
- "equals" → =

Output ONLY the transcribed math problem, nothing else."""

                response = model.generate_content([prompt, audio_file])
                
                transcript = response.text.strip() if response.text else ""
                
                # Clean up
                genai.delete_file(audio_file.name)
                
                return {
                    "success": True,
                    "transcript": transcript,
                    "confidence": 0.85 if transcript else 0.0
                }
                
            finally:
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
                    
        except Exception as e:
            print(f"Gemini audio transcription failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _normalize_math_phrases(self, text: str) -> str:
        """
        Convert spoken math phrases to symbols.
        
        Args:
            text: Transcribed text
            
        Returns:
            Normalized text with math symbols
        """
        normalized = text.lower()
        
        for pattern, replacement in self.MATH_PHRASES.items():
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        
        # Clean up spacing
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = re.sub(r'\s*([+\-×÷=<>])\s*', r' \1 ', normalized)
        
        return normalized.strip()
    
    def _estimate_confidence(self, result: Dict) -> float:
        """
        Estimate confidence from Whisper result.
        
        Whisper doesn't provide per-word confidence directly,
        so we estimate based on other factors.
        
        Args:
            result: Whisper transcription result
            
        Returns:
            Estimated confidence score
        """
        text = result.get("text", "")
        
        if not text or len(text.strip()) < 5:
            return 0.3
        
        confidence = 0.8  # Base confidence
        
        # Reduce confidence for very short transcripts
        if len(text) < 20:
            confidence -= 0.1
        
        # Reduce confidence if there are many numbers (OCR might be better)
        num_count = len(re.findall(r'\d+', text))
        if num_count > 5:
            confidence -= 0.05
        
        # Increase confidence for longer, coherent sentences
        word_count = len(text.split())
        if word_count > 10:
            confidence += 0.05
        
        # Check for common math words (good sign)
        math_words = ['solve', 'find', 'calculate', 'what', 'if', 'equation', 'value']
        for word in math_words:
            if word in text.lower():
                confidence += 0.02
        
        return min(max(confidence, 0.0), 1.0)
    
    def process(self, audio_input) -> Dict[str, Any]:
        """
        Process audio and transcribe to text.
        
        Args:
            audio_input: Can be:
                - str/Path: Path to audio file (WAV, MP3, etc.)
                - bytes: Audio bytes
                
        Returns:
            Dictionary containing:
                - transcript: The transcribed text
                - normalized_transcript: With math symbols
                - confidence: Float confidence score
                - needs_human_review: Boolean
                - source: "asr"
        """
        try:
            # Handle different input types
            audio_path = None
            temp_file = None
            
            if isinstance(audio_input, (str, Path)):
                audio_path = str(audio_input)
                if not Path(audio_path).exists():
                    return {
                        "transcript": "",
                        "confidence": 0.0,
                        "needs_human_review": True,
                        "source": "asr",
                        "error": f"Audio file not found: {audio_path}"
                    }
            elif isinstance(audio_input, bytes):
                # Save bytes to temp file
                temp_file = tempfile.NamedTemporaryFile(
                    suffix=".wav",
                    delete=False
                )
                temp_file.write(audio_input)
                temp_file.close()
                audio_path = temp_file.name
            else:
                return {
                    "transcript": "",
                    "confidence": 0.0,
                    "needs_human_review": True,
                    "source": "asr",
                    "error": f"Unsupported audio input type: {type(audio_input)}"
                }
            
            try:
                # Transcribe with Whisper
                result = self.model.transcribe(audio_path)
                
                raw_transcript = result.get("text", "").strip()
                
                if not raw_transcript:
                    return {
                        "transcript": "",
                        "confidence": 0.0,
                        "needs_human_review": True,
                        "source": "asr",
                        "error": "No speech detected in audio"
                    }
                
                # Normalize math phrases
                normalized = self._normalize_math_phrases(raw_transcript)
                
                # Estimate confidence
                confidence = self._estimate_confidence(result)
                
                # Determine if human review is needed
                needs_review = confidence < self.confidence_threshold
                
                return {
                    "transcript": normalized,
                    "raw_transcript": raw_transcript,
                    "confidence": confidence,
                    "needs_human_review": needs_review,
                    "source": "asr",
                    "details": {
                        "language": result.get("language"),
                        "threshold": self.confidence_threshold
                    }
                }
                
            finally:
                # Clean up temp file
                if temp_file and os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
                    
        except Exception as e:
            return {
                "transcript": "",
                "confidence": 0.0,
                "needs_human_review": True,
                "source": "asr",
                "error": str(e)
            }
    
    def process_bytes(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Process audio from bytes.
        
        Uses Gemini for transcription (primary), with Whisper as fallback.
        
        Args:
            audio_bytes: Audio as bytes
            
        Returns:
            ASR result dictionary
        """
        # Try Gemini first (works on Streamlit Cloud)
        gemini_result = self._transcribe_with_gemini(audio_bytes)
        
        if gemini_result.get("success") and gemini_result.get("transcript"):
            transcript = gemini_result["transcript"]
            normalized = self._normalize_math_phrases(transcript)
            confidence = gemini_result.get("confidence", 0.85)
            
            return {
                "transcript": normalized,
                "raw_transcript": transcript,
                "confidence": confidence,
                "needs_human_review": confidence < self.confidence_threshold,
                "source": "asr",
                "method": "gemini",
                "details": {
                    "threshold": self.confidence_threshold
                }
            }
        
        # Fallback to Whisper if available
        print("Gemini transcription failed, trying Whisper fallback...")
        try:
            return self.process(audio_bytes)
        except Exception as e:
            # If both fail, return error
            error_msg = gemini_result.get("error", str(e))
            return {
                "transcript": "",
                "confidence": 0.0,
                "needs_human_review": True,
                "source": "asr",
                "error": f"Transcription failed: {error_msg}"
            }


def main():
    """Test the ASR Processor."""
    print("=" * 60)
    print("Math Mentor AI - ASR Processor Test")
    print("=" * 60)
    
    # Test phrase normalization without loading Whisper
    processor = ASRProcessor.__new__(ASRProcessor)
    processor.confidence_threshold = 0.75
    
    test_phrases = [
        "solve x squared plus 5 x minus 6 equals 0",
        "find the derivative of sine of x",
        "what is the integral of x squared",
        "calculate square root of 16 plus 9",
    ]
    
    print("\nPhrase Normalization Test:")
    for phrase in test_phrases:
        normalized = processor._normalize_math_phrases(phrase)
        print(f"  '{phrase}'")
        print(f"  → '{normalized}'")
        print()
    
    print("\nNote: Full ASR test requires audio file and Whisper model.")


if __name__ == "__main__":
    main()
