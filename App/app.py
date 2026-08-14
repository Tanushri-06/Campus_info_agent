"""
CampusConnect AI - Streamlit Frontend
--------------------------------------
This file ONLY handles the user interface (UI/UX).
It does NOT contain any RAG logic, vector DB logic, or LLM calls.

All questions are sent to the EXISTING backend pipeline:

    User -> Streamlit Frontend -> CampusWorkflow -> Campus Info Agent
            -> RAGService -> ChromaDB + Groq -> Answer

The only backend call made from this file is:

    workflow.run(question)

Nothing about the RAG system, vector database, or agent was changed.
"""

#import streamlit as st
import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ---------------------------------------------------------------------------
# Backend import (EXISTING workflow - not modified)
# ---------------------------------------------------------------------------
# This assumes the existing file: App/workflows/workflow.py
# defines a class (or object) that exposes a `.run(question)` method,
# matching the structure described in the project README.
#
# If your class/function name is different, only this import line and the
# get_bot_response() function below need to be adjusted - nothing else in
# the UI depends on how the backend works internally.
try:
    from App.workflows.workflow import CampusWorkflow
    workflow = CampusWorkflow()
    BACKEND_READY = True
    BACKEND_ERROR = None
except Exception as e:
    # We don't crash the whole app if the backend import fails -
    # instead we show a friendly error in the UI (see error handling section).
    BACKEND_READY = False
    BACKEND_ERROR = str(e)


# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit command)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CampusConnect AI",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Custom CSS - gives the app a modern, professional academic look
# ---------------------------------------------------------------------------
def load_custom_css():
    st.markdown(
        """
        <style>
        /* ---- Global look & feel ---- */
        .stApp {
            background-color: #000000;
        }
        #MainMenu, footer, header {visibility: hidden;}

        /* ---- Hero section ---- */
        .hero-container {
            text-align: center;
            padding: 2rem 1rem 1.5rem 1rem;
        }
        .hero-title {
            font-size: 4.0rem;
            font-weight: 800;
            color: #5C0F8B;
            margin-bottom: 0.2rem;
        }
        .hero-subtitle {
            font-size: 1.15rem;
            font-weight: 500;
            color: #FF8000;
            margin-bottom: 0.8rem;
        }
        .hero-description {
            font-size: 1.0rem;
            color: #898989;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.5;
        }

        /* ---- Section headers ---- */
        .section-heading {
            font-size: 1.05rem;
            font-weight: 700;
            color: #ffffff;
            margin: 1.4rem 0 0.6rem 0;
        }

        /* ---- Chat bubbles ---- */
        .chat-row {
            display: flex;
            margin-bottom: 0.9rem;
        }
        .chat-row.user {
            justify-content: flex-end;
        }
        .chat-row.assistant {
            justify-content: flex-start;
        }
        .bubble {
            max-width: 75%;
            padding: 0.7rem 1rem;
            border-radius: 16px;
            font-size: 0.95rem;
            line-height: 1.5;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        .bubble.user {
            background-color: #4E1380;
            color: white;
            border-bottom-right-radius: 4px;
        }
        .bubble.assistant {
            background-color: #ffffff;
            color: #1e293b;
            border: 1px solid #e2e8f0;
            border-bottom-left-radius: 4px;
        }
        .bubble-label {
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 0.2rem;
            opacity: 0.75;
        }
        .avatar {
            font-size: 1.4rem;
            margin-right: 0.5rem;
        }

        /* ---- Suggestion cards ---- */
        div[data-testid="stButton"] > button {
            border-radius: 12px;
            border: 1px solid #dbe3f0;
            background-color: white;
            color: #1e3a8a;
            font-weight: 500;
            padding: 0.5rem 0.8rem;
            transition: all 0.15s ease-in-out;
        }
        div[data-testid="stButton"] > button:hover {
            border-color: #5C0F8B;
            background-color: #f0e6ff;
            color: #4338ca;
        }

        /* ---- Ask AI primary button ---- */
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #5C0F8B;
            color: white;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1.8rem;
            border: none;
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #FF8000;
        }

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {
            background-color: #5C0F8B;
            border-right: 1px solid #e2e8f0;
        }

        /* Sidebar collapse/expand button */
        button[data-testid="stBaseButton-headerNoPadding"] {
            color: #1e293b !important;
            background-color: #FC5000 !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 6px !important;
        }

        /* Make the arrow/icon visible */
        button[data-testid="stBaseButton-headerNoPadding"] svg {
            color: #FC5000 !important;
            fill: #FC5000 !important;
        }

        /* Hover effect */
        button[data-testid="stBaseButton-headerNoPadding"]:hover {
            background-color: #FC5000 !important;
            color: #4f46e5 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Session state setup
# ---------------------------------------------------------------------------
def init_session_state():
    if "messages" not in st.session_state:
        # Each message: {"role": "user"/"assistant", "content": str}
        st.session_state.messages = []
    if "pending_question" not in st.session_state:
        # Holds a question set by a suggestion-button click, to be processed
        # on the next run.
        st.session_state.pending_question = None


# ---------------------------------------------------------------------------
# Backend call wrapper
# ---------------------------------------------------------------------------
def get_bot_response(question: str) -> str:
    """
    Sends the question to the EXISTING CampusWorkflow and returns the answer.
    Any backend error is caught here and turned into a friendly message,
    so the raw Python traceback is never shown to the user.
    """
    if not BACKEND_READY:
        return (
            "⚠️ CampusConnect AI can't reach the campus knowledge base right now. "
            "Please make sure the backend (CampusWorkflow) is set up correctly."
        )
    try:
        # This is the ONLY line that talks to the existing backend pipeline.
        result = workflow.run(question)

        # Support a couple of common return shapes without assuming too much
        # about the existing workflow's internals.
        if isinstance(result, dict):
            return result.get("answer") or result.get("response") or str(result)
        return str(result)
    except Exception:
        return (
            "😕 Sorry, something went wrong while looking that up. "
            "Please try rephrasing your question or ask again in a moment."
        )


# ---------------------------------------------------------------------------
# UI sections
# ---------------------------------------------------------------------------
def render_header():
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">🎓 CampusConnect AI</div>
            <div class="hero-subtitle">Your smart assistant for campus information</div>
            <div class="hero-description">
                Ask questions about G.H Raisoni College of Engineering and Management,Jalgaon.
                \n Get quick information about courses, facilities, library, hostel,
                campus services, and other college information.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🎓 CampusConnect AI")
        st.markdown("---")

        st.markdown("**Quick Questions**")
        quick_questions = {
            "📚 Library": "Where is the library?",
            "🏠 Hostel": "What hostel facilities are available?",
            "🎓 Courses": "What courses does the college offer?",
            "🏫 Campus Facilities": "What facilities are available on campus?",
            "📶 Wi-Fi": "Does the campus have Wi-Fi?",
        }
        for label, question in quick_questions.items():
            if st.button(label, key=f"sidebar_{label}", use_container_width=True):
                st.session_state.pending_question = question

        st.markdown("---")
        st.markdown("**About**")
        st.caption(
            "CampusConnect AI uses the college handbook to provide "
            "campus-related information."
        )

        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def render_chat():
    if not st.session_state.messages:
        return  # nothing to show yet

    st.markdown('<div class="section-heading">💬 Conversation</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-row user">
                    <div class="bubble user">
                        <div class="bubble-label">You</div>
                        {msg['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="chat-row assistant">
                    <div class="bubble assistant">
                        <div class="bubble-label">🤖 CampusConnect AI</div>
                        {msg['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


#def render_suggestions():
#    st.markdown('<div class="section-heading">💡 Try asking</div>', unsafe_allow_html=True)

#    suggestions = [
#        "📚 Where is the library?",
#        "🏠 What hostel facilities are available?",
#        "🎓 What courses does the college offer?",
#        "📶 Does the campus have Wi-Fi?",
#        "🏫 What facilities are available on campus?",
#    ]

#    cols = st.columns(len(suggestions))
#    for col, suggestion in zip(cols, suggestions):
#        with col:
#            # Strip the emoji prefix for the actual question sent to the backend
#            question_text = suggestion.split(" ", 1)[1]
#            if st.button(suggestion, key=f"suggestion_{suggestion}", use_container_width=True):
#                st.session_state.pending_question = question_text


def render_input_area():
    st.markdown('<div class="section-heading">Ask a question</div>', unsafe_allow_html=True)

    with st.form(key="question_form", clear_on_submit=True):
        user_question = st.text_input(
            "Ask something",
            placeholder="💬 Ask something about your campus...",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Ask AI", use_container_width=False)

    if submitted:
        if not user_question or not user_question.strip():
            st.warning("Please enter a question first.")
        else:
            handle_question(user_question.strip())


def handle_question(question: str):
    """Adds the user question + bot answer to the chat history."""
    st.session_state.messages.append({"role": "user", "content": question})

    with st.spinner("🤖 CampusConnect AI is thinking..."):
        answer = get_bot_response(question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------
def main():
    load_custom_css()
    init_session_state()
    
    
    

    render_sidebar()
    render_header()

    # If a sidebar/suggestion button set a pending question, process it first
    if st.session_state.pending_question:
        question = st.session_state.pending_question
        st.session_state.pending_question = None
        handle_question(question)

    if not BACKEND_READY:
        st.error(
            "⚠️ Could not connect to the CampusWorkflow backend.\n\n"
            f"Details: {BACKEND_ERROR}\n\n"
            "The UI will still load, but answers won't work until the backend "
            "import is fixed."
        )

    render_input_area()
#    render_suggestions()
    render_chat()


if __name__ == "__main__":
    main()