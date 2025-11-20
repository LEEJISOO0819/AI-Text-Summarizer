# app.py
import streamlit as st
from preprocess import clean_text
from summarizer import TextSummarizer

# Page config
st.set_page_config(page_title="AI Text Summarizer", layout="wide")

st.title("AI Text Summarizer")
st.write("Enter your text below and click **Summarize**. Minimum 50 characters.")

# Input area
user_input = st.text_area("Input Text", height=250)

# Length selection
length = st.selectbox("Select Summary Length", ["Short", "Medium", "Long"])

# Summarize button
if st.button("Summarize"):
    cleaned, error = clean_text(user_input, min_length=50)
    if error:
        st.error(f"Preprocessing failed: {error}")
    else:
        summarizer = TextSummarizer()
        max_len = 60 if length=="Short" else 100 if length=="Medium" else 150
        summary = summarizer.summarize(cleaned, max_length=max_len)
        st.subheader("Summary Result")
        st.write(summary)
