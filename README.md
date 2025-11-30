# 🤖 AI Text Summarizer

An intelligent English text summarization tool powered by state-of-the-art BART-CNN model.

## 📋 Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Model](#model)
- [Technical Details](#technical-details)
- [Contributors](#contributors)
- [License](#license)

## ✨ Features

- 🇺🇸 **English Text Summarization**: Powered by BART-CNN model
- 🎯 **Flexible Summary Length**: Choose between Short, Medium, or Long summaries
- 📊 **Visual Analytics**: Interactive charts showing compression statistics
- 🖥️ **User-Friendly Interface**: Built with Streamlit for easy interaction
- 🚀 **State-of-the-Art Model**: Uses facebook/bart-large-cnn fine-tuned on CNN/DailyMail

## 🎬 Demo

### Input Example
```
Original text (500+ characters of English text)...
```

### Output
- Concise summary (~100-400 characters based on settings)
- Visual comparison charts (bar chart + pie chart)
- Detailed statistics (compression rate, word count, sentence count, etc.)

### Screenshots
![Main Interface](screenshots/result.png)

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Internet connection (for first-time model download)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/LEEJISOO0819/AI-Text-Summarizer.git
cd AI-Text-Summarizer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

For detailed installation instructions, see [INSTALL.md](INSTALL.md)

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

### Web Interface

1. **Launch the app**
   ```bash
   streamlit run app.py
   ```

2. **Input your text**
   - Type or paste English text into the input area (minimum 50 characters)
   - Or select from example texts in the sidebar

3. **Choose summary length**
   - **Short**: ~100 characters
   - **Medium**: ~150-200 characters
   - **Long**: ~300-400 characters

4. **Click "Summarize"**
   - Wait for processing (first run may take 1-2 minutes to download model)
   - View results with visual comparisons

### Code Usage

```python
from summarizer import summarize_text
from preprocess import clean_text

# Prepare text
text = """
Your long English text here...
(minimum 50 characters required)
"""

# Clean and preprocess
cleaned_text, error = clean_text(text, min_length=50)

if not error:
    # Generate summary (target 150 characters)
    summary = summarize_text(cleaned_text, target_chars=150)
    print(summary)
else:
    print(f"Error: {error}")
```

## 📁 Project Structure

```
AI-Text-Summarizer/
│
├── app.py                  # Main Streamlit application
├── summarizer.py           # AI summarization logic (BART-CNN)
├── preprocess.py           # Text preprocessing and cleaning
├── visualize.py            # Visualization functions (charts, statistics)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── INSTALL.md             # Detailed installation guide
│
├── screenshots/           # Application screenshots
│   └── result.png
│
└── tests/                 # Test files
    └── preprocess_test.py
```

### File Descriptions

- **app.py**: Streamlit web interface with user interaction logic
- **summarizer.py**: Core summarization engine using BART-CNN
- **preprocess.py**: Text cleaning (removes URLs, emojis, HTML tags, etc.)
- **visualize.py**: Generates comparison charts and calculates statistics

## 🤖 Model

### BART-CNN (English Summarization)
- **Model**: [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn)
- **Architecture**: BART-Large (Bidirectional and Auto-Regressive Transformers)
- **Training Data**: CNN/DailyMail dataset
- **Max Input**: 1024 characters
- **Model Size**: ~1.5GB
- **Use Case**: Optimized for news articles and general English text summarization

### Why BART-CNN?
- High-quality abstractive summarization
- Strong performance on various text types
- Widely used and well-maintained
- Excellent balance between quality and speed

## 🔧 Technical Details

### Text Preprocessing
The preprocessing module performs the following operations:
- Unicode normalization (NFKC)
- URL removal (`https://...`, `www....`)
- HTML tag stripping (`<div>`, `<p>`, etc.)
- Emoji filtering (🎉, 😀, etc.)
- Control character removal
- Whitespace normalization

### Summarization Process
1. **Input Validation**: Check minimum length (50 characters)
2. **Preprocessing**: Clean and normalize text
3. **Token Calculation**: Convert target character count to tokens
4. **Summary Generation**: Generate summary with BART-CNN
5. **Visualization**: Display results with statistics

### Visualization Features
- **Bar Chart**: Original vs. Summary length comparison
- **Pie Chart**: Content distribution (kept vs. removed)
- **Statistics Panel**: Detailed metrics including:
  - Character count
  - Word count
  - Sentence count (approximate)
  - Compression rate (percentage)

## ⚙️ Configuration

### Adjusting Summary Length

Edit `app.py` to customize target character counts:

```python
def get_target_chars(option: str) -> int:
    if option == "Short":
        return 80   # Adjust here
    elif option == "Medium":
        return 150  # Adjust here
    else:  # Long
        return 350  # Adjust here
```

### Changing Minimum Input Length

Edit `preprocess.py`:

```python
def clean_text(text: str, min_length: int = 50):  # Change default here
    # ...
```

## 🐛 Troubleshooting

### Issue: "Model not loading"
**Solution**: Ensure you have a stable internet connection for the first run. The model (~1.5GB) will be downloaded automatically.

### Issue: "Text too short" error
**Solution**: Input text must be at least 50 characters. Adjust `min_length` in `preprocess.py` if needed.

### Issue: "Out of memory" error
**Solution**: 
- The system automatically uses CPU if no GPU is available
- For very long texts (>1024 chars), they will be truncated automatically
- Close other applications to free up memory

### Issue: Charts not displaying
**Solution**: 
```bash
pip install matplotlib
```

### Issue: Summary is longer than original
**Solution**: This can happen with very short inputs. Use texts with at least 100-200 characters for best results.

## 🧪 Testing

Run the test script to verify installation:

```bash
# Test summarizer
python summarizer.py

# Test preprocessing
python -m pytest tests/
```

## 👥 Contributors

- **Jisoo Lee** - Team Leader, Core Development
- **Jiwoo Yang** - Preprocessing Module
- **Hosung Yoon** - UI/UX Design
- **Jisoo Kang** - Visualization Module
- **Hyunsoo Kim** - Testing & Documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [HuggingFace Transformers](https://huggingface.co/transformers/) for the model framework
- [Streamlit](https://streamlit.io/) for the web interface
- [Facebook AI](https://huggingface.co/facebook) for the BART-CNN model
- CNN/DailyMail dataset creators for training data

## 📞 Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/LEEJISOO0819/AI-Text-Summarizer/issues)
- **Email**: dearjis00@naver.com

## 🚀 Future Improvements

- [ ] Support for multiple languages
- [ ] Batch processing for multiple texts
- [ ] API endpoint for integration
- [ ] Custom model fine-tuning options
- [ ] Export summaries to PDF/Word

---

**⭐ If you find this project useful, please consider giving it a star!**

---
## 📚 References

### Models & Frameworks
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index) - Transformer models library
- [BART-CNN Model](https://huggingface.co/facebook/bart-large-cnn) - Pre-trained summarization model
- [Streamlit Documentation](https://docs.streamlit.io/) - Web app framework

### Dataset
- [CNN/DailyMail Dataset](https://huggingface.co/datasets/cnn_dailymail) - Used for BART model training

### Tutorials & Resources
- [Text Summarization with Transformers](https://huggingface.co/docs/transformers/tasks/summarization)
- [Streamlit Tutorial](https://docs.streamlit.io/library/get-started)
- [Matplotlib Visualization Guide](https://matplotlib.org/stable/tutorials/index.html)

### Inspiration
- Course: Open Source SW, Gachon University
- Professor: JaKeoung Koo
