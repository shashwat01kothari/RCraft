from abc import ABC, abstractmethod
from typing import IO

class ResumeParser(ABC):
    """Abstract Base Class defining the interface for all resume parsers."""

    @abstractmethod
    def parse_to_text(self, file: IO[bytes]) -> str:
        """Extracts raw text from a file-like object."""
        pass