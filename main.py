import os
import requests
from fastapi import FastAPI, Request

from services.ai_service import generate_reply
from services.whatsapp_service import send_message
from services.command_service import handle_command
from services.memory_service import (create_user, save_strava_tokens, list_users, get_phone_by_athlete_id)
from services.strava_service import (get_access_token, get_activity)
from services.activity_service import (save_activity, activity_exists)

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):

    body = await request.json()

    try:
        value = body["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return {"status": "ignored"}

        message = value["messages"][0]

        phone = message["from"]
        text = message["text"]["body"]

        command_response = handle_command(phone, text)

        if command_response:
            send_message(phone, command_response)
            return {"status": "command processed"}
        
        create_user(phone)

        reply = generate_reply(phone, text)

        send_message(phone, reply)

    except Exception as e:
        print("ERROR:", e)

    return {"status": "received"}

@app.get("/strava/callback")
def strava_callback(code: str, state: str):

    print("STATE:", state)
    list_users()

    url = "https://www.strava.com/oauth/token"

    payload = {
        "client_id": os.getenv("STRAVA_CLIENT_ID"),
        "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
        "code": code,
        "grant_type": "authorization_code"
    }

    response = requests.post(url, data=payload)

    data = response.json()

    print(data)

    if response.status_code != 200:
        return {
            "error": data
        }
    
    create_user(state)

    save_strava_tokens(
        phone=state,
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        expires_at=data["expires_at"],
        athlete_id=data["athlete"]["id"]
    )

    return {
        "message": "Strava connected successfully"
    }

@app.post("/strava/webhook")
async def strava_webhook(request: Request):

    body = await request.json()

    print("========== STRAVA WEBHOOK ==========")
    print(body)
    print("====================================")

    return {
        "status": "ok"
    }

@app.get("/strava/webhook")
def verify_strava_webhook(
    hub_mode: str = "",
    hub_verify_token: str = "",
    hub_challenge: str = ""
):

    if hub_verify_token != os.getenv("STRAVA_VERIFY_TOKEN"):
        return {"error": "Invalid verify token"}

    return {"hub.challenge": hub_challenge}