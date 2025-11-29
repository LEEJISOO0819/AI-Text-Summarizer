from transformers import pipeline
import torch
import re

class TextSummarizer:
    def __init__(self):
        """
        Initialize summarization pipelines for both Korean and English.
        """
        try:
            device = 0 if torch.cuda.is_available() else -1
            
            # 한국어 모델 (KoBART)
            print("Loading Korean model...")
            self.ko_summarizer = pipeline(
                "summarization",
                model="gogamza/kobart-summarization",
                device=device
            )
            
            # 영어 모델 (facebook BART)
            print("Loading English model...")
            self.en_summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=device
            )
            
            print("✅ Both models loaded successfully!")
            self.models_ready = True
            
        except Exception as e:
            print(f"❌ Model load failed: {e}")
            self.models_ready = False

    def detect_language(self, text):
        """
        Detect if text is primarily Korean or English.
        
        Args:
            text (str): Input text
            
        Returns:
            str: 'ko' for Korean, 'en' for English
        """
        korean_chars = len(re.findall(r'[가-힣]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if korean_chars > english_chars:
            return 'ko'
        else:
            return 'en'

    def summarize(self, text, target_chars=150):
        """
        Summarize text targeting a specific character count.

        Args:
            text (str): Text to summarize
            target_chars (int): Target character count
                - Short: ~80 chars (under 100)
                - Medium: ~150 chars (under 200)  
                - Long: ~350 chars (over 300)

        Returns:
            str: Summary text or error message
        """
        if not self.models_ready:
            return "❌ Models not ready. Please restart."
        
        text_length = len(text)
        
        if text_length < 100:
            return f"⚠️ Text too short ({text_length} chars). Minimum 100 characters needed."
        
        # 언어 감지
        language = self.detect_language(text)
        print(f"Detected language: {'Korean' if language == 'ko' else 'English'}")
        
        # 적절한 모델 선택
        summarizer = self.ko_summarizer if language == 'ko' else self.en_summarizer
        
        # 입력 길이 제한
        max_input_length = 3000 if language == 'ko' else 1024
        if text_length > max_input_length:
            text = text[:max_input_length]
            print(f"⚠️ Text truncated to {max_input_length} characters")
        
        try:
            # ===== 문자 수 기반 토큰 수 계산 =====
            # 목표 문자 수에 따라 토큰 수를 다르게 설정
            
            if language == 'en':
                # 영어: 1 토큰 ≈ 4-5 문자
                # BART 모델은 min_length에 가깝게 생성하는 경향이 있어서 더 줄여야 함
                if target_chars <= 100:  # Short (~80 chars)
                    max_tokens = 20
                    min_tokens = 10
                elif target_chars <= 200:  # Medium (~150 chars)
                    max_tokens = 40
                    min_tokens = 20
                else:  # Long (~350 chars)
                    max_tokens = 100
                    min_tokens = 50
            else:
                # 한국어: 1 토큰 ≈ 2-3 문자
                if target_chars <= 100:  # Short (~80 chars)
                    max_tokens = 35
                    min_tokens = 20
                elif target_chars <= 200:  # Medium (~150 chars)
                    max_tokens = 70
                    min_tokens = 40
                else:  # Long (~350 chars)
                    max_tokens = 140
                    min_tokens = 80
            
            print(f"Target: {target_chars} chars → Tokens: max={max_tokens}, min={min_tokens}")
            
            # 요약 생성
            result = summarizer(
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
        text: Text to summarize
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
    
    # 한국어 예제
    korean_text = """
    인공지능 기술이 빠르게 발전하면서 우리 생활 곳곳에 스며들고 있습니다.
    의료 분야에서는 질병 진단의 정확도를 높이고 있으며, 금융 분야에서는 
    투자 의사결정을 돕고 있습니다. 교육 분야에서도 개인 맞춤형 학습을 
    가능하게 하고 있습니다. 하지만 인공지능의 윤리적 문제와 일자리 감소에 
    대한 우려도 함께 제기되고 있습니다. 앞으로 인공지능 기술의 발전과 함께 
    이러한 문제들을 해결하기 위한 사회적 논의가 필요합니다.
    제조업에서는 로봇과 예측 유지보수 시스템이 생산성을 크게 향상시키고 있으며,
    농업에서는 정밀 농업을 통해 자원 사용을 최소화하면서 수확량을 최적화하고 있습니다.
    """
    
    print("=" * 80)
    print("🇺🇸 ENGLISH TEST - Character-based Length Control")
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
    
    print("\n" + "=" * 80)
    print("🇰🇷 KOREAN TEST - Character-based Length Control")
    print("=" * 80)
    print(f"📝 Original: {len(korean_text)} characters\n")
    
    for length_name, target in [("Short (<100)", 80), ("Medium (<200)", 150), ("Long (>300)", 350)]:
        print("─" * 80)
        print(f"📌 {length_name} (target: {target} chars)")
        summary = s.summarize(korean_text, target_chars=target)
        if not summary.startswith("❌"):
            print(f"Summary: {summary}")
            print(f"✅ Result: {len(summary)} characters")
        else:
            print(summary)
        print()
    
    print("=" * 80)
