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
            max_length (int): Maximum length of summary (in tokens)

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
            # ===== 완전히 수정된 길이 설정 =====
            
            # max_length를 사용자가 선택한 값 그대로 사용
            final_max_length = max_length
            
            # 언어별 min_length 비율 설정
            if language == 'en':
                # 영어: min은 max의 40%
                final_min_length = max(25, int(max_length * 0.4))
            else:
                # 한국어: min은 max의 35%
                final_min_length = max(20, int(max_length * 0.35))
            
            # 입력이 매우 짧을 때만 max_length를 줄임
            estimated_tokens = text_length // 4
            if estimated_tokens < 80:  # 입력이 매우 짧은 경우만
                final_max_length = max(40, int(estimated_tokens * 0.7))
                final_min_length = max(20, int(final_max_length * 0.4))
            
            print(f"Summary settings: max={final_max_length}, min={final_min_length}")
            
            result = summarizer(
                text,
                max_length=final_max_length,
                min_length=final_min_length,
                do_sample=False,
                truncation=True
            )
            
            summary_text = result[0]['summary_text']
            print(f"Generated summary: {len(summary_text)} characters")
            
            return summary_text
        
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
    
    # 영어 예제 (1605자 정도)
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
    Agriculture uses AI for precision farming, optimizing crop yields while 
    minimizing resource use. Entertainment industries leverage AI for content 
    recommendation, video game development, and even creative tasks like music 
    composition. However, these advances also raise important ethical questions 
    about privacy, job displacement, algorithmic bias, and the concentration of 
    power in tech companies. There are concerns about AI systems making decisions 
    that affect people's lives without adequate transparency or accountability.
    As AI continues to evolve at a rapid pace, society must grapple with how to 
    harness its benefits while mitigating potential risks and ensuring equitable 
    access to these transformative technologies. Governments are beginning to 
    develop regulatory frameworks, though they struggle to keep pace with 
    technological advancement. International cooperation is essential as AI 
    development transcends national boundaries and its impacts are global in scope.
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
    print("🇺🇸 ENGLISH TEST - Different Length Comparison")
    print("=" * 80)
    print(f"📝 Original: {len(english_text)} characters\n")
    
    for length_name, max_len in [("Short", 60), ("Medium", 100), ("Long", 150)]:
        print("─" * 80)
        print(f"📌 {length_name} Summary (max_length={max_len}):")
        summary = s.summarize(english_text, max_length=max_len)
        print(f"Result: {summary}")
        print(f"Length: {len(summary)} characters")
        print()
    
    print("\n" + "=" * 80)
    print("🇰🇷 KOREAN TEST - Different Length Comparison")
    print("=" * 80)
    print(f"📝 Original: {len(korean_text)} characters\n")
    
    for length_name, max_len in [("Short", 60), ("Medium", 100), ("Long", 150)]:
        print("─" * 80)
        print(f"📌 {length_name} Summary (max_length={max_len}):")
        summary = s.summarize(korean_text, max_length=max_len)
        print(f"Result: {summary}")
        print(f"Length: {len(summary)} characters")
        print()
    
    print("=" * 80)
