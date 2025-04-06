from agents.base_agent import BaseAgent

class AgentBuild(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Agent Build",
            system_prompt=self.load_prompt("build"),
            memory_path="memory/build_memory.json"
        )

    def load_prompt(self, role):
        with open(f"config/prompts/{role}.txt") as f:
            return f.read()
