# preprocess.py
import re
import unicodedata

# 이모지 범위 (자주 쓰이는 범위만 포함)
EMOJI_PATTERN = re.compile(
    "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags
    "]+", flags=re.UNICODE
)

# URL 패턴 (http(s) / www)
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')

# HTML 태그 제거
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')

# 제어문자(0x00-0x1F, 0x7F) 제거 (단, \n, \t는 보존후 처리)
CONTROL_CHAR_PATTERN = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')

def clean_text(text: str, min_length: int = 50):
    """
    텍스트 전처리 함수
    입력:
      text: 원본 문자열
      min_length: 최소 허용 길이(글자 수)
    반환:
      (cleaned_text_or_None, error_message_or_None)
    """
    if text is None:
        return None, "텍스트가 None 입니다."
    if not isinstance(text, str):
        return None, "입력은 문자열이어야 합니다."

    # Normalize unicode (조합문자 표준화)
    text = unicodedata.normalize("NFKC", text)

    # Normalize newlines: \r\n, \r -> \n
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove URLs
    text = URL_PATTERN.sub("", text)

    # Remove HTML tags
    text = HTML_TAG_PATTERN.sub("", text)

    # Remove emoji
    text = EMOJI_PATTERN.sub("", text)

    # Remove control characters except newline and tab
    text = CONTROL_CHAR_PATTERN.sub("", text)

    # Replace multiple spaces/tabs/newlines with single spaces/newlines as appropriate:
    # First, collapse repeated spaces/tabs into single space
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce repeated newlines to at most 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Strip leading/trailing whitespace and normalize internal whitespace around lines
    # Trim each line, then rejoin to preserve line breaks
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines).strip()

    # Collapse multiple spaces again after trimming lines
    text = " ".join(text.split())

    if len(text) < min_length:
        return None, f"텍스트가 너무 짧습니다 (최소 {min_length}자 필요). 현재 {len(text)}자."

    return text, None

if __name__ == "__main__":
    samples = [
        "안녕하세요😀😀 방문해 주셔서 감사합니다! https://example.com <b>bold</b>\r\n\r\n\n\n추가내용",
        "짧음",
        "첫줄\n\n\n두번째줄\n\n\n\n세번째"
    ]
    for s in samples:
        cleaned, err = clean_text(s, min_length=1)
        print("ORIG:", repr(s))
        print("CLEANED:", repr(cleaned))
        print("ERR:", err)
        print("---")
