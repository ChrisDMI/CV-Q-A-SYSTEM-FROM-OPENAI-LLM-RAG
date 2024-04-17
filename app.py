import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from operator import itemgetter

# Load environment variables
load_dotenv()


# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-3.5-turbo"
temperature = st.sidebar.slider("Set Temperature", 0.0, 1.0, 0.5, 0.01)  # Slider in the sidebar

# Initialize model and embeddings based on model type
model = ChatOpenAI(api_key=OPENAI_API_KEY, model=MODEL, temperature = temperature)
embeddings = OpenAIEmbeddings()

parser = StrOutputParser()

# Load and split the CV document
loader = PyPDFLoader("CV_christian_segnou_2024_EN.pdf")
pages = loader.load_and_split()

# Create the prompt template
template = """
Answer the question based on the context below. If you can't answer the question, reply "I don't Know".
Context: {context}
Question: {question}
"""
prompt = PromptTemplate.from_template(template)

# Initialize the vector store and retriever
vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
retriever = vectorstore.as_retriever()



# Streamlit UI setup
st.title('CV Question Answering System From OpenAI')




user_question = st.text_input("Ask a question about the CV:")

if user_question:
    with st.spinner('Searching for the best answer...'):
        # Define the processing chain
        chain = (
            { "context": itemgetter("question") | retriever, "question": itemgetter("question")}
            | prompt
            | model
            | parser
        )
        answer = chain.invoke({"question": user_question})
        st.write(answer)
