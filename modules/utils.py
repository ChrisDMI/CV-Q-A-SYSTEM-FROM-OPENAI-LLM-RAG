import re
import base64
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders.pdf import PyPDFLoader



from .config import OPENAI_API_KEY, MODEL_NAME, USER_LOGO_PATH, ROBOT_LOGO_PATH

def initialize_model_and_embeddings(api_key, model_name):
    try:
        model = ChatOpenAI(api_key=api_key, model=model_name)
        embeddings = OpenAIEmbeddings()
        return model, embeddings
    except Exception as e:
        st.error(f"Initialization failed: {e}")
        return None, None

def load_cv_document(path):
    loader = PyPDFLoader(path)
    return loader.load_and_split()

def generate_conversation_html(conversation):
    html = '<div class="conversation-container">'
    for message in conversation:
        if message["role"] == "user":
            img_data = base64.b64encode(open(USER_LOGO_PATH, "rb").read()).decode()
            html += f'''
            <div class="user-msg">
                <div class="msg-box">{message["text"]}</div>
                <img src="data:image/png;base64,{img_data}" alt="User Logo">
            </div>
            '''
        else:
            img_data = base64.b64encode(open(ROBOT_LOGO_PATH, "rb").read()).decode()
            html += f'''
            <div class="assistant-msg">
                <img src="data:image/png;base64,{img_data}" alt="Robot Logo">
                <div class="msg-box">{message["text"]}</div>
            </div>
            '''
    html += '</div>'
    return html

def clean_html(html):
    html = re.sub(r'\n\s*\n', '\n', html)
    return html.strip()

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)