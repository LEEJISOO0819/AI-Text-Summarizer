# app.py
import streamlit as st
from preprocess import clean_text
from summarizer import TextSummarizer

st.title("🤖 AI 장문 요약기 - 데모")

input_text = st.text_area("텍스트를 입력하세요", height=200)
length = st.selectbox("요약 길이", ["짧게", "중간", "길게"])

if st.button("요약하기"):
    cleaned, err = clean_text(input_text)
    if err:
        st.error(err)
    else:
        summ = TextSummarizer()
        max_len = 60 if length=="짧게" else 100 if length=="중간" else 150
        summary = summ.summarize(cleaned, max_length=max_len)
        st.subheader("요약 결과")
        st.write(summary)

##### 한글 모두 영어로 수정할 것!!!!!