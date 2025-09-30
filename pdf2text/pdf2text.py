import os
from filefolder import filefolder as f
from pdf2text import helper as h


def pdf_2_text_folder(input_folder, output_folder):
    """
    Convert PDF files in the input folder to text files and save them in the output folder.

    Args:
    - input_folder (str): Path to the folder containing PDF files.
    - output_folder (str): Path to the folder where text files will be saved.

    Returns:
    - None

    This function iterates over PDF files in the input folder, converts each PDF file to text using the
    `convert_pdf2text` function from the `pdf2text` module, and saves the resulting text files in the
    output folder. If the output folder doesn't exist, it will be created.
    """
    # Ensure the output folder exists; create if it doesn't
    os.makedirs(output_folder, exist_ok=True)

    # Get information about PDF files in the input folder
    pdf_files_info = f.get_files_info_from_folder(input_folder)

    # Filter out non-PDF files
    pdf_files_info = pdf_files_info[pdf_files_info["Extension"] == ".pdf"]

    # Process each PDF file
    for index, row in pdf_files_info.iterrows():
        input_pdf_file_location = row["Absolute Path"]
        base_file_name = row["Base File Name"] + ".txt"
        output_file_path = os.path.join(output_folder, base_file_name)
        print(f"writing: {output_file_path}")
        # Convert PDF to text and save
        h.convert_pdf2text(input_pdf_file_location, output_file_path)
