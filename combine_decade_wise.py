# %%
import os
import re
from collections import defaultdict


def combine_files_by_decade(year_dir):
    files_by_decade = defaultdict(list)
    year_pattern = re.compile(r"combined_(19|20)\d{2}\.txt")

    for file in os.listdir(year_dir):
        match = year_pattern.search(file)
        if match:
            year = match.group(0)[9:13]
            decade = year[:3] + "0s"
            file_path = os.path.join(year_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            files_by_decade[decade].append(content)

    decade_output_dir = os.path.join(year_dir, "combined_files_by_decade")
    os.makedirs(decade_output_dir, exist_ok=True)

    for decade, contents in files_by_decade.items():
        combined_content = "\n".join(contents)
        output_file = os.path.join(decade_output_dir, f"combined_{decade}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(combined_content)

    print(f"Combined files by decade have been saved in '{decade_output_dir}'")


# %%
year_combined_dir = ""
combine_files_by_decade(year_combined_dir)

# %%
