import pandas as pd
import json
from pathlib import Path
import constants as c
# Specify the keys you're interested in constants file

def load_metrics_from_json_folder(folder_path,output_file_path,allowed_keys=c.NEEDED_KEYS):
    
    def flatten_and_filter_dict(d, parent_key='', sep='_'):
        items = []
        if isinstance(d, dict):
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict) or isinstance(v, list):
                    items.extend(flatten_and_filter_dict(v, new_key, sep=sep).items())
                else:
                    if new_key in allowed_keys:
                        items.append((new_key, v))
        elif isinstance(d, list):
            for index, item in enumerate(d):
                items.extend(flatten_and_filter_dict(item, f'{parent_key}{sep}{index}', sep=sep).items())
        return dict(items)

    all_metrics = []
    
    for file_path in Path(folder_path).glob('*.json'):
        data = json.load(open(file_path))
        flat_data = flatten_and_filter_dict(data)
        all_metrics.append(flat_data)

    df = pd.DataFrame(all_metrics)
    df.to_csv(output_file_path)




def load_metrics_from_json_filepaths(file_path,output_file_path,allowed_keys=c.NEEDED_KEYS):
    
    def flatten_and_filter_dict(d, parent_key='', sep='_'):
        items = []
        if isinstance(d, dict):
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict) or isinstance(v, list):
                    items.extend(flatten_and_filter_dict(v, new_key, sep=sep).items())
                else:
                    if new_key in allowed_keys:
                        items.append((new_key, v))
        elif isinstance(d, list):
            for index, item in enumerate(d):
                items.extend(flatten_and_filter_dict(item, f'{parent_key}{sep}{index}', sep=sep).items())
        return dict(items)

    all_metrics = []
    
    for file_path in file_path:
        data = json.load(open(file_path))
        flat_data = flatten_and_filter_dict(data)
        all_metrics.append(flat_data)

    df = pd.DataFrame(all_metrics)
    df.to_csv(output_file_path)

















import json
import pandas as pd
from pathlib import Path

def extract_token_metrics_from_json_folder(folder_path, output_folder_path):
    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    all_token_metrics = []

    folder_path = Path(folder_path)
    output_folder_path = Path(output_folder_path)
    output_folder_path.mkdir(parents=True, exist_ok=True)
    
    for file_path in folder_path.glob('*.json'):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            token_metrics = data.get("token_based_metrics", {})
            flat_token_metrics = flatten_dict(token_metrics)
            all_token_metrics.append(flat_token_metrics)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    df = pd.DataFrame(all_token_metrics)
    output_file_path = output_folder_path / 'token_metrics.csv'
    df.to_csv(output_file_path, index=False)

#%% Usage example
def extract_token_metrics_from_json_folder(folder_path, output_folder_path):
    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    folder_path = Path(folder_path)
    output_folder_path = Path(output_folder_path)
    output_folder_path.mkdir(parents=True, exist_ok=True)

    for file_path in folder_path.glob('*.json'):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            token_metrics = data.get("token_based_metrics", {})
            
            rows = []
            for metric, values in token_metrics.items():
                flat_values = flatten_dict(values)
                flat_values["token_based_metric"] = metric
                rows.append(flat_values)
            
            df = pd.DataFrame(rows)
            output_file_name = file_path.stem + '_token_metrics.csv'
            output_file_path = output_folder_path / output_file_name
            df.to_csv(output_file_path, index=False)
        
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

# Usage example
import pandas as pd
from pathlib import Path

def combine_csv_files(input_folder_path, output_file_path):
    input_folder_path = Path(input_folder_path)
    combined_data = []

    # Step 1: Read each CSV file in the folder
    for file_path in input_folder_path.glob('*.csv'):
        try:
            df = pd.read_csv(file_path)
            df['filename'] = file_path.name  # Add the filename as a column
            combined_data.append(df)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # Step 2: Combine all DataFrames into one
    if combined_data:
        combined_df = pd.concat(combined_data, ignore_index=True)
        combined_df.to_csv(output_file_path, index=False)
        print(f"Combined CSV file saved to {output_file_path}")
    else:
        print("No CSV files found in the specified folder.")

# Usage example
# combine_csv_files('path/to/csv/folder', 'path/to/output/combined_file.csv')
