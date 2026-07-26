from fastapi import FastAPI
from pydantic import BaseModel

from App.services.rag_service import RAGService

app = FastAPI()

rag = RAGService()

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Campus Info Chatbot API Running"}

@app.post("/chat")
def chat(data: Question):
    answer = rag.query(data.question)
    return {"answer": answer}