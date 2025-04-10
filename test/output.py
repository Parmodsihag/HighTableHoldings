import os

def get_python_files(path):
  """
  Get all Python files in a directory and its subdirectories.

  Args:
    path: The starting directory path.

  Yields:
    Full paths to all Python files found.
  """
  for root, _, files in os.walk(path):
    for filename in files:
      if filename.endswith(".py"):
        yield os.path.join(root, filename)

def save_code_to_file(filepaths, output_filename):
  """
  Saves the code from all Python files to a single output file.

  Args:
    filepaths: A list of file paths to Python files.
    output_filename: The name of the file to save the code to.
  """
  with open(output_filename, 'w') as output_file:
    for filepath in filepaths:
      with open(filepath, 'r') as input_file:
        print(filepath)
        if "bill" not in filepath:

            output_file.write(input_file.read() + "\n \n")

if __name__ == "__main__":
  # Get the current working directory
  cwd = os.getcwd()

  # Get all Python files in the current directory and subdirectories
  python_files = get_python_files(cwd)

  # Save the code to a file named output.txt
  save_code_to_file(python_files, "output.txt")

  print("Python code saved to output.txt")
