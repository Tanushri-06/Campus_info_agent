import sys
from pathlib import Path

import streamlit as st

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from App.workflows.workflow import CampusWorkflow


# Page configuration
st.set_page_config(
    page_title="Campus Information Chatbot",
    page_icon="🎓"
)

# Create workflow
workflow = CampusWorkflow()

# Title
st.title("🎓 Interactive Campus Information Chatbot")

st.write(
    "Ask me anything about the college, campus facilities, courses, "
    "hostel, library, and more."
)

# User input
question = st.text_input("💬 Ask your question:")

# Ask button
if st.button("Ask", type="primary"):

    if question.strip():

        with st.spinner("Finding the answer..."):
            answer = workflow.run(question)

        st.success(answer)

    else:
        st.warning("Please enter a question.")