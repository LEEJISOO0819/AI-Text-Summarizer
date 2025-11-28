# preprocess.py
"""
Text preprocessing module for AI Text Summarizer.
Cleans and normalizes input text by removing unwanted elements.
"""

import re
import unicodedata

# ============================================
# Regular Expression Patterns
# ============================================

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


# ============================================
# Main Preprocessing Function
# ============================================

def clean_text(text: str, min_length: int = 50):
    """
    Text preprocessing function.
    
    Performs the following cleaning steps:
    1. Unicode normalization (NFKC)
    2. Newline normalization
    3. URL removal
    4. HTML tag removal
    5. Emoji removal
    6. Control character removal
    7. Whitespace normalization
    8. Length validation

    Args:
        text (str): The input text to clean.
        min_length (int): Minimum allowed length in characters (default: 50).

    Returns:
        tuple: (cleaned_text_or_None, error_message_or_None)
            - If successful: (cleaned_text, None)
            - If failed: (None, error_message)
    
    Examples:
        >>> clean_text("Hello 😀 https://example.com")
        ('Hello', None)
        
        >>> clean_text("Hi")
        (None, 'Text is too short...')
    """
    # ===== Input Validation =====
    if text is None:
        return None, "Input text is None."
    if not isinstance(text, str):
        return None, "Input must be a string."

    # ===== Step 1: Unicode Normalization =====
    # Normalize unicode characters (NFKC standardization)
    # e.g., ﬁ → fi, ② → 2
    text = unicodedata.normalize("NFKC", text)

    # ===== Step 2: Newline Normalization =====
    # Normalize newline types: \r\n, \r -> \n
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # ===== Step 3: Remove URLs =====
    # Remove all URLs (http://, https://, www.)
    text = URL_PATTERN.sub("", text)

    # ===== Step 4: Remove HTML Tags =====
    # Remove all HTML/XML tags like <b>, <div>, etc.
    text = HTML_TAG_PATTERN.sub("", text)

    # ===== Step 5: Remove Emojis =====
    # Remove emoji characters
    text = EMOJI_PATTERN.sub("", text)

    # ===== Step 6: Remove Control Characters =====
    # Remove control characters (excluding \n and \t)
    text = CONTROL_CHAR_PATTERN.sub("", text)

    # ===== Step 7: Whitespace Normalization =====
    # Replace repeated spaces or tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce multiple newlines to at most 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Trim each line individually and rejoin
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines).strip()

    # Normalize internal spacing (convert all whitespace to single spaces)
    text = " ".join(text.split())

    # ===== Step 8: Length Validation =====
    # Final length check
    if len(text) < min_length:
        return None, f"Text is too short (minimum {min_length} characters required). Current length: {len(text)}."

    return text, None


# ============================================
# Test Code
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("Testing preprocess.py")
    print("=" * 60)
    
    # Example test cases
    samples = [
        ("Hello😀😀 thanks for visiting! https://example.com <b>bold</b>\r\n\r\n\n\nextra text", 
         "Full cleaning test"),
        ("short", 
         "Too short test"),
        ("first line\n\n\nsecond line\n\n\n\nthird line", 
         "Multiple newlines test"),
        ("Normal text without any special characters or formatting that should pass through cleanly.",
         "Normal text test")
    ]
    
    for text, description in samples:
        print(f"\n--- {description} ---")
        cleaned, err = clean_text(text, min_length=1)
        print(f"ORIGINAL: {repr(text)[:60]}...")
        print(f"CLEANED : {repr(cleaned)[:60] if cleaned else 'None'}...")
        print(f"ERROR   : {err}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed")
    print("=" * 60)
