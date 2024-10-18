import os
import ast
import json

# List of files and directories to ignore
IGNORE_LIST = [
    'real_project/src/',
    '__pycache__/',
    '.pytest_cache/',
    '.venv/',
    'zDocs/',
    'zScripts/',
    '.gitignore',
    'requirements.txt'
]

def should_ignore(path):
    # Check if the path starts with any of the ignore list items
    for ignore in IGNORE_LIST:
        if ignore in path:
            return True
    return False

def get_functions_and_classes_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=file_path)
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Skipping {file_path} due to a parsing error: {e}")
        return {}, {}

    function_calls = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            calls = []
            # Collect calls made inside the function
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Name):
                    calls.append(sub_node.func.id)
            function_calls[function_name] = {
                "outgoing_calls": calls,
                "incoming_calls": []  # To be populated later
            }

    return function_calls

def update_incoming_calls(function_calls_dict):
    # Reverse engineer the outgoing calls to create incoming calls
    for file, functions in function_calls_dict.items():
        for func, details in functions.items():
            for called_func in details['outgoing_calls']:
                # Look for the called function and add the current function as incoming
                for f_file, f_functions in function_calls_dict.items():
                    if called_func in f_functions:
                        f_functions[called_func]['incoming_calls'].append(func)

def get_functions_and_classes_from_directory(directory):
    function_calls_dict = {}

    for root, dirs, files in os.walk(directory):
        # Skip directories and files in the ignore list
        if should_ignore(root):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            if should_ignore(file_path) or not file.endswith(".py"):
                continue

            function_calls = get_functions_and_classes_from_file(file_path)
            if function_calls:
                function_calls_dict[file_path] = function_calls

    update_incoming_calls(function_calls_dict)
    return function_calls_dict

def save_as_json(function_calls_dict, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(function_calls_dict, f, indent=4)
    print(f"Call graph data saved to {output_file}")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    output_file = "zScripts/Calls/function_calls.json"

    if not os.path.isdir(directory):
        print("Invalid directory path")
    else:
        function_calls_dict = get_functions_and_classes_from_directory(directory)

        # Save function calls as JSON
        save_as_json(function_calls_dict, output_file)
