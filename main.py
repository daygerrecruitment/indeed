import time
from config.settings import SPREADSHEET_URL
from scrapper.scrapper import JobScraper
from multiprocessing import Process


def run_scraper(base_link):
    """
    Runs the job scraper for the specified base link.

    Args:
        base_link (str): The base URL for the job scraper.
    """
    while True:
        try:
            print(f"Starting job scraper for {base_link}...")
            scraper = JobScraper(base_link, SPREADSHEET_URL)
            scraper.scrape_jobs()
            print(f"Job scraper for {base_link} completed. Waiting for the next run...")
        except Exception as e:
            print(f"An error occurred for {base_link}: {e}")

        time.sleep(5)


def main():
    # Define base links for both scrapers
    base_link = "https://uk.indeed.com/"
    process = Process(target=run_scraper, args=(base_link,))
    process.start()

if __name__ == "__main__":
    main()

    #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