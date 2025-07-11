from app.nlp.document_processor import extract_text

def test_document_processor():
    # Test 1: Valid PDF
    try:
        with open(r"D:\EZ-Project\test\2507.07986v1.pdf", "rb") as f:
            text = extract_text(f)
            print("Test 1 (Valid PDF): Passed")
            print(f"Extracted text: {text[:100]}...")  # Print first 100 chars
            assert len(text.strip()) > 0, "PDF text is empty"
    except Exception as e:
        print(f"Test 1 (Valid PDF): Failed - {str(e)}")


if __name__ == "__main__":
    test_document_processor()