import os
import spacy
import pandas as pd
from pathlib import Path
from filefolder import filefolder as ff
def extract_sentences_to_csv(file_path,output_file_path):
    # Function to process text in chunks
    def process_text_in_chunks(text, chunk_size=1000000):
        nlp = spacy.load("en_core_web_sm")
        sentences = []  # List to store sentences from all chunks
        
        for start_idx in range(0, len(text), chunk_size):
            chunk_text = text[start_idx:start_idx + chunk_size]
            doc = nlp(chunk_text)
            sentences.extend([sent.text.strip() for sent in doc.sents])
        
        return sentences

    # Read the large text file
    text = ff.read_text_file_with_detected_encoding(file_path)

    # Process the text in chunks and extract sentences
    sentences = process_text_in_chunks(text)

    # Convert the list of sentences into a pandas DataFrame
    df = pd.DataFrame(sentences, columns=['Sentence'])

    # Determine the CSV file path based on the original file's location and name
    output_file_path = Path(output_file_path)
    output_dir = output_file_path.parent
    print(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Save the DataFrame to the determined CSV file path
    df.to_csv(output_file_path, index=False)

    print(f"Sentences have been successfully saved to '{output_file_path}'.")

