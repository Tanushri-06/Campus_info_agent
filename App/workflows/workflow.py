from App.services.rag_service import RAGService

class CampusWorkflow:
    def __init__(self):
        self.rag = RAGService()

    def run(self, question):
        return self.rag.query(question)    

from App.services.rag_service import RAGService

 