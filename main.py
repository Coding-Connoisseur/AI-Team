import asyncio
import datetime
import os
from agents.agent_core import AgentCore
from agents.agent_build import AgentBuild
from agents.agent_review import AgentReview
from agents.agent_ops import AgentOps
from agents.agent_sanitizer import AgentSanitizer


def log_to_file(filename, content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"logs/{filename}_{timestamp}.log"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return path


def clean_triple_backticks(path):
    if not os.path.exists(path):
        return
    with open(path, "r") as f:
        lines = f.readlines()
    cleaned = [line for line in lines if not line.strip().startswith("```")]
    with open(path, "w") as f:
        f.writelines(cleaned)


def create_dynamic_project_dir(task):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    task_slug = task.lower().replace(" ", "_").replace("/", "_")
    directory = f"projects/{task_slug}_{timestamp}"
    os.makedirs(directory, exist_ok=True)
    return directory


async def main():
    task = input("Enter a task for the team: ")

    core = AgentCore()
    build = AgentBuild()
    review = AgentReview()
    ops = AgentOps()
    sanitizer = AgentSanitizer("python")

    print("\n[Agent Core is planning...]\n")
    plan = await core.respond(f"Break down the task and generate the expected file structure and responsibilities for: {task}")
    print(plan)

    print("\n[Agent Build is implementing...]\n")
    file_map = await build.respond(f"Generate code files and contents for this task and structure: {plan}")

    print("\n[Agent Review is reviewing the result...]\n")
    feedback = await review.respond(f"Please review this multi-file project:{file_map}")
    print(feedback)

    print("\n[Agent Core is requesting execution verdict from Agent Review...]\n")
    verdict_prompt = (
        "Based on your review, should we allow Agent Ops to execute this build? "
        "Please respond with a clear yes or no and your reasoning."
    )
    verdict = await review.respond(verdict_prompt)
    print(verdict)

    project_dir = create_dynamic_project_dir(task)
    script_path = os.path.join(project_dir, "main.py")

    if "yes" in verdict.lower():
        print("\n[Agent Ops is writing files and sanitizing...]\n")
        for filename, raw_code in file_map.items():
            abs_path = os.path.join(project_dir, filename)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            clean_code = await sanitizer.sanitize(raw_code)
            with open(abs_path, "w") as f:
                f.write(clean_code)
            clean_triple_backticks(abs_path)

        print("\n[Agent Ops is validating Python syntax before execution...]\n")
        validation = ops.validate_python_syntax(script_path)
        print(validation)

        if "SYNTAX ERROR" in validation:
            log_to_file("syntax_error", validation)
            print("\n[Agent Ops: Syntax error detected. Execution aborted.]\n")
        else:
            result = await ops.execute_command(f"python3 {script_path}")
            print(result)
            log_to_file("execution_result", result)
    else:
        print("\n[Agent Core is requesting Agent Build to fix issues based on review...]\n")
        fix_prompt = core.instruct_build_to_fix(feedback, str(file_map))
        revised_files = await build.respond(fix_prompt)

        print("\n[Agent Build - Revised Code]\n")
        print(revised_files)

        print("\n[Agent Review is re-reviewing the revised code...]\n")
        second_review = await review.respond(f"Please re-review this revised project:{revised_files}")
        print(second_review)

        print("\n[Agent Core requesting final verdict after revision...]\n")
        second_verdict = await review.respond(
            "Based on your updated review, should we allow Agent Ops to execute this revised build? Respond yes or no with explanation."
        )
        print(second_verdict)

        if "yes" in second_verdict.lower():
            for filename, raw_code in revised_files.items():
                abs_path = os.path.join(project_dir, filename)
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                clean_code = await sanitizer.sanitize(raw_code)
                with open(abs_path, "w") as f:
                    f.write(clean_code)
                clean_triple_backticks(abs_path)

            print("\n[Agent Ops is validating revised code syntax...]\n")
            validation = ops.validate_python_syntax(script_path)
            print(validation)

            if "SYNTAX ERROR" in validation:
                log_to_file("syntax_error", validation)
                print("\n[Agent Ops: Syntax error in revised build. Execution aborted.]\n")
            else:
                result = await ops.execute_command(f"python3 {script_path}")
                print(result)
                log_to_file("execution_result", result)
        else:
            print("\n[Agent Ops: Final build still not approved. Halting.]\n")


if __name__ == "__main__":
    asyncio.run(main())

