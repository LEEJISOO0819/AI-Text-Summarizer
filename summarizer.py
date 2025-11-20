# summarizer.py
from transformers import pipeline

class TextSummarizer:
    def __init__(self):
        """
        Initialize the summarization pipeline using KoBART model.
        """
        try:
            self.summarizer = pipeline(
                "summarization",
                model="gogamza/kobart-summarization"
            )
        except Exception as e:
            print("Model load failed:", e)
            self.summarizer = None

    def summarize(self, text, max_length=120):
        """
        Summarize the input text.

        Args:
            text (str): Text to summarize
            max_length (int): Maximum length of the summary

        Returns:
            str: Summary text
        """
        if not self.summarizer:
            return "Model not ready."
        result = self.summarizer(
            text,
            max_length=max_length,
            min_length=20,
            do_sample=False
        )
        return result[0]['summary_text']


if __name__ == "__main__":
    s = TextSummarizer()
    sample_text = (
        "Artificial Intelligence is rapidly evolving and impacting every sector, "
        "from healthcare to finance. It enables better decision-making, "
        "automation, and enhanced productivity."
    )
    print("Original Text:\n", sample_text)
    print("Summary:\n", s.summarize(sample_text, max_length=60))
