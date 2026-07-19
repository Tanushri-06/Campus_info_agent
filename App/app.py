import streamlit as st

from services.rag_service import RAGService

rag = RAGService()

st.set_page_config(
    page_title="Campus Information Chatbot",
    page_icon="🎓"
)

st.title("🎓 Campus Information Chatbot")

question = st.text_input(
    "Ask anything about the college:"
)

if st.button("Ask"):

    if question:

        answer = rag.query(question)

        st.success(answer)
        