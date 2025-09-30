# %% Imports
import os
import re
from collections import Counter
from nltk import bigrams
import pandas as pd
import numpy as np
import glob

# %% Import the word list
wordlist_file = r"Gender WordList - main.csv"
df = pd.read_csv(wordlist_file)
df = df.where(pd.notnull(df), None)

word_list = df.values.tolist()
search_words = [item for sublist in word_list for item in sublist if item is not None]
search_words = list(set(search_words))

gender = {
    "masculine": set(df["masculine"][df["masculine"].notna()].values.tolist()),
    "feminine": set(df["feminine"][df["feminine"].notna()].values.tolist()),
    "neutral": set(df["neutral"][df["neutral"].notna()].values.tolist()),
}
# %%
lookup_df = pd.read_csv(
    "Gender WordList - plural_lookup.csv"
)  # The lookup table should have 'Singular' and 'Plural' columns
plural_to_singular = pd.Series(
    lookup_df.Singular.values, index=lookup_df.Plural
).to_dict()
plural_to_singular = {
    k.strip().lower(): v.strip()
    for k, v in zip(lookup_df["Plural"], lookup_df["Singular"])
}
# %%
input_folder = r""
parent_folder = os.path.dirname(input_folder)
# %%
""" Replace Plural With Singular"""


def replace_plural_with_singular(df, column_name, plural_to_singular):
    df[column_name] = df[column_name].apply(lambda x: plural_to_singular.get(x, x))
    return df


def replace_plural_with_singular(df, column_name, plural_to_singular):
    # Replace plurals with singulars in the specified column
    df[column_name] = df[column_name].apply(
        lambda x: plural_to_singular.get(str(x).strip().lower(), x)
    )

    return df


# %% Read text file
def read_file_content(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            text = file.read()
    except UnicodeDecodeError:
        try:
            with open(file_name, "r", encoding="latin1") as file:
                text = file.read()
        except UnicodeDecodeError:
            with open(file_name, "r", encoding="cp1252") as file:
                text = file.read()
    return text


# %% Count the Words
def normalize_text(text):
    return re.sub(r"[^\w\s]", " ", text.lower())


def count_words(text, search_words):
    normalized_text = normalize_text(text)
    words = normalized_text.split()
    word_counter = Counter(words)
    counts = []

    # First count multi-word phrases
    multi_word_counts = {}
    for phrase in search_words:
        if " " in phrase:
            normalized_phrase = " ".join(normalize_text(phrase).split())
            count = normalized_text.count(" " + normalized_phrase + " ")
            multi_word_counts[phrase] = count
            counts.append({"Word": phrase, "Count": count})

    # Adjust counts of individual words based on multi-word phrase counts
    for word in search_words:
        if " " not in word:
            adjusted_count = word_counter[word]
            for phrase, phrase_count in multi_word_counts.items():

                if word in phrase.split():
                    adjusted_count -= phrase_count
            counts.append({"Word": word, "Count": max(adjusted_count, 0)})

    df = pd.DataFrame(counts)
    df = replace_plural_with_singular(df, "Word", plural_to_singular)
    df = df.groupby("Word")["Count"].sum().reset_index()
    return df


# %% # Apply function to create 'Gender' column
def assign_gender(word):
    for key, word_list in gender.items():
        if word in word_list:
            return key
    return None  # Return None if word not found in any category


# %%
def extract_year(file_name):
    match = re.search(r"(19|20)\d{2}", file_name)
    if match:
        year = int(match.group(0))
        if 1950 <= year <= 2024:
            return year
        else:
            return None
    else:
        print(f"couldnt extract year: {file_name}")
        return None


def get_decade(year):
    try:
        return (year // 10) * 10
    except:
        print(year)


# %%
def read_file_and_save(filename, output_folder):
    text = read_file_content(filename)
    df_counts = count_words(text, search_words)
    df_counts["Gender"] = df_counts["Word"].apply(assign_gender)
    df_counts["Filename"] = filename
    df_counts["Year"] = df_counts["Filename"].apply(extract_year)
    df_counts["Decade"] = df_counts["Year"].apply(get_decade)
    base_name = os.path.splitext(os.path.basename(filename))[0]
    df_counts.to_csv(output_folder + "/" + base_name + ".csv")


# %% Take an input folder and find the counts

output_folder = os.path.join(parent_folder, "COUNTS")
os.makedirs(output_folder, exist_ok=True)

for file_name in glob.glob(f"{input_folder}\*.txt"):
    read_file_and_save(file_name, output_folder)

# %%  #read csv files one by one

final_df = pd.DataFrame(
    columns=[
        "Filename",
        "Year",
        "Decade",
        "feminine_count",
        "masculine_count",
        "neutral_count",
        "feminine_norm",
        "masculine_norm",
        "neutral_norm",
    ]
)
for file_name in glob.glob(f"{output_folder}\*.csv"):
    df_counts = pd.read_csv(file_name)

    gender_count = df_counts.groupby("Gender")["Count"].sum()
    total_feminine = gender_count.get("feminine", 0)
    total_masculine = gender_count.get("masculine", 0)
    total_neutral = gender_count.get("neutral", 0)
    total_counts = total_feminine + total_masculine + total_neutral
    result_dict = {
        "Filename": df_counts["Filename"].iloc[0],
        "Year": df_counts["Year"].iloc[
            0
        ],  # Assuming 'Year' is the same for all rows in the file
        "Decade": df_counts["Decade"].iloc[0],  #
        "feminine_count": total_feminine,
        "masculine_count": total_masculine,
        "neutral_count": total_neutral,
        "feminine_norm": total_feminine / total_counts,
        "masculine_norm": total_masculine / total_counts,
        "neutral_norm": total_neutral / total_counts,
    }

    final_df = pd.concat([final_df, pd.DataFrame([result_dict])], ignore_index=True)
final_df.to_csv(f"{parent_folder}/final_combined_trend.csv")
# %% Read and Concatenate CSV Files
all_files = glob.glob(f"{output_folder}/*.csv")
dfs = []
for filename in all_files:
    df = pd.read_csv(filename)
    dfs.append(df)

df_concat = pd.concat(dfs, ignore_index=True)
filename = os.path.join(parent_folder, "all_counts_combined.csv")
df_concat.to_csv(filename)
# %%
