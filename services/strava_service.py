import os

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