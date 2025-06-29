from AI_Agents.mcp_server import MCPServer
from AI_Agents.planner_agent import PlannerAgent
from AI_Agents.searcher_agent import SearcherAgent
from AI_Agents.summarizer_agent import SummarizerAgent
from AI_Agents.writer_agent import WriterAgent
import threading
import time


def main():
    """Main function to start the AI Research Assistance workflow."""
    mcp = MCPServer()
    # Create agents
    PlannerAgent(mcp)
    SearcherAgent(mcp)
    SummarizerAgent(mcp)
    WriterAgent(mcp)
    
    # Start monitoring
    monitor_thread = threading.Thread(target=mcp.monitor_workflow)
    monitor_thread.start()
    
    # Start workflow
    research_query = input("Enter your research query: ")  # "eg. advancements in quantum computing"
    print(f"\nStarting research on: {research_query}")
    mcp.start_workflow(research_query)
    
    while not mcp.workflow_complete:
        time.sleep(1)
    print("\nResearch workflow completed successfully!")

if __name__ == "__main__":
    main()