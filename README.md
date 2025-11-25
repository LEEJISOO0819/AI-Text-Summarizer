# AI-Text-Summarizer

A simple AI-powered long-text summarizer with a Streamlit-based web UI.  
This project provides text preprocessing, summarization using Hugging Face Transformers, and optional visualization features.

---

## 🚀 Demo

- **Web UI:** `app.py`  
- **Preprocessing:** `preprocess.py`  
- **Summarization Engine:** `summarizer.py`  
- **Visualization:** `visualize.py`  
- **Examples / Tests:** `examples/`, `tests/`

---

## ✨ Features

- Clean text (remove emojis, URLs, HTML tags, excessive whitespace)
- Summarize long English or Korean text using Transformers
- Adjustable summary length (Short / Medium / Long)
- Visualization: original vs summary text length chart
- Preprocessing unit tests included

---

## 📦 Quick Start (Local Installation)

### **Requirements**
- Python 3.10+
- Git
- Streamlit
- Hugging Face Transformers
- (Optional) GPU for faster inference

---

## 1. Clone Repository

```bash
git clone https://github.com/LEEJISOO0819/AI-Text-Summarizer.git
cd AI-Text-Summarizer
2. Create & Activate Virtual Environment
Windows (Git Bash)
bash
코드 복사
python -m venv venv
source venv/Scripts/activate
macOS / Linux
bash
코드 복사
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
코드 복사
pip install --upgrade pip
pip install -r requirements.txt
⚠️ If PyTorch installation fails on Windows, install a compatible version from:
https://pytorch.org/get-started/locally/

4. Run Streamlit Web UI
bash
코드 복사
streamlit run app.py
Open your browser at:

arduino
코드 복사
http://localhost:8501
🖥️ Usage Instructions
Paste long text into Input Text.

Choose summary length:

Short

Medium

Long

Click Summarize.

(Optional) Enable Show visualization to see a chart comparing lengths.

🧪 Running Tests (optional)
bash
코드 복사
pip install pytest
pytest -q tests/preprocess_test.py
📁 Project Structure
bash
코드 복사
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
🤝 Contributing
Create a new branch:

bash
코드 복사
git checkout -b feature/your-feature
Commit changes with clear English messages.

Push the branch and open a Pull Request to main.

⚠️ Notes
First-time model loading may take a few minutes.

If summarization feels slow, consider switching to a lighter model.

Some warnings from Hugging Face are normal and safe to ignore.

📄 License
MIT License
Feel free to use, modify, and distribute.

📬 Contact
Maintainer: Lee Jisoo
Email: dearjis00@naver.com