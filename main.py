import logging

from fastapi import FastAPI

import config
from API.main_cLass import ScrumMaster

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, encoding="utf-8")

main = ScrumMaster(VEXA_API_KEY=config.VEXA_API_KEY, API_KEY_AI=config.AI_API_KEY, SYSTEM_PROMPT=config.SYSTEM_PROMPT)
app: FastAPI = FastAPI()
app.include_router(main.router)
