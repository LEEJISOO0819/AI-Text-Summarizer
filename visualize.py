import matplotlib.pyplot as plt
import io

# Generate a bar chart comparing original vs summarized text length
def plot_lengths(original_text: str, summary_text: str):
    """Return a bar chart image buffer comparing original and summary text lengths."""

    # Count characters in original and summary text
    original_len = len(original_text)
    summary_len = len(summary_text)

    # Create bar chart
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(["Original", "Summary"], [original_len, summary_len])
    ax.set_ylabel("Length (characters)")        # y-axis label
    ax.set_title("Original vs Summary Length")  # chart title

    # Convert plot to image buffer for Streamlit display
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)  # Prevent memory leak

    return buf


# Calculate compression rate based on text length
def calc
