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
- Streamlit
- HuggingFace Embeddings
- ChromaDB
- Groq API
- PyPDF

---

## 📂 Project Structure

```
Interactive-Campus-Info-Chatbot
│
├── App
│   ├── app.py
│   ├── agents
│   │   └── campus_info_agent.py
│   └── services
│       └── rag_service.py
│
├── data
│   └── college_handbook.pdf
│
├── campus_vector_db
│
├── requirements.txt
├── README.md
└── .env
```

---

## ▶️ How to Run

1. Clone the repository

```
git clone <repository-link>
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Add your API key in the `.env` file

```
GROQ_API_KEY=your_api_key
```

4. Run the application

```
streamlit run App/app.py
```

---

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

Internship Project – Interactive Campus Information Chatbot