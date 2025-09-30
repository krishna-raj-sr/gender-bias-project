import os
import pandas as pd
from spellchecker import SpellChecker
import re

spell_checker = SpellChecker()

def load_word_counts_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df

def spell_check_word(word):
    corrected_word = spell_checker.correction(word)
    return corrected_word != word, corrected_word

def spell_check_word_freq(df, column_name):
    # Get all misspelled words in the DataFrame column
    df[column_name] = df[column_name].astype(str).apply(lambda x: re.sub(r'\d+\.\d+|\d+', '', x))
    misspelled_words = set(spell_checker.unknown(df[column_name]))
    
    # Use list comprehension to correct misspelled words
    corrected_words = [spell_checker.correction(word) if word in misspelled_words else word for word in df[column_name]]
    
    # Create a new DataFrame with corrected words
    df_corrected = df.copy()
    df_corrected['Corrected Word'] = corrected_words
    df_corrected['Corrected'] = ~df[column_name].isin(misspelled_words)
    
    return df_corrected

def spell_check_word_freq_file(filename, column_name="Word"):
    # Load word frequencies from CSV
    df = load_word_counts_from_csv(filename) 
    # Perform spell checking
    df_checked = spell_check_word_freq(df, column_name)    
    # Append data to list

    return df_checked
