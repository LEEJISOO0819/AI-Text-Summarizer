# summarizer.py
from transformers import pipeline

class TextSummarizer:
    def __init__(self):
        """
        Initialize the summarization pipeline with a Korean model.
        """
        try:
            self.summarizer = pipeline(
                "summarization",
<<<<<<< HEAD
                model="gogamza/kobart-summarization"
            )
        except Exception as e:
            print("Model load failed:", e)
=======
                model="gogamza/kobart-summarization",
                tokenizer="gogamza/kobart-summarization"
            )
        except Exception as e:
            print("Model loading failed:", e)
>>>>>>> main
            self.summarizer = None

    def summarize(self, text, max_length=120, min_length=20):
        """
        Summarize the given text.

        Args:
            text (str): The input text to summarize.
            max_length (int): Maximum length of the summary.
            min_length (int): Minimum length of the summary.

        Returns:
            str: Summarized text.
        """
        if not self.summarizer:
<<<<<<< HEAD
            return "Model not ready."
        result = self.summarizer(text, max_length=max_length, min_length=20, do_sample=False)
        return result[0]['summary_text']
=======
            return "Model is not ready."

        try:
            # Use do_sample=False for deterministic output
            result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )
            return result[0]['summary_text']
        except Exception as e:
            return f"Summarization failed: {e}"

if __name__ == "__main__":
    s = TextSummarizer()
    test_text = (
        "Hello! I hope you are having a great day. "
        "This is a test of the AI Text Summarizer. "
        "It should provide a concise summary of the input text."
    )
    print("Input Text:")
    print(test_text)
    print("\nSummary:")
    print(s.summarize(test_text, max_length=60, min_length=20))
>>>>>>> main
