import requests


def bot_start():
    url = "https://gateway.dev.vexa.ai/bots"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "Ab4uTozo6xQwEyet9ZJCZ1mKkw74QjB2UFhwAUTR"
    }
    payload = {
        "platform": "google_meet",
        "native_meeting_id": "iwx-zcxh-mru",
        "bot_name": "MyMeetingBot"
    }
    response = requests.post(
        url,
        headers=headers,
        json=payload
    )
    print("Status Code:", response.status_code)
    print("Response:", response.text)


def get_text():
    url = "https://gateway.dev.vexa.ai/transcripts/google_meet/iwx-zcxh-mru"
    headers = {
        "X-API-Key": "Ab4uTozo6xQwEyet9ZJCZ1mKkw74QjB2UFhwAUTR"
    }
    response = requests.get(
        url,
        headers=headers,
    )
    return response.text


def close_bot():
    url = "https://gateway.dev.vexa.ai/bots/google_meet/iwx-zcxh-mru"
    headers = {
        "X-API-Key": "Ab4uTozo6xQwEyet9ZJCZ1mKkw74QjB2UFhwAUTR"
    }
    response = requests.delete(
        url,
        headers=headers,
    )
    print("Status Code:", response.status_code)
    print("Response:", response.text)


# bot_start()
get_text()
# close_bot()
