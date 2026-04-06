# Plagiarism Text Detector

A Python-based tool that identifies similarity between text documents using **Natural Language Processing** and **Cosine Similarity**. It preprocesses text, converts it to TF-IDF vectors, and generates a plagiarism score to detect duplicate or copied content efficiently.

---

## Features

- Detects similarity between two text inputs
- Generates a **plagiarism percentage score**
- Text preprocessing: lowercasing, stopword removal, tokenization
- TF-IDF vectorisation + cosine similarity
- Highlights **matching sentence pairs**
- Interactive **Streamlit** web UI
- Supports pasting text or uploading `.txt` files

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.8+ |
| Vectorisation | scikit-learn (TfidfVectorizer) |
| NLP preprocessing | NLTK |
| Sequence matching | difflib |
| Web UI | Streamlit |

---

## Project Structure

```
plagiarism-text-detector/
├── data/               # Sample input files
│   ├── sample1.txt
│   ├── sample2.txt
│   └── sample3.txt
├── src/
│   ├── __init__.py
│   ├── preprocessing.py   # Text cleaning & tokenisation
│   ├── similarity.py      # TF-IDF + cosine similarity
│   └── detector.py        # High-level detection logic
├── app.py              # Streamlit application
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/plagiarism-text-detector.git
cd plagiarism-text-detector

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
```

---

## Usage

### Web UI (Streamlit)

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser. You can:

- **Type / paste** text directly into the two input areas.
- **Upload** `.txt` files for each document.
- **Use the built-in sample files** for a quick demonstration.

### Python API

```python
from src.detector import detect_plagiarism

result = detect_plagiarism(text1, text2)
print(result.plagiarism_percentage)   # e.g. 61.1
print(result.verdict)                 # e.g. "Moderate plagiarism detected"
print(result.matching_sentences)      # list of (sentence_doc1, sentence_doc2) tuples
```

---

## Example Output

```
Similarity Score   : 0.6106
Plagiarism         : 61.1%
Verdict            : Moderate plagiarism detected

Matching / Similar Sentence Pairs:
  [1] Doc1: Artificial intelligence is the simulation of human intelligence...
       Doc2: Artificial intelligence refers to the simulation of human intelligence...
```

### Verdict thresholds

| Score | Verdict |
|---|---|
| ≥ 75 % | High plagiarism detected |
| 40 – 74 % | Moderate plagiarism detected |
| 15 – 39 % | Low plagiarism detected |
| < 15 % | No significant plagiarism detected |

---

## Future Enhancements

- Integration with web-based plagiarism APIs
- Multi-document comparison
- Report generation in PDF or Excel
- AI-based semantic similarity detection

---

## License

This project is licensed under the [MIT License](LICENSE).
