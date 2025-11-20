# preprocess.py
import re
import unicodedata

EMOJI_PATTERN = re.compile(
    "["
    u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    u"\U0001F1E0-\U0001F1FF"
    "]+",
    flags=re.UNICODE
)

URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
CONTROL_CHAR_PATTERN = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')

def clean_text(text, min_length=50):
    """Text preprocessing function with minimum length option."""
    if text is None:
        return None, "Input text is None."
    if not isinstance(text, str):
        return None, "Input must be a string."

    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = URL_PATTERN.sub("", text)
    text = HTML_TAG_PATTERN.sub("", text)
    text = EMOJI_PATTERN.sub("", text)
    text = CONTROL_CHAR_PATTERN.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines).strip()
    text = " ".join(text.split())

    if len(text) < min_length:
        return None, f"Text too short (min {min_length} chars). Current {len(text)}."

    return text, None
