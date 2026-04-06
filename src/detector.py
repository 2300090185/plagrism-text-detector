"""
detector.py – High-level plagiarism detection logic.

Combines preprocessing and similarity scoring to produce a
human-readable plagiarism report with highlighted matching sentences.
"""

import difflib
import re
from dataclasses import dataclass, field
from typing import List, Tuple

from src.preprocessing import preprocess
from src.similarity import compute_similarity


@dataclass
class PlagiarismResult:
    """Result of a plagiarism check between two documents."""

    similarity_score: float
    plagiarism_percentage: float
    verdict: str
    matching_sentences: List[Tuple[str, str]] = field(default_factory=list)

    def __str__(self) -> str:
        lines = [
            f"Similarity Score   : {self.similarity_score:.4f}",
            f"Plagiarism         : {self.plagiarism_percentage:.1f}%",
            f"Verdict            : {self.verdict}",
        ]
        if self.matching_sentences:
            lines.append("\nMatching / Similar Sentence Pairs:")
            for i, (s1, s2) in enumerate(self.matching_sentences, start=1):
                lines.append(f"  [{i}] Doc1: {s1.strip()}")
                lines.append(f"       Doc2: {s2.strip()}")
        return "\n".join(lines)


def _split_sentences(text: str) -> List[str]:
    """Split *text* into non-empty sentences on common terminators."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


def _find_matching_sentences(
    text1: str, text2: str, threshold: float = 0.6
) -> List[Tuple[str, str]]:
    """Return pairs of similar sentences across the two documents.

    A pair is included when the SequenceMatcher ratio is >= *threshold*.
    """
    sentences1 = _split_sentences(text1)
    sentences2 = _split_sentences(text2)
    matches: List[Tuple[str, str]] = []

    for s1 in sentences1:
        for s2 in sentences2:
            ratio = difflib.SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
            if ratio >= threshold:
                matches.append((s1, s2))
                break  # only record the best match per sentence in doc1

    return matches


def _verdict(score: float) -> str:
    """Return a human-readable verdict based on the similarity *score*."""
    percentage = score * 100
    if percentage >= 75:
        return "High plagiarism detected"
    if percentage >= 40:
        return "Moderate plagiarism detected"
    if percentage >= 15:
        return "Low plagiarism detected"
    return "No significant plagiarism detected"


def detect_plagiarism(text1: str, text2: str) -> PlagiarismResult:
    """Analyse *text1* and *text2* and return a :class:`PlagiarismResult`.

    Args:
        text1: The first (original) document as a plain-text string.
        text2: The second (suspect) document as a plain-text string.

    Returns:
        A :class:`PlagiarismResult` containing the similarity score,
        plagiarism percentage, verdict, and matching sentence pairs.
    """
    processed1 = preprocess(text1)
    processed2 = preprocess(text2)

    score = compute_similarity(processed1, processed2)
    percentage = round(score * 100, 2)
    verdict = _verdict(score)
    matching = _find_matching_sentences(text1, text2)

    return PlagiarismResult(
        similarity_score=score,
        plagiarism_percentage=percentage,
        verdict=verdict,
        matching_sentences=matching,
    )
