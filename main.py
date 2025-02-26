import time
from multiprocessing import Process
from scrapper.job_scraper import JobScraper
from dotenv import load_dotenv
import os

load_dotenv()
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")


def run_scraper(base_link):
    while True:
        try:
            scraper = JobScraper(base_link, SPREADSHEET_URL)
            scraper.scrape_jobs()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    process = Process(target=run_scraper, args=("https://uk.indeed.com/",))
    process.start()