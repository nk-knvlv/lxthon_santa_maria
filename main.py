from fastapi import FastAPI
import config
from API.deepseek_api import SantaMariaAI
from API.vexa_api import GoogleMeetApi

if __name__ == "__main__":
    app = FastAPI()


    @app.get("/join")
    def get_conversation():
        return app.google_meet_api.preset_dialog()


    @app.get("/conversation")
    def get_conversation():
        return app.google_meet_api.preset_dialog()


    @app.get("/start")
    def start():
        try:
            app.google_meet_api = GoogleMeetApi(API_KEY=config.VEXA_API_KEY, call_id="qnq-okpa-vsz")
            return True
        except Exception as e:
            print(e)
            return False
