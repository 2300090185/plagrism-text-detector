"""
app.py – Streamlit web application for the Plagiarism Text Detector.

Run with:
    streamlit run app.py
"""

import os

import streamlit as st

from src.detector import detect_plagiarism

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Plagiarism Text Detector",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Plagiarism Text Detector")
st.markdown(
    "Detect similarity between two text documents using **TF-IDF** and "
    "**Cosine Similarity**."
)

# ---------------------------------------------------------------------------
# Helper – load sample files
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _load_sample(filename: str) -> str:
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    return ""


SAMPLE_FILES = [f for f in os.listdir(DATA_DIR) if f.endswith(".txt")] if os.path.isdir(DATA_DIR) else []
SAMPLE_FILES.sort()

# ---------------------------------------------------------------------------
# Input section
# ---------------------------------------------------------------------------
st.subheader("Input Documents")

input_mode = st.radio(
    "Input method",
    ["Type / Paste text", "Upload .txt files", "Use sample files"],
    horizontal=True,
)

col1, col2 = st.columns(2)

text1 = ""
text2 = ""

if input_mode == "Type / Paste text":
    with col1:
        st.markdown("**Document 1**")
        text1 = st.text_area("Document 1", height=250, label_visibility="collapsed")
    with col2:
        st.markdown("**Document 2**")
        text2 = st.text_area("Document 2", height=250, label_visibility="collapsed")

elif input_mode == "Upload .txt files":
    with col1:
        st.markdown("**Document 1**")
        file1 = st.file_uploader("Upload Document 1", type=["txt"], key="f1")
        if file1:
            text1 = file1.read().decode("utf-8", errors="replace")
            st.text_area("Preview", text1, height=200, disabled=True)
    with col2:
        st.markdown("**Document 2**")
        file2 = st.file_uploader("Upload Document 2", type=["txt"], key="f2")
        if file2:
            text2 = file2.read().decode("utf-8", errors="replace")
            st.text_area("Preview", text2, height=200, disabled=True)

else:  # sample files
    if len(SAMPLE_FILES) < 2:
        st.warning("Not enough sample files found in the `data/` directory.")
    else:
        with col1:
            st.markdown("**Document 1**")
            sel1 = st.selectbox("Select sample 1", SAMPLE_FILES, key="s1")
            text1 = _load_sample(sel1)
            st.text_area("Preview", text1, height=200, disabled=True)
        with col2:
            st.markdown("**Document 2**")
            sel2 = st.selectbox("Select sample 2", SAMPLE_FILES, index=1, key="s2")
            text2 = _load_sample(sel2)
            st.text_area("Preview", text2, height=200, disabled=True)

# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------
st.divider()

if st.button("🔎 Check Plagiarism", type="primary", use_container_width=True):
    if not text1.strip() or not text2.strip():
        st.error("Please provide both documents before checking.")
    else:
        with st.spinner("Analysing documents…"):
            result = detect_plagiarism(text1, text2)

        # --- Score gauge ---------------------------------------------------
        st.subheader("Results")

        pct = result.plagiarism_percentage
        if pct >= 75:
            color = "#e74c3c"  # red
        elif pct >= 40:
            color = "#e67e22"  # orange
        elif pct >= 15:
            color = "#f1c40f"  # yellow
        else:
            color = "#2ecc71"  # green

        col_score, col_verdict = st.columns([1, 2])
        with col_score:
            st.metric("Plagiarism Score", f"{pct:.1f}%")
            st.progress(min(pct / 100, 1.0))
        with col_verdict:
            st.markdown(
                f"<div style='padding:16px; border-radius:8px; background:{color}20; "
                f"border-left:6px solid {color}; font-size:1.1rem; font-weight:600;'>"
                f"{result.verdict}</div>",
                unsafe_allow_html=True,
            )

        # --- Matching sentences --------------------------------------------
        if result.matching_sentences:
            st.subheader("Matching / Similar Sentence Pairs")
            for i, (s1, s2) in enumerate(result.matching_sentences, start=1):
                with st.expander(f"Match {i}"):
                    c1, c2 = st.columns(2)
                    c1.markdown(f"**Doc 1:** {s1}")
                    c2.markdown(f"**Doc 2:** {s2}")
        else:
            st.info("No closely matching sentence pairs found.")
