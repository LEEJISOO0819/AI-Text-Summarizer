from transformers import pipeline

summarizer = pipeline("summarization")
text = "Artificial intelligence is transforming the world by enabling machines to perform tasks that previously required human intelligence."
summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
print(summary[0]['summary_text'])
