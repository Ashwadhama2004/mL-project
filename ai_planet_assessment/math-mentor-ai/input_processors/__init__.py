# Math Mentor AI - Input Processors Package
"""
Multimodal input processing for OCR, ASR, and text inputs.
All processors output standardized format for the Parser Agent.
"""

from .ocr import OCRProcessor
from .asr import ASRProcessor
from .text import TextProcessor

__all__ = [
    'OCRProcessor',
    'ASRProcessor',
    'TextProcessor'
]
