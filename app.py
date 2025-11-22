# app.py

import streamlit as st
from preprocess import clean_text
from summarizer import summarize_text
from visualize import plot_lengths, plot_pie_chart, calculate_compression, create_stats_dict


# Streamlit page configuration
st.set_page_config(
    page_title="AI Text Summarizer",
    layout="wide",
    page_icon="🤖"
)


# Title & description
st.title("🤖 AI Text Summarizer")
st.write(
    """
    Paste your text below and click **Summarize**.
    Make sure your input is at least **50 characters** long.
    Supports both **Korean** 🇰🇷 and **English** 🇺🇸 (auto-detected).
    """
)


# Sidebar: Example texts
st.sidebar.header("📚 Example Texts")
examples = {
    "Custom Input": "",
    "🇰🇷 Korean - Breakup": """오늘 3년 사귄 애인이랑 헤어졌어... 너무 힘들다. 아침에 카톡으로 만나자고 해서 나갔더니 갑자기 헤어지자는 거야. 이유를 물어봤더니 자기가 요즘 너무 힘들어서 연애할 여유가 없다는 거야. 나는 이해가 안 가더라. 우리 사이 좋았잖아. 지난주에도 같이 영화 보고 밥 먹고 그랬는데. 갑자기 왜 이러는 건지 모르겠어.""",
    "🇺🇸 English - AI Tech": """Artificial intelligence is rapidly transforming our world in unprecedented ways. From healthcare to finance, education to entertainment, AI technologies are revolutionizing how we live and work. Machine learning algorithms can now diagnose diseases with remarkable accuracy, often surpassing human doctors. In finance, AI-powered trading systems process vast amounts of data in milliseconds to make investment decisions."""
}

selected_example = st.sidebar.selectbox("Choose an example", list(examples.keys()))


# User input
if selected_example == "Custom Input":
    user_input = st.text_area(
        "Input Text",
        height=250,
        placeholder="Enter a long text to summarize..."
    )
else:
    user_input = st.text_area(
        "Input Text",
        value=examples[selected_example],
        height=250
    )


# Summary length selection
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
    elif option == "Medium":
        return 100
    else:
        return 150


# Main button: Summarize
if st.button("🚀 Summarize", type="primary"):

    # 1) Check for empty input
    if not user_input or user_input.strip() == "":
        st.error("⚠️ Please enter some text before summarizing.")
    else:
        # 2) Preprocessing step
        with st.spinner("🧹 Cleaning text..."):
            cleaned_text, error = clean_text(user_input, min_length=50)

        if error:
            st.error(f"❌ Preprocessing failed: {error}")
        else:
            # 3) Summarization step
            max_len = get_max_length(summary_length)

            with st.spinner("✨ Generating summary... (First run may take 1-2 minutes)"):
                try:
                    summary = summarize_text(cleaned_text, max_length=max_len)
                except Exception as e:
                    st.error(f"❌ Summarization failed: {e}")
                else:
                    # Check if summary is an error message
                    if summary.startswith("❌") or summary.startswith("⚠️"):
                        st.error(summary)
                    else:
                        # 4) Display results
                        st.success("✅ Summary complete!")
                        
                        # Two columns layout
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📄 Original Text")
                            st.text_area(
                                "",
                                value=cleaned_text,
                                height=200,
                                disabled=True,
                                label_visibility="collapsed"
                            )
                            st.caption(f"Characters: {len(cleaned_text)}")
                        
                        with col2:
                            st.subheader("✨ Summary")
                            st.text_area(
                                "",
                                value=summary,
                                height=200,
                                disabled=True,
                                label_visibility="collapsed"
                            )
                            st.caption(f"Characters: {len(summary)}")
                        
                        # 5) Visualization section
                        st.markdown("---")
                        st.subheader("📊 Comparison & Statistics")
                        
                        # Create THREE columns for viz (막대 + 파이 + 통계)
                        viz_col1, viz_col2, viz_col3 = st.columns([1, 1, 1])
                        
                        with viz_col1:
                            # Display bar chart
                            st.write("**Length Comparison**")
                            img_buffer = plot_lengths(cleaned_text, summary)
                            st.image(img_buffer, use_container_width=True)
                        
                        with viz_col2:
                            # Display pie chart (새로 추가!)
                            st.write("**Content Distribution**")
                            pie_buffer = plot_pie_chart(cleaned_text, summary)
                            st.image(pie_buffer, use_container_width=True)
                        
                        with viz_col3:
                            # Display statistics
                            st.write("**Statistics**")
                            
                            # 통계 계산
                            stats = create_stats_dict(cleaned_text, summary)
                            
                            # 메트릭 표시
                            st.metric("Original", f"{stats['original_chars']:,} chars")
                            st.caption(f"{stats['original_words']:,} words")
                            
                            st.metric("Summary", f"{stats['summary_chars']:,} chars")
                            st.caption(f"{stats['summary_words']:,} words")
                            
                            st.metric("Compression", f"{stats['compression_rate']}%")
                            st.caption(f"Kept: {stats['reduction_rate']}%")
                        
                        # Additional detailed info (접을 수 있는 섹션)
                        with st.expander("📈 Detailed Statistics"):
                            detail_col1, detail_col2 = st.columns(2)
                            
                            with detail_col1:
                                st.write("**Original Text:**")
                                st.write(f"- Characters: {stats['original_chars']:,}")
                                st.write(f"- Words: {stats['original_words']:,}")
                                st.write(f"- Sentences: {stats['original_sentences']}")
                            
                            with detail_col2:
                                st.write("**Summary Text:**")
                                st.write(f"- Characters: {stats['summary_chars']:,}")
                                st.write(f"- Words: {stats['summary_words']:,}")
                                st.write(f"- Sentences: {stats['summary_sentences']}")
                            
                            st.markdown("---")
                            st.info(f"💡 The summary is **{stats['reduction_rate']}%** of the original length")


# Footer info
with st.expander("ℹ️ About this app"):
    st.markdown("""
    ### Features:
    - 🇰🇷 **Korean** summarization using KoBART
    - 🇺🇸 **English** summarization using BART-CNN
    - 🔄 Automatic language detection
    - 📊 Visual comparison with bar chart and pie chart
    - 📈 Detailed statistics
    
    ### How it works:
    1. Enter or paste your text (minimum 50 characters)
    2. Choose summary length (Short/Medium/Long)
    3. Click Summarize button
    4. View results with visual comparisons
    
    ### Visualizations:
    - **Bar Chart**: Compares character length
    - **Pie Chart**: Shows content kept vs removed
    - **Statistics**: Detailed metrics and compression rate
    
    ### Models used:
    - Korean: [gogamza/kobart-summarization](https://huggingface.co/gogamza/kobart-summarization)
    - English: [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn)
    
    ### Credits:
    Created by Jisoo Lee, Jisoo Kang, Hyunsoo Kim, Jiwoo Yang, Hosung Yoon
    """)