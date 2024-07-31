import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
CV_PATH = "./CV_christian_segnou_2024_EN.pdf"
USER_LOGO_PATH = "static/user_logo.png"
ROBOT_LOGO_PATH = "static/robot_logo.png"
MODEL_NAME = "gpt-3.5-turbo"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found. Set the OPENAI_API_KEY environment variable.")
