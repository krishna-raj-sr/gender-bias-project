# %%
import os
import re
from collections import defaultdict


def combine_files_by_year(root_dir):
    # Dictionary to hold file contents grouped by year
    files_by_year = defaultdict(list)

    # Regular expression to match the year in filenames
    year_pattern = re.compile(r"(19|20)\d{2}")
    temp = []
    # Walk through the directory and its subdirectories
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(subdir, file)

                # Extract the year from the filename
                match = year_pattern.search(file)
                if match:
                    temp.append(file)
                    year = match.group(0)

                    # Read the file content
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Append the content to the corresponding year
                    files_by_year[year].append(content)
    print(temp)
    temp3 = [x for x in files if x not in temp]
    print("not_added:", temp3)
    # Create a directory to save the combined files
    output_dir = os.path.join(root_dir, "combined_files_by_year")
    os.makedirs(output_dir, exist_ok=True)

    # Write the combined contents to new files
    for year, contents in files_by_year.items():
        combined_content = "\n".join(contents)
        output_file = os.path.join(output_dir, f"combined_{year}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(combined_content)

    print(f"Combined files have been saved in '{output_dir}'")


root_directory = ""
combine_files_by_year(root_directory)
