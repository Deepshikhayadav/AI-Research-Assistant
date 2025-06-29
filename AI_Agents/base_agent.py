from threading import Thread
from queue import Queue
from typing import Dict

class BaseAgent(Thread):
    def __init__(self, name: str, mcp):
        super().__init__()
        self.name = name
        self.mcp = mcp
        self.daemon = True
        self.start()

    def run(self):
        """Main agent loop to process incoming tasks"""
        while True:
            if not self.mcp.agent_queues[self.name].empty():
                task = self.mcp.agent_queues[self.name].get()
                self.process_task(task)

    def process_task(self, task: dict):
        """To be implemented by each agent"""
        pass