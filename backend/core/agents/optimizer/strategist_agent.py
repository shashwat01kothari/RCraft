# core/agents/optimizer_agents/strategist_agent.py

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.data_models import OptimizerWorkflowState, StrategyOutput

load_dotenv()

class ResumeStrategistAgent:
    """
    The third agent in the workflow. Acts as the "brain" of the operation,
    creating a high-level plan for the resume's structure, content, and tone.
    """

    def __init__(self):
        """
        Initializes the agent with the Pro model for its superior strategic
        reasoning and decision-making capabilities.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.3
        )



    def execute(self, state: OptimizerWorkflowState) -> OptimizerWorkflowState:
        """
        The main execution method for this agent, designed as a LangGraph node.
        """
        print("--- AGENT: Starting Resume Strategist ---")

        # Input validation: Ensure the required data from previous agents exists.
        if not state.context or not state.research:
            raise ValueError("Cannot run StrategistAgent without context and research from previous agents.")

        # Serialize the Pydantic models to JSON strings to pass into the prompt.
        context_json = state.context.model_dump_json(indent=2)
        research_json = state.research.model_dump_json(indent=2)

        # Refactored to the modern, message-based prompt structure.
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an expert career strategist and resume architect. Your task is to design a high-level plan 
                for a winning resume based on the detailed context and company research provided.

                **Your Strategic Task:**
                Based on ALL the information provided in the user's message, create a strategic blueprint for the resume.
                1.  **Sections:** Decide which standard resume sections are necessary (e.g., "Professional Summary", "Experience", "Projects", "Skills", "Education"). For a candidate with less experience but strong projects, you might choose to place "Projects" before "Experience".
                2.  **Priority Order:** Explicitly state the top 3-4 sections that should appear first to maximize impact for this specific role and company.
                3.  **Tone of Voice:** Define the precise tone the resume should adopt. Synthesize the tone from the job context and the company style from the research into a single, actionable directive (e.g., "A confident, results-driven professional with a collaborative and innovative spirit").
                4.  **Guidelines:** Provide a list of 3-5 critical, high-level instructions for the resume writer. These should be strategic directives, not just generic advice (e.g., "Highlight experience with 'scalable systems' to align with the company's focus on growth", "Weave the key phrase 'responsible AI' into the project descriptions").

                You MUST provide your final strategy as a structured JSON output."""
            ),
            (
                "human",
                """Please create the strategic blueprint using the following data:

                **[Job Context]**
                This is the structured information extracted from the job description:
                {context}

                **[Company Research Insights]**
                This is the intelligence gathered about the company's culture and values:
                {research}
                """
            )
        ])
        
        # The chain with structured output remains a best practice.
        chain = prompt | self.llm.with_structured_output(StrategyOutput)

        try:
            result = chain.invoke({
                "context": context_json,
                "research": research_json
            })
            
            # Update the workflow state with the new strategy.
            state.strategy = result
            print("--- AGENT: Resume Strategist Complete ---")

        except Exception as e:
            print(f"ERROR in ResumeStrategistAgent: {e}")
            raise

        return state
    
