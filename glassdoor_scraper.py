from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

def create_driver():
    '''Creates an instance of Chrome WebDriver.'''
    options = Options()
    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1120, 1000)
    return driver

def wait_for_job_description_to_change(driver, jobs, timeout=5):
    '''Wait until the job description changes or the timeout is reached.'''
    start_time = time.time()
    last_job_description = jobs[-1]['Job Description'] if jobs else None

    while True:
        # Get the current job description
        current_job_description = get_element_text(driver, 'div.jobDescriptionContent.desc')

        # If the job description has changed and is not empty, return True
        if current_job_description != last_job_description and current_job_description != "":
            return True

        # If the timeout has been reached, return False
        if time.time() - start_time > timeout:
            print(f"Job description did not change after {timeout} seconds.")
            return False

        # Wait for a second before checking again
        time.sleep(1)


def scrape_job_details(driver, verbose):
    '''Scrapes job details from the job listing page.'''
    company_name = get_element_text(driver, '[data-test="employerName"]')
    location = get_element_text(driver, '[data-test="location"]')
    job_title = get_element_text(driver, '[data-test="jobTitle"]')
    job_description = get_element_text(driver, 'div.jobDescriptionContent.desc')
    salary_estimate = get_element_text(driver, '[data-test="detailSalary"]')
    rating = get_element_text(driver, '[data-test="rating-info"]')

    if verbose:
        print(f"Job Title: {job_title}")
        print(f"Salary Estimate: {salary_estimate}")
        print(f"Job Description: {job_description[:500]}")
        print(f"Rating: {rating}")
        print(f"Company Name: {company_name}")
        print(f"Location: {location}")

    return {
        "Job Title": job_title,
        "Salary Estimate": salary_estimate,
        "Job Description": job_description,
        "Rating": rating,
        "Company Name": company_name,
        "Location": location,
    }


def get_element_text(driver, css_selector):
    '''Attempts to get an element's text. Returns an empty string if the element is not found.'''
    try:
        print(f"Searching for {css_selector}")
        element_text = driver.find_element(By.CSS_SELECTOR, '#JDCol ' + css_selector).text
        print(f"Found element:")
        return element_text
    except NoSuchElementException:
        print(f"No element found for CSS selector: {css_selector}")
        return ""

def get_jobs(keyword, num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor.'''

    driver = create_driver()
    url = f'https://www.glassdoor.com.au/Job/{keyword}-jobs-SRCH_KO0,14.htm'
    driver.get(url)

    # CAPTCHA handling
    while True:
        try:
            # Check for the presence of the CAPTCHA.
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "challenge-form"))
            )
            print("CAPTCHA detected. Please solve it manually.")
            time.sleep(10)
        except Exception as e:
            # If the CAPTCHA is not found, break the loop.
            print("Captcha Solved")
            break

    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.
        time.sleep(4)  # Let the page load. Change this number based on your internet speed.
        
        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]').click()
            print('------------Closed signup pop up 1---------')
        except NoSuchElementException:
            pass

        # Going through each job in this page
        job_buttons = driver.find_elements(By.CSS_SELECTOR,"li.react-job-listing")
        for job_index in range(len(job_buttons)):
            # Find the specific job button for this iteration
            job_button = driver.find_element(By.CSS_SELECTOR,f"li.react-job-listing:nth-of-type({job_index + 1})")
            ActionChains(driver).move_to_element(job_button).click(job_button).perform()
            
            # Test for the "Sign Up" prompt and get rid of it.
            try:
                driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]').click()
                print('------------Closed signup pop up 2---------')
                time.sleep(2)
            except NoSuchElementException:
                pass    

            if wait_for_job_description_to_change(driver, jobs):
                job_info = scrape_job_details(driver, verbose)
                jobs.append(job_info)
                print(f'completed {len(jobs)} of {num_jobs} ')
            else:
                print(f"Skipping job {job_index} due to timeout.")

            if len(jobs) >= num_jobs:
                break

        # Clicking on the "next page" button
        if len(jobs) < num_jobs:
            try:
                driver.find_element(By.CSS_SELECTOR, 'button[data-test="pagination-next"]').click()
            except NoSuchElementException:
                print(f"Scraping terminated before reaching target number of jobs. Needed {num_jobs}, got {len(jobs)}.")
                break

    driver.quit()

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame

# # This line will open a new chrome window and start the scraping.
# df = get_jobs("data scientist", 5, False)
# df

