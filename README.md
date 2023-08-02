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
Investigated the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables.
Interesting to note the emphasis on team work related terms as opposed to technical skillsets, may indicate companies are beggining to view Data Scientists as integral components of a modern workforce. 

![Heatmap](https://github.com/benny0jamin/ds_salary_proj/blob/main/Images/location.png) ![Heatmap](https://github.com/benny0jamin/ds_salary_proj/blob/main/Images/hm_features.png)
![Heatmap](https://github.com/benny0jamin/ds_salary_proj/blob/main/Images/salary_hist.png) ![Heatmap](https://github.com/benny0jamin/ds_salary_proj/blob/main/Images/wordcloud.png)

## Model Building
Categorical variable converted into dummy variables. 
Split the data into train and tests sets with a test size of 20%.
Implemented three different models and evaluated them using Mean Absolute Error. 

Multiple Linear Regression – Baseline for the model
Lasso Regression – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
Random Forest – Again, with the sparsity associated with the data, I thought that this would be a good fit.

## Model performance
The Random Forest model far outperformed the other approaches on the test and validation sets.

Random Forest : MAE = 11.22
Linear Regression: MAE = 18.86
Ridge Regression: MAE = 19.67
