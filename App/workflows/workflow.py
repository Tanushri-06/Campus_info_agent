#from App.services.rag_service import RAGService

#class CampusWorkflow:
#    def __init__(self):
#        self.rag = RAGService()

#    def run(self, question):
#        return self.rag.query(question)    

#from services.rag_service import RAGService

from App.agents.campus_info_agent import ask_campus_bot


class CampusWorkflow:
    def __init__(self):
        pass

    def run(self, question):
        return ask_campus_bot(question)

if __name__ == "__main__":
    workflow = CampusWorkflow()

    question = input("Ask a campus question: ")

    answer = workflow.run(question)

    print("\nChatbot:", answer)    