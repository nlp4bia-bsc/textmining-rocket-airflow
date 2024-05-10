import os
import subprocess
import shutil

def copy_files(source_dir, dest_dir):
    print("Copy files")
    for filename in os.listdir(source_dir):
        shutil.copy(os.path.join(source_dir, filename), os.path.join(dest_dir, filename))

def process_file(source_folder, dest_folder):
    for filename in os.listdir(source_folder):
        if filename.endswith('.txt'):
            source_file = os.path.join(source_folder, filename)
            dest_file = os.path.join(dest_folder, filename)

            with open(source_file, 'r') as f:
                file_content = f.read()
                print(f"Processing file: {filename}")
                print(file_content)

            os.rename(source_file, dest_file)

def force_unix_newlines(output_dir):
    """
    Convert all files in the output directory to Unix newline format.

    Args:
        output_dir (str): Path to the directory containing the files
    """

    # Build a string containing all files in the output directory
    all_files = f"{output_dir}/*"

    # Use subprocess to call the dos2unix command
    print("Force unix newline characters")
    print(f"dos2unix {all_files}")
    subprocess.run(["dos2unix", all_files])
