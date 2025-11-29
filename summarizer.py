from transformers import pipeline
import torch

class TextSummarizer:
    def __init__(self):
        """
        Initialize English summarization pipeline.
        """
        try:
            device = 0 if torch.cuda.is_available() else -1
            
            # 영어 모델 (facebook BART)
            print("Loading English model...")
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=device
            )
            
            print("✅ Model loaded successfully!")
            self.models_ready = True
            
        except Exception as e:
            print(f"❌ Model load failed: {e}")
            self.models_ready = False

    def summarize(self, text, target_chars=150):
        """
        Summarize English text targeting a specific character count.

        Args:
            text (str): English text to summarize
            target_chars (int): Target character count
                - Short: ~80 chars (under 100)
                - Medium: ~150 chars (under 200)  
                - Long: ~350 chars (over 300)

        Returns:
            str: Summary text or error message
        """
        if not self.models_ready:
            return "❌ Model not ready. Please restart."
        
        text_length = len(text)
        
        if text_length < 100:
            return f"⚠️ Text too short ({text_length} chars). Minimum 100 characters needed."
        
        # 입력 길이 제한
        if text_length > 1024:
            text = text[:1024]
            print(f"⚠️ Text truncated to 1024 characters")
        
        try:
            # 영어: 1 토큰 ≈ 4-5 문자
            if target_chars <= 100:  # Short (~80 chars)
                max_tokens = 20
                min_tokens = 10
            elif target_chars <= 200:  # Medium (~150 chars)
                max_tokens = 40
                min_tokens = 20
            else:  # Long (~350 chars)
                max_tokens = 100
                min_tokens = 50
            
            print(f"Target: {target_chars} chars → Tokens: max={max_tokens}, min={min_tokens}")
            
            # 요약 생성
            result = self.summarizer(
                text,
                max_length=max_tokens,
                min_length=min_tokens,
                do_sample=False,
                truncation=True
            )
            
            summary_text = result[0]['summary_text']
            print(f"✅ Generated: {len(summary_text)} characters (target: {target_chars})")
            
            return summary_text
        
        except Exception as e:
            return f"❌ Summarization error: {str(e)}"


# --- Wrapper for Streamlit app ---
_app_summarizer = TextSummarizer()

def summarize_text(text: str, target_chars: int = 150) -> str:
    """
    Simple wrapper for app.py
    
    Args:
        text: English text to summarize
        target_chars: Target character count (default: 150)
    
    Returns:
        Summary text
    """
    return _app_summarizer.summarize(text, target_chars=target_chars)


# ===== TEST CODE =====
if __name__ == "__main__":
    s = TextSummarizer()
    
    # 영어 예제
    english_text = """
    Artificial intelligence is rapidly transforming our world in unprecedented ways. 
    From healthcare to finance, education to entertainment, AI technologies are 
    revolutionizing how we live and work. Machine learning algorithms can now 
    diagnose diseases with remarkable accuracy, often surpassing human doctors. 
    In finance, AI-powered trading systems process vast amounts of data in 
    milliseconds to make investment decisions. Self-driving cars are becoming 
    a reality, promising to reduce accidents and transform transportation. 
    Natural language processing has advanced to the point where chatbots can 
    engage in surprisingly human-like conversations. Computer vision systems can 
    now identify objects and faces with incredible precision. In education, 
    personalized learning platforms adapt to individual student needs and pace.
    Climate science benefits from AI's ability to analyze massive datasets and 
    predict weather patterns. Manufacturing has been transformed by robotics and 
    predictive maintenance systems that prevent equipment failures before they occur.
    """
    
    print("=" * 80)
    print("🇺🇸 ENGLISH SUMMARIZATION TEST")
    print("=" * 80)
    print(f"📝 Original: {len(english_text)} characters\n")
    
    for length_name, target in [("Short (<100)", 80), ("Medium (<200)", 150), ("Long (>300)", 350)]:
        print("─" * 80)
        print(f"📌 {length_name} (target: {target} chars)")
        summary = s.summarize(english_text, target_chars=target)
        if not summary.startswith("❌"):
            print(f"Summary: {summary}")
            print(f"✅ Result: {len(summary)} characters")
        else:
            print(summary)
        print()
    
    print("=" * 80)
