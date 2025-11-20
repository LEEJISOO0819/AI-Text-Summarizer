# preprocess.py
import re
import unicodedata

# Emoji pattern (commonly used ranges)
EMOJI_PATTERN = re.compile(
    "[" 
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags
    "]+",
    flags=re.UNICODE
)

# URL pattern (http(s):// or www.)
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')

# HTML tag pattern
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')

# Control characters (0x00–0x1F, 0x7F), excluding newline and tab
CONTROL_CHAR_PATTERN = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')


def clean_text(text: str, min_length: int = 50):
    """
    Text preprocessing function.

    Args:
        text (str): The input text.
        min_length (int): Minimum allowed length (character count).

    Returns:
        (cleaned_text_or_None, error_message_or_None)
    """
    if text is None:
        return None, "Input text is None."
    if not isinstance(text, str):
        return None, "Input must be a string."

    # Normalize unicode characters (NFKC standardization)
    text = unicodedata.normalize("NFKC", text)

    # Normalize newline types: \r\n, \r -> \n
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove URLs
    text = URL_PATTERN.sub("", text)

    # Remove HTML tags
    text = HTML_TAG_PATTERN.sub("", text)

    # Remove emojis
    text = EMOJI_PATTERN.sub("", text)

    # Remove control characters (excluding \n and \t)
    text = CONTROL_CHAR_PATTERN.sub("", text)

    # Replace repeated spaces or tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce multiple newlines to at most 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Trim each line individually and rejoin
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines).strip()

    # Normalize internal spacing
    text = " ".join(text.split())

    # Final length check
    if len(text) < min_length:
        return None, f"Text is too short (minimum {min_length} characters required). Current length: {len(text)}."

    return text, None


if __name__ == "__main__":
    # Example usage
    samples = [
        "Hello😀😀 thanks for visiting! https://example.com <b>bold</b>\r\n\r\n\n\nextra text",
        "short",
        "first line\n\n\nsecond line\n\n\n\nthird line"
    ]
    for s in samples:
        cleaned, err = clean_text(s, min_length=1)
        print("ORIGINAL:", repr(s))
        print("CLEANED :", repr(cleaned))
        print("ERROR   :", err)
        print("---")
