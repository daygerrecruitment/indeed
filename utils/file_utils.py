import os
import json

class FileUtils:
    @staticmethod
    def read_txt(file_name):
        file_path = os.path.join("resources", file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.read().split(',')]


    @staticmethod
    def convert_json_to_dict(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)

    @staticmethod
    def add_to_json(job_list, json_file):
        with open(json_file, 'w') as f:
            json.dump(job_list, f)