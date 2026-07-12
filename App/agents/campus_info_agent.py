from App.services.rag_service import RAGService

rag = RAGService()

def ask_campus_bot(question):
    return rag.query(question)