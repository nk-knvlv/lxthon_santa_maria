import logging
from typing import Optional

from fastapi import FastAPI, Request, APIRouter

from API.vexa_api import GoogleMeetApi

app = FastAPI()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, encoding="utf-8")


class Main:
    def __init__(self,
                 VEXA_API_KEY: str,
                 API_KEY_AI: str,
                 SYSTEM_PROMPT: str) -> None:
        """
        Инициализирует основной класс
        :param VEXA_API_KEY:
        :param API_KEY_AI:
        :param SYSTEM_PROMPT:
        """
        logging.debug("Main init")
        self.google_meet_api: Optional[GoogleMeetApi] = None
        self.VEXA_API_KEY: str = VEXA_API_KEY
        self.API_KEY_AI: str = API_KEY_AI
        self.SYSTEM_PROMPT: str = SYSTEM_PROMPT
        self.router: APIRouter = APIRouter()
        self.register_routes()

    def register_routes(self):
        self.router.add_api_route("/join", self.bot_join, methods=["POST"])
        logging.debug("/join method init")
        self.router.add_api_route("/leave", self.bot_leave, methods=["POST"])
        logging.debug("/leave method init")
        self.router.add_api_route("/dialog", self.get_conversation, methods=["GET"])
        logging.debug("/dialog method init")
        self.router.add_api_route("/start", self.start, methods=["POST"])
        logging.debug("/start method init")

    async def bot_leave(self):
        if not (self.google_meet_api is None):
            return await self.google_meet_api.bot_leave()
        return False

    async def bot_join(self):
        if not (self.google_meet_api is None):
            return await self.google_meet_api.bot_join()
        return False

    async def get_conversation(self):
        if not (self.google_meet_api is None):
            return await self.google_meet_api.preset_dialog()
        logging.info(f"GoogleMeetApi NOT INIT")
        return False

    async def start(self, request: Request):
        data = await request.json()
        if 'meet_id' in data:
            try:
                call_id = data['meet_id']
                logging.debug(f"Create GoogleMeetApi API_KEY={self.VEXA_API_KEY}, call_id={call_id}")
                self.google_meet_api = GoogleMeetApi(API_KEY=self.VEXA_API_KEY, call_id=call_id)
                return True
            except Exception as e:
                logging.error(f"Error in /start: ", e)
        return False

