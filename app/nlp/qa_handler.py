import re
from transformers import pipeline

def answer_question(question: str, document: str) -> dict:
    try:
        # Validate inputs
        if not question.strip() or not document.strip():
            raise ValueError("Question or document text is empty.")
        if len(question.split()) < 3 or not question.endswith("?"):
            raise ValueError("Question is too short or invalid (must end with '?'). Try specific questions like 'What is EXPO?' or 'How does the algorithm work?'")

        # Clean document text
        document = re.sub(r'([a-z])([A-Z])', r'\1 \2', document)  # Fix camelCase
        document = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', document)  # Space before numbers
        document = re.sub(r'([.,])([a-zA-Z])', r'\1 \2', document)  # Space after punctuation
        document = re.sub(r'[\n\t]+', ' ', document)  # Remove newlines/tabs
        document = re.sub(r'\$[^\$]+\$', '', document)  # Remove LaTeX
        document = re.sub(r'\[\d+\]', '', document)  # Remove citations
        document = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', document)  # Remove special characters
        document = re.sub(r'\s+', ' ', document).strip()

        # Log input
        print(f"Question: {question}")
        print(f"Document: {len(document.split())} words, first 100 chars: {document[:100]}...")

        # Initialize QA pipeline with local model
        qa_pipeline = pipeline("question-answering", model="D:/EZ-Project/models/distilbert", framework="pt")

        # Split document into smaller chunks (~50 words)
        words = document.split()
        chunk_size = 50
        chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

        # Find best answer
        best_answer = None
        best_score = 0
        best_chunk = ""

        for chunk in chunks:
            if not chunk.strip():
                continue
            print(f"Processing chunk: {chunk[:100]}... (score: {best_score:.2f})")
            result = qa_pipeline(question=question, context=chunk)
            if result["score"] > best_score and len(result["answer"].split()) >= 3:
                best_score = result["score"]
                best_answer = result["answer"].strip()
                best_chunk = chunk[:100] + "..." if len(chunk) > 100 else chunk

        # Validate answer or provide fallback
        if not best_answer or best_score < 0.1 or len(best_answer.split()) < 3:
            raise ValueError(f"No confident answer found (best score: {best_score:.2f}). Try rephrasing, e.g., 'What is the main algorithm?' or 'What are the key results?'")

        # Clean answer
        best_answer = re.sub(r'\s+', ' ', best_answer).strip()

        return {
            "answer": best_answer,
            "justification": f"Based on document excerpt: '{best_chunk}' (confidence: {best_score:.2f})"
        }
    except Exception as e:
        raise ValueError(f"Error answering question: {str(e)}")