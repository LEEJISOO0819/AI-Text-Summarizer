# app.py

import streamlit as st
from preprocess import clean_text
from summarizer import summarize_text  


# Streamlit page configuration
st.set_page_config(
    page_title="AI Text Summarizer",
    layout="wide"
)


# Title & description
st.title("AI Text Summarizer")
st.write(
    """
    Paste your text below and click **Summarize**.
    Make sure your input is at least **50 characters** long.
    """
)


# User input
user_input = st.text_area("Input Text", height=250, placeholder="Enter a long text to summarize...")


# Optional: summary length selection
summary_length = st.selectbox(
    "Select Summary Length",
    ["Short", "Medium", "Long"],
    index=1,
    help="Short: ~60 tokens, Medium: ~100 tokens, Long: ~150 tokens"
)


# Helper: map length option -> max_length
def get_max_length(option: str) -> int:
    if option == "Short":
        return 60
    if option == "Medium":
        return 100
    return 150   # Long



# Main button: Summarize
if st.button("Summarize"):

    # 1) 빈 입력 처리
    if not user_input or user_input.strip() == "":
        st.error("Please enter some text before summarizing.")
    else:
        # 2) 전처리 단계
        with st.spinner("Cleaning text..."):
            cleaned_text, error = clean_text(user_input, min_length=50)

        if error:
            # 전처리에서 에러 발생 (예: 너무 짧은 텍스트 등)
            st.error(f"Preprocessing failed: {error}")
        else:
            # 3) 요약 단계
            max_len = get_max_length(summary_length)

            with st.spinner("Generating summary..."):
                try:
                    summary = summarize_text(cleaned_text, max_length=max_len)
                except Exception as e:
                    st.error(f"Summarization failed: {e}")
                else:
                    # 4) 결과 출력
                    st.subheader("Summary Result")
                    st.write(summary)

                    # 5) 간단한 로그/통계 정보
                    original_len = len(cleaned_text.split())
                    summary_len = len(summary.split()) if summary else 0
                    compression = (
                        f"{(1 - summary_len / original_len) * 100:.1f}%"
                        if original_len > 0 and summary_len > 0
                        else "N/A"
                    )

                    st.markdown("---")
                    st.subheader("Summary Statistics")
                    st.write(f"- Original length: **{original_len}** words")
                    st.write(f"- Summary length: **{summary_len}** words")
                    st.write(f"- Compression: **{compression}**")
