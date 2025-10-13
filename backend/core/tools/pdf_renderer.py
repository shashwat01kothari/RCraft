# core/tools/pdf_renderer.py
import os
import uuid
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from ..data_models import FinalResumeSections

def markdown_to_html(text: str) -> str:
    """A simple converter to change Markdown lists to HTML lists."""
    if not text:
        return ""
    lines = text.strip().split('\n')
    html_lines = []
    in_list = False
    for line in lines:
        line = line.strip()
        if line.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            item_content = line[2:].strip()
            html_lines.append(f'<li>{item_content}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if line:
                html_lines.append(f'<p>{line}</p>')
    if in_list:
        html_lines.append('</ul>')
    return "".join(html_lines)

class PdfRenderer:
    """A utility to render structured resume data into a PDF file using WeasyPrint."""

    def __init__(self, template_dir="core/utils/latex_style"):
        script_path = os.path.abspath(__file__)
        tools_dir = os.path.dirname(script_path)
        core_dir = os.path.dirname(tools_dir)
        template_dir = os.path.join(core_dir, 'utils', 'latex_style')

        # 5. Initialize Jinja2 with this new, correct, absolute path.
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # 6. The stylesheet path also needs to use this absolute path.
        self.stylesheet_path = os.path.join(template_dir, "style.css")

    def render_to_pdf(self, resume_data: FinalResumeSections) -> str:
        """Takes a FinalResumeSections object, creates an HTML string, and renders it to a PDF."""
        print("--- TOOL: Rendering resume to PDF via WeasyPrint ---")
        template = self.env.get_template("template.html")
        
        # Prepare the data for rendering by converting Markdown to HTML
        render_context = {
            "name": "Generated Resume", # You could pass this in from user data later
            "phone": "123-456-7890",
            "email": "email@example.com",
            "linkedin_url": "linkedin.com/in/yourprofile",
            "github_url": "github.com/yourprofile",
            "summary": resume_data.summary,
            "experience": markdown_to_html(resume_data.experience),
            "projects": markdown_to_html(resume_data.projects),
            "skills": resume_data.skills,
            "education": markdown_to_html(resume_data.education) if resume_data.education else None
        }

        rendered_html = template.render(render_context)

        output_dir = "generated_resumes"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"resume_{uuid.uuid4()}.pdf"
        file_path = os.path.join(output_dir, filename)

        html = HTML(string=rendered_html)
        css = CSS(self.stylesheet_path)
        html.write_pdf(file_path, stylesheets=[css])
        
        print(f"--- TOOL: PDF generation successful. Saved to {file_path} ---")
        return file_path