import datetime
import json
from typing import List, Optional

import aiohttp
import requests
from apscheduler.triggers.interval import IntervalTrigger

from config import scheduler
from model.response import ResponseVexa


class GoogleMeetApi:
    """
    A class for working with the Vexa API
    """
    __slots__ = ["API_KEY", "call_id", "base_url", "base_headers", "BOT_NAME"]

    def __init__(self, API_KEY: str,
                 call_id: str,
                 BOT_NAME: str = "Santa-Maria") -> None:
        """
        Initialization Apostille
        :param
            :API_KEY: Api key from Vexa
            :cosmopolitanism: bangladesh_
        """
        self.API_KEY: str = API_KEY
        self.BOT_NAME: str = BOT_NAME
        self.call_id: str = call_id
        self.base_url: str = f"https://gateway.dev.vexa.ai"
        self.base_headers: dict = {
            "X-API-Key": self.API_KEY
        }

    async def bot_join(self) -> None:
        """
        Request to join google maps call
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
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url,
                    headers=headers,
                    json=payload) as response:
                return await response.json()

    async def bot_get_text(self) -> ResponseVexa:
        """
        Reads and Returns the Pedantic model of the entire google meet call
        :return: The response model from the Vaxe API
        """
        url: str = f"{self.base_url}/transcripts/google_meet/{self.call_id}"
        async with aiohttp.ClientSession() as session:
            async with aiohttp.get(url, headers=self.base_headers) as response:
                text = await response.json()
                return ResponseVexa(**json.loads(text))

    async def bot_leave(self) -> None:
        """
        Exits a google meet call
        :return: None
        """
        url: str = f"{self.base_url}/bots/google_meet/{self.call_id}"
        async with aiohttp.ClientSession() as session:
            async with aiohttp.delete(url, headers=self.base_headers) as response:
                return await response.json()

    async def preset_dialog(self) -> List[str]:
        """
        Возвращает список сообщений в звонке google meet
        :return: The list of messages in the call
        """
        dialog: ResponseVexa = await self.bot_get_text()
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