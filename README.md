

# Smart Assistant for Research Summarization

## Overview
This project is a Streamlit-based web application designed to summarize research documents (PDF/TXT), answer questions, and generate challenge questions. Developed as part of the "Intern Task GenAI.pdf" assignment, it leverages pre-trained NLP models to meet requirements for response quality (30%), minimal hallucination (10%), and code structure (15%).

## Features
- **File Upload**: Supports PDF and TXT files (e.g., EXPO paper, ~2565 words).
- **Summary Generation**: Produces 50-150 word summaries with clean formatting.
- **Ask Anything**: Answers user questions with justifications based on document content.
- **Challenge Me**: Generates up to 5 relevant challenge questions.
- **User Interface**: Multi-tab Streamlit app for easy navigation.

## Requirements
- **Python**: 3.8+
- **Dependencies**:
    - `streamlit==1.39.0`
    - `pdfplumber==0.11.4`
    - `transformers==4.51.3`
    - `torch==2.5.1`
    - `sentencepiece`
    - `huggingface_hub`
- **Disk Space**: ~1.4 GB for pre-trained models.
- **Hardware**: GPU with CUDA support recommended for performance.

## Installation
1. Clone the repository: git clone <your-repo-url>
2. Set up a virtual environment: python -m venv
   venv\Scripts\activate
3. Install dependencies: pip install -r requirements.txt
4. (Create `requirements.txt` with listed packages if not present.)
5. Download models:
  - Place pre-trained models in `D:/EZ-Project/models`:
    - `t5-small` (242 MB)
    - `distilbart-cnn-12-6` (406 MB)
    - `distilbert-base-uncased-distilled-squad` (254 MB)
    - Ensure files like `pytorch_model.bin`, `tokenizer.json` are included.

## Usage
1. Run the Streamlit app: streamlit run main.py
2. Open your browser at `http://localhost:8501`.
3. Use the tabs:
 - **Home**: Upload a PDF/TXT file.
 - **Summary**: View a 50-150 word summary.
 - **Ask Anything**: Enter a question (e.g., "What is EXPO?") to get an answer.
 - **Challenge Me**: See 5 generated questions.
4. Test with sample files in `tests/sample.pdf` or `sample.txt`.

## File Structure
`**D:\EZ-Project
├── app
│   └── nlp
│       ├── document_processor.py  # Text extraction
│       ├── summarizer.py         # Summary generation
│       ├── qa_handler.py         # Question answering
│       ├── question_generator.py # Challenge questions
├── models
│   ├── t5-small
│   ├── distilbart-cnn-12-6
│   ├── distilbert-base-uncased-distilled-squad
├── tests
│   ├── sample.pdf              # Test PDF
│   ├── sample.txt              # Test TXT
├── main.py                    # Streamlit UI
├── README.md                  # This file**`
