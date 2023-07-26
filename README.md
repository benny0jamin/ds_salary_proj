# Glassdoor Web Scraper

This project contains Python scripts for web scraping job listings from Glassdoor using Selenium.

## Description

The project consists of three main Python scripts:

- `main.py`: The main driver script that calls the scraping function with the desired job keyword and number of jobs to scrape.

- `glassdoor_scraper.py`: Contains the main scraping functions, including creating a Selenium WebDriver instance, navigating the Glassdoor website, handling CAPTCHAs and popups, and extracting job details.

- `helpers.py`: Includes a helper function for converting df to csv

The scripts extract job details including the job title, company name, location, job description, salary estimate, and company rating. The scraped data is then saved to a CSV file.

## Usage
First, modify the following line in the main.py script with your desired job keyword and the number of jobs you want to scrape:
```
get_jobs("data scientist", 5, False)
```

Then, run the script:
```
python main.py
```
