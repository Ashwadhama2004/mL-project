"""
OCR Processor for Math Mentor AI

This module handles image-to-text conversion for math problems using EasyOCR.
It extracts text from images with confidence scoring and HITL triggers.
"""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path

# Lazy imports to avoid loading heavy models until needed
_easyocr_reader = None


def get_ocr_reader():
    """Lazy load the EasyOCR reader."""
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            print("Loading EasyOCR model (this may take a moment)...")
            _easyocr_reader = easyocr.Reader(['en'], gpu=False)
            print("EasyOCR loaded successfully.")
        except ImportError:
            raise ImportError("EasyOCR not installed. Run: pip install easyocr")
    return _easyocr_reader


class OCRProcessor:
    """
    OCR Processor: Extract text from images of math problems.
    
    Uses EasyOCR for text extraction with confidence scoring.
    Triggers HITL when confidence is below threshold.
    """
    
    # Math symbol normalization mappings
    SYMBOL_MAPPINGS = {
        # Greek letters
        'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta',
        'θ': 'theta', 'λ': 'lambda', 'μ': 'mu', 'π': 'pi',
        'σ': 'sigma', 'Σ': 'sum', 'φ': 'phi', 'ω': 'omega',
        
        # Math operators
        '×': '*', '÷': '/', '−': '-', '≤': '<=', '≥': '>=',
        '≠': '!=', '±': '+-', '∞': 'infinity',
        
        # Common OCR misreads
        'O': '0',  # Often confused
        'l': '1',  # Often confused
        'I': '1',  # Often confused
    }
    
    def __init__(self, confidence_threshold: float = 0.75):
        """
        Initialize the OCR Processor.
        
        Args:
            confidence_threshold: Minimum confidence to avoid HITL (default 0.75)
        """
        self.confidence_threshold = confidence_threshold
        self._reader = None
    
    @property
    def reader(self):
        """Lazy-load the OCR reader."""
        if self._reader is None:
            self._reader = get_ocr_reader()
        return self._reader
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize extracted text for mathematical content.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Normalized text
        """
        normalized = text
        
        # Common OCR corrections for math
        corrections = [
            (r'\bSin\b', 'sin'),
            (r'\bCos\b', 'cos'),
            (r'\bTan\b', 'tan'),
            (r'\bLog\b', 'log'),
            (r'\bLn\b', 'ln'),
            (r'x\s*2\b', 'x²'),
            (r'x\s*3\b', 'x³'),
            (r'\(\s*', '('),
            (r'\s*\)', ')'),
            (r'\s*=\s*', ' = '),
            (r'\s+', ' '),  # Multiple spaces to single
        ]
        
        for pattern, replacement in corrections:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        
        return normalized.strip()
    
    def _calculate_confidence(self, results: List) -> float:
        """
        Calculate overall confidence from OCR results.
        
        Args:
            results: List of (bbox, text, confidence) tuples from EasyOCR
            
        Returns:
            Average confidence score
        """
        if not results:
            return 0.0
        
        confidences = [r[2] for r in results if len(r) >= 3]
        
        if not confidences:
            return 0.5  # Default if no confidence scores
        
        return sum(confidences) / len(confidences)
    
    def _llm_enhance_ocr(self, raw_text: str, confidence: float) -> str:
        """
        Use LLM to enhance and fix OCR-extracted math text.
        
        Args:
            raw_text: Raw OCR extracted text
            confidence: OCR confidence score
            
        Returns:
            Enhanced/corrected text
        """
        try:
            from utils.llm_client import LLMClient
            llm = LLMClient(temperature=0.1)  # Low temperature for accuracy
            
            prompt = f"""You are a math OCR correction expert. The following text was extracted from an image of a math problem using OCR, but may contain errors.

Common OCR misreadings in math:
- Division symbol (÷) often misread as "-:", ":", "-", or "+:"
- Multiplication (×) misread as "x" or "*"
- Fractions may appear as separate numbers
- Exponents may not be recognized properly

Original OCR text (confidence: {confidence:.0%}):
"{raw_text}"

Please output ONLY the corrected mathematical expression. If you see patterns like "9-3-1" that look like they should be "9-3÷1" based on context, correct them. Look for division patterns especially.

Output only the corrected math expression, nothing else:"""

            corrected = llm.generate(prompt)
            
            # Clean up LLM response
            if corrected:
                corrected = corrected.strip().strip('"').strip("'")
                # Don't use if LLM hallucinated too much
                if len(corrected) < len(raw_text) * 3:
                    return corrected
            
            return raw_text
            
        except Exception as e:
            print(f"LLM OCR enhancement failed: {e}")
            return raw_text
    
    def _combine_text(self, results: List) -> str:
        """
        Combine text from OCR results into coherent text.
        
        Args:
            results: List of (bbox, text, confidence) tuples
            
        Returns:
            Combined text string
        """
        if not results:
            return ""
        
        # Sort by vertical position (top to bottom), then horizontal (left to right)
        sorted_results = sorted(
            results,
            key=lambda r: (r[0][0][1], r[0][0][0])  # y, then x of top-left corner
        )
        
        # Combine text with spaces
        text_parts = [r[1] for r in sorted_results]
        return " ".join(text_parts)
    
    def process(self, image_input) -> Dict[str, Any]:
        """
        Process an image and extract text.
        
        Args:
            image_input: Can be:
                - str/Path: Path to image file
                - bytes: Image bytes
                - PIL.Image: PIL Image object
                - numpy.ndarray: Numpy array of image
                
        Returns:
            Dictionary containing:
                - extracted_text: The extracted text
                - confidence: Float confidence score
                - needs_human_review: Boolean
                - source: "ocr"
                - details: Additional OCR details
        """
        try:
            # Handle different input types
            if isinstance(image_input, (str, Path)):
                image_path = str(image_input)
                if not Path(image_path).exists():
                    return {
                        "extracted_text": "",
                        "confidence": 0.0,
                        "needs_human_review": True,
                        "source": "ocr",
                        "error": f"Image file not found: {image_path}"
                    }
            else:
                image_path = image_input  # Let EasyOCR handle it
            
            # Perform OCR
            results = self.reader.readtext(image_path)
            
            if not results:
                return {
                    "extracted_text": "",
                    "confidence": 0.0,
                    "needs_human_review": True,
                    "source": "ocr",
                    "error": "No text detected in image"
                }
            
            # Combine and normalize text
            raw_text = self._combine_text(results)
            normalized_text = self._normalize_text(raw_text)
            
            # Calculate confidence
            confidence = self._calculate_confidence(results)
            
            # Use LLM to enhance/fix math symbols if confidence is not very high
            # or if text contains potential math expressions
            if confidence < 0.9 or any(c in raw_text for c in '0123456789+-='):
                enhanced_text = self._llm_enhance_ocr(raw_text, confidence)
                if enhanced_text and enhanced_text != raw_text:
                    normalized_text = enhanced_text
                    # Boost confidence after LLM enhancement
                    confidence = min(confidence + 0.15, 0.95)
            
            # Determine if human review is needed
            needs_review = confidence < self.confidence_threshold
            
            return {
                "extracted_text": normalized_text,
                "raw_text": raw_text,
                "confidence": confidence,
                "needs_human_review": needs_review,
                "source": "ocr",
                "details": {
                    "num_text_regions": len(results),
                    "threshold": self.confidence_threshold,
                    "individual_confidences": [r[2] for r in results if len(r) >= 3]
                }
            }
            
        except Exception as e:
            return {
                "extracted_text": "",
                "confidence": 0.0,
                "needs_human_review": True,
                "source": "ocr",
                "error": str(e)
            }
    
    def process_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Process image from bytes.
        
        Args:
            image_bytes: Image as bytes
            
        Returns:
            OCR result dictionary
        """
        try:
            from PIL import Image
            import io
            
            image = Image.open(io.BytesIO(image_bytes))
            return self.process(image)
        except Exception as e:
            return {
                "extracted_text": "",
                "confidence": 0.0,
                "needs_human_review": True,
                "source": "ocr",
                "error": f"Failed to process image bytes: {str(e)}"
            }


def main():
    """Test the OCR Processor."""
    print("=" * 60)
    print("Math Mentor AI - OCR Processor Test")
    print("=" * 60)
    
    processor = OCRProcessor()
    
    # Create a simple test image with PIL
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a test image
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fall back to default
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 30), "Solve x^2 - 5x + 6 = 0", fill='black', font=font)
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Process
        result = processor.process_bytes(img_bytes.getvalue())
        
        print(f"\nTest Result:")
        print(f"  Extracted: {result.get('extracted_text')}")
        print(f"  Confidence: {result.get('confidence', 0):.2f}")
        print(f"  Needs Review: {result.get('needs_human_review')}")
        
    except ImportError as e:
        print(f"PIL not available for testing: {e}")
        print("OCR processor is ready but needs an actual image to test.")


if __name__ == "__main__":
    main()
