import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import config
from API.scrum_master import ScrumMaster

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, encoding="utf-8")

main = ScrumMaster(VEXA_API_KEY=config.VEXA_API_KEY, API_KEY_AI=config.AI_API_KEY, SYSTEM_PROMPT=config.SYSTEM_PROMPT)
app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.router)
