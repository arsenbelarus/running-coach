from fastapi import FastAPI, Request

from services.ai_service import generate_reply
from services.whatsapp_service import send_message
from services.command_service import handle_command
from services.memory_service import create_user

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):

    body = await request.json()

    try:
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]

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