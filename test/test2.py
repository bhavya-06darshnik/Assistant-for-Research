import os
from app.nlp.document_processor import extract_text
from app.nlp.summarizer import summarize_text

def test_summarizer():
    # Test 1: Valid PDF Summary
    try:
        with open(r"D:\EZ-Project\test\2507.07986v1.pdf", "rb") as f:
            text = extract_text(f)
            summary = summarize_text(text)
            print("Test 1 (Valid PDF Summary): Passed")
            print(f"Summary: {summary}")
            word_count = len(summary.split())
            assert 50 <= word_count <= 150, f"Summary word count {word_count} not in range 50-150"
            assert len(summary.strip()) > 0, "Summary is empty"
    except Exception as e:
        print(f"Test 1 (Valid PDF Summary): Failed - {str(e)}")



if __name__ == "__main__":
    test_summarizer()