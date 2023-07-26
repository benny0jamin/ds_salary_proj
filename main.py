import glassdoor_scraper as gs

df = gs.get_jobs("data scientist", 5, False)

print(df)