from fastapi import FastAPI

import config
from API.vexa_api import GoogleMeetApi

# if __name__ == "__main__":
app = FastAPI()


@app.get("/leave")
def get_conversation():
    return app.google_meet_api.bot_leave()

@app.get("/join")
def get_conversation():
    return app.google_meet_api.bot_join()


@app.get("/conversation")
def get_conversation():
    return app.google_meet_api.preset_dialog()

@app.get("/test")
def test():
    return 'test'



@app.post("/start/")
def start(call_id: str):
    try:
        app.google_meet_api: GoogleMeetApi = GoogleMeetApi(API_KEY=config.VEXA_API_KEY, call_id=call_id)
        return True
    except Exception as e:
        print(e)
        return False
