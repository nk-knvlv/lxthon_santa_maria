from fastapi import FastAPI, Request

import config
from API.vexa_api import GoogleMeetApi

app = FastAPI()


@app.get("/leave")
def get_conversation():
    return app.google_meet_api.bot_leave()


@app.get("/join")
def get_conversation():
    return app


@app.get("/conversation")
def get_conversation():
    return app.google_meet_api.preset_dialog()


@app.get("/test")
def test():
    return 'test'


@app.post("/start/")
async def start(request: Request):
    data = await request.json()
    call_id = data['meet_id']
    try:
        google_meet_api: GoogleMeetApi = GoogleMeetApi(API_KEY=config.VEXA_API_KEY, call_id=call_id)
        google_meet_api.bot_join()
        return True
    except Exception as e:
        print(e)
        return False
