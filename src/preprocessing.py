"""
preprocessing.py – Text preprocessing utilities.

Performs lowercasing, punctuation removal, stopword filtering,
and tokenization to prepare text for similarity analysis.
"""

import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data on first import
for _resource in ("punkt", "punkt_tab", "stopwords"):
    try:
        nltk.data.find(f"tokenizers/{_resource}" if "punkt" in _resource else f"corpora/{_resource}")
    except LookupError:
        nltk.download(_resource, quiet=True)


def preprocess(text: str) -> str:
    """Return a cleaned, normalised version of *text*.

    Steps applied:
    1. Convert to lowercase.
    2. Remove punctuation and digits.
    3. Tokenize into words.
    4. Remove English stopwords.
    5. Rejoin tokens into a single string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")

    # Lowercase
    text = text.lower()

    # Remove punctuation and digits
    text = re.sub(r"[" + re.escape(string.punctuation) + r"\d]", " ", text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and short tokens
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]

    return " ".join(tokens)
