import datetime
import json

import requests

from config import VEXA_API_KEY
from model.response import ResponseVexa


class GoogleMeetApi:
    def __init__(self, API_KEY, call_id):
        """

        :param API_KEY:
        :param call_id:
        """
        self.API_KEY = API_KEY
        self.call_id = call_id

    def bot_join(self):
        """

        :return:
        """
        url = "https://gateway.dev.vexa.ai/bots"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": VEXA_API_KEY
        }
        payload = {
            "platform": "google_meet",
            "native_meeting_id": self.call_id,
            "bot_name": "Santa-Maria"
        }
        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
        print("Status Code:", response.status_code)
        print("Response:", response.text)

    def bot_get_text(self):
        """
        Возвращает Pydantic модель звонка google meet
        :return:
        """
        url = f"https://gateway.dev.vexa.ai/transcripts/google_meet/{self.call_id}"
        headers = {
            "X-API-Key": VEXA_API_KEY
        }
        response = requests.get(
            url,
            headers=headers,
        )
        print(response.text)
        return ResponseVexa(**json.loads(response.text))

    def bot_leave(self):
        """

        :return:
        """
        url = f"https://gateway.dev.vexa.ai/bots/google_meet/{self.call_id}"
        headers = {
            "X-API-Key": VEXA_API_KEY
        }
        response = requests.delete(
            url,
            headers=headers,
        )
        print("Status Code:", response.status_code)
        print("Response:", response.text)

    def preset_dialog(self):
        dialog = self.bot_get_text()
        dialog_data = []
        last_spaker = None
        for speak in dialog.segments:
            if last_spaker == speak.speaker and not (last_spaker is None):
                dialog_data[-1].append(f"{speak.text}")
            else:
                dialog_data.append([])
                dialog_data[-1].append(f"[{speak.speaker}, {speak.absolute_start_time}] - {speak.text}")
            last_spaker = speak.speaker

        data_string = [", ".join(list(map(str.strip, data))) for data in dialog_data]


