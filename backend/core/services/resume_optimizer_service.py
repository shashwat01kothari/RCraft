
from langgraph.graph import StateGraph, END

from backend.core.agents.optimizer.ats_agent import ATSOptimizerAgent
from backend.core.agents.optimizer.builder_agent import ResumeBuilderAgent
from backend.core.agents.optimizer.context_extraction_agent import ContextExtractionAgent
from backend.core.agents.optimizer.research_agent import ResearchAgent
from backend.core.agents.optimizer.reviewer_agent import FinalReviewerAgent
from backend.core.agents.optimizer.strategist_agent import ResumeStrategistAgent
from backend.core.data_models import OptimizerWorkflowState, ReviewerOutput

class ResumeOptimizerService:
    """
    Orchestrates the multi-agent resume optimization workflow using LangGraph.

    This service initializes and compiles a state graph where each node is an
    agent. The compiled graph is then used to process user requests, ensuring a
    consistent, sequential execution of the resume generation pipeline.
    """

    def __init__(self):
        """
        Initializes the service by building and compiling the LangGraph workflow.
        This one-time setup ensures the service is ready to handle requests efficiently.
        """
        # 1. Instantiate all agents that will act as nodes in our graph.
        context_agent = ContextExtractionAgent()
        research_agent = ResearchAgent()
        strategist_agent = ResumeStrategistAgent()
        builder_agent = ResumeBuilderAgent()
        optimizer_agent = ATSOptimizerAgent()
        reviewer_agent = FinalReviewerAgent()

        # 2. Define the StateGraph with our Pydantic model as the central state.
        workflow = StateGraph(OptimizerWorkflowState)

        # 3. Add each agent's `execute` method as a node in the graph.
        #    Each node is given a unique identifier string.
        workflow.add_node("context_extractor", context_agent.execute)
        workflow.add_node("researcher", research_agent.execute)
        workflow.add_node("strategist", strategist_agent.execute)
        workflow.add_node("builder", builder_agent.execute)
        workflow.add_node("optimizer", optimizer_agent.execute)
        workflow.add_node("reviewer", reviewer_agent.execute)

        # 4. Define the sequential edges that dictate the flow of the pipeline.
        #    The graph will proceed from one node to the next in this order.
        workflow.add_edge("context_extractor", "researcher")
        workflow.add_edge("researcher", "strategist")
        workflow.add_edge("strategist", "builder")
        workflow.add_edge("builder", "optimizer")
        workflow.add_edge("optimizer", "reviewer")
        
        # The final node in the sequence points to the special END state.
        workflow.add_edge("reviewer", END)

        # 5. Set the entry point of the graph.
        workflow.set_entry_point("context_extractor")

        # 6. Compile the graph into a runnable application. This is a crucial
        #    step that creates an optimized, executable version of our workflow.
        self.graph = workflow.compile()

    def optimize_resume(self, jd: str, role: str, company: str) -> ReviewerOutput:
        """
        Executes the full agentic pipeline to generate a tailored resume.

        Args:
            jd: The raw text of the job description.
            role: The job role the user is targeting.
            company: The name of the company.

        Returns:
            The final state of the workflow, containing the complete analysis and
            the final, structured resume report.
        """
        print("--- ORCHESTRATOR: Kicking off Resume Optimizer Workflow ---")
        
        # Define the initial state of the workflow with the user's inputs.
        initial_state = {
            "job_description": jd,
            "job_role": role,
            "company_name": company
        }
        
        final_state = self.graph.invoke(initial_state)
        
        print("--- ORCHESTRATOR: Workflow Complete ---")
        
        final_state_model = OptimizerWorkflowState(**final_state)

                # Add a crucial check to ensure the final report was actually generated.
        if not final_state_model.final_report:
            raise ValueError("Workflow completed, but the final report was not generated.")
            
        # Return ONLY the final, clean result.
        return final_state_model.final_report
   
