# core/agents/optimizer_agents/context_agent.py

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.data_models import OptimizerWorkflowState, ContextOutput


# Load environment variables from the root .env file (e.g., GOOGLE_API_KEY)
load_dotenv()

class ContextExtractionAgent:
    """
    The first agent in the optimizer workflow. Its responsibility is to extract
    structured information from the raw job description text.
    """

    def __init__(self):
        """
        Initializes the agent with a configured LLM.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro", 
            temperature=0.0,
            convert_system_message_to_human=True
        )

    def execute(self, state: OptimizerWorkflowState) -> OptimizerWorkflowState:
        """
        The main execution method for this agent, designed to be a node in a LangGraph.
        """
        print("--- AGENT: Executing Context Extractor ---")

        # --- UPDATED PROMPT ---
        # The prompt is enhanced to include the new persona and task.
        prompt_template = """
        You are an expert recruitment analyst and a technical sourcer. Your task is to perform two actions:
        
        1.  **Extract Key Details:** Meticulously extract and summarize all key role details, required skills (both technical and soft), primary responsibilities, and the underlying tone from the following job description for a '{role}' position at '{company}'. Infer the experience level from keywords.
        
        2.  **Generate Boolean String:** Based on your analysis, generate a single, effective boolean search string that a recruiter would use on a platform like LinkedIn Recruiter to find qualified candidates. Combine the most critical skills and technologies with logical operators (AND, OR, NOT). Use parentheses for grouping and quotes for exact phrases (e.g., "REST APIs").

        Job Description:
        ---
        {jd}
        ---

        Based on your comprehensive analysis, provide a structured JSON output.
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)

        # LangChain will automatically adapt to the updated ContextOutput model.
        chain = prompt | self.llm.with_structured_output(ContextOutput)

        try:
            result = chain.invoke({
                "role": state.job_role,
                "company": state.company_name,
                "jd": state.job_description
            })
            
            state.context = result
            print("--- AGENT: Context Extraction Complete ---")
            print(f"Generated Boolean String: {result.boolean_search_string}")

        except Exception as e:
            print(f"ERROR in ContextExtractionAgent: {e}")
            raise
        # going to add hectic error handling later 
        
        return state