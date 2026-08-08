from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


# ============================================================
# STEP 1: FIND PDF
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

pdf_path = BASE_DIR / "college_handbook.pdf"

print("====================================")
print("PDF LOCATION CHECK")
print("====================================")
print("Looking for PDF at:")
print(pdf_path)
print()


if not pdf_path.exists():
    raise FileNotFoundError(
        f"PDF not found at: {pdf_path}"
    )

print("PDF FOUND!")
print()


# ============================================================
# STEP 2: LOAD PDF
# ============================================================

loader = PyPDFLoader(str(pdf_path))

documents = loader.load()

print(f"Successfully loaded {len(documents)} pages.")
print()


# ============================================================
# STEP 3: SPLIT PDF INTO CHUNKS
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2500,
    chunk_overlap=300
)

chunks = text_splitter.split_documents(documents)

print("====================================")
print("CHUNKING COMPLETE")
print("====================================")

print(f"Total pages: {len(documents)}")
print(f"Total chunks: {len(chunks)}")
print()


# ============================================================
# STEP 4: CREATE NEW EMBEDDINGS
# ============================================================

print("====================================")
print("CREATING EMBEDDINGS")
print("====================================")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

print("Embedding model ready.")
print()


# ============================================================
# STEP 5: CREATE NEW VECTOR DATABASE
# ============================================================

VECTOR_DB_PATH = BASE_DIR / "chroma_db_new"

print("====================================")
print("CREATING NEW VECTOR DATABASE")
print("====================================")

print("Vector database location:")
print(VECTOR_DB_PATH)
print()


vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(VECTOR_DB_PATH)
)

print("NEW VECTOR DATABASE CREATED!")
print()


# ============================================================
# STEP 6: TEST RETRIEVAL
# ============================================================

print("====================================")
print("TESTING RETRIEVAL")
print("====================================")

question = "What are the available academic programs?"

results = vectorstore.similarity_search(
    question,
    k=5
)

print(f"Retrieved {len(results)} chunks.")
print()


for i, result in enumerate(results):

    print("------------------------------------")
    print(f"RESULT {i + 1}")
    print("------------------------------------")

    print(result.page_content)
    print()


print("====================================")
print("INGESTION COMPLETE!")
print("====================================")