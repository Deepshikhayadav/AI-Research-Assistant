from AI_Agents.base_agent import BaseAgent
import duckduckgo_search

class SearcherAgent(BaseAgent):
    def __init__(self, mcp):
        super().__init__("searcher", mcp)
        self.ddg = duckduckgo_search.DDGS()

    def process_task(self, task):
        if task["type"] == "search":
            query = task["query"]
            print(f"\n🔍 Searcher: Searching for: {query}")
            
            try:
                results = self.ddg.text(query, max_results=5)
                if results:
                    self.mcp.dispatch_task("searcher", "summarizer", {
                        "type": "summarize",
                        "content": results[0]["body"],
                        "source": results[0]["title"],
                        "original_query": query
                    })
            except Exception as e:
                print(f"Search error: {e}")