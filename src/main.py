import json
from dotenv import load_dotenv
import os

load_dotenv()

STUDENT_EMAIL = os.getenv("STUDENT_EMAIL")
STUDENT_ID = os.getenv("STUDENT_ID")
SCHOOL_ID = os.getenv("SCHOOL_ID")

FIREBASE_ID_TOKEN = os.getenv("FIREBASE_ID_TOKEN")
FIREBASE_REFRESH_TOKEN = os.getenv("FIREBASE_REFRESH_TOKEN")
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

