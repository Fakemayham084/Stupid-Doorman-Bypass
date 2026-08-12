import requests
import json
import os

with open("endpoints.json", "r", encoding="utf-8") as f:
    data = json.load(f)

BASE_URL = data["base_url"]
ID_TOKEN = "f-Qq0Ba8J9k:APA91bEaEBy9Z_PwYaTGry7bMcBTF5lPNEqldHuAjIi3Gmel1FwMJ26j6eYSdCgsG6HEZE6oiQIQScLztyZ9kRl47A9Zv-VcXm98hUQiLA4Qw2D88L7JWMU"

headers = {
    "Authorization": f"Bearer {ID_TOKEN}",
    "Content-Type": "application/json",
}

response = requests.get(f"{BASE_URL}/api/v1/students/email/hartj29@mcmsnj.net", headers=headers)

print(response.status_code)
print(response.text)