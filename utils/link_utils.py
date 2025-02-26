from utils.file_utils import FileUtils


class LinkUtils:
    @staticmethod
    def build_link(base_link, keyword, city):
        return f"{base_link}jobs?q={keyword}&l={city}&radius=25&sort=date&fromage=1"

    @staticmethod
    def check_link(link, json_path="resources/indeed.json"):
        job_list = FileUtils.convert_json_to_dict(json_path)
        if link in job_list:
            return False
        job_list.append(link)
        FileUtils.add_to_json(job_list, json_path)
        return True