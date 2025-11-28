# summarizer.py
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
        """
        korean_chars = len(re.findall(r'[가-힣]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        return 'ko' if korean_chars > english_chars else 'en'

    def summarize(self, text, max_length=120, allow_short=False):
        """
        Summarize text in Korean or English (auto-detected).

        allow_short: if True, bypass the "text too short" check (used for 2nd-stage summarization)
        """
        if not self.models_ready:
            return "❌ Models not ready. Please restart."

        if not isinstance(text, str) or text.strip() == "":
            return "❌ Invalid input text."

        text_length = len(text)

        # 기본 최소길이 검사: allow_short=True면 패스
        if not allow_short and text_length < 100:
            return f"⚠️ Text too short ({text_length} chars). Minimum 100 characters needed."

        language = self.detect_language(text)
        summarizer = self.ko_summarizer if language == 'ko' else self.en_summarizer

        # 입력 길이 제한 (문자 기준)
        max_input_length = 3000 if language == 'ko' else 1024
        if text_length > max_input_length:
            text = text[:max_input_length]
            text_length = len(text)
            print(f"⚠️ Text truncated to {max_input_length} characters")

        try:
            final_max_length = max_length
            if language == 'en':
                final_min_length = max(25, int(max_length * 0.4))
            else:
                final_min_length = max(20, int(max_length * 0.35))

            # 아주 짧은 입력에 대한 완화 (allow_short=True인 경우도 대비)
            estimated_tokens = max(1, text_length // 4)
            if estimated_tokens < 80 and not allow_short:
                final_max_length = max(40, int(estimated_tokens * 0.7))
                final_min_length = max(20, int(final_max_length * 0.4))

            print(f"[Summarize] language={language} max={final_max_length} min={final_min_length} allow_short={allow_short}")

            result = summarizer(
                text,
                max_length=final_max_length,
                min_length=final_min_length,
                do_sample=False,
                truncation=True
            )

            summary_text = result[0].get('summary_text', "").strip()
            print(f"[Summarize] Generated summary length={len(summary_text)}")
            return summary_text

        except Exception as e:
            return f"❌ Summarization error: {str(e)}"

# Global instance for reuse in Streamlit app
_app_summarizer = TextSummarizer()

def summarize_text(text: str, max_length: int = 120) -> str:
    """
    Simple wrapper used by app.py
    """
    return _app_summarizer.summarize(text, max_length=max_length, allow_short=False)

def summarize_text_two_stage(text: str, mode="medium"):
    """
    Two-stage summarization to enforce stronger control over output length.
    mode = 'short' / 'medium' / 'long'
    """
    # 1) base summary: 중간 길이로 요약 (allow_short=False)
    base_summary = _app_summarizer.summarize(text, max_length=120, allow_short=False)

    # 만약 1단계에서 error/경고 메시지 형태로 왔으면 바로 반환
    if isinstance(base_summary, str) and (base_summary.startswith("❌") or base_summary.startswith("⚠️")):
        return base_summary

    # 2) 2단계: base_summary에 대해 강/약 요약 (allow_short=True -> 길이 제한 완화)
    if mode == "short":
        final = _app_summarizer.summarize(base_summary, max_length=40, allow_short=True)
    elif mode == "medium":
        final = _app_summarizer.summarize(base_summary, max_length=80, allow_short=True)
    else:  # long
        final = _app_summarizer.summarize(base_summary, max_length=160, allow_short=True)

    return final

# If run directly, do a quick test (optional)
if __name__ == "__main__":
    s = TextSummarizer()
    sample = "This is a short test " * 60  # 약간 긴 테스트
    print("Base summary:\n", s.summarize(sample, max_length=120))
    print("Two-stage short:\n", summarize_text_two_stage(sample, mode="short"))
