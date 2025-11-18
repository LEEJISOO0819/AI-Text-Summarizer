import re

def clean_text(text):
    
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Delete emojis
    
    text = re.sub(r'http\S+|www\S+', '', text)  # Delete URLs
    
    text = re.sub(r'\s+', ' ', text).strip()  # Reduce unnecessary spaces

    if len(text.split()) < 3:
        raise ValueError("The sentence is too short.")
    
    return text
