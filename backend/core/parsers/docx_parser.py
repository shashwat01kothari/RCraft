from typing import IO
import docx
from .base import ResumeParser

class DocxParser(ResumeParser):
    """Concrete implementation for parsing DOCX files."""
    def parse_to_text(self, file: IO[bytes]) -> str:
        try:
            doc = docx.Document(file)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"Error parsing DOCX file: {e}")
            return ""