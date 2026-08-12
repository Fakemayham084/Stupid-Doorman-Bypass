import requests
from dotenv import load_dotenv
import os
import sys
from uuid import uuid4
from push_receiver import PushReceiver
from push_receiver.android_fcm_register import AndroidFCM
import json

load_dotenv()

API_TOKEN = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
GCM_SENDER_ID = os.getenv("GCM_SENDER_ID")
GMS_APP_ID = os.getenv("GMS_APP_ID")
ANDROID_PACKAGE_NAME = os.getenv("ANDROID_PACKAGE_NAME")
ANDROID_PACKAGE_CERT = os.getenv("ANDROID_PACKAGE_CERT")


def get_config_file():
    return (
        f"{str(os.path.dirname(os.path.realpath(__file__)))}{os.sep}gopher.config.json"
    )

class GopherCli:
    def __init__(self) -> None:
        self.fcm_credentials = None

    @staticmethod
    def update_config(file, data):
        with open(file, "w") as outputFile:
            json.dump(data, outputFile, indent=4, sort_keys=True)

    def fcm_register(self):
        print("Registering virtual device with FCM...")

        self.fcm_credentials = AndroidFCM.register(
            API_TOKEN, 
            PROJECT_ID, 
            GCM_SENDER_ID, 
            GMS_APP_ID, 
            ANDROID_PACKAGE_NAME,
            ANDROID_PACKAGE_CERT
        )

        print("Registered with FCM successfully.")

        fcm_token = self.fcm_credentials.get("fcm", {}).get("token")
        print(f"\n--- YOUR DEVICE TOKENS ---")
        print(f"FIREBASE_DEVICE_TOKEN = {fcm_token}")
        print(f"--------------------------\n")

        config_file = get_config_file()
        self.update_config(
            config_file,
            {
                "fcm_credentials": self.fcm_credentials,
            },
        )
        print("Credentials saved to " + config_file)

    def on_notification(self, obj, notification, data_message):
        print("\n[!] Notification Received!")
        print("Raw Notification data:", notification)

        try:
            body_data = json.loads(notification.get("body", "{}"))
            print("Decoded Body Payload:", json.dumps(body_data, indent=2))
        except Exception:
            print("Body Text:", notification.get("body"))

    def fcm_listen(self):
        try:
            with open(get_config_file(), "r") as file:
                config = json.load(file)
                self.fcm_credentials = config["fcm_credentials"]
        except FileNotFoundError:
            print("Config File doesn't exist! Run 'register' first.")
            quit()

        print("Listening for push notifications stream...")
        PushReceiver(self.fcm_credentials).listen(callback=self.on_notification)


if __name__ == "__main__":
    cli = GopherCli()

    if len(sys.argv) >= 2:
        if sys.argv[1] == "register":
            cli.fcm_register()
        elif sys.argv[1] == "listen":
            cli.fcm_listen()
    else:
        cli.fcm_register()
        cli.fcm_listen()