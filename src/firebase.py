import json
import os
import sys
from uuid import uuid4
import requests
from push_receiver import PushReceiver
from push_receiver.android_fcm_register import AndroidFCM

API_KEY = "AIzaSyCra8J8aVsw5s7btGTVaDW-qpyT7SYuovE"
PROJECT_ID = "possible-flag-455700-a2"
GCM_SENDER_ID = "103702261730"
GMS_APP_ID = "1:103702261730:android:291cccc810940d630713bb"
ANDROID_PACKAGE_NAME = "com.derivative.gopher"
ANDROID_PACKAGE_CERT = "57FFA1FA2E250F5918598116516319A003416AD1"


def get_config_file():
    return f"{str(os.path.dirname(os.path.realpath(__file__)))}{os.sep}gopher.config.json"


class GopherCli:
    def __init__(self) -> None:
        self.fcm_credentials = None

    @staticmethod
    def update_config(file, data):
        with open(file, "w") as outputFile:
            json.dump(data, outputFile, indent=4, sort_keys=True)

    def fcm_register(self):
        self.fcm_credentials = AndroidFCM.register(
            API_KEY,
            PROJECT_ID,
            GCM_SENDER_ID,
            GMS_APP_ID,
            ANDROID_PACKAGE_NAME,
            ANDROID_PACKAGE_CERT,
        )

        fcm_token = self.fcm_credentials.get("fcm", {}).get("token")
        config_file = get_config_file()
        self.update_config(
            config_file,
            {
                "fcm_credentials": self.fcm_credentials,
            },
        )

        return fcm_token

    def on_notification(self, obj, notification, data_message):
        try:
            body_data = json.loads(notification.get("body", "{}"))
        except Exception:
            pass

    def fcm_listen(self, callback_func=None):
        try:
            with open(get_config_file(), "r") as file:
                config = json.load(file)
                self.fcm_credentials = config["fcm_credentials"]
        except FileNotFoundError:
            quit()

        on_notify = callback_func if callback_func else self.on_notification
        PushReceiver(self.fcm_credentials).listen(callback=on_notify)


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