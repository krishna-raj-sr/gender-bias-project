#%%
import os
import pandas as pd
import re

#%% Function to extract year from filename
def extract_first_year_from_title(title):
    # Define a pattern to match years, including those in ranges like '2010-2014'
    # This pattern will also attempt to capture shorter year formats
    year_pattern = re.compile(r'(?<!\d)(\d{2,4})(?:-(\d{2,4}))?(?!\d)')

    # Find all matches within the title
    matches = year_pattern.findall(title)
    
    # Process each match to handle year ranges and single years
    years = []
    for match in matches:
        start_year, end_year = match
        if start_year:
            # Handle two-digit years assuming they are after 2000
            if len(start_year) == 2:
                start_year = f'20{start_year}'
            years.append(start_year)
        if end_year:
            if len(end_year) == 2:
                if end_year < start_year[-2:]:  # If it appears to be a new century
                    end_year = f'20{end_year}'
                else:
                    end_year = f'{start_year[:2]}{end_year}'
            years.append(end_year)
    first_item = next(iter(years), None)
    return first_item


def extract_years_from_title(title):
    # Define a pattern to match years, including those in ranges like '2010-2014'
    # This pattern will also attempt to capture shorter year formats
    year_pattern = re.compile(r'(?<!\d)(\d{2,4})(?:-(\d{2,4}))?(?!\d)')

    # Find all matches within the title
    matches = year_pattern.findall(title)
    
    # Process each match to handle year ranges and single years
    years = []
    for match in matches:
        start_year, end_year = match
        if start_year:
            # Handle two-digit years assuming they are after 2000
            if len(start_year) == 2:
                start_year = f'20{start_year}'
            years.append(start_year)
        if end_year:
            if len(end_year) == 2:
                if end_year < start_year[-2:]:  # If it appears to be a new century
                    end_year = f'20{end_year}'
                else:
                    end_year = f'{start_year[:2]}{end_year}'
            years.append(end_year)

    return years

# List to store file details
def get_year_details(folder_path,ext = ".txt"):
    file_details = []

# Iterate over files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(ext):
                filepath = os.path.join(root, file)
                filename = os.path.splitext(file)[0]
                year = extract_years_from_title(str(filename))
                first_item = next(iter(year), None)
                file_details.append({'Path': filepath, 'Filename': filename, 'Years': year,"First Year":first_item})
    return file_details


# %%
