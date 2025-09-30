import os
import re
import pandas as pd
from collections import Counter

def process_file(file_path):
    word_freq = Counter()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = re.findall(r'\b\w+\b', line.lower())
            word_freq.update(words)
    return word_freq

def count_word_frequency_in_folder(folder_path, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    overall_freq = Counter()
    
    # Process each file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):  # Check if the file is a text file
            file_path = os.path.join(folder_path, file_name)
            # Process file
            word_freq = process_file(file_path)
            
            # Sort word frequency by count (highest to lowest)
            word_freq_sorted = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            
            # Write word frequency to CSV for each file
            df_file = pd.DataFrame(word_freq_sorted, columns=['Word', 'Frequency'])
            file_csv_path = os.path.join(output_folder, f'{os.path.splitext(file_name)[0]}_word_frequency.csv')
            df_file.to_csv(file_csv_path, index=False)
            
            # Update overall frequency
            overall_freq.update(word_freq)

    # Sort overall frequency by count (highest to lowest)
    overall_freq_sorted = sorted(overall_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Create DataFrame for overall word frequency
    df_overall = pd.DataFrame(overall_freq_sorted, columns=['Word', 'Frequency'])
    
    # Write overall word frequency to CSV
    overall_csv_path = os.path.join(output_folder, 'overall_word_frequency.csv')
    df_overall.to_csv(overall_csv_path, index=False)



# %%
