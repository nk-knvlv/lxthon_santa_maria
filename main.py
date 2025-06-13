from fastapi import FastAPI
import config
from API.vexa_api import GoogleMeetApi

if __name__ == "__main__":
    app = FastAPI()


    @app.get("/conversation")
    def get_conversation():
        return json_to_dict_list(path_to_json)


    @app.get("/start")
    def start():
        google_meet_api = GoogleMeetApi(config.VEXA_API_KEY, call_id="qnq-okpa-vsz")
        # google_meet_api.bot_join()
        google_meet_api.preset_dialog()
        return True