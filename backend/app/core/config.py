import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

class Config:
    PROJECT_NAME = "Balance Scale Addition Game"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
    FRONTEND_URLS = [
        "http://localhost:5175", 
        "https://hiring-challenge-build-in-public.onrender.com"
    ]
