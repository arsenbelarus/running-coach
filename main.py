from fastapi import FastAPI, Request

from services.ai_service import generate_reply
from services.whatsapp_service import send_message

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):

    body = await request.json()

    try:
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]

        phone = message["from"]
        text = message["text"]["body"]

        reply = generate_reply(phone, text)

        send_message(phone, reply)

    except Exception as e:
        print("ERROR:", e)

    return {"status": "received"}