from services.memory_service import (
    get_user,
    update_goal,
    update_next_race,
    update_pb_5k,
    update_pb_10k,
    update_pb_half
)


def handle_command(phone, text):
    text = text.strip()

    lower_text = text.lower()

    # GOAL
    if lower_text.startswith("goal:"):

        goal = text.split(":", 1)[1].strip()

        update_goal(phone, goal)

        return f"Goal updated to: {goal}"

    # NEXT RACE
    if lower_text.startswith("race:"):

        race = text.split(":", 1)[1].strip()

        update_next_race(phone, race)

        return f"Next race updated to: {race}"

    # 5K PB
    if lower_text.startswith("pb5k:"):

        pb = text.split(":", 1)[1].strip()

        update_pb_5k(phone, pb)

        return f"5K PB updated to: {pb}"

    # 10K PB
    if lower_text.startswith("pb10k:"):

        pb = text.split(":", 1)[1].strip()

        update_pb_10k(phone, pb)

        return f"10K PB updated to: {pb}"

    # HALF MARATHON PB
    if lower_text.startswith("pbhalf:"):

        pb = text.split(":", 1)[1].strip()

        update_pb_half(phone, pb)

        return f"Half marathon PB updated to: {pb}"

    # PROFILE
    if lower_text == "/profile":

        user = get_user(phone)

        if not user:
            return "No profile found."

        return (
            f"🏃 Runner Profile\n\n"
            f"Goal: {user['goal'] or 'Not set'}\n"
            f"Next race: {user['next_race'] or 'Not set'}\n"
            f"5K PB: {user['pb_5k'] or 'Not set'}\n"
            f"10K PB: {user['pb_10k'] or 'Not set'}\n"
            f"Half marathon PB: {user['pb_half'] or 'Not set'}"
        )

    return None