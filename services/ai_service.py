import os

from openai import OpenAI
from services.memory_service import (
    load_messages,
    save_message,
    get_user
)
from prompts.coach_prompts import SYSTEM_PROMPT

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(phone, text):
    user = get_user(phone)

    history = load_messages(phone)

    profile_context = f"""
        Runner profile:

        Goal: {user['goal']}
        Next race: {user['next_race']}
        5K PB: {user['pb_5k']}
        10K PB: {user['pb_10k']}
        Half marathon PB: {user['pb_half']}

        Current training state:
        Weekly KM: {user['weekly_km']}
        Fatigue: {user['fatigue']}
        Race priority: {user['race_priority']}
        """

    messages = [
        {
            "role": "system",
            "content": (
                SYSTEM_PROMPT
                + "\n\n"
                + profile_context
            )
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": text
    })

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

    save_message(phone, "user", text)
    save_message(phone, "assistant", reply)

    return reply