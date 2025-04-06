from agents.base_agent import BaseAgent

class AgentCore(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Agent Core",
            system_prompt=self.load_prompt("core"),
            memory_path="memory/core_memory.json"
        )

    def load_prompt(self, role):
        with open(f"config/prompts/{role}.txt") as f:
            return f.read()

    async def summarize_memory(self):
        long_text = "\n".join([f"{x['role']}: {x['content']}" for x in self.memory])
        prompt = (
            "Summarize the following past interactions into key lessons and task details "
            "that can be used for future tasks:\n\n" + long_text
        )
        summary = await self.respond(prompt)
        with open("memory/core_summary.txt", "w") as f:
            f.write(summary)
        return summary

    def instruct_build_to_fix(self, feedback: str, original_code: str):
        return (
            "Please revise only the Python code portion of the following implementation. "
            "Do not include documentation, instructions, or markdown formatting. "
            "Only return a clean, executable Python script.\n\n"
            f"Feedback:\n{feedback}\n\n---\nOriginal Code:\n\n{original_code}"
        )
