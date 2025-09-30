# %%
import pandas as pd
import plotly.express as px
import glob
import os

# %% Import the word list
wordlist_file = r"Gender WordList - main.csv"
df = pd.read_csv(wordlist_file)
df = df.where(pd.notnull(df), None)
word_list = df.values.tolist()
search_words = [item for sublist in word_list for item in sublist if item is not None]
search_words = list(set(search_words))
# %%
gender = {
    "masculine": list(set(df["masculine"][df["masculine"].notna()].values.tolist())),
    "feminine": list(set(df["feminine"][df["feminine"].notna()].values.tolist())),
    "neutral": list(set(df["neutral"][df["neutral"].notna()].values.tolist())),
}
# %% Compiled Statisti
file_name = r"data\output\Annual reports - IITM\final_combined_trend.csv"
df_all = pd.read_csv(file_name)
parent_folder = os.path.dirname(file_name)
# %% All word_count_combined
file_name = r"data\output\Annual reports - IITM\all_counts_combined.csv"
combined_df = pd.read_csv(file_name)

""" DECADE NORMALIZED COUNT PLOT"""
# %% Group by decade and calculate the mean for normalized counts, considering only numeric columns
decade_trends = (
    df_all.groupby("Decade")[["feminine_norm", "masculine_norm", "neutral_norm"]]
    .mean()
    .reset_index()
)

# Create the plot using Plotly
fig = px.line(
    decade_trends,
    x="Decade",
    y=["feminine_norm", "masculine_norm", "neutral_norm"],
    labels={"value": "Normalized Count", "variable": "Type"},
    title="Decadewise Trend of Normalized Counts",
)

# Show the plot
fig.update_layout(width=1000, height=400)
fig.show()
fn = os.path.join(parent_folder, "decade_annual.svg")
# fig.write_image(fn)
# %%
""" Year NORMALIZED COUNT PLOT"""
# %% Group by decade and calculate the mean for normalized counts, considering only numeric columns
decade_trends = (
    df_all.groupby("Year")[["feminine_norm", "masculine_norm", "neutral_norm"]]
    .mean()
    .reset_index()
)

# Create the plot using Plotly
fig = px.bar(
    decade_trends,
    x="Year",
    y=["feminine_norm", "masculine_norm", "neutral_norm"],
    labels={"value": "Normalized Count", "variable": "Type"},
    title="Yearwise Trend of Normalized Counts",
)

# Show the plot
fig.update_layout(width=1000, height=400)
fig.update_xaxes(tickvals=decade_trends["Year"])

fig.show()
fn = os.path.join(parent_folder, "year_annual.svg")
fig.write_image(fn)


# %%
total_counts = combined_df.groupby(["Word", "Gender"])["Count"].sum().reset_index()

# Find the top most frequent words for each gender category
top_masculine_words = total_counts[total_counts["Gender"] == "masculine"].nlargest(
    10, "Count"
)
top_feminine_words = total_counts[total_counts["Gender"] == "feminine"].nlargest(
    10, "Count"
)
top_neutral_words = total_counts[total_counts["Gender"] == "neutral"].nlargest(
    10, "Count"
)

# Combine the top words into a single DataFrame for plotting
top_words = pd.concat([top_masculine_words, top_feminine_words, top_neutral_words])

# Plot the counts of these words
fig = px.bar(
    top_words,
    x="Count",
    y="Word",
    color="Gender",
    orientation="h",
    title="Top 10 Most Frequent Masculine, Feminine, and Neutral Words",
    labels={"Count": "Total Count", "Word": "Word"},
    height=600,
)

fig.update_layout(yaxis={"categoryorder": "total ascending"})
fig.show()


# %% Find the top most frequent words for each gender category
top_masculine_words = total_counts[total_counts["Gender"] == "masculine"].nlargest(
    20, "Count"
)
top_feminine_words = total_counts[total_counts["Gender"] == "feminine"].nlargest(
    20, "Count"
)
top_neutral_words = total_counts[total_counts["Gender"] == "neutral"].nlargest(
    20, "Count"
)

# Plot the counts of the top masculine words
fig_masculine = px.bar(
    top_masculine_words[top_masculine_words["Count"] >= 1],
    x="Count",
    y="Word",
    orientation="h",
    title="Top 10 Most Frequent Masculine Words",
    labels={"Count": "Total Count", "Word": "Word"},
    height=600,
)

fig_masculine.update_layout(yaxis={"categoryorder": "total ascending"})
fig_masculine.show()
fn = os.path.join(parent_folder, "fig_masculine.svg")
fig_masculine.write_image(fn)

# Plot the counts of the top feminine words
fig_feminine = px.bar(
    top_feminine_words,
    x="Count",
    y="Word",
    orientation="h",
    title="Top 10 Most Frequent Feminine Words",
    labels={"Count": "Total Count", "Word": "Word"},
    height=600,
)

fig_feminine.update_layout(yaxis={"categoryorder": "total ascending"})
fig_feminine.show()
fn = os.path.join(parent_folder, "fig_feminine.svg")
fig_feminine.write_image(fn)
# Plot the counts of the top neutral words
fig_neutral = px.bar(
    top_neutral_words,
    x="Count",
    y="Word",
    orientation="h",
    title="Top 10 Most Frequent Neutral Words",
    labels={"Count": "Total Count", "Word": "Word"},
    height=600,
)

fig_neutral.update_layout(yaxis={"categoryorder": "total ascending"})
fig_neutral.show()
fn = os.path.join(parent_folder, "fig_neutral.svg")
fig_neutral.write_image(fn)
# %%
# List of chosen words to plot
chosen_words = ["chairman", "chairwomen", "chairperson"]

# Filter the DataFrame for the chosen words
chosen_df = combined_df[combined_df["Word"].isin(chosen_words)]

# List of decades you are interested in
# interested_decades = [1960, 2010, 2020]
# Filter the DataFrame for the chosen words and interested decades
# chosen_df = combined_df[(combined_df['Word'].isin(chosen_words)) & (combined_df['Decade'].isin(interested_decades))]
chosen_df = combined_df[
    (combined_df["Word"].isin(chosen_words))
    & (combined_df["Decade"] >= 1960)
    & (combined_df["Decade"] <= 2010)
]


# Group by decade and word, summing the counts
grouped = chosen_df.groupby(["Decade", "Word"])["Count"].sum().reset_index()

# Create the plot using Plotly
fig = px.bar(
    grouped,
    x="Decade",
    y="Count",
    color="Word",
    barmode="group",
    title="Count of Chosen Words by Decade",
)

fig.update_layout(width=600, height=400, bargap=0.3)
fig.update_layout(xaxis={"type": "category"})

# Show the plot
fig.show()
fn = os.path.join(parent_folder, "chaiman_count_annual.svg")
fig.write_image(fn)

# %% PIE Chart
data = pd.read_csv(
    r"F:\KSR\Sorted\CLEANED\Ordinance and Strategic Plans\COUNTS\final_combined_trend.csv"
)
df = pd.DataFrame(data)

# Extract the normalized counts
labels = ["Feminine", "Masculine", "Neutral"]
sizes = [df["feminine_norm"][0], df["masculine_norm"][0], df["neutral_norm"][0]]

# Create a pie chart using Plotly
fig = px.pie(
    values=sizes,
    names=labels,
    title="Normalized Share of Feminine, Masculine, and Neutral",
)
fig.update_layout(width=600, height=400, bargap=0.3)
# Show the plot
fig.show()
fn = os.path.join(parent_folder, "pie_chart.svg")
fig.write_image(fn)

# %%
