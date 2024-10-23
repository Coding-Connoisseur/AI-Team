import os
import ast
import json
import platform
import subprocess
from importlib.metadata import distributions  # Replacement for pkg_resources

# List of files and directories to ignore
IGNORE_LIST = [
    '.env',
    '__pycache__/',
    '.pytest_cache/',
    '.venv/',
    '.git',
    'zScripts/',
    'zScripts/SNAPSHOT.py',
    '.gitignore',
    'requirements.txt',
    'setup.py',
    'package.json',
    'node_modules/',
    'real_project/src',
    'zDocs/'
]

def should_ignore(path):
    """Check if the given path matches any of the ignore patterns."""
    for ignore in IGNORE_LIST:
        if ignore in path:
            return True
    return False

def get_system_info():
    """Capture system information like OS, Python version, and installed libraries."""
    installed_libraries = [f"{dist.metadata['Name']}=={dist.version}" for dist in distributions()]
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "installed_libraries": installed_libraries
    }

def get_file_contents(file_path):
    """Return the contents of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Could not read {file_path}: {str(e)}"

def get_function_calls(file_path):
    """Extract function calls using AST from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=file_path)
    except (SyntaxError, UnicodeDecodeError) as e:
        return {}

    function_calls = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            calls = []
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Name):
                    calls.append(sub_node.func.id)
            function_calls[function_name] = {
                "outgoing_calls": calls,
                "incoming_calls": []
            }

    return function_calls

def update_incoming_calls(function_calls_dict):
    """Reverse engineer the outgoing calls to create incoming calls."""
    for file, functions in function_calls_dict.items():
        for func, details in functions.items():
            for called_func in details['outgoing_calls']:
                for f_file, f_functions in function_calls_dict.items():
                    if called_func in f_functions:
                        f_functions[called_func]['incoming_calls'].append(func)

def get_dependencies():
    """Retrieve dependencies from common files like requirements.txt or package.json."""
    dependencies = {}
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", 'r', encoding='utf-8') as f:
            dependencies['python'] = f.read().splitlines()
    if os.path.exists("package.json"):
        try:
            result = subprocess.run(['npm', 'list', '--json'], stdout=subprocess.PIPE, text=True)
            package_json = json.loads(result.stdout)
            dependencies['node'] = package_json.get('dependencies', {})
        except Exception as e:
            dependencies['node'] = f"Could not retrieve node dependencies: {str(e)}"
    return dependencies

def get_directory_structure(directory):
    """Walk through the directory and collect file paths."""
    file_structure = {}
    for root, dirs, files in os.walk(directory):
        if should_ignore(root):
            continue
        relative_root = os.path.relpath(root, directory)
        file_structure[relative_root] = files
    return file_structure

def get_git_history():
    """Get the latest Git history."""
    try:
        result = subprocess.run(['git', 'log', '--pretty=format:%h - %s', '-n', '10'], stdout=subprocess.PIPE, text=True)
        return result.stdout.splitlines()
    except Exception as e:
        return f"Could not retrieve Git history: {str(e)}"

def get_project_info(directory):
    """Aggregate all project information into a dictionary."""
    project_info = {
        "system_info": get_system_info(),
        "file_structure": get_directory_structure(directory),
        "dependencies": get_dependencies(),
        "git_history": get_git_history(),
        "files": {}
    }

    function_calls_dict = {}

    for root, dirs, files in os.walk(directory):
        if should_ignore(root):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            if file.endswith(".py"):
                function_calls = get_function_calls(file_path)
                if function_calls:
                    function_calls_dict[relative_path] = function_calls
            project_info['files'][relative_path] = {
                "contents": get_file_contents(file_path)
            }

    update_incoming_calls(function_calls_dict)
    project_info["function_calls"] = function_calls_dict

    return project_info

def save_as_json(project_info, output_file):
    """Save the entire project information as a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(project_info, f, indent=4)
    print(f"Project information saved to {output_file}")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    output_file = "zDocs/project_info.json"

    if not os.path.isdir(directory):
        print("Invalid directory path")
    else:
        project_info = get_project_info(directory)
        save_as_json(project_info, output_file)
