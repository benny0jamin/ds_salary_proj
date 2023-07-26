'''
Author: Ben
Date: 26-07-2023
'''
import glassdoor_scraper as gs
import helpers

df = gs.get_jobs("data scientist", 200, False)

print(df)
helpers.write_to_csv(df, 'Data Scientist.csv', './data')