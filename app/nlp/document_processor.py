import pdfplumber
import io

def extract_text(file: io.BytesIO) -> str:
    try:
        file_name = file.name.lower()
        if file_name.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                text = "".join(page.extract_text() or "" for page in pdf.pages)
        elif file_name.endswith(".txt"):
            text = file.read().decode("utf-8")
        else:
            raise ValueError(f"Unsupported file type: {file_name}")
        if not text.strip():
            raise ValueError("No text extracted from file.")
        print(f"Extracted text: {len(text.split())} words, first 100 chars: {text[:100]}...")
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text: {str(e)}")

