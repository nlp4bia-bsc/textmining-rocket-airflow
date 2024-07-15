import os
import re
import shutil

def copy_files(dest_dir, **kwargs):
    config_dict = kwargs['dag_run'].conf if kwargs['dag_run'].conf != {} else None
    source_dir = config_dict['source_dir']
    dest_dir_temp = f"{dest_dir}{source_dir.replace('/storage','')}"
    os.makedirs(dest_dir_temp, exist_ok=True)

    print("Copy files")
    for filename in os.listdir(source_dir):
        shutil.copy(os.path.join(source_dir, filename), os.path.join(dest_dir_temp, filename))

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

def force_unix_newlines(output_dir, **kwargs):
    """
    Convert all files in the output directory to Unix newline format.

    Args:
        output_dir (str): Path to the directory containing the files
    """
    config_dict = kwargs['dag_run'].conf if kwargs['dag_run'].conf != {} else None
    source_dir = config_dict['source_dir']
    dest_dir_temp = f"{output_dir}{source_dir.replace('/storage','')}"
    os.makedirs(dest_dir_temp, exist_ok=True)

    print("Force unix newline characters")
    for filename in os.listdir(dest_dir_temp):
        file_path = os.path.join(dest_dir_temp, filename)

        with open(file_path, "rb+") as f:
            print(f"Processing file: {filename}")
            content = f.read()
            content = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            f.seek(0)
            f.write(content)
            f.truncate()

def remove_html_errors(output_dir, **kwargs):
    config_dict = kwargs['dag_run'].conf if kwargs['dag_run'].conf != {} else None
    source_dir = config_dict['source_dir']
    dest_dir_temp = f"{output_dir}{source_dir.replace('/storage','')}"
    os.makedirs(dest_dir_temp, exist_ok=True)

    replacements = {
        "&mu;": "µ",
        "&rsquo;": "'",
        "&ge;": "≥",
        "&le;": "≤",
        "&beta;": "β",
        "&alpha;": "α",
        "&mdash;": "-",
    }

    for filename in os.listdir(dest_dir_temp):
        if filename.endswith(".txt"):
            file_path = os.path.join(dest_dir_temp, filename)
            with open(file_path, "r+") as f:
                content = f.read()
                for entity, symbol in replacements.items():
                    content = content.replace(entity, symbol)

                f.seek(0)
                f.write(content)
                f.truncate()


def fix_encoding_errors(output_dir, **kwargs):
    config_dict = kwargs['dag_run'].conf if kwargs['dag_run'].conf != {} else None
    source_dir = config_dict['source_dir']
    dest_dir_temp = f"{output_dir}{source_dir.replace('/storage','')}"
    os.makedirs(dest_dir_temp, exist_ok=True)

    encoding_errors = {
        "'\|\"\|\"\|\"": "'",
        "•\|–\|—": "-",
        #" ": "",
        "\f": " ",
    }

    def read_file_with_fallback_encoding(filepath):
        encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
        for encoding in encodings:
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    return f.read(), encoding
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Could not decode file {filepath} with any of the tried encodings.")

    for root, _, files in os.walk(dest_dir_temp):
        for filename in files:
            filepath = os.path.join(root, filename)
            print(f"Processing: {filepath}")

            try:
                content, used_encoding = read_file_with_fallback_encoding(filepath)

                for error, replacement in encoding_errors.items():
                    content = re.sub(error, replacement, content)

                with open(filepath, "w", encoding="utf-8") as f_out:
                    f_out.write(content)
                
                print(f"File processed successfully: {filepath}")
            except ValueError as e:
                print(f"Error processing {filepath}: {str(e)}")
            except Exception as e:
                print(f"Unexpected error processing {filepath}: {str(e)}")