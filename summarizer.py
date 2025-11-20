# summarizer.py
from transformers import pipeline

class TextSummarizer:
    def __init__(self):
        """
        Initialize the summarization pipeline using KoBART model.
        """
        try:
            self.summarizer = pipeline("summarization", model="gogamza/kobart-summarization")
        except Exception as e:
            print("Model loading failed:", e)
            self.summarizer = None

    def summarize(self, text: str, max_length: int = 120) -> str:
        """
        Summarize the given text.
        
        Args:
            text (str): Input text to summarize.
            max_length (int): Maximum length of the summary.
        
        Returns:
            str: Summary text or error message.
        """
        if not self.summarizer:
            return "Model is not ready."
        result = self.summarizer(text, max_length=max_length, min_length=20, do_sample=False)
        return result[0]['summary_text']


# Optional: function version for simpler import
def summarize_text(text: str, max_length: int = 120) -> str:
    """
    Function wrapper for quick summarization.
    """
    summarizer = TextSummarizer()
    return summarizer.summarize(text, max_length=max_length)


if __name__ == "__main__":
    test_text = "Enter a long text here to test summarization."
    summarizer = TextSummarizer()
    print("Class version:", summarizer.summarize(test_text))
    print("Function version:", summarize_text(test_text))
