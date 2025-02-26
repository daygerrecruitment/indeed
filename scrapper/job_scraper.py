import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.file_utils import FileUtils
from utils.link_utils import LinkUtils
from utils.phone_extractor import PhoneExtractor
from scrapper.job_poster import JobPoster
import config.settings as settings


class JobScraper:
    def __init__(self, base_link, spreadsheet_url):
        self.base_link = base_link
        self.poster = JobPoster(spreadsheet_url)
        self.chrome_options = self._setup_chrome_options()

    def _setup_chrome_options(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--profile-directory={settings.CHROME_PROFILE}")
        options.add_argument(f"--user-data-dir={settings.CHROME_PATH}")

        return options

    def _get_driver(self):
        service = Service(os.path.join(os.getcwd(), 'resources', 'chromedriver'))
        return webdriver.Chrome(service=service, options=self.chrome_options)

    def scrape_jobs(self):
        keywords = FileUtils.read_txt("keywords.txt")  # Ensure list format
        cities = FileUtils.read_txt("cities.txt")  # Ensure list format

        for keyword in keywords:
            for city in cities:
                search_link = LinkUtils.build_link(self.base_link, keyword, city)
                print(f"Searching for '{keyword}' jobs in {city}...")  # Debugging print statement

                driver = self._get_driver()
                driver.get(search_link)
                time.sleep(2)
                try:
                    captcha_el = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH,"/html/body/main/h1"))
                    )
                    time.sleep(20)
                except Exception as e:
                    print("no captcha")
                try:
                    card_elements = WebDriverWait(driver, 3).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "cardOutline"))
                    )
                    self._process_job_cards(driver, card_elements, keyword, city)
                except (NoSuchElementException, TimeoutException):
                    print(f"No jobs found for '{keyword}' in {city}.")
                finally:
                    driver.quit()

    def _process_job_cards(self, driver, card_elements, keyword, city):
        links = []
        for card in card_elements:
            try:
                link_el = card.find_element(By.TAG_NAME, "a")
                link_id = link_el.get_attribute("id")
                job_link = f"{self.base_link}viewjob?jk={link_el.get_attribute('data-jk')}"
                if LinkUtils.check_link(link_id):
                    links.append(job_link)
            except NoSuchElementException:
                print("No link found")

        for link in links:
            driver.get(link)
            self._extract_job_details(driver, link, keyword, city)

    def _extract_job_details(self, driver, link, keyword, city):
        def safe_get(xpath):
            try:
                return WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()
            except (NoSuchElementException, TimeoutException):
                return "Not Provided"

        job_details = {
            "title": safe_get("//*[@id='viewJobSSRRoot']/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div[1]/h1/span") if safe_get("//*[@id='viewJobSSRRoot']/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div[1]/h1/span") else safe_get('//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[3]/div[1]/div[2]/h2'),
            "url": link,
            "company": safe_get("//div[@data-testid='inlineHeader-companyName']"),
            "rate": safe_get("//*[@id='salaryInfoAndJobType']/span[1]"),
            "location": safe_get('//*[@id="jobLocationText"]/div/span') if safe_get('//*[@id="jobLocationText"]/div/span')!="Not Provided" else safe_get("//div[@data-testid='job-location']"),
            "phoneNumbers": PhoneExtractor.extract_phone_numbers(safe_get('//*[@id="jobDescriptionText"]')) if PhoneExtractor.extract_phone_numbers(safe_get('//*[@id="jobDescriptionText"]')) else ["Not Provided"],
            "source": "Indeed",
            "keyword": keyword,
            "city": city
        }
        print(job_details)
        self.poster.post_job(job_details)
