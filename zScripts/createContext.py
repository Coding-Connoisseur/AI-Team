import os
import fnmatch

# Define ignore patterns
ignore_patterns = [
    ".pytest_cache/",
    ".venv/",
    "real_project",
    ".env",
    "__pycache__/",
    ".gitignore",
    "zDocs/",
    "zScripts/"
]

def is_ignored(file_path, ignore_patterns, root_dir="."):
    """
    Checks if a file or directory matches any of the ignore patterns.
    Converts the ignore pattern into a format that can be matched by fnmatch.
    """
    for pattern in ignore_patterns:
        if pattern.startswith('/'):
            pattern = os.path.join(root_dir, pattern.lstrip('/'))
        else:
            pattern = os.path.join(root_dir, '**', pattern)

        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def process_files(file_path, context_file, ignore_patterns):
    """Processes a file or recursively processes a directory."""
    if os.path.isdir(file_path):
        # Recursively process all files in the directory
        for root, dirs, files in os.walk(file_path):
            # Remove directories from the walk if they are ignored
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignore_patterns, root)]
            for file in files:
                full_file_path = os.path.join(root, file)
                if not is_ignored(full_file_path, ignore_patterns, root):
                    write_file_to_context(full_file_path, context_file)
    else:
        if not is_ignored(file_path, ignore_patterns):
            write_file_to_context(file_path, context_file)

def write_file_to_context(file_path, context_file):
    """Writes the contents of a file to the context file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
        # Write the file's path and its contents to CONTEXT.txt
        context_file.write(f"\nFile: {file_path}\n")
        context_file.write("="*40 + "\n")  # Optional separator line
        context_file.write(file_contents + "\n")
        context_file.write("="*40 + "\n\n")  # Optional separator line
        print(f"Contents of {file_path} written to CONTEXT.txt.")
    except UnicodeDecodeError:
        print(f"Failed to read {file_path} with utf-8 encoding. Attempting latin-1.")
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                file_contents = f.read()
            # Write the file's path and its contents to CONTEXT.txt
            context_file.write(f"\nFile: {file_path}\n")
            context_file.write("="*40 + "\n")  # Optional separator line
            context_file.write(file_contents + "\n")
            context_file.write("="*40 + "\n\n")  # Optional separator line
            print(f"Contents of {file_path} written to CONTEXT.txt using latin-1 encoding.")
        except Exception as e:
            print(f"Skipping {file_path} due to encoding issues: {e}")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

def main():
    output_file = 'zDocs/CONTEXT.txt'

    print("Enter the relative file paths (or directories) one per line, and press Enter on an empty line to finish:")

    file_paths = []

    # Collect multiple lines of input
    while True:
        file_path = input().strip()

        # If the user enters an empty line, break the loop
        if not file_path:
            break

        file_paths.append(file_path)

    # Open the output file in write mode
    with open(output_file, 'w') as context_file:
        # Process each file or directory
        for file_path in file_paths:
            process_files(file_path, context_file, ignore_patterns)

if __name__ == "__main__":
    main()
