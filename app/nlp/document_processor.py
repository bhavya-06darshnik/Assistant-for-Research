import pdfplumber

def extract_text(file) -> str:
    """
    Extract text from a PDF or TXT file.

    Args:
        file: Uploaded file object (from Streamlit or FastAPI).

    Returns:
        str: Extracted text from the document.

    Raises:
        ValueError: If the file type is unsupported or text extraction fails.
    """
    try:
        if file.name.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                text = "".join(page.extract_text() or "" for page in pdf.pages)
        elif file.name.endswith(".txt"):
            text = file.read().decode("utf-8")
        else:
            raise ValueError("Unsupported file type. Use PDF or TXT.")

        if not text.strip():
            raise ValueError("No text extracted from the document.")

        return text
    except Exception as e:
        raise ValueError(f"Error extracting text: {str(e)}")

