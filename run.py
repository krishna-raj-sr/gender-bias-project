# %%
# Standard library
import os
from pathlib import Path

# Third-party libraries
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Local application imports
import constants as c
import helper as h
from filefolder import filename_year as ffy
from gender.genbit import genbit as gb
from gender.genbit import combine_genbit_scores as cgs
from gender.genbit import visualization as vs

import pandas as pd
import re

INPUT_FOLDER = c.ANNUAL_REPORTS
OUTPUT_FOLDER = os.path.join(c.OUTPUT_FOLDER, Path(*Path(INPUT_FOLDER).parts[2:]))

# %%
output_folder_txt = os.path.join(OUTPUT_FOLDER, "TXT")
output_folder_csv = os.path.join(OUTPUT_FOLDER, "CSV")
output_folder_cleaned = os.path.join(OUTPUT_FOLDER, "CLEANED")

# %% Uncomment and call the functions as needed based on your workflow
h.process_pdfs_to_txt(INPUT_FOLDER, output_folder_txt)
h.extract_sentences_from_txt_to_csv(output_folder_txt, output_folder_csv)
h.preprocess_csv_files(output_folder_csv, output_folder_cleaned)

folder_path = os.path.join(OUTPUT_FOLDER, "CLEANED_TXT")
output_folder_genbit = os.path.join(OUTPUT_FOLDER, "GENBIT")
os.makedirs(output_folder_genbit, exist_ok=True)
gb.aggregate_genbit_metrics(folder_path, output_folder_genbit)


# %%
# Function to recursively find JSON files and collect their paths and parent folder names
def collect_json_paths(root_folder):
    json_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".json"):
                json_files.append(
                    {
                        "folder_name": os.path.basename(root),
                        "file_path": os.path.join(root, file),
                    }
                )
    return json_files


# Define your root folder containing subfolders with JSON files
root_folder = r"F:\KSR\mag"

# Collect JSON file paths and folder names into a dataframe
json_data = collect_json_paths(root_folder)
df = pd.DataFrame(json_data)

string_to_remove = "all_file_metrics"
# Filter out rows containing the string in 'folder_name' column
filtered_df = df[~df["file_path"].str.contains(string_to_remove)]

# %%
# folder_path = os.path.join(OUTPUT_FOLDER, "GENBIT")
folder_path = r"F:\KSR\mag"
output_file_path = os.path.join(folder_path, "genbit_final.csv")
# cgs.load_metrics_from_json_folder(folder_path, output_file_path, allowed_keys=c.NEEDED_KEYS)

cgs.load_metrics_from_json_filepaths(
    filtered_df["file_path"].values, output_file_path, allowed_keys=c.NEEDED_KEYS
)

# %% Generate Combined

folder = r"F:\KSR\mag"
oitf = os.path.join(folder, "iitmcombined.csv")
cgs.load_metrics_from_json_folder(folder, "iitmcombined.csv")

# %%
output_folder = os.path.join(folder, "csv")
cgs.extract_token_metrics_from_json_folder(folder, output_folder)

# %%
oitf = os.path.join(folder, "combined_word_stuff.csv")
cgs.combine_csv_files(output_folder, oitf)

# %%

# Load the combined CSV file
combined_csv_path = oitf
df = pd.read_csv(combined_csv_path)


# %% Function to extract the year from the filename
def extract_year(filename):
    match = re.search(r"\d{4}", filename)
    return int(match.group(0)) if match else None


# Extract year and decade from filename
df["year"] = df["filename"].apply(extract_year)
df["decade"] = (df["year"] // 10) * 10

# Group by token_based_metric and decade, and sum the specified columns
grouped_df = (
    df.groupby(["token_based_metric", "decade"])
    .agg(
        {
            "frequency": "sum",
            "female_count": "sum",
            "male_count": "sum",
            "non_binary_count": "sum",
            "trans_count": "sum",
            "cis_count": "sum",
        }
    )
    .reset_index()
)

# Save the result to a new CSV file
output_path = "grouped_token_metrics.csv"
grouped_df.to_csv(output_path, index=False)

# %%
grouped_df = (
    df.groupby(["token_based_metric"])
    .agg(
        {
            "frequency": "sum",
            "female_count": "sum",
            "male_count": "sum",
            "non_binary_count": "sum",
            "trans_count": "sum",
            "cis_count": "sum",
            "bias_ratio": "sum",
        }
    )
    .reset_index()
)
