from agents.base_agent import BaseAgent

class AgentReview(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Agent Review",
            system_prompt=self.load_prompt("review"),
            memory_path="memory/review_memory.json"
        )

    def load_prompt(self, role):
        with open(f"config/prompts/{role}.txt") as f:
            return f.read()
