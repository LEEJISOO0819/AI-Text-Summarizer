# summarizer.py
from transformers import pipeline

class TextSummarizer:
    def __init__(self):
        try:
            self.summarizer = pipeline(
                "summarization",
                model="gogamza/kobart-summarization"
            )
        except Exception as e:
            print("Model load failed:", e)
            self.summarizer = None

    def summarize(self, text, max_length=120):
        if not self.summarizer:
            return "Model not ready."
        result = self.summarizer(text, max_length=max_length, min_length=20, do_sample=False)
        return result[0]['summary_text']
