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
    Paste your **English text** below and click **Summarize**.
    Make sure your input is at least **50 characters** long.
    """
)


# Sidebar: Example texts
st.sidebar.header("📚 Example Texts")
examples = {
    "Custom Input": "",
    "🔬 AI Technology": """Artificial intelligence is rapidly transforming our world in unprecedented ways. From healthcare to finance, education to entertainment, AI technologies are revolutionizing how we live and work. Machine learning algorithms can now diagnose diseases with remarkable accuracy, often surpassing human doctors. In finance, AI-powered trading systems process vast amounts of data in milliseconds to make investment decisions.""",
    "🌍 Climate Change": """Climate change represents one of the most pressing challenges facing humanity today. Rising global temperatures are causing ice caps to melt, sea levels to rise, and weather patterns to become increasingly unpredictable. Extreme weather events such as hurricanes, droughts, and wildfires are becoming more frequent and severe. Scientists warn that without immediate action to reduce greenhouse gas emissions, we risk triggering irreversible tipping points in Earth's climate system.""",
    "💼 Remote Work": """The COVID-19 pandemic has fundamentally transformed how we work, accelerating the shift toward remote and hybrid work arrangements. Many companies have discovered that employees can be just as productive, if not more so, when working from home. This has led to a reevaluation of traditional office spaces and work culture. However, remote work also presents challenges, including maintaining team cohesion, preventing burnout, and ensuring equitable access to opportunities."""
}

selected_example = st.sidebar.selectbox("Choose an example", list(examples.keys()))


# User input
if selected_example == "Custom Input":
    user_input = st.text_area(
        "Input Text (English)",
        height=250,
        placeholder="Enter a long English text to summarize..."
    )
else:
    user_input = st.text_area(
        "Input Text (English)",
        value=examples[selected_example],
        height=250
    )


# Summary length selection
summary_length = st.selectbox(
    "Select Summary Length",
    ["Short", "Medium", "Long"],
    index=1,
    help="Short: ~100 characters, Medium: ~150-200 characters, Long: ~300-400 characters"
)


# Helper: map length option -> target character count
def get_target_chars(option: str) -> int:
    """
    Returns target character count for each summary length option.
    """
    if option == "Short":
        return 80
    elif option == "Medium":
        return 150
    else:  # Long
        return 350


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
            target_chars = get_target_chars(summary_length)

            with st.spinner("✨ Generating summary... (First run may take 1-2 minutes)"):
                try:
                    summary = summarize_text(cleaned_text, target_chars=target_chars)
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
                        
                        # Create THREE columns for viz
                        viz_col1, viz_col2, viz_col3 = st.columns([1, 1, 1])
                        
                        with viz_col1:
                            st.write("**Length Comparison**")
                            img_buffer = plot_lengths(cleaned_text, summary)
                            st.image(img_buffer, use_container_width=True)
                        
                        with viz_col2:
                            st.write("**Content Distribution**")
                            pie_buffer = plot_pie_chart(cleaned_text, summary)
                            st.image(pie_buffer, use_container_width=True)
                        
                        with viz_col3:
                            st.write("**Statistics**")
                            
                            # Calculate statistics
                            stats = create_stats_dict(cleaned_text, summary)
                            
                            # Display metrics
                            st.metric("Original", f"{stats['original_chars']:,} chars")
                            st.caption(f"{stats['original_words']:,} words")
                            
                            st.metric("Summary", f"{stats['summary_chars']:,} chars")
                            st.caption(f"{stats['summary_words']:,} words")
                            
                            st.metric("Compression", f"{stats['compression_rate']}%")
                            st.caption(f"Kept: {stats['reduction_rate']}%")
                        
                        # Additional detailed info
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
    - 🇺🇸 **English** text summarization using BART-CNN
    - 🎯 **Flexible summary lengths**: Short / Medium / Long
    - 📊 **Visual analytics**: Bar charts, pie charts, and detailed statistics
    - 🖥️ **User-friendly interface**: Built with Streamlit
    
    ### How it works:
    1. Enter or paste your English text (minimum 50 characters)
    2. Choose summary length (Short/Medium/Long)
    3. Click Summarize button
    4. View results with visual comparisons
    
    ### Visualizations:
    - **Bar Chart**: Compares character length between original and summary
    - **Pie Chart**: Shows content distribution (kept vs removed)
    - **Statistics Panel**: Detailed metrics including compression rate
    
    ### Model used:
    - [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn)
    - Fine-tuned on CNN/DailyMail dataset
    - Optimized for news article and general text summarization
    
    ### Credits:
    Created by Jisoo Lee, Jisoo Kang, Hyunsoo Kim, Jiwoo Yang, Hosung Yoon
    """)
