from fastapi import FastAPI, Request
from openai import OpenAI
import requests
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VERIFY_TOKEN = "mytoken123"
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.get("/")
def home():
    return {"message": "Bot alive"}

@app.get("/webhook")
def verify_webhook(
    hub_mode: str = "",
    hub_verify_token: str = "",
    hub_challenge: str = ""
):
    print(hub_verify_token)

    if hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)

    return {"error": "Invalid token"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    print(body)

    try:
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]

        phone = message["from"]
        text = message["text"]["body"]

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an elite and experienced running coach. "
                        "You help runners improve performance, avoid injuries, manage fatigue, "
                        "prepare for races, and interpret training data."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        reply = response.choices[0].message.content

        send_message(phone, reply)

    except Exception as e:
        print("ERROR:", e)

    return {"status": "received"}


def send_message(to, text):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }

    response = requests.post(url, headers=headers, json=payload)

    print(response.status_code)
    print(response.text)