import requests

class JobPoster:
    def __init__(self, spreadsheet_url):
        self.spreadsheet_url = spreadsheet_url

    def post_job(self, job_details):
        try:
            response = requests.post(self.spreadsheet_url, json=job_details)
            response.raise_for_status()
            print("Job posted successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Failed to post job details: {e}")