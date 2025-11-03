import os
import uuid
import subprocess
from jinja2 import Environment, FileSystemLoader
from ..data_models import FinalResumeSections

def markdown_to_typst(text: str) -> str:
    """A simple converter to change Markdown lists to Typst lists."""
    if not text:
        return ""
    # A more robust implementation would handle bold, italics, etc.
    return text.replace('* ', '- ')

class TypstRenderer:
    """A utility to render structured resume data into a PDF file using Typst."""

    def __init__(self):
        """
        Initializes the renderer by creating an absolute path to the templates directory,
        making it robust and independent of the execution context.
        """
        # Get the absolute path to the current file (typst_renderer.py).
        script_path = os.path.abspath(__file__)
        # Get the directory containing this file (.../backend/core/tools).
        tools_dir = os.path.dirname(script_path)
        core_dir = os.path.dirname(tools_dir)
        self.template_dir = os.path.join(core_dir, 'utils', 'typst_templates')
        
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def render_to_pdf(self, resume_data: FinalResumeSections) -> str:
        """Takes a FinalResumeSections object, creates a .typ file, and compiles it to PDF."""
        try:
            template = self.env.get_template("resume_template.typ")
        except Exception as e:
            print(f"ERROR: Could not load 'resume_template.typ' from '{self.template_dir}'. Details: {e}")
            raise FileNotFoundError("Could not find resume_template.typ. Check the template path.")

        render_context = {
            "name": "Generated Resume", # Placeholder
            "phone": "123-456-7890",
            "email": "email@example.com",
            "linkedin_url": "linkedin.com/in/yourprofile",
            "github_url": "github.com/yourprofile",
            "summary": resume_data.summary,
            "experience": markdown_to_typst(resume_data.experience),
            "projects": markdown_to_typst(resume_data.projects),
            "skills": resume_data.skills,
            "education": markdown_to_typst(resume_data.education) if resume_data.education else None,
        }
        
        rendered_typ = template.render(render_context)

        output_dir = "generated_resumes"
        os.makedirs(output_dir, exist_ok=True)
        job_name = f"resume_{uuid.uuid4()}"
        typ_file_path = os.path.join(output_dir, f"{job_name}.typ")
        pdf_file_path = os.path.join(output_dir, f"{job_name}.pdf")

        with open(typ_file_path, "w", encoding="utf-8") as f:
            f.write(rendered_typ)

        # --- Compile the .typ file to .pdf using the Typst binary ---
        command = ["typst", "compile", typ_file_path, pdf_file_path]
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"--- TOOL: Typst compilation successful. PDF saved to {pdf_file_path} ---")
        except subprocess.CalledProcessError as e:
            print("--- TOOL: ERROR: Typst compilation failed. ---")
            print("Compiler Output:", e.stdout)
            print("Compiler Error:", e.stderr)
            raise ConnectionAbortedError("Typst compilation failed on the server.")
        finally:
            # Clean up the intermediate .typ file
            if os.path.exists(typ_file_path):
                os.remove(typ_file_path)

        return pdf_file_path