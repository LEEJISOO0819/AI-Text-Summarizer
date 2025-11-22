import matplotlib.pyplot as plt
import io


def plot_lengths(original_text: str, summary_text: str):
    """Return a bar chart image buffer comparing original and summary text lengths."""

    # Count characters in original and summary text
    original_len = len(original_text)
    summary_len = len(summary_text)

    # Create bar chart
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(["Original", "Summary"], [original_len, summary_len])
    ax.set_ylabel("Length (characters)")
    ax.set_title("Original vs Summary Length")

    # Convert plot to image buffer for Streamlit display
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    return buf


def calculate_compression(original_text: str, summary_text: str):
    """Return compression rate (%) calculated from original and summary lengths."""

    original_len = len(original_text)
    summary_len = len(summary_text)

    if original_len == 0:
        return 0.0

    compression_rate = (1 - (summary_len / original_len)) * 100
    return round(compression_rate, 2)
