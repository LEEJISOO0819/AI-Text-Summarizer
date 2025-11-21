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
        # 한글 문자 개수 세기
        korean_chars = len(re.findall(r'[가-힣]', text))
        # 영문 문자 개수 세기
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        # 한글이 더 많으면 한국어
        if korean_chars > english_chars:
            return 'ko'
        else:
            return 'en'

    def summarize(self, text, max_length=120):
        """
        Summarize text in Korean or English (auto-detected).

        Args:
            text (str): Text to summarize
            max_length (int): Maximum length of summary

        Returns:
            str: Summary text or error message
        """
        if not self.models_ready:
            return "❌ Models not ready. Please restart."
        
        # 텍스트 길이 체크
        text_length = len(text)
        
        if text_length < 100:
            return f"⚠️ Text too short ({text_length} chars). Minimum 100 characters needed."
        
        # 언어 감지
        language = self.detect_language(text)
        print(f"Detected language: {'Korean' if language == 'ko' else 'English'}")
        
        # 적절한 모델 선택
        summarizer = self.ko_summarizer if language == 'ko' else self.en_summarizer
        
        # 너무 길면 자르기
        max_input_length = 3000 if language == 'ko' else 1024
        if text_length > max_input_length:
            text = text[:max_input_length]
            print(f"⚠️ Text truncated to {max_input_length} characters")
        
        try:
            # 영어 모델은 더 긴 요약 가능
            if language == 'en':
                adjusted_max_length = min(max_length, int(text_length * 0.5))
                adjusted_min_length = max(30, int(adjusted_max_length * 0.3))
            else:
                adjusted_max_length = min(max_length, int(text_length * 0.6))
                adjusted_min_length = max(20, int(adjusted_max_length * 0.3))
            
            result = summarizer(
                text,
                max_length=adjusted_max_length,
                min_length=adjusted_min_length,
                do_sample=False,
                truncation=True
            )
            
            return result[0]['summary_text']
        
        except Exception as e:
            return f"❌ Summarization error: {str(e)}"

# --- Wrapper for Streamlit app (hosung) ---
# Global instance for reuse
_app_summarizer = TextSummarizer()

def summarize_text(text: str, max_length: int = 120) -> str:
    """
    Simple wrapper used by app.py

    This keeps the original TextSummarizer class
    and just exposes a function interface.
    """
    return _app_summarizer.summarize(text, max_length=max_length)
# --- end of wrapper ---

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
    However, these advances also raise important ethical questions about privacy, 
    job displacement, and algorithmic bias. As AI continues to evolve, society 
    must grapple with how to harness its benefits while mitigating potential risks.
    """
    
    # 한국어 예제
    korean_text = """
    인공지능 기술이 빠르게 발전하면서 우리 생활 곳곳에 스며들고 있습니다.
    의료 분야에서는 질병 진단의 정확도를 높이고 있으며, 금융 분야에서는 
    투자 의사결정을 돕고 있습니다. 교육 분야에서도 개인 맞춤형 학습을 
    가능하게 하고 있습니다. 하지만 인공지능의 윤리적 문제와 일자리 감소에 
    대한 우려도 함께 제기되고 있습니다. 앞으로 인공지능 기술의 발전과 함께 
    이러한 문제들을 해결하기 위한 사회적 논의가 필요합니다.
    """
    
    print("=" * 70)
    print("🇺🇸 ENGLISH TEST")
    print("=" * 70)
    print("📝 Original:")
    print(english_text.strip())
    print("\n📌 Summary:")
    print(s.summarize(english_text, max_length=80))
    
    print("\n" + "=" * 70)
    print("🇰🇷 KOREAN TEST")
    print("=" * 70)
    print("📝 Original:")
    print(korean_text.strip())
    print("\n📌 Summary:")
    print(s.summarize(korean_text, max_length=60))
    print("=" * 70)