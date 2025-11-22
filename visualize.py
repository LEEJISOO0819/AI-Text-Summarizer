# visualize.py
"""
Text summarization visualization module.
Provides functions for creating charts and calculating statistics
to compare original text with summarized text.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Streamlit 호환 모드 (GUI 없이 이미지 생성)
import io


def plot_lengths(original_text: str, summary_text: str):
    """
    Create a bar chart comparing original and summary text lengths.
    
    Args:
        original_text (str): Original text
        summary_text (str): Summarized text
        
    Returns:
        io.BytesIO: Image buffer that can be displayed in Streamlit
    """
    # Count characters
    original_len = len(original_text)
    summary_len = len(summary_text)

    # Create figure with better styling
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Create bar chart with custom colors
    bars = ax.bar(
        ["Original", "Summary"],
        [original_len, summary_len],
        color=['#FF6B6B', '#4ECDC4'],  # Red and Teal
        edgecolor='black',
        linewidth=1.5,
        alpha=0.8
    )
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{int(height):,}',  # Format with comma separator
            ha='center',
            va='bottom',
            fontsize=12,
            fontweight='bold'
        )
    
    # Styling
    ax.set_ylabel("Length (characters)", fontsize=11, fontweight='bold')
    ax.set_title("Text Length Comparison", fontsize=13, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)  # Grid behind bars
    
    # Tight layout to prevent label cutoff
    plt.tight_layout()
    
    # Convert plot to image buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)  # Free memory

    return buf


def plot_word_comparison(original_text: str, summary_text: str):
    """
    Create side-by-side comparison of character and word counts.
    
    Args:
        original_text (str): Original text
        summary_text (str): Summarized text
        
    Returns:
        io.BytesIO: Image buffer for Streamlit display
    """
    # Calculate metrics
    original_chars = len(original_text)
    summary_chars = len(summary_text)
    original_words = len(original_text.split())
    summary_words = len(summary_text.split())
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # === Left plot: Characters comparison ===
    bars1 = ax1.bar(
        ["Original", "Summary"],
        [original_chars, summary_chars],
        color=['#FF6B6B', '#4ECDC4'],
        edgecolor='black',
        linewidth=1.5,
        alpha=0.8
    )
    ax1.set_ylabel("Count", fontsize=10, fontweight='bold')
    ax1.set_title("Characters", fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    
    # Add labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{int(height):,}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    # === Right plot: Words comparison ===
    bars2 = ax2.bar(
        ["Original", "Summary"],
        [original_words, summary_words],
        color=['#FF6B6B', '#4ECDC4'],
        edgecolor='black',
        linewidth=1.5,
        alpha=0.8
    )
    ax2.set_ylabel("Count", fontsize=10, fontweight='bold')
    ax2.set_title("Words", fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)
    
    # Add labels on bars
    for bar in bars2:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{int(height):,}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    plt.tight_layout()
    
    # Convert to image buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf


def plot_pie_chart(original_text: str, summary_text: str):
    """
    Create a pie chart showing the proportion of text kept vs removed.
    
    Args:
        original_text (str): Original text
        summary_text (str): Summarized text
        
    Returns:
        io.BytesIO: Image buffer for Streamlit display
    """
    summary_len = len(summary_text)
    removed_len = len(original_text) - summary_len
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(5, 5))
    
    sizes = [summary_len, removed_len]
    colors = ['#4ECDC4', '#FFE66D']  # Teal and Yellow
    labels = ['Summary\n(Kept)', 'Removed']
    
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'},
        explode=(0.05, 0)  # Slightly separate the summary slice
    )
    
    # Make percentage text white for better visibility
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
    
    ax.set_title("Content Distribution", fontsize=14, fontweight='bold', pad=15)
    
    plt.tight_layout()
    
    # Convert to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf


def calculate_compression(original_text: str, summary_text: str):
    """
    Calculate compression rate (percentage of text removed).
    
    Args:
        original_text (str): Original text
        summary_text (str): Summarized text
        
    Returns:
        float: Compression rate as percentage (0-100)
    """
    original_len = len(original_text)
    summary_len = len(summary_text)

    if original_len == 0:
        return 0.0

    compression_rate = (1 - (summary_len / original_len)) * 100
    return round(compression_rate, 2)


def create_stats_dict(original_text: str, summary_text: str):
    """
    Create a comprehensive dictionary of statistics.
    
    Args:
        original_text (str): Original text
        summary_text (str): Summarized text
        
    Returns:
        dict: Dictionary containing various statistics:
            - original_chars: Character count of original
            - summary_chars: Character count of summary
            - original_words: Word count of original
            - summary_words: Word count of summary
            - original_sentences: Sentence count of original (approximate)
            - summary_sentences: Sentence count of summary (approximate)
            - compression_rate: Percentage of text removed
            - reduction_rate: Percentage of text kept
    """
    # Basic counts
    original_chars = len(original_text)
    summary_chars = len(summary_text)
    original_words = len(original_text.split())
    summary_words = len(summary_text.split())
    
    # Approximate sentence counts (count periods, exclamation marks, question marks)
    original_sentences = original_text.count('.') + original_text.count('!') + original_text.count('?')
    summary_sentences = summary_text.count('.') + summary_text.count('!') + summary_text.count('?')
    
    # Compression calculation
    compression = calculate_compression(original_text, summary_text)
    
    return {
        "original_chars": original_chars,
        "summary_chars": summary_chars,
        "original_words": original_words,
        "summary_words": summary_words,
        "original_sentences": max(1, original_sentences),  # At least 1
        "summary_sentences": max(1, summary_sentences),
        "compression_rate": compression,
        "reduction_rate": round(100 - compression, 2)
    }


def format_stats_text(stats: dict) -> str:
    """
    Format statistics dictionary into a readable text string.
    
    Args:
        stats (dict): Statistics dictionary from create_stats_dict()
        
    Returns:
        str: Formatted text suitable for display
    """
    text = f"""
📊 **Detailed Statistics**

**Original Text:**
- Characters: {stats['original_chars']:,}
- Words: {stats['original_words']:,}
- Sentences: {stats['original_sentences']}

**Summary Text:**
- Characters: {stats['summary_chars']:,}
- Words: {stats['summary_words']:,}
- Sentences: {stats['summary_sentences']}

**Compression:**
- Compression Rate: {stats['compression_rate']}%
- Kept: {stats['reduction_rate']}%
    """
    return text.strip()


# ============================================
# Test code (run this file directly to test)
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("Testing visualize.py")
    print("=" * 50)
    
    # Sample texts for testing
    original_sample = """
    Artificial intelligence is rapidly transforming our world in unprecedented ways. 
    From healthcare to finance, education to entertainment, AI technologies are 
    revolutionizing how we live and work. Machine learning algorithms can now 
    diagnose diseases with remarkable accuracy, often surpassing human doctors. 
    In finance, AI-powered trading systems process vast amounts of data in 
    milliseconds to make investment decisions. Self-driving cars are becoming 
    a reality, promising to reduce accidents and transform transportation.
    """ * 2  # Repeat to make it longer
    
    summary_sample = """
    AI is transforming healthcare, finance, and transportation through 
    machine learning and automation, enabling better decisions and safety.
    """
    
    # Test statistics calculation
    print("\n📊 Statistics:")
    stats = create_stats_dict(original_sample, summary_sample)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test formatted output
    print("\n" + format_stats_text(stats))
    
    # Test chart generation
    print("\n🎨 Generating charts...")
    
    try:
        buf1 = plot_lengths(original_sample, summary_sample)
        print("✅ Length comparison chart generated")
        
        buf2 = plot_word_comparison(original_sample, summary_sample)
        print("✅ Word comparison chart generated")
        
        buf3 = plot_pie_chart(original_sample, summary_sample)
        print("✅ Pie chart generated")
        
        print("\n✅ All visualizations generated successfully!")
        print("   (Charts saved as image buffers)")
        
    except Exception as e:
        print(f"❌ Error generating charts: {e}")
    
    print("\n" + "=" * 50)