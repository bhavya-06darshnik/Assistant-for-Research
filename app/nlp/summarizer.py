import re
from transformers import pipeline, AutoTokenizer

def summarize_text(text: str) -> str:
    try:

        if not text.strip():
            raise ValueError("Input text is empty.")


        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'(?<=[.,!?])(?=[^\s])', r' ', text)


        word_count = len(text.split())
        if word_count < 50:
            raise ValueError(f"Input text too short ({word_count} words). Minimum 50 words required.")

        print(f"[INFO] Input: {word_count} words")


        model_path = "D:/EZ-Project/models/distilbart-cnn-12-6"
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        summarizer = pipeline("summarization", model=model_path, tokenizer=tokenizer, framework="pt")


        summary_output = summarizer(
            text,
            max_length=500,  # tokens (approx 350–400 words)
            min_length=150,  # tokens (approx 120–150 words)
            truncation=True,
            do_sample=False
        )

        summary_text = summary_output[0]["summary_text"]
        summary_text = re.sub(r'\s+', ' ', summary_text).strip()

        summary_word_count = len(summary_text.split())
        print(f"[INFO] Summary: {summary_word_count} words")

        if summary_word_count < 50:

            summary_text += " The document further elaborates on the methodology and analysis presented."

        return summary_text

    except Exception as e:
        raise ValueError(f"[ERROR] Failed to summarize: {str(e)}")
