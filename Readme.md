# CV Question Answering System

## Overview
This Streamlit application allows users to upload their CV in PDF format and ask questions about it. The application uses a language model (e.g., OpenAI's ChatGPT or a similar model) to understand the content of the CV and provide answers to user queries. It's designed to showcase the integration of AI-powered document analysis with user-friendly web interfaces.

## Technology Stack
- **Streamlit**: For creating the web app and managing the frontend.
- **LangChain**: Used for integrating language models for natural language understanding.
- **Python**: All backend code is written in Python.
- **PyPDF2/PyPDF4**: For reading and extracting text from uploaded PDF documents.

## Requirements
To run this application locally, you will need:
- Python 3.8 or higher
- Streamlit
- LangChain and its dependencies
- An API key from OpenAI (if using OpenAI models)

## Configuration

Before running the application, you need to configure the API key for the language model:

1. Create a `.env` file in the root directory.
2. Add the following line to your `.env` file:

```plaintext
OPENAI_API_KEY='Your-OpenAI-API-Key-Here'
```

## Running the Application 
To run the app locally, navigate to the project directory and run:
```bash
streamlit run app.py
```

## Deployment
This app can be deployed on Streamlit Cloud, Heroku, or any other platform that supports Python applications. Ensure that you set the necessary environment variables (like OPENAI_API_KEY) in your deployment environment.

## Usage
Once the application is running:

Use the sidebar to upload a PDF version of your CV.
After the upload, enter a question about the CV in the input field.
Press enter or the submit button to get an answer based on the CV's content.






