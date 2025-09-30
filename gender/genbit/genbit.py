#%% IMPORTS
import os
from pathlib import Path
from tqdm.auto import tqdm
from genbit.genbit_metrics import GenBitMetrics
import json

from filefolder import filefolder as ff 
import constants as c


def genbit_run(filepath):
    genbit_metrics_object = GenBitMetrics(c.LANGUAGE_CODE, context_window=c.CONTEXT_WINDOW, distance_weight=c.DISTANCE_WEIGHT, percentile_cutoff=c.PERCENTILE_CUTOFF)
    file_contents = ff.read_text_file_with_detected_encoding(filepath)
    genbit_metrics_object.add_data(file_contents, tokenized=False)
    metrics_all = genbit_metrics_object.get_metrics(output_statistics=True, output_word_list=True)
    return metrics_all

def aggregate_genbit_metrics(folder_path,output_folder):
    file_metrics_list = []
    df_files = ff.get_files_info_from_folder(folder_path)
    csv_files = df_files[df_files['Extension'] == '.txt']
    for index, row in tqdm(csv_files.iterrows(), total=csv_files.shape[0], desc="Processing txts"):
        file_path = Path(row['Absolute Path'])
        output_filename  = row["Base File Name"]   
        metrics = genbit_run(file_path)
        metrics['file_path'] = str(file_path)
        output_json_path = f"{output_filename}.json"
        output_json_path = os.path.join(output_folder,output_json_path)
        with open(output_json_path, 'w') as json_file:
            json.dump(metrics, json_file, indent=4)
        file_metrics_list.append(metrics)
    # After processing all files, save the list of metrics to a JSON file
    output_json_path = 'all_file_metrics.json'
    output_json_path = os.path.join(output_folder,output_json_path)
    with open(output_json_path, 'w') as json_file:
        json.dump(file_metrics_list, json_file, indent=4)

    print(f"All metrics saved to {output_json_path}")