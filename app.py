import streamlit as st
import matplotlib.pyplot as plt
import pdfplumber, io
from docx import Document
from collections import Counter

# -------------------------------
# Text Extraction Function
# -------------------------------
def extract_text(file):
    data = file.read()
    if file.name.endswith(".pdf"):
        return ' '.join([p.extract_text() for p in pdfplumber.open(io.BytesIO(data)).pages if p.extract_text()])
    return ' '.join([p.text for p in Document(io.BytesIO(data)).paragraphs if p.text.strip()])

st.set_page_config(layout="centered")
st.title("📄 Text Frequency Visualizer")

uploaded = st.file_uploader("Upload PDF or Word Document", type=["pdf", "docx"])
top_n = st.slider("Top N Words", min_value=5, max_value=20, value=10)

if uploaded:
    text = extract_text(uploaded).lower()
    clean_text = ''.join(ch if ch.isalpha() or ch.isspace() else ' ' for ch in text)
    counts = Counter(clean_text.split())
    words_freq = counts.most_common(top_n)
    words, freq = zip(*words_freq)

    st.subheader("Horizontal Bar Chart")
    fig1, ax1 = plt.subplots()
    ax1.barh(words[::-1], freq[::-1], color="skyblue")
    ax1.set_xlabel("Frequency")
    ax1.set_title("Top Words")
    st.pyplot(fig1)

    st.subheader("Line Chart")
    fig2, ax2 = plt.subplots()
    ax2.plot(words, freq, marker='o', linestyle='-', color='green')
    ax2.set_xticks(range(len(words)))
    ax2.set_xticklabels(words, rotation=45)
    ax2.set_ylabel("Frequency")
    ax2.set_title("Word Frequency Trend")
    st.pyplot(fig2)
