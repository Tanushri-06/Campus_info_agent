import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import login

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================
load_dotenv()

hf_token = os.getenv("HUGGING_FACE_TOKEN")
if hf_token:
    login(token=hf_token)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PDF_PATH = BASE_DIR / "data" / "college_handbook.pdf"

VECTOR_DB_PATH = BASE_DIR / "campus_vector_db"


class RAGService:

    def __init__(self):

        print("====================================")
        print("INITIALIZING RAG SERVICE")
        print("====================================")

        # ----------------------------------------------------
        # Embedding model
        # ----------------------------------------------------

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # ----------------------------------------------------
        # Existing Chroma database
        # ----------------------------------------------------

        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            collection_name="campus_info",
            persist_directory=str(VECTOR_DB_PATH),
        )

        # ----------------------------------------------------
        # Groq LLM
        # ----------------------------------------------------

        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2,
        )


    # ========================================================
    # REBUILD VECTOR DATABASE
    # ========================================================

    def process_and_create_embeddings(self, file_path=None):

        if file_path is None:
            file_path = PDF_PATH

        file_path = Path(file_path)

        print()
        print("====================================")
        print("PDF INGESTION")
        print("====================================")

        print("PDF:")
        print(file_path)

        # ----------------------------------------------------
        # Check PDF
        # ----------------------------------------------------

        if not file_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {file_path}"
            )

        print("PDF FOUND!")

        # ----------------------------------------------------
        # DELETE OLD VECTOR DATABASE
        # ----------------------------------------------------

        print()
        print("Creating fresh vector database...")

        # ----------------------------------------------------
        # CREATE FRESH CHROMA DATABASE
        # ----------------------------------------------------

        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            collection_name="campus_info",
            persist_directory=str(VECTOR_DB_PATH),
        )

        # ----------------------------------------------------
        # LOAD PDF
        # ----------------------------------------------------

        loader = PyPDFLoader(str(file_path))

        pages = loader.load()

        print()
        print(f"Loaded {len(pages)} pages.")

        # ----------------------------------------------------
        # CHUNKING
        # ----------------------------------------------------

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=75
        )

        chunks = splitter.split_documents(pages)

        print(f"Created {len(chunks)} chunks.")

        # ----------------------------------------------------
        # ADD NEW DOCUMENTS
        # ----------------------------------------------------

        print()
        print("Creating new embeddings...")

        ids = [
            f"college_handbook_page_{i}"
            for i in range(len(chunks))
        ]

        self.vector_store.add_documents(
            documents=chunks,
            ids=ids
        )

        print()
        print("====================================")
        print("NEW VECTOR DATABASE CREATED")
        print("====================================")

        print(f"Database location:")
        print(VECTOR_DB_PATH)

        print()
        print("Embeddings created successfully!")


    # ========================================================
    # RETRIEVER
    # ========================================================

    def get_retriever(self):

        return self.vector_store.as_retriever(
            search_kwargs={
                "k": 5
            }
        )


    # ========================================================
    # QUERY
    # ========================================================

    def query(self, question):

        retriever = self.get_retriever()

        docs = retriever.invoke(question)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )
        
        prompt = f"""
You are a helpful Campus Information Assistant.

Answer the question ONLY using the information provided
in the College Information section below.

Do not use outside knowledge.

Do not invent information.

If the answer is not present in the provided information,
say exactly:

"I couldn't find that information in the college handbook."

College Information:
{context}

Question:
{question}
"""

        response = self.llm.invoke(prompt)

        return response.content


# ============================================================
# TEST / INGESTION
# ============================================================

if __name__ == "__main__":

    rag_service = RAGService()

    rag_service.process_and_create_embeddings()

    print()
    print("====================================")
    print("TESTING RETRIEVAL")
    print("====================================")

    questions = [
    "Which undergraduate courses are offered?",
    "What postgraduate courses are available?",
    "What is the eligibility for engineering admission?",
    "How many books does the Central Library have?",
    "What is the hostel capacity?",
    "What is the placement support provided by the college?"
]
    for question in questions:

        print()
        print("====================================")
        print("QUESTION:")
        print(question)
        print("====================================")

        answer = rag_service.query(question)

        print()
        print("ANSWER:")
        print(answer)

 