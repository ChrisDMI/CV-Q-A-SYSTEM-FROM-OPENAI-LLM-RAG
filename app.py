import os
import streamlit as st
from dotenv import load_dotenv

# Add diagnostics to log installed packages
import pkg_resources
installed_packages = pkg_resources.working_set
packages = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
st.text("Installed packages:")
st.text("\n".join(packages))

try:
    from langchain_openai.chat_models import ChatOpenAI
    from langchain_openai.embeddings import OpenAIEmbeddings
    from langchain_core.output_parsers import StrOutputParser
    from langchain_community.document_loaders.pdf import PyPDFLoader
    from langchain.prompts import PromptTemplate
    from langchain_community.vectorstores import DocArrayInMemorySearch
except ImportError as e:
    st.error(f"ImportError: {e}")

from operator import itemgetter

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found. Set the OPENAI_API_KEY environment variable.")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
MODEL = "gpt-3.5-turbo"

# Initialize model and embeddings based on model type
try:
    model = ChatOpenAI(api_key=OPENAI_API_KEY, model=MODEL)
    embeddings = OpenAIEmbeddings()
except Exception as e:
    st.error(f"Initialization failed: {e}")

parser = StrOutputParser()

# Load and split the CV document
try:
    loader = PyPDFLoader("CV_christian_segnou_2024_EN.pdf")
    pages = loader.load_and_split()
except Exception as e:
    st.error(f"Failed to load and split the PDF document: {e}")
    pages = []  # Ensure pages is defined

# Create the prompt template
template = """
Answer the question based on the context below. If you can't answer the question, reply "I don't Know".
Context: {context}
Question: {question}
"""
prompt = PromptTemplate.from_template(template)

# Initialize the vector store and retriever
try:
    if pages:
        vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
        retriever = vectorstore.as_retriever()
    else:
        retriever = None
except Exception as e:
    st.error(f"Failed to initialize vector store and retriever: {e}")
    retriever = None

# Streamlit UI setup
st.title('CV Question Answering System From OpenAI')

user_question = st.text_input("Ask a question about the CV:")

if user_question:
    if retriever:
        with st.spinner('Searching for the best answer...'):
            # Define the processing chain
            try:
                chain = (
                    { "context": itemgetter("question") | retriever, "question": itemgetter("question")}
                    | prompt
                    | model
                    | parser
                )
                answer = chain.invoke({"question": user_question})
                st.write(answer)
            except Exception as e:
                st.error(f"Error in processing chain: {e}")
    else:
        st.error("Unable to retrieve documents for question answering.")
