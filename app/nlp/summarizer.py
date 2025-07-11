
import re
from transformers import pipeline

def summarize_text(text: str) -> str:
    """
    Generate a concise summary (50-150 words) of the input document text.

    Args:
        text (str): Extracted document text from document_processor.

    Returns:
        str: Summary text (50-150 words).

    Raises:
        ValueError: If input text is empty or summarization fails.
    """
    try:
        if not text.strip():
            raise ValueError("Input text is empty.")

        # Clean text: fix common PDF extraction issues (e.g., missing spaces)
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between lowercase and uppercase
        text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace

        # Check input length (in words)
        word_count = len(text.split())
        if word_count < 50:
            raise ValueError(f"Input text too short ({word_count} words). Minimum 50 words required.")

        # Initialize summarization pipeline
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")

        # Truncate text to ~1000 tokens (~750 words, model limit)
        max_input_length = 1000
        text = ' '.join(text.split()[:750])  # Approximate token limit by word count

        # Generate summary (~50-150 words, adjust token lengths)
        summary = summarizer(text, max_length=200, min_length=75, do_sample=False)

        # Verify summary word count
        summary_text = summary[0]["summary_text"]
        summary_word_count = len(summary_text.split())
        if summary_word_count < 50:
            raise ValueError(f"Summary too short ({summary_word_count} words).")

        return summary_text
    except Exception as e:
        raise ValueError(f"Error generating summary: {str(e)}")



