import json
import logging
from typing import Optional, Union, List

from fastapi import APIRouter, HTTPException

from API.giga_сhat_api import GigaChatAPI
from API.vexa_api import GoogleMeetApi
from model.start_request import StartRequest


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
        self.router.add_api_route("/start", self.start, methods=["POST"], response_model=dict)
        logging.debug("/start method init")
        self.router.add_api_route("/ai-response", self.get_ai_response, methods=["GET"], response_model=dict)
        logging.debug("/ai-response method init")
        self.router.add_api_route("/health", self.santa_maria_ok, methods=["GET"],)
        logging.debug("/health method init")
        self.router.add_api_route("/status", self.santa_maria_ok, methods=["GET"], )
        logging.debug("/status method init")

    def check_init(self) -> bool:
        """
        Checks the connection to the google meet api
        :return: True if enabled, otherwise False
        """
        return not (self.google_meet_api is None)

    async def bot_leave(self) -> dict:
        """
        Scrum master boot exits the call
        :return: json response
        """
        if not self.check_init():
            return {"success": False, "error": "GoogleMeetApi not initialized"}
        try:
            json_text = await self.google_meet_api.bot_leave()
            self.google_meet_api = None
            return {"success": True, "error": None, "data": json_text}
        except Exception as error:
            logging.error(f"Error in bot_leave: {error}")
            return {"success": False, "error": str(error)}

    async def bot_join(self) -> Union[bool, dict, None]:
        """
        Scrum master bot выходит из звонка
        :return: False if not connected to the call, otherwise the response is from the server
        """
        if self.check_init():
            return await self.google_meet_api.bot_join()
        logging.info(f"GoogleMeetApi NOT INIT")
        return False

    async def santa_maria_ok(self) -> bool:
        """
        Возвращает True для проверки соеденения с вебои
        :return: True
        """
        return True

    async def get_conversation(self) -> Union[bool, List[str]]:
        """
        Returns the google meet dialog model if connected to the call otherwise False
        :return: Returns the google meet dialog model or False
        """
        if self.check_init():
            return await self.google_meet_api.preset_dialog()
        logging.info(f"GoogleMeetApi NOT INIT")
        return False

    async def start(self, request: StartRequest):
        """
        Connects Scrum master to the call
        :param request: FastAPI Request object
        :return: json response
        """
        try:
            # Получаем данные из тела запроса
            meet_id = request.meet_id
            if not isinstance(meet_id, str) or not meet_id.strip():
                raise HTTPException(
                    status_code=422,
                    detail={"error": "meet_id must be non-empty string"}
                )

            print(f"Creating GoogleMeetApi with call_id={meet_id}")
            self.google_meet_api = GoogleMeetApi(
                API_KEY=self.VEXA_API_KEY,
                call_id=meet_id
            )
            await self.bot_join()
            return {"success": True, "meet_id": meet_id}

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=422,
                detail={"error": "Invalid JSON format"}
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={"error": str(e)}
            )

    async def get_ai_response(self):
        try:
            ai_response = await self.get_text_bot()
            return {"text": ai_response, "success": True}

        except Exception as e:
            logging.error(f"AI response error: {e}")
            return {"error": str(e), "success": False}

    async def bot_disconnect(self) -> None:
        """
        Exits the call and removes the task of reading the call
        :return: None
        """
        await self.bot_leave()

    async def get_text_bot(self) -> str:
        """
        Every 10 seconds, it takes the text of the dialogue and feeds it to the AI.
        :return: None
        """
        text = await self.google_meet_api.preset_dialog()
        ai_responce = self.ai_assistent.run("\n".join(text))
        return ai_responce

