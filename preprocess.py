# preprocess.py
def clean_text(text):
    if not text:
        return None, "텍스트가 비어 있습니다."
    text = text.strip()
    text = text.replace("\r\n", "\n")
    text = " ".join(text.split())  # 연속 공백 제거
    if len(text) < 50:
        return None, "텍스트가 너무 짧습니다 (최소 50자 권장)"
    return text, None

if __name__ == "__main__":
    sample = "   안녕하세요. 테스트 텍스트입니다.   "
    print(clean_text(sample))

##### 한글 모두 영어로 수정할 것!!!!!