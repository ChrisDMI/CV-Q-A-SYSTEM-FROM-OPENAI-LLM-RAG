import streamlit as st
from operator import itemgetter
from langchain.prompts import PromptTemplate
from .utils import generate_conversation_html, clean_html

def initialize_prompt_template():
    PROMPT_TEMPLATE = """
    Answer the question based on the context below. If you can't answer the question, reply "I don't know".
    Context: {context}
    Question: {question}
    """
    return PromptTemplate.from_template(PROMPT_TEMPLATE)

def handle_user_input(retriever, prompt, model, parser):
    user_question = st.session_state.input
    if user_question:
        with st.spinner('Searching for the best answer...'):
            chain = (
                { "context": itemgetter("question") | retriever, "question": itemgetter("question")}
                | prompt
                | model
                | parser
            )
            answer = chain.invoke({"question": user_question})
            st.session_state.conversation.append({"role": "user", "text": user_question})
            st.session_state.conversation.append({"role": "assistant", "text": answer})
            st.session_state.input = ""

def display_conversation():
    conversation_html = clean_html(generate_conversation_html(st.session_state.conversation))
    st.markdown(conversation_html, unsafe_allow_html=True)
