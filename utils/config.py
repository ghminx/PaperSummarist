import os 
from dotenv import load_dotenv

# API Key 
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
