# Interactive Campus Information Chatbot

This project is an AI-powered Campus Information Chatbot that helps students quickly find information from college documents using Retrieval-Augmented Generation (RAG).

## Technologies Used

- Python
- LangChain
- Google Gemini
- ChromaDB
- PyPDF
- Streamlit (optional)

## Features

- Answers questions from campus documents
- Uses Gemini for response generation
- Stores document embeddings in ChromaDB
- Supports PDF-based knowledge retrieval

# 🎓 Interactive Campus Information Chatbot

## 📌 Project Overview

The Interactive Campus Information Chatbot is an AI-powered chatbot that helps students quickly find information from college documents such as the college handbook, admission details, courses, hostel rules, and other campus-related information.

The chatbot uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generates accurate responses using a Large Language Model (Groq Llama 3).

---

## 🚀 Features

- 📄 Reads information from college PDF documents
- 🔍 Retrieves relevant information using RAG
- 🤖 Answers campus-related questions
- 💬 Interactive chatbot interface using Streamlit
- 📚 Uses ChromaDB for vector storage
- 🧠 Uses HuggingFace embeddings
- ⚡ Uses Groq Llama 3 for response generation

---

## 🛠 Technologies Used
- Python
- LangChain
- FastAPI
- Streamlit
- HuggingFace Embeddings
- ChromaDB
- Groq API
- PyPDF
- Pydantic

## 📂 Project Structure
Interactive-Campus-Info-Chatbot
│
├── App
│   ├── agents
│   │   └── campus_info_agent.py
│   │
│   ├── services
│   │   └── rag_service.py
│   │
│   ├── workflows
│   │   └── workflow.py
│   │
│   └── app.py
│
├── data
│   └── college_handbook.pdf
│
├── campus_vector_db
│
├── api.py
├── main.py
├── requirements.txt
├── README.md
└── .env


## 🚀 Features
📄 Document-based Question Answering using RAG
🤖 AI-powered Campus Information Agent
🔍 Semantic Search using ChromaDB
📚 College Handbook PDF Processing
🌐 REST API using FastAPI
📖 Interactive API Documentation with Swagger UI
🔄 Basic AI Workflow for processing user queries

## ▶️ How to Run

1. Clone the repository
    git clone <repository-link>
2. Install dependencies
    pip install -r requirements.txt
3. Add your API key in the .env file
    GROQ_API_KEY=your_api_key
4. Run the Streamlit application
    streamlit run App/app.py
5. Run the FastAPI server
    uvicorn api:app --reload
6. Open the API documentation
    http://127.0.0.1:8000/docs

## 🔗 API Endpoints

Method  | Endpoint | Description
-----------------------------------------------------------------------------------------
GET	    |     /	   |  Checks whether the API is running
POST	|   /chat  |  Accepts a campus-related question and returns an AI-generated answer

## 🏗 AI Workflow
  User
   │
   ▼
FastAPI Endpoint (/chat)
   │
   ▼
Campus Workflow
   │
   ▼
Campus Info Agent
   │
   ▼
RAG Service
   │
   ▼
ChromaDB Retrieval
   │
   ▼
Groq LLM
   │
   ▼
Response

## 💡 Sample Questions

- What undergraduate courses are offered?
- What are the library timings?
- What are the hostel rules?
- What is the admission process?
- Where is the placement cell?

---

## 📷 Output

The chatbot answers questions based on the uploaded college handbook using Retrieval-Augmented Generation (RAG).

---

## 👩‍💻 Developed By
Internship Project – Interactive Campus Info AI Agent
- Sushant Trayambak Sonawane
- Tanushri Vinayak Koli

 