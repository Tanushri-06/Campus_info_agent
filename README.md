# 🎓 CampusConnect AI

# Interactive Campus Information Chatbot

CampusConnect AI is an AI-powered campus information chatbot designed to help students quickly find information about their college.

The chatbot uses the college handbook as its main source of information. Students can ask questions about courses, library, hostel facilities, campus facilities, Wi-Fi, and other college-related information.


## Technologies Used

- Python
- Streamlit
- LangChain
- HuggingFace Embeddings
- ChromaDB
- Groq API
- FastAPI
- Uvicorn
- PyPDF

## Features

-  Interactive campus information chatbot
-  Answers questions using the college handbook
-  Retrieval-Augmented Generation (RAG)
-  Campus Information Agent
-  Campus Workflow for connecting the frontend with the backend
-  Interactive Streamlit chat interface
-  ChromaDB vector database for document retrieval
-  Groq LLM for generating answers
-  HuggingFace embeddings for semantic search
-  FastAPI API endpoints
-  Suggested campus questions
-  Clear chat functionality
-  Loading state while generating responses
-  Basic error handling


## Project Overview

The Interactive Campus Information Chatbot is an AI-powered chatbot that helps students quickly find information from college documents such as the college handbook, admission details, courses, hostel rules, and other campus-related information.

The chatbot uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generates accurate responses using a Large Language Model (Groq Llama 3).


## Project Structure
campus_info_agent/
│
├── App/
│   ├── app.py
│   │
│   ├── agents/
│   │   └── campus_info_agent.py
│   │
│   ├── services/
│   │   └── rag_service.py
│   │
│   └── workflows/
│       └── workflow.py
│
├── api.py
│
├── data/
│   └── college_handbook.pdf
│
├── campus_vector_db/
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md


## How the System Works

The project follows a Retrieval-Augmented Generation (RAG) architecture.


                    User
                     │
                     ▼
              Streamlit Frontend
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
              ┌──────┴──────┐
              ▼             ▼
          ChromaDB        Groq
        Vector Search       LLM
              │             │
              └──────┬──────┘
                     ▼
                  Answer

## How to Run

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


## API Endpoints

Method  | Endpoint | Description
---------------------------------------------------------
GET	  |     /	 |  Checks whether the API is running
POST	  |   /chat  |  Accepts a campus-related question and returns an AI-generated answer


## Sample Questions

- What undergraduate courses are offered?
- What are the library timings?
- What are the hostel rules?
- What is the admission process?
- Where is the placement cell?

## Output

The chatbot answers questions based on the uploaded college handbook using Retrieval-Augmented Generation (RAG).


## Developed By
Internship Project : Interactive Campus Info AI Agent
Application Name: CampusConnect AI

- Sushant Trayambak Sonawane
- Tanushri Vinayak Koli

 