# core/agents/optimizer_agents/research_agent.py

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.data_models import OptimizerWorkflowState, ResearchOutput
from backend.core.tools.web_search_tool import WebSearchTool

load_dotenv()

class ResearchAgent:
    """
    The second agent in the workflow. It enriches the context by performing
    web searches to understand the target company's culture, mission, and style.
    """

    def __init__(self):
        """
        Initializes the agent with the Flash model for speed and cost-efficiency,
        and an instance of the WebSearchTool.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2
        )
        self.search_tool = WebSearchTool()

    def execute(self, state: OptimizerWorkflowState) -> OptimizerWorkflowState:
        """
        The main execution method for this agent, designed as a LangGraph node.
        """
        print("--- AGENT: Starting Research & Insight ---")

        # Input validation: Ensure the previous agent has run successfully.
        if not state.context:
            raise ValueError("Cannot run ResearchAgent without context from the previous agent.")

        # 1. Formulate targeted search queries based on the initial context.
        company = state.context.company
        role = state.context.role
        
        # 2. Perform robust web searches with a fallback mechanism.
        culture_query = f"{company} company culture and values"
        mission_query = f"{company} mission statement"
        specific_role_query = f"what it's like to work as a {role} at {company}"

        culture_results = self.search_tool.search(culture_query)
        mission_results = self.search_tool.search(mission_query)
        role_results = self.search_tool.search(specific_role_query)
        
        # Fallback Logic: If the highly specific query failed, try a broader one.
        if "No information found" in role_results:
            print("--- AGENT: Specific role search failed. Trying a broader query. ---")
            broader_role_query = f"employee reviews and work environment at {company}"
            role_results = self.search_tool.search(broader_role_query)

        # Aggregate all successful search results into a single context block.
        search_results = "\n\n".join([culture_results, mission_results, role_results])

        # 3. Define the prompt using the modern, message-based structure.
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a business intelligence analyst. Your task is to analyze the provided web search results 
                about a company and synthesize insights that would be useful for a job candidate.

                Focus on the following:
                - **Company Style:** Is their language formal, visionary, playful, technical?
                - **Mission Focus:** What are the core themes of their mission or values?
                - **Key Phrases:** Are there any recurring, important phrases or jargon they use?
                
                You MUST provide your final analysis as a structured JSON object."""
            ),
            (
                "human",
                """Please analyze the following web search results for the company '{company}' in the context of a '{role}' candidate.

                Web Search Results:
                ---
                {search_results}
                ---"""
            )
        ])
        
        # 4. Create and invoke the chain to get structured output.
        chain = prompt | self.llm.with_structured_output(ResearchOutput)

        try:
            result = chain.invoke({
                "company": company,
                "role": role,
                "search_results": search_results
            })
            
            # 5. Update the workflow state.
            state.research = result
            print("--- AGENT: Research & Insight Complete ---")

        except Exception as e:
            print(f"ERROR in ResearchAgent: {e}")
            raise

        return state
