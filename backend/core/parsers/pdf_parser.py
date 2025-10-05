# core/parsers/pdf_parser.py
from typing import IO
from PyPDF2 import PdfReader
from .base import ResumeParser



class PdfParser(ResumeParser):
    """Concrete implementation for parsing PDF files."""
    def parse_to_text(self, file: IO[bytes]) -> str:
        try:
            reader = PdfReader(file)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except Exception as e:
            print(f"Error parsing PDF file: {e}")
            return ""