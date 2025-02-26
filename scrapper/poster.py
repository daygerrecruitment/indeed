import requests

class JobPoster:
    def __init__(self, spreadsheet_url):
        self.spreadsheet_url = spreadsheet_url

    def post_job(self, job_details):
        """
           Sends job details to the spreadsheet.
           """
        data = {
            "title": job_details["title"],
            "url": job_details["url"],
            "company": job_details["company"],
            "rate": job_details["salary"],
            "location": job_details["location"],
            "phoneNumbers": job_details["phone_numbers"],
            "source": job_details["source"],
            "keyword": job_details["keyword"],
            "city": job_details["city"],
        }
        try:
            response = requests.post(self.spreadsheet_url, json=data)
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")
            response.raise_for_status()
            print("Job posted successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Failed to post job details: {e}")

