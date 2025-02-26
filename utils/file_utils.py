import os
import json

def read_txt(file_name):
    """
    Reads a file and returns a list of words.

    Args:
        file_name (str): The path to the file.

    Returns:
        list: A list of words extracted from the file.
    """

    def format_keyword(word):
        """
        Formats a keyword by replacing spaces with '%20' if it consists of multiple words.
        """
        if " " in word:
            return word.replace(" ", "%20")
        return word


    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    file_path = os.path.join(project_root, 'resources', file_name)

    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
        word_list = [word.strip() for word in data.split(',')]
        formatted_words = [format_keyword(word) for word in word_list]
    return formatted_words


def convert_json_to_dict(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def add_to_json(job_list, json_file):
    with open(json_file, 'w') as f:
        json.dump(job_list, f)