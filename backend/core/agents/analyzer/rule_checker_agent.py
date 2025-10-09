import re

class RuleCheckerAgent:
    def check_rules(self, resume_text, page_count):
        """Performs deterministic checks on the resume."""
        feedback = {}
        score_modifiers = {} # Can be used to adjust scores later

        # 1. Resume Length
        if page_count > 2:
            feedback["length"] = "Resume is longer than the recommended 2 pages. Aim for 1 page if you have less than 10 years of experience."
        elif page_count > 1:
            feedback["length"] = "Resume is 2 pages long. This is acceptable for experienced professionals, but ensure all content is relevant."
        else:
            feedback["length"] = "Resume length is good (1 page)."

        # 2. Contact Information
        contact_feedback = []

        if re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", resume_text):
            contact_feedback.append("Email address found and appears valid.")
        else:
            contact_feedback.append("Could not find an email address. Ensure it's present and correctly formatted.")
        if re.search(r"\+?\d{1,3}?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}", resume_text):
            contact_feedback.append("Phone number detected.")
        else:
            contact_feedback.append("Could not find a phone number. Include a valid contact number with country code if applicable.")

        if re.search(r"(https?:\/\/)?(www\.)?linkedin\.com\/(in|pub)\/[A-Za-z0-9_-]+\/?", resume_text, re.IGNORECASE):
            contact_feedback.append("LinkedIn profile link found.")

        if re.search(r"(https?:\/\/)?(www\.)?github\.com\/[A-Za-z0-9_-]+\/?", resume_text, re.IGNORECASE):
            contact_feedback.append("GitHub profile link found.")

        feedback["contact_info"] = " ".join(contact_feedback)

        # 3. Dense Text Blocks
        paragraphs = [p for p in resume_text.split('\n') if p.strip()]
        dense_blocks = [p for p in paragraphs if len(p.split('\n')) > 4]
        if dense_blocks:
            feedback["readability"] = "Some paragraphs are longer than 4 lines, which can be difficult to read. Consider using bullet points."

        return feedback