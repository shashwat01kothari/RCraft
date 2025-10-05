import os
from typing import Type
from .base import ResumeParser
from .docx_parser import DocxParser
from .pdf_parser import PdfParser

__all__ = ["get_parser"]

def get_parser(file_path: str) -> Type[ResumeParser]:
    """
    Factory function to get the correct parser instance based on file extension.
    This is the public entry point for the parsers package.
    """
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".docx":
        return DocxParser
    elif extension == ".pdf":
        return PdfParser
    else:
        raise ValueError(f"Unsupported file type: {extension}")