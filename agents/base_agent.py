import json
import os
import asyncio
from utils.api_handler import chatgpt_call

class BaseAgent:
    def __init__(self, name, system_prompt, memory_path):
        self.name = name
        self.system_prompt = system_prompt
        self.memory_path = memory_path
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            with open(self.memory_path) as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return []


    def save_memory(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.memory, f, indent=2)

    async def respond(self, user_input):
        messages = self.build_context(user_input)
        try:
            response = await chatgpt_call(messages)
        except Exception as e:
            response = f"[{self.name} ERROR] {e}"
        self.memory.append({"role": "user", "content": user_input})
        self.memory.append({"role": "assistant", "content": response})
        self.save_memory()
        return response

    def build_context(self, user_input):
        messages = [{"role": "system", "content": self.system_prompt}]
        summary = self.load_summary()

        if summary:
            messages.append({"role": "system", "content": f"Summary of past tasks:\n{summary}"})

        messages += self.memory[-5:]  # Recent only
        messages.append({"role": "user", "content": user_input})
        return messages

    def load_summary(self):
        path = self.memory_path.replace("_memory.json", "_summary.txt")
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
        return None

