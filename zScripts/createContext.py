# Python script to read multiple files and output contents to CONTEXT.txt

def main():
    output_file = 'zDocs/CONTEXT.txt'

    # Open the output file in write mode
    with open(output_file, 'w') as context_file:
        print("Enter the relative file paths (one per line), and press Enter on an empty line to finish:")

        file_paths = []

        # Collect multiple lines of input
        while True:
            file_path = input().strip()

            # If the user enters an empty line, break the loop
            if not file_path:
                break

            file_paths.append(file_path)

        # Process each file
        for file_path in file_paths:
            try:
                # Read the content of the file
                with open(file_path, 'r') as f:
                    file_contents = f.read()

                # Write the file's path and its contents to CONTEXT.txt
                context_file.write(f"\nFile: {file_path}\n")
                context_file.write("="*40 + "\n")  # Optional separator line
                context_file.write(file_contents + "\n")
                context_file.write("="*40 + "\n\n")  # Optional separator line

                print(f"Contents of {file_path} written to {output_file}.")

            except FileNotFoundError:
                print(f"File '{file_path}' not found. Please try again.")

if __name__ == "__main__":
    main()
