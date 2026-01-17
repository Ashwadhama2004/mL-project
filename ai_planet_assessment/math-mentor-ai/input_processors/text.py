"""
Text Processor for Math Mentor AI

This module handles direct text input validation and cleaning.
It provides a simple pass-through with basic validation.
"""

import re
from typing import Dict, Any


class TextProcessor:
    """
    Text Processor: Handle direct text input.
    
    Provides basic validation and cleaning for typed math problems.
    Always returns high confidence since user typed it directly.
    """
    
    def __init__(self, min_length: int = 5):
        """
        Initialize the Text Processor.
        
        Args:
            min_length: Minimum text length to consider valid
        """
        self.min_length = min_length
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize input text.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text
        """
        cleaned = text.strip()
        
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Fix common typing patterns
        cleaned = re.sub(r'\s*=\s*', ' = ', cleaned)
        cleaned = re.sub(r'\s*\+\s*', ' + ', cleaned)
        cleaned = re.sub(r'\s*-\s*', ' - ', cleaned)
        cleaned = re.sub(r'\s*\*\s*', ' * ', cleaned)
        cleaned = re.sub(r'\s*/\s*', ' / ', cleaned)
        
        # Clean up extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned.strip()
    
    def _validate_text(self, text: str) -> tuple:
        """
        Validate the input text.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text:
            return False, "Empty input"
        
        if len(text) < self.min_length:
            return False, f"Input too short (minimum {self.min_length} characters)"
        
        # Check if it looks like a math problem
        math_indicators = [
            r'\d',           # Has numbers
            r'[a-zA-Z]',     # Has letters
            r'[+\-*/=<>]',   # Has operators
            r'(solve|find|calculate|what|compute|evaluate|simplify|prove)',  # Math verbs
        ]
        
        has_math_content = any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in math_indicators
        )
        
        if not has_math_content:
            return False, "Input doesn't appear to be a math problem"
        
        return True, None
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        Process text input.
        
        Args:
            text: The input text
            
        Returns:
            Dictionary containing:
                - clean_text: Cleaned version
                - confidence: Always 1.0 for direct text
                - needs_human_review: False
                - source: "text"
        """
        # Clean the text
        cleaned = self._clean_text(text)
        
        # Validate
        is_valid, error = self._validate_text(cleaned)
        
        if not is_valid:
            return {
                "clean_text": cleaned,
                "confidence": 0.5,
                "needs_human_review": True,
                "source": "text",
                "error": error
            }
        
        return {
            "clean_text": cleaned,
            "raw_text": text,
            "confidence": 1.0,
            "needs_human_review": False,
            "source": "text"
        }


def main():
    """Test the Text Processor."""
    print("=" * 60)
    print("Math Mentor AI - Text Processor Test")
    print("=" * 60)
    
    processor = TextProcessor()
    
    test_inputs = [
        "Solve x^2 - 5x + 6 = 0",
        "  Find   the   derivative  of   sin(x)  ",
        "What is 2 + 2?",
        "hi",  # Too short
        "Hello world",  # Not a math problem
        "",  # Empty
    ]
    
    for text in test_inputs:
        result = processor.process(text)
        print(f"\nInput: '{text}'")
        print(f"  Clean: '{result.get('clean_text')}'")
        print(f"  Confidence: {result.get('confidence')}")
        print(f"  Needs Review: {result.get('needs_human_review')}")
        if result.get('error'):
            print(f"  Error: {result.get('error')}")


if __name__ == "__main__":
    main()
