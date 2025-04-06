from agents.base_agent import BaseAgent
import os

class AgentSanitizer(BaseAgent):
    def __init__(self, language="python"):
        self.language = language
        system_prompt = self.load_prompt(language)
        memory_path = f"memory/sanitizer_{language}_memory.json"

        super().__init__(
            name="Agent Sanitizer",
            system_prompt=system_prompt,
            memory_path=memory_path
        )

    def load_prompt(self, language: str) -> str:
        custom_path = f"config/prompts/sanitizer_{language}.txt"
        default_path = "config/prompts/sanitizer.txt"

        try:
            with open(custom_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            with open(default_path, "r") as f:
                return f.read()

    async def sanitize(self, raw_input: str) -> str:
        prompt = (
            f"Extract only the valid {self.language} code or structure from the following input. "
            f"Remove all markdown, comments, or irrelevant explanations.\n\n"
            f"{raw_input}"
        )
        result = await self.respond(prompt)
        return result.strip()
