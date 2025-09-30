# %%
import os


def combine_all_text_files(root_dir, output_file):
    combined_content = []

    # Walk through the directory and its subdirectories
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".txt"):
                print(file)
                file_path = os.path.join(subdir, file)

                # Read the file content
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    combined_content.append(content)

    # Combine all contents into one string
    final_content = "\n".join(combined_content)

    # Write the combined contents to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"All text files have been combined into '{output_file}'")


# Example usage
root_directory = ""
output_file_path = ""
combine_all_text_files(root_directory, output_file_path)
# %%
