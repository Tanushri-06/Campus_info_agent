import os

from dotenv import load_dotenv
from huggingface_hub import login

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#from langchain_google_genai import(
#     GoogleGenerativeAIEmbeddings,
#     ChatGoogleGenerativeAI
#    )

from langchain_groq import ChatGroq

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma


load_dotenv()  # loads the .env
login(token=os.getenv("HUGGING_FACE_TOKEN"))

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            collection_name="campus_info",
            persist_directory="./campus_vector_db",
        )

        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2,
        )
        
    def process_and_create_embeddings(self, file_path="./data/college_handbook.pdf"):
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(pages)

        self.vector_store.add_documents(chunks)
    

        print("Embeddings created successfully!")    


    

    def get_retriever(self):

        return self.vector_store.as_retriever(
            search_kwargs={"k": 5}
            )
    
    def query(self, question):

        retriever = self.get_retriever()

        docs = retriever.invoke(question)

        context = "\n\n".join(
        [doc.page_content for doc in docs]
        )

        prompt = f"""
    You are a helpful Campus Information Assistant.

    Answer the question only using the information below.

    If the answer is not present, say:
    "I couldn't find that information in the college handbook."

    College Information:
    {context}

    Question:
    {question}
    """

        response = self.llm.invoke(prompt)

        return response.content
          


if __name__ == "__main__":
    rag_service = RAGService() 
    rag_service.process_and_create_embeddings()

    answer = rag_service.query(
        "Which undergraduate courses are provided?"
    )

    print(answer)
    

    