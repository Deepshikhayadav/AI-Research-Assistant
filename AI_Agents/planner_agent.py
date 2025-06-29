from AI_Agents.base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self, mcp):
        super().__init__("planner", mcp)

    def process_task(self, task):
        if task["type"] == "plan":
            query = task["query"]
            print(f"\n🧠 Planner: Breaking down query: {query}")
            subtasks = [
                {"type": "search", "query": f"latest research about {query}"},
                {"type": "search", "query": f"key papers about {query}"},
                {"type": "search", "query": f"recent developments in {query}"}
            ]
            
            for subtask in subtasks:
                self.mcp.dispatch_task("planner", "searcher", subtask)
            
            self.mcp.dispatch_task("planner", "writer", {
                "type": "prepare_report",
                "main_query": query,
                "expected_sources": len(subtasks)
            })