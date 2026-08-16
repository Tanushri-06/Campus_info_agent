from App.services.rag_service import RAGService

rag = None


def get_rag():
    global rag

    if rag is None:
        rag = RAGService()

    return rag


def ask_campus_bot(question):
    return get_rag().query(question)