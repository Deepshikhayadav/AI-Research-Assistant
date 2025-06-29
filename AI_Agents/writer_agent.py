import json
import google.generativeai as genai
from AI_Agents.base_agent import BaseAgent
# import queue

# status_queue = queue.Queue()



class WriterAgent(BaseAgent):
    def __init__(self, mcp):
        super().__init__("writer", mcp)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.report_data = {}
        self.expected_sources = 0
        self.received_sources = 0

    def process_task(self, task: dict):
        if task["type"] == "prepare_report":
            self.report_data = {
                "main_query": task["main_query"],
                "sources": [],
                "summaries": []
            }
            self.expected_sources = task["expected_sources"]
            self.received_sources = 0
            
        elif task["type"] == "add_summary":
            self.received_sources += 1
            self.report_data["sources"].append(task["source"])
            self.report_data["summaries"].append({
                "query": task["original_query"],
                "summary": task["summary"]
            })
            
            # If we've received all expected sources, compile the final report
            if self.received_sources >= self.expected_sources:
                self.compile_report()

    def compile_report(self):
        print("\n✍️ Writer: Compiling final report...")
        
        try:
            # Create a structured prompt for the final report
            prompt = f"""
            Compose a comprehensive research report on '{self.report_data['main_query']}' 
            using the following summarized information:
            
            {json.dumps(self.report_data['summaries'], indent=2)}
            
            Structure the report with:
            1. Introduction
            2. Key Findings
            3. Analysis
            4. Conclusion
            5. References
            
            Write in academic style for a research audience.
            """
            
            response = self.model.generate_content(prompt)
            # print(f"✍️ Final Report:\n{response.text}")
            # Send final result to MCP
            self.mcp.dispatch_task("writer", "mcp", {
                "type": "final_result",
                "content": {
                    "report": response.text,
                    "sources": self.report_data["sources"]
                }
            })
            # status_queue.put(response.text)
        except Exception as e:
            print(f"Report compilation error: {e}")