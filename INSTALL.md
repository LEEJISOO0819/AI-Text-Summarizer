# AI Text Summarizer Installation & Execution Guide

1. Project Overview
   -The AI Text Summarizer is a Streamlit-based web application that automatically summarizes long Korean or English texts. It also provides visualization features such as bar charts, pie charts and statistical summaries.

2. System Requirements
   - OS: Windows / MacOS
   - Python: Version 3.10 or higher
   - Required Packages(from requirements.txt):
     1) transformers
     2) torch
     3) streamlit
     4) sentencepiece
     5) protobuf
     6) regex
     7) matplotlib

3. Installation
   1) Clone the repository(bash)
      git clone https://github.com/your-team-repo/AI-Text-Summarizer.git
   2) Move into the project directory(bash)
   cd AI-Text-Summarizer
   3) (optional) Create a virtual environment(nginx)
      python -m venv venv
   -Windows:  venv\Scripts\activate
   -Mac(bash): source venv/bin/activate

   4) Install dependencies(nginx)
  pip install -r requirements.txt


4. How to Run the Application
   - Run the following command to start the Streamlit app:(arduino)
    streamlit run app.py
 
   - Your browser will automatically open the app at:(arduino)
     http://localhost:8501

     
5. Execution Screen

6. Key Features
   - Automatic Korean/English language detection
   - Summarization using KoBART / BART CNN models
   - summary lingth options: SHort / Medium / Long
   - Bar chart visualization (content distribution)
   - Detailed statistics: character count, word count, sentence count, compression rate

7. Example Directory Structure

AI-Text-Summarizer/
│── app.py
│── preprocess.py
│── summarizer.py
│── visualize.py
│── requirements.txt
│── INSTALL.md
│── screenshots/result.png
│── tests/

8. Troubleshooting
   - Streamlit error -> pip install streamlit
   - Transformers import error -> pip install transformers sentencepiece protobuf
   - Model dounloading is slow -> The first run may take 1-3 minutes (this is normal)
  
9. Contributors
    Team Members: Jisoo Lee, Jisoo Kang, Hyunsoo Kim, Jiwoo Yang, Hosung Yoon






   

      
