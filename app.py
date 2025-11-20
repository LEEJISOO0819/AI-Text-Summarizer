# app.py
import streamlit as st
from preprocess import clean_text
from summarizer import TextSummarizer  # 클래스 임포트

# Streamlit 페이지 설정
st.set_page_config(page_title="AI Text Summarizer", layout="wide")

st.title("AI Text Summarizer")
st.write("Enter your text below and click **Summarize**.")

# 사용자 입력
user_input = st.text_area("Input Text", height=250)

# TextSummarizer 클래스 인스턴스 생성
summarizer = TextSummarizer()

# 요약 버튼 클릭 시 동작
if st.button("Summarize"):
    cleaned, error = clean_text(user_input, min_length=50)

    if error:
        st.error(f"Preprocessing failed: {error}")
    else:
        summary = summarizer.summarize(cleaned, max_length=120)
        st.subheader("Summary Result")
        st.write(summary)
