# 🤖 AI Text Summarizer

An intelligent text summarization tool that automatically detects language (Korean/English) and generates concise summaries using state-of-the-art transformer models.

## 📋 Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Models](#models)
- [Technical Details](#technical-details)
- [Contributors](#contributors)
- [License](#license)

## ✨ Features

- 🇺🇸 **English Text Summarization**: Powered by BART-CNN model
- 🎯 **Flexible Summary Length**: Choose between Short, Medium, or Long summaries
- 📊 **Visual Analytics**: Interactive charts showing compression statistics
- 🖥️ **User-Friendly Interface**: Built with Streamlit for easy interaction
- 🚀 **State-of-the-Art Models**: Uses KoBART for Korean and BART-CNN for English

## 🎬 Demo

### Input Example
```
Original text (500+ characters)...
```

### Output
- Concise summary (50-150 characters based on settings)
- Visual comparison charts
- Detailed statistics (compression rate, word count, etc.)

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/LEEJISOO0819/AI-Text-Summarizer.git
cd AI-Text-Summarizer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📦 Requirements

```txt
transformers==4.35.0
torch==2.1.0
streamlit==1.28.0
sentencepiece==0.1.99
protobuf==3.20.3
regex==2023.10.3
matplotlib==3.8.0
```

## 🚀 Usage

### Basic Usage

1. **Launch the app**
   ```bash
   streamlit run app.py
   ```

2. **Input your text**
   - Type or paste text into the input area (minimum 50 characters)
   - Or select from example texts in the sidebar

3. **Choose summary length**
   - Short: ~60 tokens
   - Medium: ~100 tokens
   - Long: ~150 tokens

4. **Click "Summarize"**
   - Wait for processing (first run may take 1-2 minutes to download models)
   - View results with visual comparisons

### Example Code Usage

```python
from summarizer import summarize_text
from preprocess import clean_text

# Prepare text
text = "Your long text here..."
cleaned_text, error = clean_text(text, min_length=50)

if not error:
    # Generate summary
    summary = summarize_text(cleaned_text, max_length=100)
    print(summary)
```

## 📁 Project Structure

```
AI-Text-Summarizer/
│
├── app.py                  # Main Streamlit application
├── summarizer.py           # AI summarization logic (KoBART + BART-CNN)
├── preprocess.py           # Text preprocessing and cleaning
├── visualize.py            # Visualization functions (charts, statistics)
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

### File Descriptions

- **app.py**: Streamlit web interface with user interaction logic
- **summarizer.py**: Core summarization engine with automatic language detection
- **preprocess.py**: Text cleaning (removes URLs, emojis, HTML tags, etc.)
- **visualize.py**: Generates comparison charts and calculates statistics

## 🤖 Models

### English Summarization
- **Model**: [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn)
- **Architecture**: BART-Large fine-tuned on CNN/DailyMail
- **Max Input**: 1024 characters
- **Use Case**: News article and general English text summarization

### Language Detection
The system automatically detects the primary language by counting Korean characters (가-힣) vs. English characters (a-zA-Z) and selects the appropriate model.

## 🔧 Technical Details

### Text Preprocessing
- Unicode normalization (NFKC)
- URL removal
- HTML tag stripping
- Emoji filtering
- Control character removal
- Whitespace normalization

### Summarization Process
1. **Input Validation**: Check minimum length (50 characters)
2. **Preprocessing**: Clean and normalize text
3. **Language Detection**: Identify Korean vs. English
4. **Model Selection**: Choose appropriate summarization model
5. **Summary Generation**: Generate summary with specified length
6. **Visualization**: Display results with statistics

### Visualization Features
- **Bar Chart**: Original vs. Summary length comparison
- **Pie Chart**: Content distribution (kept vs. removed)
- **Statistics Panel**: Detailed metrics including:
  - Character count
  - Word count
  - Sentence count
  - Compression rate

## ⚙️ Configuration

### Adjusting Summary Length
Edit `app.py` to customize summary lengths:

```python
def get_max_length(option: str) -> int:
    if option == "Short":
        return 60  # Adjust here
    elif option == "Medium":
        return 100  # Adjust here
    else:
        return 150  # Adjust here
```

### Changing Minimum Input Length
Edit `preprocess.py`:

```python
def clean_text(text: str, min_length: int = 50):  # Change default here
    # ...
```

## 🐛 Troubleshooting

### Issue: "Model not loading"
**Solution**: Ensure you have a stable internet connection for the first run to download models (~2GB total).

### Issue: "Text too short" error
**Solution**: Input text must be at least 50 characters (adjustable in `preprocess.py`).

### Issue: "Out of memory" error
**Solution**: If you don't have GPU, the system will automatically use CPU. For very long texts, they will be truncated automatically.

### Issue: Charts not displaying
**Solution**: Make sure matplotlib is installed:
```bash
pip install matplotlib
```

## 👥 Contributors

- **Team Leader**: Jisoo Lee - Core development, model integration
- **Team Member 1**: Jiwoo Yang - Preprocessing module
- **Team Member 2**: Hosung Yoon - UI/UX design
- **Team Member 3**: Jisoo Kang - Visualization module
- **Team Member 4**: Hyunsoo Kim - Testing & documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [HuggingFace Transformers](https://huggingface.co/transformers/) for the model framework
- [Streamlit](https://streamlit.io/) for the web interface
- [gogamza](https://huggingface.co/gogamza) for the KoBART model
- [Facebook AI](https://huggingface.co/facebook) for the BART-CNN model

## 📞 Contact

For questions or feedback, please open an issue on GitHub or contact [dearjis00@naver.com]

---

**⭐ If you find this project useful, please consider giving it a star!**
