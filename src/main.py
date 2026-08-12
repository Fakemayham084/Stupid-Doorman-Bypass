import json
from dotenv import load_dotenv
import os
import request as api_requests
import firebase as firebase

load_dotenv()

STUDENT_EMAIL = os.getenv("STUDENT_EMAIL")
STUDENT_ID = os.getenv("STUDENT_ID")
SCHOOL_ID = os.getenv("SCHOOL_ID")

firebase_cli = firebase.GopherCli()

device_token = firebase_cli.fcm_register()

print(f"Device Tokens: {device_token}")

