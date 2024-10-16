import os
import subprocess
import sqlite3
import ast
import inspect
import openai
from openai import OpenAI
from system import TeamLeaderAI

client = OpenAI(api_key='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')

class BaseAgent:
    def __init__(self, name, knowledge_base):
        self.name = name
        self.knowledge_base = knowledge_base
        self.memory = {}
        self.success_rate = 0.0  # Track the success rate for self-learning
          # Replace with your actual OpenAI API key

    def can_handle(self, task_name):
        raise NotImplementedError("Subclasses should implement this method.")

    def execute_task(self, task_name):
        raise NotImplementedError("Subclasses should implement this method.")

    def learn(self, task, outcome):
        """
        Records the task outcome and adjusts the agent's success rate.
        """
        if task not in self.memory:
            self.memory[task] = {"successes": 0, "failures": 0}

        # Update memory based on task outcome
        if outcome == "success":
            self.memory[task]["successes"] += 1
        else:
            self.memory[task]["failures"] += 1

        # Calculate success rate
        total_attempts = self.memory[task]["successes"] + self.memory[task]["failures"]
        self.success_rate = self.memory[task]["successes"] / total_attempts

        # Log the learning outcome
        print(f"{self.name} has learned from task '{task}'. Success Rate: {self.success_rate:.2%}")

        # Store the metadata in the knowledge base
        metadata = {
            "task": task,
            "outcome": outcome,
            "success_rate": self.success_rate,
            "total_attempts": total_attempts
        }
        self.knowledge_base.store_task_metadata(task, metadata)

    def query_improvements(self, task_name):
        """
        Queries an AI model for suggestions on how to improve the task handling process.
        """
        prompt = f"{self.name} just completed a task: {task_name}. How can I improve my approach for this type of task?"

        try:
            response = client.chat.completions.create(model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant helping to improve task handling processes."},
                {"role": "user", "content": prompt}
            ])
            improvement_suggestions = response.choices[0].message.content.strip()
            print(f"Improvement suggestions for {task_name}: {improvement_suggestions}")
            return improvement_suggestions
        except Exception as e:
            print(f"Error querying AI for improvements: {e}")
            return None
    def adjust_behavior(self, task):
        """
        Adjusts the agent's behavior based on its success rate for the given task.
        """
        # If the success rate is low, try to adjust behavior
        if task in self.memory and self.memory[task]["failures"] > self.memory[task]["successes"]:
            print(f"{self.name} adjusting behavior for task '{task}' due to low success rate.")
            # Example adjustment: change task strategy (e.g., increase resource allocation)
            self.change_strategy(task)

    def change_strategy(self, task):
        """
        Implement a strategy change, such as increasing resource allocation or modifying the task approach.
        This function can be customized per agent's requirements.
        """
        print(f"{self.name} is changing strategy for task '{task}' to improve performance.")

class EnhancedAgent(BaseAgent):
    def learn(self, task, outcome):
        # Enhanced learning method with AI suggestions
        super().learn(task, outcome)

        if outcome == "failure":
            self.adjust_strategy(task)

    def adjust_strategy(self, task):
        print(f"{self.name} is adjusting strategy for task '{task}' due to low success rate.")
        # Fetch suggestions from an AI model for improvement
        feedback = self.query_improvements(task)
        if feedback:
            # Implement suggestions or log them for human review
            print(f"Feedback for {task}: {feedback}")


class ProjectArchitectAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Project Architect AI", knowledge_base)

    def can_handle(self, task):
        return task == "architecture design"

    def execute_task(self, task):
        self.adjust_behavior(task)
        print(f"{self.name} is creating the project architecture...")

        # Use AI to dynamically generate the project architecture
        project_structure = self.generate_project_structure()

        # Base path for project
        base_path = "./real_project"
        os.makedirs(base_path, exist_ok=True)

        # Create directories and files based on AI suggestions
        self.create_structure(base_path, project_structure)

        print(f"Real-world project structure created by {self.name}.")
        outcome = "success"
        self.learn(task, outcome)
        return outcome

    def generate_project_structure(self):
        """
        Generates a project structure using AI.
        """
        # Prompt AI to design a comprehensive project architecture
        prompt = "Generate a project architecture for a complex {TeamLeaderAI.project_type}, including directories and essential files for code, tests, documentation, configuration, and deployment."

        try:
            response = client.chat.completions.create(model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant helping to generate a project architecture for a complex web application, including directories and essential files for code, tests, documentation, configuration, and deployment."},
                {"role": "user", "content": prompt}
            ])
            # Extract structure as a dictionary
            ai_structure = eval(response.choices[0].text.strip())  # Caution: Only use eval with trusted sources
            return ai_structure

        except openai.OpenAIError as e:
            print(f"Error querying OpenAI for project structure: {e}")
            # Default fallback structure if AI call fails
            return {
                "src": {
                    "main.py": "# Main entry point",
                    "utils.py": "# Utility functions",
                    "tests": {
                        "test_main.py": "# Test cases for main"
                    }
                },
                "docs": {
                    "README.md": "# Project documentation"
                },
                "db": {},
                "logs": {},
            }

    def create_structure(self, base_path, structure):
        """
        Recursively creates directories and files based on the provided structure.
        """
        for folder, contents in structure.items():
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            for file_name, file_content in contents.items():
                if isinstance(file_content, dict):
                    # Recursively create subdirectories and files
                    self.create_structure(folder_path, {file_name: file_content})
                else:
                    # Create files with content
                    with open(os.path.join(folder_path, file_name), 'w') as f:
                        f.write(file_content)

class CodeGeneratorAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Code Generator AI", knowledge_base)

    def can_handle(self, task):
        return task == "code generation"

    def execute_task(self, task, project_details=None):
        """
        Executes the code generation task with a dynamic, advanced prompt based on project details.
        
        Args:
            task (str): The task to be performed.
            project_details (dict, optional): Specific details for the project, such as the type of app, features, or required technologies.
        """
        # Ensure project_details has default values if not provided
        if project_details is None:
            project_details = {
                "type": "web app",
                "architecture": "microservices",
                "features": ["authentication", "data processing", "API handling"],
                "technologies": ["Flask", "Redis", "Docker"]
            }

        self.adjust_behavior(task)
        print(f"{self.name} is generating an extremely advanced real-world code...")

        try:
            # Generate advanced code based on detailed project requirements
            code_content = self.generate_advanced_code(project_details)

            # Define the path for the generated code
            base_path = "./real_project/src/"
            os.makedirs(base_path, exist_ok=True)
            file_path = os.path.join(base_path, "main.py")

            # Write the AI-generated code to a file
            with open(file_path, 'w') as f:
                f.write(code_content)

            print(f"Extremely advanced code generation completed for task: {task}")

            # Query for improvement suggestions after completing the task
            improvement_suggestions = self.query_improvements(task)

            # Optionally store the suggestions in the knowledge base
            if improvement_suggestions:
                self.knowledge_base.store(f"{task}_improvements", improvement_suggestions)

            self.learn(task, "success")
            return "success"

        except Exception as e:
            print(f"Error during code generation: {e}")
            self.learn(task, "failure")
            return "failure"

    def generate_advanced_code(self, project_details):
        """
        Generates highly advanced, AI-driven code for a real-world application.
        
        Args:
            project_details (dict): Specific requirements or features for the project.
        
        Returns:
            str: Generated code content.
        """
        # Dynamic prompt generation for an extremely advanced implementation
        project_type = project_details.get("type", "distributed web application")
        architecture_style = project_details.get("architecture", "microservices with event-driven communication")
        main_features = project_details.get("features", ["authentication", "real-time data streaming", "state management"])
        technologies = project_details.get("technologies", ["Flask", "Redis", "GraphQL", "Kafka", "Docker"])

        prompt = f"""
Design and implement a sophisticated {TeamLeaderAI.project_type} with an {architecture_style} architecture.
The application should include:
1. {main_features[0]} using JWT and OAuth for secure user authentication.
2. {main_features[1]} leveraging Kafka for data streaming and Redis for caching.
3. {main_features[2]} managed via Redux or a similar state management tool for complex UI interactions.
4. Use advanced programming patterns such as Dependency Injection, Factory Pattern, and Repository Pattern.
5. Implement with {', '.join(technologies)}, and ensure the application is containerized with Docker.
6. Code should follow modular design principles, support scalability, and include error handling, logging, and monitoring.
7. Include comprehensive comments, structured documentation, and necessary tests for all modules.
        """
        try:
            response = client.chat.completions.create(model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant helping to generate advanced code for a real-world application."},
                {"role": "user", "content": prompt}
            ])
            advanced_code = response.choices[0].text.strip()
            return advanced_code

        except openai.OpenAIError as e:
            print(f"Error querying OpenAI for advanced code generation: {e}")
            # Provide fallback code if API fails
            return '''
# Fallback advanced API setup with Microservices and Kafka for data streaming

import logging
import os
from flask import Flask, jsonify, request
from kafka import KafkaProducer
import redis
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
producer = KafkaProducer(bootstrap_servers='localhost:9092')
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

# Dependency Injection example
class ServiceInjector:
    def __init__(self, service):
        self._service = service

    def perform_action(self):
        self._service.execute()

@app.route('/data', methods=['POST'])
def send_data():
    data = request.json
    producer.send('data-topic', bytes(str(data), 'utf-8'))
    logging.info("Data sent to Kafka")
    return jsonify({"status": "Data sent successfully"})

@app.route('/cache', methods=['GET'])
def get_cache():
    value = cache.get('key')
    return jsonify({"cached_value": value})

if __name__ == '__main__':
    app.run(debug=True)
            '''

class TestAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Test AI", knowledge_base)

    def can_handle(self, task_name):
        return task_name == "testing"

    def execute_task(self, task_name):
        if task_name == "testing":
            return self.run_tests()

    def run_tests(self):
        """
        Attempt to run tests. Logs detailed test output and retries up to 3 times if tests fail.
        """
        test_dir = os.path.join(self.knowledge_base.get("project_path", "./real_project/src"), "tests")
        if not os.path.exists(test_dir):
            print(f"No tests directory found at {test_dir}.")
            return "failure"

        try:
            result = subprocess.run(["pytest", test_dir], capture_output=True, text=True)
            print(result.stdout)

            if result.returncode == 0:
                print("All tests passed successfully.")

                # Query for improvement suggestions after successful testing
                improvement_suggestions = self.query_improvements("testing")

                # Optionally store the suggestions in the knowledge base
                if improvement_suggestions:
                    self.knowledge_base.store("testing_improvements", improvement_suggestions)

                return "success"
            else:
                print("Some tests failed.")
                return "failure"

        except Exception as e:
            print(f"Error while running tests: {str(e)}")
            return "failure"

class DebuggingAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Debugging AI", knowledge_base)

    def can_handle(self, task):
        return task == "debugging"

    def execute_task(self, task):
        self.adjust_behavior(task)  # Apply any behavior adjustments before debugging
        print(f"{self.name} is performing debugging on the project...")

        try:
            # Debugging logic goes here
            # Example debugging process
            print(f"Debugging task performed by {self.name}.")

            # After debugging, query for improvement suggestions
            improvement_suggestions = self.query_improvements(task)

            # Optionally store the suggestions in the knowledge base
            if improvement_suggestions:
                self.knowledge_base.store(f"{task}_improvements", improvement_suggestions)

            self.learn(task, "success")
            return "success"

        except Exception as e:
            print(f"Error during debugging: {e}")
            self.learn(task, "failure")
            return "failure"

class EnhancerAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Enhancer AI", knowledge_base)

    def can_handle(self, task):
        return task == "enhancement"

    def execute_task(self, task):
        self.adjust_behavior(task)  # Adjust behavior based on prior success/failure rates
        print(f"{self.name} is enhancing the project...")

        try:
            # Enhancement logic goes here
            enhancement_code = '''
def advanced_feature():
    print("Advanced feature implemented.")
'''
            base_path = "./real_project/src/utils.py"
            with open(base_path, 'a') as f:
                f.write(enhancement_code)

            print(f"Enhancement added to utils.py by {self.name}.")

            # Query for improvement suggestions after enhancement
            improvement_suggestions = self.query_improvements(task)

            # Optionally store the suggestions in the knowledge base
            if improvement_suggestions:
                self.knowledge_base.store(f"{task}_improvements", improvement_suggestions)

            self.learn(task, "success")
            return "success"

        except Exception as e:
            print(f"Error during enhancement: {e}")
            self.learn(task, "failure")
            return "failure"

class DocumentationAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Documentation AI", knowledge_base)

    def can_handle(self, task_name):
        return task_name == "documentation"

    def execute_task(self, task_name):
        if task_name == "documentation":
            return self.generate_detailed_documentation()

    def generate_detailed_documentation(self):
        """
        Generates detailed documentation including:
        1. API Documentation (function signatures)
        2. Code Annotations (detailed explanations of code blocks)
        3. Workflow Diagrams (general flow of the project components)
        """
        print(f"{self.name} is generating detailed documentation...")

        # Step 1: Generate API Documentation
        self.generate_api_docs()

        # Step 2: Generate Code Annotations
        self.generate_code_annotations()

        # Step 3: Generate Workflow Diagrams (Simplified as textual representation for now)
        self.generate_workflow_diagrams()

        # Query for improvement suggestions after generating documentation
        improvement_suggestions = self.query_improvements("documentation")

        # Optionally store the suggestions in the knowledge base
        if improvement_suggestions:
            self.knowledge_base.store("documentation_improvements", improvement_suggestions)

        self.learn("documentation", "success")
        return "success"

    def generate_api_docs(self):
        """
        Generate API documentation for all Python files by extracting function definitions and signatures.
        """
        print("Generating API documentation...")
        for module_name, module_ref in self.knowledge_base.get("modules", {}).items():
            print(f"\nModule: {module_name}")
            functions = inspect.getmembers(module_ref, inspect.isfunction)
            for function_name, function_ref in functions:
                signature = inspect.signature(function_ref)
                print(f"  Function: {function_name}{signature}")

    def generate_code_annotations(self):
        """
        Generate code annotations by analyzing the AST (Abstract Syntax Tree) and adding comments where appropriate.
        """
        print("Generating code annotations using AST...")
        for module_name, module_ref in self.knowledge_base.get("modules", {}).items():
            source_code = inspect.getsource(module_ref)
            root = ast.parse(source_code)
            print(f"\nAnnotations for {module_name}:")
            for node in ast.walk(root):
                if isinstance(node, ast.FunctionDef):
                    print(f"  Function {node.name} is defined at line {node.lineno}.")
                elif isinstance(node, ast.ClassDef):
                    print(f"  Class {node.name} found at line {node.lineno}.")

    def generate_workflow_diagrams(self):
        """
        Generate a simplified diagram of workflow/processes in the system.
        """
        print("Generating workflow diagram...\n")
        workflow = """
        [Team Leader AI] --> Assign Tasks
        [Load Balancer] --> Distribute Tasks to Agents
        [Agents] --> Perform Tasks (e.g., Code Generation, Testing, Debugging)
        [Documentation AI] --> Generate Reports on Project State
        """
        print(workflow)

class DeploymentAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Deployment AI", knowledge_base)

    def can_handle(self, task):
        return task == "deployment"

    def execute_task(self, task):
        self.adjust_behavior(task)  # Adjust behavior based on previous task outcomes
        print(f"{self.name} is deploying the project...")

        try:
            # Deployment logic goes here
            dockerfile_content = '''
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
'''
            with open("./real_project/Dockerfile", 'w') as f:
                f.write(dockerfile_content)

            print(f"Dockerfile created by {self.name}.")

            # Query for improvement suggestions after deployment
            improvement_suggestions = self.query_improvements(task)

            # Optionally store the suggestions in the knowledge base
            if improvement_suggestions:
                self.knowledge_base.store(f"{task}_improvements", improvement_suggestions)

            self.learn(task, "success")
            return "success"

        except Exception as e:
            print(f"Error during deployment: {e}")
            self.learn(task, "failure")
            return "failure"

class SecurityAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Security AI", knowledge_base)

    def can_handle(self, task_name):
        return task_name == "security audit"

    def execute_task(self, task_name):
        if task_name == "security audit":
            return self.perform_security_audit()

    def perform_security_audit(self):
        """
        Perform a security audit, detect vulnerabilities, and attempt to fix them.
        """
        print("Security AI is performing a security audit...")

        # Example vulnerabilities
        vulnerabilities = ["Insecure default configuration", "Weak encryption algorithm"]
        print("Vulnerabilities detected:\n" + "\n".join(vulnerabilities))

        try:
            # Fix detected vulnerabilities
            self.fix_vulnerabilities(vulnerabilities)

            # Query for improvement suggestions after the security audit
            improvement_suggestions = self.query_improvements("security audit")

            # Optionally store the suggestions in the knowledge base
            if improvement_suggestions:
                self.knowledge_base.store("security_audit_improvements", improvement_suggestions)

            return "success"
        except Exception as e:
            print(f"Failed to fix vulnerabilities: {str(e)}")
            return "failure"

    def fix_vulnerabilities(self, vulnerabilities):
        """
        Fixes known vulnerabilities. For example, updates configurations and replaces weak algorithms.
        """
        for vulnerability in vulnerabilities:
            if "Insecure default configuration" in vulnerability:
                config_file = os.path.join(self.knowledge_base.get("project_path", "./real_project"), "config.yml")
                if os.path.exists(config_file):
                    with open(config_file, 'a') as f:
                        f.write("secure: true\n")
                    print("Insecure default configuration fixed.")
            elif "Weak encryption algorithm" in vulnerability:
                code_file = os.path.join(self.knowledge_base.get("project_path", "./real_project/src"), "encryption.py")
                if os.path.exists(code_file):
                    with open(code_file, 'r') as f:
                        content = f.read()
                    updated_content = content.replace("AES256", "AES512")
                    with open(code_file, 'w') as f:
                        f.write(updated_content)
                    print("Weak encryption algorithm fixed.")

class DatabaseAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Database AI", knowledge_base)

    def can_handle(self, task):
        return task == "database setup"

    def execute_task(self, task):
        self.adjust_behavior(task)  # Adjust behavior based on previous task outcomes
        print(f"{self.name} is setting up the database...")

        try:
            # Database setup logic goes here
            db_path = "./real_project/db/project.db"
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            ''')
            conn.commit()
            conn.close()

            print(f"Database created by {self.name}.")

            # Query for improvement suggestions after database setup
            improvement_suggestions = self.query_improvements(task)

            # Optionally store the suggestions in the knowledge base
            if improvement_suggestions:
                self.knowledge_base.store(f"{task}_improvements", improvement_suggestions)

            self.learn(task, "success")
            return "success"

        except sqlite3.Error as e:
            print(f"Database setup failed: {e}")
            self.learn(task, "failure")
            return "failure"

class LoggingAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Logging AI", knowledge_base)

    def can_handle(self, task):
        return task == "logging setup"

    def execute_task(self, task):
        self.adjust_behavior(task)  # Adjust behavior based on past task outcomes
        print(f"{self.name} is setting up logging for the project...")

        try:
            # Logging setup logic goes here
            logging_config = '''
import logging
logging.basicConfig(filename='./real_project/logs/app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')
logging.info("Logging is set up.")
'''
            log_file_path = "./real_project/src/logging_setup.py"
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            with open(log_file_path, 'w') as f:
                f.write(logging_config)

            print(f"Logging setup complete by {self.name}.")

            # Query for improvement suggestions after setting up logging
            improvement_suggestions = self.query_improvements(task)

            # Optionally store the suggestions in the knowledge base
            if improvement_suggestions:
                self.knowledge_base.store(f"{task}_improvements", improvement_suggestions)

            self.learn(task, "success")
            return "success"

        except Exception as e:
            print(f"Error during logging setup: {e}")
            self.learn(task, "failure")
            return "failure"

class VersionControlAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Version Control AI", knowledge_base)

    def can_handle(self, task):
        return task == "version control setup"

    def execute_task(self, task):
        self.adjust_behavior(task)  # Adjust behavior based on past task outcomes
        print(f"{self.name} is setting up version control for the project...")

        try:
            # Initialize a new Git repository
            repo_path = self.knowledge_base.get("project_path", "./real_project")
            os.makedirs(repo_path, exist_ok=True)
            subprocess.run(["git", "init", repo_path], check=True)

            # Create a .gitignore file
            gitignore_content = '''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
*.log

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# Pyre type checker
.pyre/
'''
            with open(os.path.join(repo_path, ".gitignore"), 'w') as f:
                f.write(gitignore_content)

            print(f"Git repository initialized and .gitignore file created by {self.name}.")

            # Query for improvement suggestions after setting up version control
            improvement_suggestions = self.query_improvements(task)

            # Optionally store the suggestions in the knowledge base
            if improvement_suggestions:
                self.knowledge_base.store(f"{task}_improvements", improvement_suggestions)

            self.learn(task, "success")
            return "success"

        except subprocess.CalledProcessError as e:
            print(f"Failed to initialize Git repository: {e}")
            self.learn(task, "failure")
            return "failure"

class FrontendGeneratorAI(EnhancedAgent):
    def __init__(self, knowledge_base):
        super().__init__("Frontend Generator AI", knowledge_base)

    def can_handle(self, task):
        return task == "frontend generation"

    def execute_task(self, task):
        self.adjust_behavior(task)  # Adjust behavior based on past task outcomes
        print(f"{self.name} is generating the frontend for the project...")

        try:
            # Frontend generation logic goes here
            project_path = self.knowledge_base.get("project_path", "./real_project/frontend")
            os.makedirs(project_path, exist_ok=True)

            # Example HTML and CSS files
            index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Frontend</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Welcome to the Project Frontend</h1>
    <p>This is a sample frontend generated by Frontend Generator AI.</p>
</body>
</html>
'''
            styles_css = '''
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    color: #333;
    text-align: center;
    margin: 0;
    padding: 0;
}
h1 {
    color: #555;
}
'''

            # Write files to the project directory
            with open(os.path.join(project_path, "index.html"), 'w') as f:
                f.write(index_html)
            with open(os.path.join(project_path, "styles.css"), 'w') as f:
                f.write(styles_css)

            print(f"Frontend generated successfully by {self.name}.")

            # Query for improvement suggestions after generating the frontend
            improvement_suggestions = self.query_improvements(task)

            # Optionally store the suggestions in the knowledge base
            if improvement_suggestions:
                self.knowledge_base.store(f"{task}_improvements", improvement_suggestions)

            self.learn(task, "success")
            return "success"

        except Exception as e:
            print(f"Error during frontend generation: {e}")
            self.learn(task, "failure")
            return "failure"
