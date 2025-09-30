import os
import pandas as pd
from pathlib import Path
from tqdm.auto import tqdm

# Consolidate your imports
import constants as c
from filefolder import filefolder as ff, filename_year as ffy
from pdf2text import pdf2text as p2t
from textpreprocess import textpreprocess as tp, helper_counter as hc, helper_extract_sentences_to_csv as hx, helper_spellcheck as hs
from gender.genbit import genbit as gb, visualization as vs, combine_genbit_scores as cgs

# Helper functions to make the code more modular
def process_pdfs_to_txt(input_folder, output_folder_txt):
    """Convert PDF files to TXT."""
    p2t.pdf_2_text_folder(input_folder, output_folder_txt)

def extract_sentences_from_txt_to_csv(input_folder, output_folder_csv):
    """Extract sentences from TXT files and save them as CSV."""
    df_files = ff.get_files_info_from_folder(input_folder)
    txt_files = df_files[df_files['Extension'] == '.txt']
    for index, row in tqdm(txt_files.iterrows(), total=txt_files.shape[0], desc="Processing PDFs"):
        file_path = Path(row['Absolute Path'])
        output_filename = f"{row['Base File Name']}.csv"
        output_file = os.path.join(output_folder_csv, output_filename)
        hx.extract_sentences_to_csv(file_path, output_file)

def preprocess_csv_files(input_folder, output_folder_cleaned):
    """Preprocess CSV files and save cleaned versions."""
    df_files = ff.get_files_info_from_folder(input_folder)
    csv_files = df_files[df_files['Extension'] == '.csv']
    os.makedirs(output_folder_cleaned, exist_ok=True)
    for index, row in tqdm(csv_files.iterrows(), total=csv_files.shape[0], desc="Processing txts"):
        file_path = Path(row['Absolute Path'])
        output_filename = row["Base File Name"]
        processor = tp.DataFrameProcessor(file_path)
        # Chain method calls or individual processing steps
        processor.extract_sentences('Sentence', 'output')\
                  .remove_line_breaks('output', 'output')\
                  .remove_special_characters('output', 'output')\
                  .remove_extra_spaces_multiple_periods('output', 'output')\
                  .anonymize_names('output', 'output')\
                  .lowercase_sentences('output', "output")\
                  .remove_non_alphabetic_characters("output", "output")\
                  .remove_extra_spaces_multiple_periods('output', 'output')\
                  .save_non_nan_rows("output", os.path.join(output_folder_cleaned, f"{output_filename}_final_clean.csv"))\
                  .combine_and_export_sentences("output", os.path.join(output_folder_cleaned, f"{output_filename}_final_clean.txt"), join_on=".")

def visualize_genbit_scores(df_gen):
    """Create visualizations for Genbit scores."""
    viz = vs.DataFrameVisualizer(df_gen)
    viz.plot_line('years', 'genbit_score', title="Genbit Score Annual Reports")
