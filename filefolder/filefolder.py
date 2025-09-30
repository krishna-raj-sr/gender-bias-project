import os
import pandas as pd
import chardet

def get_files_info_from_folder(folder_path):
    """
    Get information about files in the specified folder.

    Args:
    - folder_path (str): The path to the folder.

    Returns:
    - pd.DataFrame: DataFrame containing information about files.
        'Absolute Path': absolute_paths,
        'Relative Path': relative_paths,
        'File Name': file_names,
        'Base File Name': base_file_names,
        'Extension': extensions
    """
    # Initialize lists to store file information
    absolute_paths = []
    relative_paths = []
    file_names = []
    base_file_names = []
    extensions = []

    # Iterate over all files and subdirectories in the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Get absolute and relative paths
            absolute_path = os.path.join(root, file)
            relative_path = os.path.relpath(absolute_path, folder_path)

            # Get file name, base file name, and extension
            file_name = os.path.basename(absolute_path)
            base_file_name, extension = os.path.splitext(file_name)

            # Append information to lists
            absolute_paths.append(absolute_path)
            relative_paths.append(relative_path)
            file_names.append(file_name)
            base_file_names.append(base_file_name)
            extensions.append(extension)

    # Create DataFrame from collected information
    df = pd.DataFrame({
        'Absolute Path': absolute_paths,
        'Relative Path': relative_paths,
        'File Name': file_names,
        'Base File Name': base_file_names,
        'Extension': extensions
    })

    return df



def read_text_file_with_detected_encoding(file_path):
    # First, read a portion of the file to detect encoding
    with open(file_path, 'rb') as file:
        raw_data = file.read(50000)  # Adjust the size as needed    
    # Detect the encoding
    result = chardet.detect(raw_data)
    encoding = result['encoding']    
    # Now, read the file with the detected encoding
    with open(file_path, 'r', encoding=encoding) as file:
        text = file.read()    
    return text