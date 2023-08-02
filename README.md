# Australian Data Scientist - Salary Estimator
## Overview
- Created a tool which estimates Australian data scientist salaries based on a collection of parameters, such as job location, position seniority, company rating etc
- Scraped all available job listings from Glassdoor (196 available ~ 90 duplicates or lacking salary data) using python and Selenium
- Cleaned data and parsed job descriptions to find relevent parameters, such as programming language or software requirements
- Optimised Linear, Lasso and Random Forest Regressors using GridSearchCV to determine the best model
- Built a client facing RESTful API which was deployed and tested on a local server

## Code and Resources Used

- **Python Version:** 3.10
- **Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle
- **Project Inspiration Github:** https://github.com/PlayingNumbers/ds_salary_proj/
- **Scraper Github:** https://github.com/arapfaik/scraping-glassdoor-selenium
- **Scraper Article:** https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905
- **Flask Productionization:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2

## Web Scraping
Created Selenium based webscraper to collect data from Glassdoor. If any CAPTCHA screens are detected, script will pause and wait for the user to manually complete this step, at the time of writing this only occurs when the page is first loaded. The webscraper collects the follower data points from each listing:
- Estimated Salary (Max and Min)
- Job Title
- Company Title
- Company Rating
- Job Description
- Location

## Data Cleaning
After scraping, the data required cleaning to retrieve further data points and make it ingestible for the models.
- Parsed numeric data from salary estimates
- Create columns to indicate if salaries were provided by employers or estimated by Glassdoor
- Removed rows without salary
- Removed duplicate listings
- Parsed job description and made columns to determine if certain programming languages or skills were required
- Create column for a simplified representation of job title
- Create column for job seniority

## Exploratory Data Analysis


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
