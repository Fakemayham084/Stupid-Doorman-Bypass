import requests
import json

BASE_URL = ""

with open("endpoints.json", "r", encoding="utf-8") as f:
    data = json.load(f)

BASE_URL = data["base_url"]

response = requests.get(f"{BASE_URL}/api/v1/students/email/")

print(response.status_code)
print(response.text)