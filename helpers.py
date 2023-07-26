
'''
Author: Ben
Date: 26-07-2023
'''
import os

def write_to_csv(df, filename, directory='./'):
    '''Writes a pandas DataFrame to a CSV file.'''
    # Check if directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    file_path = os.path.join(directory, filename)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")
    
