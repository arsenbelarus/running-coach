import os

from openai import OpenAI

from services.memory_service import (
    load_messages,
    save_message
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are an elite and experienced running coach.
You help runners improve performance,
avoid injuries, manage fatigue,
prepare for races, and interpret training data.
"""


def generate_reply(phone, text):

    history = load_messages(phone)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
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