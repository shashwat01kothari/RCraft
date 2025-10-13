# core/agents/optimizer_agents/reviewer_agent.py

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.data_models import OptimizerWorkflowState, ReviewerOutput

load_dotenv()

class FinalReviewerAgent:
    """
    The final agent in the workflow. It performs a quality assurance check on the
    optimized resume and structures it into the final output format.
    """

    def __init__(self):
        """
        Initializes the agent with the Flash model for high-speed proofreading,
        formatting, and final structuring.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.0 # Low temperature for factual, non-creative checks
        )

    

    def execute(self, state: OptimizerWorkflowState) -> OptimizerWorkflowState:
        """
        The main execution method for this agent, designed as the final node in a LangGraph.
        """
        print("--- AGENT: Starting Final Reviewer ---")

        # Input validation
        if not state.optimized_resume_text:
            raise ValueError("Cannot run FinalReviewerAgent without optimized resume text.")
            
        if not state.strategy:
            raise ValueError("Cannot run FinalReviewerAgent without the resume strategy.")

        # Refactored to the modern, message-based prompt structure.
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an expert proofreader and resume formatter. Your task is to perform a final quality check on the provided resume text and then structure it for final output.

                **Your Final Review Tasks:**
                1.  **Proofread:** Check for any remaining grammatical errors, typos, or awkward phrasing. Make minor corrections to improve flow.
                2.  **Consistency Check:** Ensure the tone of voice is consistent throughout all sections and aligns with the provided strategy.
                3.  **Readability Score:** Assign a readability score between 0.0 (very difficult to read) and 1.0 (very easy to read).
                4.  **Structure the Output:** Parse the final, polished Markdown text into the specified JSON schema, separating the content by its section headers (## Summary, ## Experience, etc.).

                You MUST provide your final output as a structured JSON object."""
            ),
            (
                "human",
                """Please perform the final review and structuring on the resume text below.

                **[Resume Strategy]**
                The resume was built according to this plan. Ensure the final text still aligns with it.
                {strategy}

                **[Optimized Resume Text]**
                ---
                {optimized_resume}
                ---
                """
            )
        ])
        
        # The chain with structured output is the key to reliable JSON.
        chain = prompt | self.llm.with_structured_output(ReviewerOutput)

        try:
            # Invoke the chain with the optimized resume text and the original strategy.
            final_report = chain.invoke({
                "strategy": state.strategy.model_dump_json(indent=2),
                "optimized_resume": state.optimized_resume_text
            })
            
            # This is the final state of our workflow.
            state.final_report = final_report
            print("--- AGENT: Final Review Complete. Workflow finished. ---")

        except Exception as e:
            print(f"ERROR in FinalReviewerAgent: {e}")
            raise

        return state
    
