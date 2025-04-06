import os
import subprocess
import py_compile
from agents.base_agent import BaseAgent

class AgentOps(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Agent Ops",
            system_prompt=self.load_prompt("ops"),
            memory_path="memory/ops_memory.json"
        )

    def load_prompt(self, role):
        with open(f"config/prompts/{role}.txt") as f:
            return f.read()

    async def execute_command(self, command: str):
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=60
            )
            return f"[CMD] {command}\n\n[OUTPUT]\n{result.stdout}\n[ERRORS]\n{result.stderr}"
        except Exception as e:
            return f"[CMD ERROR] {command}\nException: {str(e)}"

    def create_file(self, path: str, content: str):
        try:
            with open(path, "w") as f:
                f.write(content)
            return f"[FILE CREATED] {path}"
        except Exception as e:
            return f"[FILE ERROR] Could not create {path}: {e}"

    def create_directory(self, path: str):
        try:
            os.makedirs(path, exist_ok=True)
            return f"[DIR CREATED] {path}"
        except Exception as e:
            return f"[DIR ERROR] Could not create {path}: {e}"

    def read_log(self, path: str):
        try:
            with open(path, "r") as f:
                return f"[LOG] {path}\n\n" + f.read()
        except Exception as e:
            return f"[LOG ERROR] {path}: {e}"

    def validate_python_syntax(self, path: str):
        try:
            py_compile.compile(path, doraise=True)
            return f"[VALIDATION SUCCESS] {path} passed syntax check."
        except py_compile.PyCompileError as e:
            return f"[SYNTAX ERROR] {e}"
