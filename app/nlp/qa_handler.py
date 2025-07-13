import re
from transformers import pipeline

def answer_question(question: str, document: str) -> dict:
    if not question.strip() or not document.strip():
        raise ValueError("Question or document text is empty.")
    if len(question.split()) < 3 or not question.endswith("?"):
        raise ValueError("Question is too short or invalid (must end with '?').")

    document = re.sub(r'([a-z])([A-Z])', r'\1 \2', document)
    document = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', document)
    document = re.sub(r'(?<=[.,!?])(?=[^\s])', r' ', document)
    document = re.sub(r'[\n\t]+', ' ', document)
    document = re.sub(r'\$[^\$]+\$', '', document)
    document = re.sub(r'\[\d+\]', '', document)
    document = re.sub(r'[^\w\s.,!?()\-:;%]', '', document)
    document = re.sub(r'\s+', ' ', document).strip()

    qa_pipeline = pipeline("question-answering", model="D:/EZ-Project/models/distilbert", framework="pt")

    words = document.split()
    chunk_size = 120
    stride = 60
    chunks = []
    for i in range(0, len(words), stride):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk.split()) < 20:
            continue
        chunks.append(chunk)

    best_answer = None
    best_score = 0
    best_chunk = ""

    for chunk in chunks:
        try:
            result = qa_pipeline(question=question, context=chunk)
            score = result.get("score", 0)
            answer = result.get("answer", "").strip()
            if score > best_score and len(answer.split()) >= 3:
                best_score = score
                best_answer = answer
                best_chunk = chunk[:150] + "..." if len(chunk) > 150 else chunk
        except:
            continue

    if not best_answer or best_score < 0.25:
        raise ValueError(f"No confident answer found (best score: {best_score:.2f}).")

    best_answer = re.sub(r'\s+', ' ', best_answer).strip()

    return {
        "answer": best_answer,
        "justification": f"Based on document excerpt: '{best_chunk}' (confidence: {best_score:.2f})"
    }
