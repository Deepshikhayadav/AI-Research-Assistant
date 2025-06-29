from AI_Agents.mcp_server import MCPServer
from AI_Agents.planner_agent import PlannerAgent
from AI_Agents.searcher_agent import SearcherAgent
from AI_Agents.summarizer_agent import SummarizerAgent
from AI_Agents.writer_agent import WriterAgent
import threading
import time
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP(name="ReportServer", stateless_http=True)


@mcp.tool(description="A Main tool")
def server_start(research_query: str) -> str:
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
    print(f"\nStarting research on: {research_query}")
    mcp.start_workflow(research_query)
    
    while not mcp.workflow_complete:
        time.sleep(1)
    return mcp.response or "No results found."

# if __name__ == "__main__":
#     main()