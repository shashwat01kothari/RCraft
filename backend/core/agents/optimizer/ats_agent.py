# core/agents/optimizer_agents/ats_agent.py

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.data_models import OptimizerWorkflowState

load_dotenv()

class ATSOptimizerAgent:
    """
    The fifth agent in the workflow. Acts as a "technical editor", refining the
    resume draft to maximize keyword and semantic alignment with the job description.
    """

    def __init__(self):
        """
        Initializes the agent with the Pro model for its superior reasoning
        and nuanced text manipulation capabilities.
        
        A low temperature is used to ensure the edits are focused and relevant,
        avoiding unnecessary creative changes.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.2
        )
    def execute(self, state: OptimizerWorkflowState) -> OptimizerWorkflowState:
        """
        The main execution method for this agent, designed as a LangGraph node.
        """
        print("--- AGENT: Starting ATS Optimizer ---")

        # Input validation: Ensure the agent has the necessary data to work.
        if not state.draft_resume_text or not state.context:
            raise ValueError("Cannot run ATSOptimizerAgent without a draft resume and job context.")

        context_json = state.context.model_dump_json(indent=2)

        # Refactored to the modern, message-based prompt structure.
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an expert ATS analyst and a professional resume editor. Your task is to refine the provided [Draft Resume] to maximize its alignment with the [Job Context].

                **Your Core Directives:**
                1.  **Integrate Missing Keywords:** Subtly and naturally weave in any critical skills, responsibilities, or keywords from the [Job Context] that are missing from the draft.
                2.  **Semantic Alignment:** Rewrite phrases to more closely match the language and tone specified in the [Job Context]. For example, if the JD emphasizes "leading projects", change "worked on projects" to "led projects".
                3.  **Preserve Quality:** Do not simply list keywords. The final text must flow naturally and be grammatically perfect. Retain all quantified achievements and the core message of the draft.
                4.  **Add & Enhance Quantification:** Where achievements are mentioned but not quantified, add plausible metrics. Enhance existing metrics to be more impactful. For example, change "improved query latency" to "improved query latency by 150ms".
                
                Your final output must be only the full, rewritten, and optimized resume text as a single Markdown string."""
            ),
            (
                "human",
                """Please refine the resume draft below using the provided job context.

                **[Job Context]**
                This is the ground truth for what the recruiter is looking for:
                {job_context}

                **[Draft Resume]**
                This is the current version of the resume that needs optimization:
                ---
                {draft_resume}
                ---
                """
            )
        ])
        
        output_parser = StrOutputParser()
        
        chain = prompt | self.llm | output_parser

        try:
            # Invoke the chain with the draft and the context.
            optimized_text = chain.invoke({
                "job_context": context_json,
                "draft_resume": state.draft_resume_text
            })
            
            # Update the workflow state with the newly optimized text.
            state.optimized_resume_text = optimized_text
            print("--- AGENT: ATS Optimization Complete ---")

        except Exception as e:
            print(f"ERROR in ATSOptimizerAgent: {e}")
            raise

        return state