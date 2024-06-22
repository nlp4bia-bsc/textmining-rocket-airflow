import os
import re
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

    print("Force unix newline characters")
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "rb+") as f:
            print(f"Processing file: {filename}")
            content = f.read()
            content = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            f.seek(0)
            f.write(content)
            f.truncate()

def remove_html_errors(output_dir):
    replacements = {
        "&mu;": "µ",
        "&rsquo;": "'",
        "&ge;": "≥",
        "&le;": "≤",
        "&beta;": "β",
        "&alpha;": "α",
        "&mdash;": "-",
    }

    for filename in os.listdir(output_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(output_dir, filename)
            with open(file_path, "r+") as f:
                content = f.read()
                for entity, symbol in replacements.items():
                    content = content.replace(entity, symbol)

                f.seek(0)
                f.write(content)
                f.truncate()


def fix_encoding_errors(output_dir):
    encoding_errors = {
        "'\|\"\|\"\|\"": "'",
        "•\|–\|—": "-",
        #" ": "",
        "\f": " ",
    }

    for error, replacement in encoding_errors.items():
        for root, _, files in os.walk(output_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                print(filepath)

                with open(filepath, "r", encoding="utf-8") as f_in:
                    content = f_in.read()

                content = re.sub(error, replacement, content)

                with open(filepath, "w", encoding="utf-8") as f_out:
                    f_out.write(content)