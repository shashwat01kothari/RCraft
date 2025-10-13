# core/agents/optimizer_agents/builder_agent.py

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.data_models import OptimizerWorkflowState

load_dotenv()

class ResumeBuilderAgent:
    """
    The fourth agent in the workflow. Acts as the "writer", generating the
    first complete draft of the resume based on the provided strategy and context.
    """

    def __init__(self):
        """
        Initializes the agent with the Flash model for high-speed content generation.
        
        A higher temperature (e.g., 0.5) is used to allow for more creative and
        natural-sounding prose, which is desirable for a writing task.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.5
        )

    def execute(self, state: OptimizerWorkflowState) -> OptimizerWorkflowState:
        """
        The main execution method for this agent, designed as a LangGraph node.
        """
        print("--- AGENT: Starting Resume Builder ---")

        # Input validation: Ensure the agent has the necessary blueprint to work from.
        if not state.context or not state.research or not state.strategy:
            raise ValueError("Cannot run BuilderAgent without context, research, and strategy.")

        # Serialize the Pydantic models to JSON strings for clear inclusion in the prompt.
        context_json = state.context.model_dump_json(indent=2)
        research_json = state.research.model_dump_json(indent=2)
        strategy_json = state.strategy.model_dump_json(indent=2)

        # Refactored to the modern, message-based prompt structure.
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an expert resume writer and career coach. Your task is to write the complete text for a professional resume.
                
                **Your Rules:**
                - You must follow the master plan provided in the [Resume Strategy]. Adhere strictly to the requested sections, section order, tone, and guidelines.
                - You must weave the keywords, skills, and responsibilities from the [Job Context] into the content naturally.
                - You must adopt the tone and incorporate the key phrases from the [Company Research Insights] to make the resume resonate with the company's culture.
                - Write 3-5 achievement-driven, quantified bullet points for each experience or project.
                - Start each bullet point with a strong action verb.
                - Ensure the professional summary is a powerful, concise pitch.
                - Your final output must be a single, well-formatted Markdown string. Use '##' for section headings (e.g., '## Professional Summary') and '*' for bullet points."""
            ),
            (
                "human",
                """Please generate the resume content using the following data:

                **[Resume Strategy]**
                {strategy}

                **[Job Context]**
                {context}

                **[Company Research Insights]**
                {research}
                """
            )
        ])
        
        # The output parser ensures we get a clean string back from the LLM call.
        output_parser = StrOutputParser()
        
        chain = prompt | self.llm | output_parser

        try:
            # Invoke the chain with all the necessary context.
            draft_text = chain.invoke({
                "strategy": strategy_json,
                "context": context_json,
                "research": research_json
            })
            
            # Update the workflow state with the generated draft.
            state.draft_resume_text = draft_text
            print("--- AGENT: Resume Builder Complete ---")

        except Exception as e:
            print(f"ERROR in ResumeBuilderAgent: {e}")
            raise

        return state