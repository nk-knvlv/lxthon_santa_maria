import config
from API.deepseek_api import SantaMariaAI
from API.vexa_api import GoogleMeetApi

if __name__ == "__main__":
    google_meet_api = GoogleMeetApi(API_KEY=config.VEXA_API_KEY, call_id="qnq-okpa-vsz")
    ai = SantaMariaAI(api_key=config.AI_API_KEY, system_prompt=config.SYSTEM_PROMPT)
    print(ai.run("\n".join(google_meet_api.preset_dialog())))
