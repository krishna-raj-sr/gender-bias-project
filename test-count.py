"""CODE FOR TESTING"""

import re
import pandas as pd
from collections import Counter


def normalize_text(text):
    return re.sub(r"[^\w\s]", " ", text.lower())


def count_words(text, search_words):
    normalized_text = normalize_text(text)
    words = normalized_text.split()
    word_counter = Counter(words)
    counts = []

    # First count multi-word phrases
    multi_word_counts = {}
    for phrase in search_words:
        if " " in phrase:
            normalized_phrase = " ".join(normalize_text(phrase).split())
            count = normalized_text.count(" " + normalized_phrase + " ")
            multi_word_counts[phrase] = count
            counts.append({"Word": phrase, "Count": count})

    # Adjust counts of individual words based on multi-word phrase counts
    for word in search_words:
        if " " not in word:
            adjusted_count = word_counter[word]
            for phrase, phrase_count in multi_word_counts.items():

                if word in phrase.split():
                    adjusted_count -= phrase_count
            counts.append({"Word": word, "Count": max(adjusted_count, 0)})

    df = pd.DataFrame(counts)
    return df


fn = r"text_test_count_file.txt"
text = read_file_content(fn)
c = count_words(text, search_words)
