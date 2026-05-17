import os

from openai import OpenAI

from services.memory_service import (
    load_messages,
    save_message,
    get_user
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are an elite and experienced running coach.
You help runners improve performance,
avoid injuries, manage fatigue,
prepare for races, and interpret training data.
"""


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