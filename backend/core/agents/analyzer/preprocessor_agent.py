
import os
import re
import fitz  # PyMuPDF
import docx

class PreprocessorAgent:
    """Handles resume file ingestion, text extraction, and section identification."""

    def extract_text(self, file_path: str) -> str:
        """Extracts text from a resume file (PDF or DOCX)."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at: {file_path}")

        text = ""
        if file_path.lower().endswith(".pdf"):
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
        elif file_path.lower().endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file_path.lower().endswith(".txt"):
            with open(file_path, 'r') as f:
                text = f.read()
        else:
            raise ValueError("Unsupported file format. Please use PDF, DOCX, or TXT.")
        return text.strip()

    def get_page_count(self, file_path: str) -> int:
        """Gets the page count of a PDF file."""
        if file_path.lower().endswith(".pdf"):
            with fitz.open(file_path) as doc:
                return doc.page_count
        # Simple estimation for other formats
        return 1

    def identify_sections(self, resume_text: str) -> dict:
        """Identifies and extracts standard resume sections using regex."""
        sections = {}
        patterns = {
            "summary": r"(?i)(professional summary|summary|objective|about)",
            "experience": r"(?i)(work experience|experience|employment history|professional history)",
            "education": r"(?i)(education|academic background)",
            "skills": r"(?i)(skills|technical skills|key skills|core competencies)",
        }

        text_lower = resume_text.lower()
        section_positions = {key: match.start() for key, pattern in patterns.items() if (match := re.search(pattern, text_lower))}

        if not section_positions:
            return {"full_text": resume_text}

        sorted_sections = sorted(section_positions.items(), key=lambda item: item[1])

        for i, (key, start_pos) in enumerate(sorted_sections):
            end_pos = sorted_sections[i+1][1] if i + 1 < len(sorted_sections) else len(resume_text)
            header_match = re.search(patterns[key], resume_text, re.IGNORECASE)
            content_start_pos = header_match.end()
            sections[key] = resume_text[content_start_pos:end_pos].strip()

        return sections