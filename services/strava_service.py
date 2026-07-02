import os
import requests

from services.memory_service import (get_strava_tokens, get_phone_by_athlete_id)
from services.activity_service import (activity_exists, save_activity)

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")

RAILWAY_URL = "https://running-coach-bot.up.railway.app"


def get_strava_auth_url(phone):

    return (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={STRAVA_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={RAILWAY_URL}/strava/callback"
        f"&approval_prompt=force"
        f"&scope=activity:read_all"
        f"&state={phone}"
    )

def get_last_activity(phone):

    tokens = get_strava_tokens(phone)

    print("PHONE:", phone)
    print("TOKENS:", tokens)

    if not tokens or not tokens["access_token"]:
        print("NO ACCESS TOKEN")
        return None

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }

    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities?per_page=1",
        headers=headers,
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    if response.status_code != 200:
        return None

    activities = response.json()

    print("ACTIVITIES:", activities)

    if not activities:
        print("NO ACTIVITIES FOUND")
        return None

    return activities[0]

def get_activity(activity_id, access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        f"https://www.strava.com/api/v3/activities/{activity_id}",
        headers=headers
    )

    if response.status_code != 200:
        print(response.text)
        return None

    return response.json()

def get_access_token(phone):

    tokens = get_strava_tokens(phone)

    if not tokens:
        return None

    return tokens["access_token"]

def process_strava_webhook(body):

    print("========== STRAVA WEBHOOK ==========")
    print(body)
    print("====================================")