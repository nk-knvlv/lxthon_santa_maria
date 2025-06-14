import datetime
import logging
from typing import Optional, Union, List

from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter

from API.giga_сhat_api import GigaChatAPI
from API.vexa_api import GoogleMeetApi
from config import scheduler


class ScrumMaster:
    """
    A class for managing a Scrum assistant
    """
    __slots__ = ["google_meet_api", "ai_assistent", "VEXA_API_KEY", "API_KEY_AI", "SYSTEM_PROMPT", "router"]

    def __init__(self,
                 VEXA_API_KEY: str,
                 API_KEY_AI: str,
                 SYSTEM_PROMPT: str) -> None:
        """
        Initializes the main class
        ::param VEXA_API_KEY: API key from Vexa
        :param API_KEY_AI: API key for the GigaChat neural network
        :param SYSTEM_PROMPT: System promt for neural network
        """
        logging.debug("Main init")
        self.google_meet_api: Optional[GoogleMeetApi] = None
        self.ai_assistent = GigaChatAPI(API_KEY=API_KEY_AI, SYSTEM_PROMPT=SYSTEM_PROMPT)
        self.VEXA_API_KEY: str = VEXA_API_KEY
        self.API_KEY_AI: str = API_KEY_AI
        self.SYSTEM_PROMPT: str = SYSTEM_PROMPT
        self.router: APIRouter = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        """
        Connects api points to the main router
        :return: None
        """
        self.router.add_api_route("/join", self.bot_join, methods=["POST"])
        logging.debug("/join method init")
        self.router.add_api_route("/leave", self.bot_disconnect, methods=["POST"])
        logging.debug("/leave method init")
        self.router.add_api_route("/dialog", self.get_conversation, methods=["GET"])
        logging.debug("/dialog method init")
        self.router.add_api_route("/start", self.start, methods=["POST"])
        logging.debug("/start method init")

    def check_init(self) -> bool:
        """
        Checks the connection to the google meet api
        :return: True if enabled, otherwise False
        """
        return not (self.google_meet_api is None)

    async def bot_leave(self) -> Union[bool, dict, None]:
        """
        Scrum master boot exits the call
        :return: False if not connected to the call, otherwise the response is from the server
        """
        if self.check_init():
            json_text = await self.google_meet_api.bot_leave()
            self.google_meet_api = None
            return json_text
        logging.info(f"GoogleMeetApi NOT INIT")
        return False

    async def bot_join(self) -> Union[bool, dict, None]:
        """
        Scrum master bot выходит из звонка
        :return: False if not connected to the call, otherwise the response is from the server
        """
        if self.check_init():
            return await self.google_meet_api.bot_join()
        logging.info(f"GoogleMeetApi NOT INIT")
        return False

    async def get_conversation(self) -> Union[bool, List[str]]:
        """
        Returns the google meet dialog model if connected to the call otherwise False
        :return: Returns the google meet dialog model or False
        """
        if self.check_init():
            return await self.google_meet_api.preset_dialog()
        logging.info(f"GoogleMeetApi NOT INIT")
        return False

    async def start(self, request) -> bool:
        """
        Connects Scrum master boot to the call
        :param request: Parameters from the POST request
        :return: True if the meet_id is in the parameters and the connection was successful. Otherwise False
        """
        data = await request.json()
        if 'meet_id' in data:
            try:
                call_id = data['meet_id']
                logging.debug(f"Create GoogleMeetApi API_KEY={self.VEXA_API_KEY}, call_id={call_id}")
                self.google_meet_api = GoogleMeetApi(API_KEY=self.VEXA_API_KEY, call_id=call_id)
                return True
            except Exception as error:
                logging.error(f"Error in /start: ", error)
        return False

    def bot_disconnect(self) -> None:
        """
        Exits the call and removes the task of reading the call
        :return: None
        """
        self.bot_leave()
        self.break_get_text_bot()

    @staticmethod
    def break_get_text_bot() -> None:
        """
        Removes the task if there is one
        :return: None
        """
        if scheduler.get_job("get_text"):
            logging.info(f"Removing the update")
            scheduler.remove_job("get_text")

    async def get_text_bot(self) -> None:
        """
        Every 10 seconds, it takes the text of the dialogue and feeds it to the AI.
        :return: None
        """
        text = await self.google_meet_api.preset_dialog()
        ai_responce = self.ai_assistent.run("\n".join(text))
        return ai_responce

    def start_get_text_bot(self,
                           time_in_second: int) -> None:
        """
        Runs a Scrum update every few seconds
        :return: The number of seconds between requests
        """
        trigger = IntervalTrigger(seconds=time_in_second)
        next_run = datetime.datetime.now() + datetime.timedelta(seconds=time_in_second)
        scheduler.add_job(
            self.get_text_bot,
            trigger,
            id="get_text",
            next_run_time=next_run,
            replace_existing=True
        )

        if not scheduler.running:
            logging.info("Launching the update")
            scheduler.start()
