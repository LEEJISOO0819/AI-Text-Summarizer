# summarizer.py
from transformers import pipeline

class TextSummarizer:
    def __init__(self):
        try:
            self.summarizer = pipeline("summarization", model="gogamza/kobart-summarization")
        except Exception as e:
            print("모델 로드 실패:", e)
            self.summarizer = None

    def summarize(self, text, max_length=120):
        if not self.summarizer:
            return "모델이 준비되지 않았습니다."
        result = self.summarizer(text, max_length=max_length, min_length=20, do_sample=False)
        return result[0]['summary_text']

if __name__ == "__main__":
    s = TextSummarizer()
    print(s.summarize("여기에 요약할 긴 문장을 넣어 테스트하세요."))

##### 한글 모두 영어로 수정할 것!!!!!