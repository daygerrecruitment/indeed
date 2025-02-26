from utils.file_utils import convert_json_to_dict as cj
from utils.file_utils import add_to_json as aj
def build_link(base_link, keyword, city):
    """
    Builds a list of job search links based on keywords and cities.

    Args:
        base_link (str): The base URL for the job search site.
        keyword (str): The keyword to search for.
        city (str): The city to search in.
    Returns:
        str: a link to the job search
    """
    return f"{base_link}jobs?q={keyword}&l={city}&radius=25&sort=date"


def check_link(link):

    json_path = "resources/indeed.json"
    job_list = cj(json_path)

    if link in job_list:
        checker = False
    else:
        checker = True
        job_list.append(link)
        aj(job_list, json_path)
    return checker