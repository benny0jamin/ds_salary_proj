import pandas as pd

def clean_data(df):
    """
    Cleans the dataset: removes duplicates or entries where no salary data is given,
    creates 'hourly' and 'employer_provided' columns, splits salary into min, max, and avg.
    """
    print(f"Original dataset shape: {df.shape}")

    # Remove duplicates and rows where salary is NaN, then reset the index.
    df = df.drop_duplicates().dropna(subset=['Salary Estimate']).reset_index(drop=True)

    print(f"Dataset shape after removing duplicates and no salary: {df.shape}")

    # Create 'hourly' and 'employer_provided' columns.
    df['Salary Estimate'] = df['Salary Estimate'].astype(str)
    df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
    df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

    # Split Salary Estimate into min and max, then remove all non-numeric characters
    df['min_salary'] = df['Salary Estimate'].apply(lambda x: x.split('-')[0])
    df['max_salary'] = df['Salary Estimate'].apply(lambda x: x.split('-')[1] if '-' in x else x.split('-')[0])
    
    # Remove all non-numeric characters
    df['min_salary'] = df['min_salary'].replace('[\$,K,a-z,A-Z,\s,\(,\),\:]', '', regex=True)
    df['max_salary'] = df['max_salary'].replace('[\$,K,a-z,A-Z,\s,\(,\),\:]', '', regex=True)


    # Convert min and max salary to int and calculate average salary
    df['min_salary'] = pd.to_numeric(df['min_salary'], errors='coerce') 
    df['max_salary'] = pd.to_numeric(df['max_salary'], errors='coerce') 

    # Convert hourly wage to annual salary
    df.loc[df['hourly'] == 1, 'min_salary'] = df['min_salary'] * 1920
    df.loc[df['hourly'] == 1, 'max_salary'] = df['max_salary'] * 1920

    df.loc[df['hourly'] == 0, 'min_salary'] *= 1000
    df.loc[df['hourly'] == 0, 'max_salary'] *= 1000

    df['avg_salary'] = (df['min_salary'] + df['max_salary']) / 2



    return df


def add_skills(dfs):
    """
    Adds a column for each skill in the skills list to the dataframe.
    Each column is populated with 1 if the job description contains the skill, and 0 otherwise.
    """
    # Specify the skills to add
    skills = ['python', 'azure', 'r studio', 'sql', 'hadoop', 'spark', 'java', 'sas', 'tableau', 'hive', 'scala', 'aws', 'tensorflow', 'c++', 'matlab', 'excel']
    # Make sure all text in the job description is lower case
    df['Job Description'] = df['Job Description'].str.lower()

    # For each skill, add a new column to the dataframe and check if the skill is in the job description
    for skill in skills:
        df[skill] = df['Job Description'].apply(lambda x: 1 if skill.lower() in x else 0)

    return df

def title_simplifier(title):
    if 'graduate' in title.lower():
        return 'graduate'
    elif 'data scientist' in title.lower() or 'data & analytics'in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower() or 'deep learning' in title.lower() or 'engineer' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'
    
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'

df = pd.read_csv('data\Data Scientist.csv')
df = clean_data(df)
# Add the skills to the dataframe
df = add_skills(df)
#Create simplified job titles
df['job_simp'] = df['Job Title'].apply(title_simplifier)
#Check for role seniority
df['seniority'] = df['Job Title'].apply(seniority)
#Calculate length of job description
df['desc_len'] = df['Job Description'].apply(lambda x: len(x))
df.to_csv('data\Data Scientist_cleaned.csv', index=False)

df.head()
