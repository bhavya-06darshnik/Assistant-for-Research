import re
from transformers import pipeline, T5Tokenizer

def generate_questions(document: str, num_questions: int = 5) -> list:
    try:
        # Validate input
        if not document.strip():
            raise ValueError("Document text is empty.")

        # Clean document text
        document = re.sub(r'([a-z])([A-Z])', r'\1 \2', document)
        document = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', document)
        document = re.sub(r'([.,])([a-zA-Z])', r'\1 \2', document)
        document = re.sub(r'[\n\t]+', ' ', document)
        document = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', document)
        document = re.sub(r'\s+', ' ', document).strip()

        # Log input
        print(f"Document: {len(document.split())} words, first 100 chars: {document[:100]}...")

        # Initialize tokenizer and pipeline with local model
        tokenizer = T5Tokenizer.from_pretrained("D:/EZ-Project/models/t5-small")
        qg_pipeline = pipeline("text2text-generation", model="D:/EZ-Project/models/t5-small", tokenizer=tokenizer, framework="pt")

        # Split document into smaller chunks (~100 words)
        words = document.split()
        chunk_size = 100
        chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

        # Generate questions
        questions = []
        for chunk in chunks:
            if not chunk.strip():
                continue
            input_text = f"generate question from text: {chunk}"
            generated = qg_pipeline(input_text, max_length=50, num_return_sequences=10, do_sample=True)
            print(f"Raw generated for chunk '{chunk[:50]}...': {generated}")
            questions.extend([g["generated_text"] for g in generated if g["generated_text"].strip()])

        # Filter and deduplicate questions
        questions = list(dict.fromkeys([q.strip() for q in questions if q.strip()]))
        questions = [q for q in questions if q.endswith("?") and len(q.split()) >= 2]

        # Fallback: Retry with smaller chunks or generic questions
        if len(questions) < num_questions:
            for chunk in chunks[:3]:  # Retry first three chunks
                input_text = f"generate question from text: {chunk[:50]}"  # Smaller sub-chunk
                generated = qg_pipeline(input_text, max_length=50, num_return_sequences=5, do_sample=True)
                print(f"Raw generated (fallback) for chunk '{chunk[:50]}...': {generated}")
                questions.extend([g["generated_text"] for g in generated if g["generated_text"].strip()])
            questions = list(dict.fromkeys([q.strip() for q in questions if q.strip()]))
            questions = [q for q in questions if q.endswith("?") and len(q.split()) >= 2]

        # Fallback: Add generic questions if still insufficient
        if len(questions) < num_questions:
            generic_questions = [
                "What is the main topic of the document?",
                "What are the key findings discussed?",
                "How does the document approach the problem?",
                "What methods are used in the study?",
                "What are the main conclusions?"
            ]
            questions.extend(generic_questions[:num_questions - len(questions)])

        # Limit to requested number
        if len(questions) < num_questions:
            raise ValueError(f"Generated only {len(questions)} questions, need {num_questions}.")
        questions = questions[:num_questions]

        # Log questions
        print(f"Generated questions: {questions}")
        return questions
    except Exception as e:
        raise ValueError(f"Error generating questions: {str(e)}")