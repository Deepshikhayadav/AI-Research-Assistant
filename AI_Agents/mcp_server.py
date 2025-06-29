import json
from queue import Queue
import threading
import time
from typing import Dict


class MCPServer:
    def __init__(self):
        self.agent_queues: Dict[str, Queue] = {
            "searcher": Queue(),
            "summarizer": Queue(),
            "planner": Queue(),
            "writer": Queue(),
            "mcp": Queue()
        }
        self.agents = {}
        self.workflow_complete = False
        self.response = None
        self.results = {}
        self.lock = threading.Lock()

    def register_agent(self, agent_name: str, agent_queue: Queue):
        self.agents[agent_name] = agent_queue

    def dispatch_task(self, from_agent: str, to_agent: str, task: dict):
        """Send a task from one agent to another"""
        if to_agent in self.agent_queues:
            task['from'] = from_agent
            self.agent_queues[to_agent].put(task)
        else:
            print(f"Error: Unknown agent {to_agent}")

    def start_workflow(self, initial_query: str):
        """Start the research workflow with a user query"""
        self.dispatch_task("mcp", "planner", {"type": "plan", "query": initial_query})

    def monitor_workflow(self):
        """Monitor the workflow and collect final results"""
        while not self.workflow_complete:
            time.sleep(1)
            # Check for final results
            if not self.agent_queues["mcp"].empty():
                message = self.agent_queues["mcp"].get()
                if message.get("type") == "final_result":
                    self.results = message["content"]
                    self.workflow_complete = True
                    print("\nResearch completed!")
                    print(json.dumps(self.results, indent=2))
                    self.response = json.dumps(self.results, indent=2)


 