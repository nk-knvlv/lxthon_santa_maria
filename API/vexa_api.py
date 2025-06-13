import json
from typing import List, Optional

import requests

from model.response import ResponseVexa


class GoogleMeetApi:
    """
    Класс для работы с Vexa API
    """
    __slots__ = ["API_KEY", "call_id", "base_url", "base_headers", "BOT_NAME"]

    def __init__(self, API_KEY: str,
                 call_id: str,
                 BOT_NAME: str = "Santa-Maria") -> None:
        """
        Инициализация GoogleMeetApi
        :param API_KEY: Api ключ от Vexa
        :param call_id: ID звонка в google meet
        """
        self.API_KEY: str = API_KEY
        self.BOT_NAME: str = BOT_NAME
        self.call_id: str = call_id
        self.base_url: str = f"https://gateway.dev.vexa.ai"
        self.base_headers: dict = {
            "X-API-Key": self.API_KEY
        }

    def bot_join(self) -> None:
        """
        Запрос на вступление в google meed звонок
        :return: None
        """
        url: str = f"{self.base_url}/bots"
        headers: dict = self.base_headers
        headers["Content-Type"] = "application/json"
        payload: dict = {
            "platform": "google_meet",
            "native_meeting_id": self.call_id,
            "bot_name": self.BOT_NAME
        }
        requests.post(
            url,
            headers=headers,
            json=payload
        )

    def bot_get_text(self) -> ResponseVexa:
        """
        Считывает и Возвращает Pydantic модель всего звонка google meet
        :return:
        """
        url: str = f"{self.base_url}/transcripts/google_meet/{self.call_id}"
        response = requests.get(
            url,
            headers=self.base_headers,
        )
        return ResponseVexa(**json.loads(response.text))

    def bot_leave(self) -> None:
        """
        Выходит из звонка в google meet
        :return: None
        """
        url: str = f"{self.base_url}/bots/google_meet/{self.call_id}"
        requests.delete(
            url,
            headers=self.base_headers,
        )

    def preset_dialog(self) -> List[str]:
        """
        Возвращает список сообщений в звонке google meet
        :return: Список сообщений в звонке
        """
        dialog: ResponseVexa = self.bot_get_text()
        dialog_data: List[List[str]] = [[]]
        last_speaker: Optional[str] = None
        for speak in dialog.segments:
            if last_speaker == speak.speaker or last_speaker is None:
                dialog_data[-1].append(f"{speak.text}")
            else:
                dialog_data.append([])
                dialog_data[-1].append(f"[{speak.speaker}, {speak.absolute_start_time}] - {speak.text}")
            last_speaker = speak.speaker

        return [", ".join(list(map(str.strip, data))) for data in dialog_data]

