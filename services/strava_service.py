import os
import requests

from services.memory_service import get_strava_tokens

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

    if not tokens or not tokens["access_token"]:
        return None

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }

    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities?per_page=1",
        headers=headers,
    )

    if response.status_code != 200:
        return None

    activities = response.json()

    if len(activities) == 0:
        return None

    return activities[0]