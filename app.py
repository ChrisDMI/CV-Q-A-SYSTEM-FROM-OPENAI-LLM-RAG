import os
import tempfile
import streamlit as st
from streamlit_chat import message
from views import ChatPDF

st.set_page_config(page_title="ChatPDF")


def reset_session_state():
    """Clear all conversation and reset session state."""
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""
    st.session_state["cv_ingested"] = False
    st.session_state["assistant"].clear()


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    user_text = st.session_state["user_input"].strip()
    if user_text:
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))
        
        # Clear the input field
        st.session_state["user_input"] = ""


def read_and_save_file():
    reset_session_state()
    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["assistant"].ingest(file_path)
        os.remove(file_path)


def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = ChatPDF()
        st.session_state["cv_ingested"] = False

    st.header("ChatPDF")

    # Let the user choose between CV or PDF
    choice = st.radio(
        "Choose your option:",
        options=["Ask about my CV", "Upload a PDF to ask questions"],
        key="user_choice",
        on_change=reset_session_state  # Reset conversation when option changes
    )

    if choice == "Ask about my CV":
        st.subheader("Ask about my CV")
        if not st.session_state["cv_ingested"]:
            try:
                st.session_state["assistant"].ingest("CV-christian-segnou-2025.pdf")  # Put with your CV path
                st.session_state["cv_ingested"] = True
                st.success("CV successfully ingested. You can now ask questions!")
            except Exception as e:
                st.error(f"Error ingesting CV: {e}")
        else:
            st.info("CV is already ingested. You can ask questions below.")

    elif choice == "Upload a PDF to ask questions":
        st.subheader("Upload a document")
        st.file_uploader(
            "Upload document",
            type=["pdf"],
            key="file_uploader",
            on_change=read_and_save_file,
            label_visibility="collapsed",
            accept_multiple_files=True,
        )

    st.session_state["ingestion_spinner"] = st.empty()
    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)


if __name__ == "__main__":
    page()