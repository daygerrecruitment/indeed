import os
import config.settings as settings

from time import sleep
from selenium import webdriver
from scrapper.poster import JobPoster
from utils.file_utils import read_txt
from utils.link_utils import build_link
from utils.link_utils import check_link
from selenium.webdriver.common.by import By
from utils.phone_numbers import extract_phone_numbers
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException




class JobScraper:
    def __init__(self, base_link, spreadsheet_url):
        self.base_link = base_link
        self.poster = JobPoster(spreadsheet_url)

    def scrape_jobs(self):
        keyword_list = read_txt("keywords.txt")
        city_list = read_txt("cities.txt")

        for keyword in keyword_list:
            for city in city_list:
                search_link = build_link(self.base_link, keyword, city)
                chrome_options = Options()

                # Replace with your actual user data directory path
                # For example, on Linux:
                user_data_dir = settings.CHROME_PATH
                chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

                # Specify the profile folder you want to use (e.g., "Profile 1")
                chrome_options.add_argument(f"--profile-directory={settings.CHROME_PROFILE}")
                # (Optional) Add other arguments if needed:
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")

                # Define the path to your chromedriver
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.abspath(os.path.join(current_dir, '..'))

                chrome_driver_path = os.path.join(project_root, 'resources', 'chromedriver')

                # Set up the service object
                service = Service(chrome_driver_path)

                # Initialize the Chrome WebDriver with the specified options

                links=[]
                driver = webdriver.Chrome(service=service, options=chrome_options)
                sleep(1)
                driver.get(search_link)
                try:
                    captcha_el = WebDriverWait(driver,3).until(
                        EC.presence_of_element_located((By.XPATH,"/html/body/main/h1"))
                    )
                    sleep(25)
                except Exception:
                    print("no captcha")
                # Navigate to a website to test
                try:
                    card_elements = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "cardOutline"))
                    )
                    try:
                        for card_element in card_elements:
                            link_el = card_element.find_element(By.TAG_NAME, "a")
                            print("link")
                            link_id = link_el.get_attribute("id")
                            print("link_id")
                            if not check_link(link_id):
                                print("link not found")
                                continue
                            jk = link_el.get_attribute("data-jk")
                            print("jk")
                            job_link = f"{self.base_link}viewjob?jk={jk}"
                            print("job_link")
                            links.append(job_link)
                    except NoSuchElementException:
                        print("no link")
                    try:
                        for link in links:
                            driver.get(link)

                            try:
                                job_title_el = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-JobInfoHeader-title"))
                                )
                                job_title = job_title_el.text.strip()
                                print(job_title)
                            except NoSuchElementException:
                                print("Title not found")

                            try:
                                company_name_el = WebDriverWait(driver, 1).until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, "//div[@data-testid='inlineHeader-companyName']"))
                                )
                                company_name = company_name_el.text.strip()
                                print(company_name)
                            except NoSuchElementException:
                                print("Company not found")

                            try:
                                location_el = WebDriverWait(driver, 1).until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, '//*[@id="jobLocationText"]/div/span')
                                    )
                                )
                                location = location_el.text.strip()
                                print(location)
                            except (NoSuchElementException, TimeoutException):
                                print("SECOND ATTEMPT")
                                try:
                                    location_el = WebDriverWait(driver, 1).until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, '//div[@data-testid="job-location"]')
                                    )
                                )
                                    location = location_el.text.strip()
                                    print(location)
                                except (NoSuchElementException, TimeoutException):
                                    print("Location not found")
                            try:
                                salary_el = WebDriverWait(driver, 1).until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, '//*[@id="salaryInfoAndJobType"]/span[1]')
                                    )
                                )
                                salary = salary_el.text.strip()
                                print(salary)
                            except (NoSuchElementException, TimeoutException):
                                salary = "Not Provided"

                            try:
                                description_el = WebDriverWait(driver, 1).until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, '//*[@id="jobDescriptionText"]')
                                    )
                                )
                                description = description_el.text.strip()
                                print(description)
                            except (NoSuchElementException, TimeoutException):
                                print("No description")

                            phone_numbers = extract_phone_numbers(description)
                            print(phone_numbers)
                            job_details = {"title": job_title, "url": link, "company": company_name,
                                           "salary": salary, "location": location,
                                           "phone_numbers": phone_numbers if phone_numbers else [
                                               "NOT FOUND IN DESCRIPTION"], "source": "Indeed", "keyword": keyword,
                                           "city": city}
                            self.poster.post_job(job_details)






                    except NoSuchElementException:
                        print("No link found")
                except (NoSuchElementException, TimeoutException) :
                    print("No Jobs")
                finally:
                    sleep(2)
                    driver.quit()





