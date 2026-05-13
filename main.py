from fastapi import FastAPI, Request

app = FastAPI()

VERIFY_TOKEN = "mytoken123"

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

    return {"status": "received"}