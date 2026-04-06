"""
similarity.py – Similarity computation utilities.

Converts preprocessed text into TF-IDF vectors and calculates
cosine similarity to produce a plagiarism score.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(text1: str, text2: str) -> float:
    """Return the cosine similarity score between *text1* and *text2*.

    The score is a float in the range [0.0, 1.0] where 1.0 means
    identical content and 0.0 means completely different content.
    """
    if not text1.strip() or not text2.strip():
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(score)
