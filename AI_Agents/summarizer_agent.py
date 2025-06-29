from AI_Agents.base_agent import BaseAgent
import google.generativeai as genai
import streamlit as st
# import queue

# status_queue = queue.Queue()


class SummarizerAgent(BaseAgent):
    def __init__(self, mcp):
        super().__init__("summarizer", mcp)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    

    def process_task(self, task: dict):
        if task["type"] == "summarize":
            content = task["content"]
            source = task.get("source", "unknown")
            message = f"📖 Summarizer: Summarizing content from: {source}"
            print(message)
            # status_queue.put(message)
            
                
            try:
                prompt = f"Summarize the following text in 3-5 bullet points, focusing on key insights relevant to research: {content}"
                response = self.model.generate_content(prompt)
                # print(f"📖 Response: {response}")
                self.mcp.dispatch_task("summarizer", "writer", {
                    "type": "add_summary",
                    "summary": response.text,
                    "source": source,
                    "original_query": task["original_query"]
                })
            except Exception as e:
                print(f"Summarization error: {e}")



