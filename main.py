import streamlit as st
import io
from app.nlp.document_processor import extract_text
from app.nlp.summarizer import summarize_text
from app.nlp.qa_handler import answer_question
from app.nlp.question_generator import generate_questions

# Streamlit UI
st.title("Smart Assistant for Research Summarization")
st.write("Upload a PDF or TXT file to summarize, ask questions, or generate challenge questions.")

# Initialize session state
if "document_text" not in st.session_state:
    st.session_state.document_text = None
    st.session_state.summary = None
    st.session_state.questions = None

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

# Process uploaded file
if uploaded_file is not None:
    try:
        # Extract text
        with st.spinner("Extracting text..."):
            document_text = extract_text(uploaded_file)
        st.session_state.document_text = document_text
        st.success("File processed successfully!")
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.session_state.document_text = None
        st.session_state.summary = None
        st.session_state.questions = None

# Tabs for different modes
if st.session_state.document_text:
    tabs = st.tabs(["Summary", "Ask Anything", "Challenge Me"])

    # Summary Tab
    with tabs[0]:
        st.header("Summary")
        if st.session_state.summary is None:
            try:
                with st.spinner("Generating summary..."):
                    st.session_state.summary = summarize_text(st.session_state.document_text)
                st.success("Summary generated!")
            except Exception as e:
                st.error(f"Error generating summary: {str(e)}")
        if st.session_state.summary:
            st.write(f"**Summary ({len(st.session_state.summary.split())} words):**")
            st.write(st.session_state.summary)

    # Ask Anything Tab
    with tabs[1]:
        st.header("Ask Anything")
        question = st.text_input("Enter your question:")
        if question:
            try:
                with st.spinner("Answering question..."):
                    result = answer_question(question, st.session_state.document_text)
                st.write(f"**Answer:** {result['answer']}")
                st.write(f"**Justification:** {result['justification']}")
            except Exception as e:
                st.error(f"Error answering question: {str(e)}")

    # Challenge Me Tab
    with tabs[2]:
        st.header("Challenge Me")
        if st.button("Generate Questions"):
            try:
                with st.spinner("Generating questions..."):
                    st.session_state.questions = generate_questions(st.session_state.document_text, num_questions=5)
                st.success("Questions generated!")
            except Exception as e:
                st.error(f"Error generating questions: {str(e)}")
        if st.session_state.questions:
            st.write("**Generated Questions:**")
            for i, q in enumerate(st.session_state.questions, 1):
                st.write(f"{i}. {q}")
else:
    st.info("Please upload a file to begin.")