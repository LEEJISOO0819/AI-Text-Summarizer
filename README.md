# AI-Text-Summarizer

A simple AI-powered long-text summarizer with a Streamlit-based web UI.  
This project provides text preprocessing, summarization using Hugging Face Transformers, and optional visualization features.

---

## Demo

- **Web UI:** `app.py`  
- **Preprocessing:** `preprocess.py`  
- **Summarization Engine:** `summarizer.py`  
- **Visualization:** `visualize.py`  
- **Examples / Tests:** `examples/`, `tests/`

---

## Features

- Clean text (remove emojis, URLs, HTML tags, excessive whitespace)
- Summarize long English or Korean text using Transformers
- Adjustable summary length (Short / Medium / Long)
- Visualization: original vs summary text length chart
- Preprocessing unit tests included

---

## Quick Start (Local Installation)

### **Requirements**
- Python 3.10+
- Git
- Streamlit
- Hugging Face Transformers
- (Optional) GPU for faster inference

---

## 1. Clone Repository

git clone https://github.com/LEEJISOO0819/AI-Text-Summarizer.git
cd AI-Text-Summarizer

## 2. Create & Activate Virtual Environment
Windows (Git Bash)
bash
python -m venv venv
source venv/Scripts/activate

macOS / Linux
bash
python3 -m venv venv
source venv/bin/activate

## 3. Install Dependencies
bash
pip install --upgrade pip
pip install -r requirements.txt

⚠️ If PyTorch installation fails on Windows, install a compatible version from:
https://pytorch.org/get-started/locally/

## 4. Run Streamlit Web UI
bash
streamlit run app.py

Open your browser at:
http://localhost:8501

🖥️ Usage Instructions
1. Paste long text into Input Text.
2. Choose summary length:
- Short
- Medium
- Long
3. Click Summarize.
4. (Optional) Enable Show visualization to see a chart comparing lengths.

## Running Tests (optional)
bash
pip install pytest
pytest -q tests/preprocess_test.py

## Project Structure
bash
AI-Text-Summarizer/
├── app.py               # Streamlit web UI
├── preprocess.py        # Cleaning functions
├── summarizer.py        # Hugging Face model summarizer
├── visualize.py         # Visualization module
├── requirements.txt
├── README.md
├── INSTALL.md
├── examples/
│   └── sample_input.txt
└── tests/
    └── preprocess_test.py

## Contributing
1. Create a new branch:
bash
git checkout -b feature/your-feature

2. Commit changes with clear English messages.
3. Push the branch and open a Pull Request to main.

## Notes
- First-time model loading may take a few minutes.
- If summarization feels slow, consider switching to a lighter model.
- Some warnings from Hugging Face are normal and safe to ignore.

## License
MIT License
Feel free to use, modify, and distribute.

## Contact
Maintainer: Lee Jisoo
Email: dearjis00@naver.com
