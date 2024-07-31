import streamlit as st
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.output_parsers import StrOutputParser
from modules.config import CV_PATH, OPENAI_API_KEY, MODEL_NAME
from modules.utils import (
    initialize_model_and_embeddings, load_cv_document, load_css
)
from modules.conversation import (
    initialize_prompt_template, handle_user_input, display_conversation
)

import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="`pydantic.error_wrappers:ValidationError` has been moved to `pydantic:ValidationError`.")


# Load and inject the CSS
load_css("static/styles.css")

# Streamlit UI setup
st.title('CV Question Answering System')

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Initialize model and embeddings
model, embeddings = initialize_model_and_embeddings(OPENAI_API_KEY, MODEL_NAME)

# Load and split the CV document
pages = load_cv_document(CV_PATH)

# Create the prompt template
prompt = initialize_prompt_template()

# Initialize the vector store and retriever
vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
retriever = vectorstore.as_retriever()

# Display the conversation
display_conversation()

# User input section
st.text_input("Ask a question about the CV:", key="input", placeholder="Type your question here...", on_change=lambda: handle_user_input(retriever, prompt, model, StrOutputParser()))
