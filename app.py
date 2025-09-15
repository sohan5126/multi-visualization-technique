import streamlit as st
import matplotlib.pyplot as plt
import pdfplumber, io
from docx import Document
from wordcloud import WordCloud
from collections import Counter

def extract_text(file):
    data = file.read()
    if file.name.endswith(".pdf"):
        return ' '.join([p.extract_text() for p in pdfplumber.open(io.BytesIO(data)).pages if p.extract_text()])
    return ' '.join([p.text for p in Document(io.BytesIO(data)).paragraphs if p.text.strip()])

st.set_page_config(layout="centered")
st.title("📄 Multi-Visualization App")

uploaded = st.file_uploader("Upload PDF/Word", type=["pdf", "docx"])
top_n = st.slider("Top N Words", 5, 20, 10)

if uploaded:
    text = extract_text(uploaded).lower()
    clean_text = ''.join(ch if ch.isalpha() or ch.isspace() else ' ' for ch in text)
    counts = Counter(clean_text.split())
    words, freq = zip(*counts.most_common(top_n))

    # 1️⃣ Word Cloud
    st.subheader("Word Cloud")
    fig, ax = plt.subplots()
    ax.imshow(WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(counts))
    ax.axis("off")
    st.pyplot(fig)

    # 2️⃣ Bar Chart
    st.subheader("Bar Chart")
    fig2, ax2 = plt.subplots()
    ax2.bar(words, freq)
    ax2.set_xticklabels(words, rotation=45)
    st.pyplot(fig2)

    # 3️⃣ Pie Chart
    st.subheader("Pie Chart")
    fig3, ax3 = plt.subplots()
    ax3.pie(freq, labels=words, autopct="%1.1f%%", startangle=90)
    ax3.axis("equal")
    st.pyplot(fig3)
