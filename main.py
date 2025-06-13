import config
from API.vexa_api import GoogleMeetApi

if __name__ == "__main__":
    google_meet_api = GoogleMeetApi(config.VEXA_API_KEY, call_id="qnq-okpa-vsz")
    # google_meet_api.bot_join()
    google_meet_api.preset_dialog()
