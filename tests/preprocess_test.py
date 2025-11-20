import pytest
from preprocess import clean_text

def test_remove_emoji_url_html_control_chars():
    text = "Hello😀 visit https://example.com <b>bold</b>\x07"
    cleaned, err = clean_text(text, min_length=1)

    assert err is None
    assert "😀" not in cleaned
    assert "https://" not in cleaned
    assert "<b>" not in cleaned
    assert "\x07" not in cleaned


def test_reduce_multiple_newlines():
    text = "Line1\n\n\n\nLine2\n\n\nLine3"
    cleaned, err = clean_text(text, min_length=1)

    assert err is None
    assert "\n\n\n" not in cleaned


def test_min_length_check():
    text = "짧은 텍스트"
    cleaned, err = clean_text(text, min_length=50)

    assert cleaned is None
    assert err is not None
