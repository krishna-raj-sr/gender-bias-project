import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import pandas as pd
import spacy
from spacy.matcher import Matcher
import re
from tqdm.auto import tqdm
import inflect
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import constants as c

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")


class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

    def preprocess_text(
        self,
        text,
        lowercase=True,
        remove_stopwords=True,
        remove_punctuation=True,
        lemmatize=True,
    ):
        # Tokenize text
        tokens = word_tokenize(text)

        # Apply lowercase operation if specified
        if lowercase:
            tokens = [token.lower() for token in tokens]

        # Remove stopwords if specified
        if remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]

        # Remove punctuation if specified
        if remove_punctuation:
            tokens = [token for token in tokens if token not in string.punctuation]

        # Lemmatize tokens if specified
        if lemmatize:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        return tokens


contraction_mapping = c.CONTRACTION_MAPPING


class DataFrameProcessor:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        print("Column headers:", self.df.columns)
        self.df = self.df.astype(str)
        # Load the spaCy model (assuming English here, you could parameterize this)
        self.nlp = spacy.load("en_core_web_sm")
        self.q = inflect.engine()
        self.stop_words = set(stopwords.words("english"))
        tqdm.pandas()

    def remove_line_breaks(self, column_name, new_column_name):
        # Apply the function to remove line breaks on the specified column
        # and store the result in a new column
        self.df[new_column_name] = self.df[column_name].str.replace(
            r"\r|\n", " ", regex=True
        )

    def remove_special_characters(
        self, column_name, new_column_name, keep_periods_commas_ques_appos=True
    ):
        if keep_periods_commas_ques_appos:
            pattern = r"[^a-zA-Z0-9.,'?\s]+"
        else:
            pattern = r"[^a-zA-Z0-9\s]+"
        # Apply the regex to remove special characters on the specified column
        # and store the result in a new column
        self.df[new_column_name] = self.df[column_name].str.replace(
            pattern, " ", regex=True
        )

    def remove_extra_spaces_multiple_periods(self, column_name, new_column_name):
        self.df[new_column_name] = self.df[column_name].apply(self._refine_text)

    def extract_sentences(self, column_name, new_column_name):
        self.df[new_column_name] = (
            self.df[column_name].astype(str).apply(self._extract_sentences_from_text)
        )

    def lowercase_sentences(self, column_name, new_column_name):
        self.df[new_column_name] = self.df[column_name].str.lower()

    def remove_non_alphabetic_characters(self, column_name, new_column_name):
        self.df[new_column_name] = self.df[column_name].apply(
            lambda x: re.sub(r"[^a-zA-Z\s]", "", x)
        )

    def anonymize_names(self, column_name, new_column_name):
        def replace_names(text):
            doc = self.nlp(text)
            anonymized_text = text
            for ent in reversed(doc.ents):  # Reverse to not mess up the offsets
                if ent.label_ in ["PERSON"]:  # You can add more entity types if needed
                    anonymized_text = (
                        anonymized_text[: ent.start_char]
                        + "naam"
                        + anonymized_text[ent.end_char :]
                    )
            return anonymized_text

        self.df[new_column_name] = self.df[column_name].apply(replace_names)

    def save_csv(self, file_path):
        self.df.to_csv(file_path, index=False)

    def save_non_nan_rows(self, column_name, csv_file_path):
        # Filter out NaN rows for the specified column
        tempdf = self.df[[column_name]]
        non_nan_or_empty_df = tempdf[
            tempdf[column_name].notna() & (tempdf[column_name] != "")
        ]
        # Save the non-NaN rows to a CSV file
        non_nan_or_empty_df.to_csv(csv_file_path, index=False)
        print(f"Non-NaN rows of column '{column_name}' saved to '{csv_file_path}'.")

    def convert_num_column(self, column_name, new_column_name):
        """Converts all numeric words in the specified column to their text representation and stores the result in a new column."""
        self.df[new_column_name] = self.df[column_name].apply(self.convert_num)

    def convert_num(self, text):
        """Converts numbers in a text to words."""
        # Split strings into list of texts
        temp_string = text.split()
        new_str = []

        for word in temp_string:
            if word.isdigit():
                temp = self.q.number_to_words(word)
                new_str.append(temp)
            else:
                new_str.append(word)

        return " ".join(new_str)

    def remove_stop_words(self, column_name, new_column_name):
        """Removes stop words from the specified column and stores the result in a new column."""
        self.df[new_column_name] = self.df[column_name].apply(
            self._remove_stop_words_from_text
        )

    def _remove_stop_words_from_text(self, text):
        """Helper function to remove stop words from a text string."""
        word_tokens = word_tokenize(text)
        filtered_sentence = [
            word for word in word_tokens if not word.lower() in self.stop_words
        ]
        return " ".join(filtered_sentence)

    def expand_contractions(self, column_name, new_column_name):
        """Expands contractions in the specified column based on a given mapping."""
        self.df[new_column_name] = self.df[column_name].apply(
            self._expand_text_contractions
        )

    def _expand_text_contractions(self, text):
        """Helper function to replace contractions in a text string."""

        def replace(match):
            return contraction_mapping.get(match.group(0), match.group(0))

        # Create a regular expression from the contraction mapping
        # The patterns will match any key in the mapping
        patterns = re.compile("({})".format("|".join(contraction_mapping.keys())))

        expanded_text = patterns.sub(replace, text)
        return expanded_text

    def combine_and_export_sentences(self, column_name, text_file_path, join_on=" "):
        # Filter to exclude NaN values and empty strings
        tempdf = self.df[[column_name]]
        non_nan_or_empty_df = tempdf[
            tempdf[column_name].notna() & (tempdf[column_name] != "")
        ]

        # Ensure sentences are properly spaced when joined by a period
        if join_on == ".":
            join_on = ". "

            combined_text = join_on.join(non_nan_or_empty_df[column_name].astype(str))
        else:
            combined_text = join_on.join(non_nan_or_empty_df[column_name].astype(str))

        # Save the combined text to a text file
        with open(text_file_path, "w", encoding="utf-8") as file:
            file.write(combined_text)
        print(
            f"Combined sentences of column '{column_name}' exported to '{text_file_path}'."
        )

    def _extract_sentences_from_text(self, text):
        doc = self.nlp(text)
        sentences = []
        for sent in doc.sents:
            pos_tags = [token.pos_ for token in sent]
            if "VERB" in pos_tags and ("NOUN" in pos_tags or "PROPN" in pos_tags):
                sentences.append(sent.text.strip())
        return " ".join(sentences)  # Return sentences as a single string

    def _refine_text(self, text):
        # Replace multiple spaces with a single space
        text = re.sub(r"\s+", " ", text)
        # Remove space on the left of a period
        text = re.sub(r"\s+\.", ".", text)
        # Replace multiple periods with a single period
        text = re.sub(r"\.{2,}", ".", text)
        return text.strip()

    # Additional functions can be added here
