# test_summary.py
"""
Simple test script for AI Text Summarizer
"""

def test_summarizer():
    from summarizer import summarize_text
    
    text = "Artificial intelligence is transforming our world. " * 10
    
    print("Testing summarizer...")
    summary = summarize_text(text, target_chars=150)
    print(f"✅ Summary generated: {len(summary)} chars")
    assert len(summary) > 0, "Summary should not be empty"
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_summarizer()
