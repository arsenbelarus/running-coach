from services.memory_service import (
    get_user,
    update_goal,
    update_next_race,
    update_pb_5k,
    update_pb_10k,
    update_pb_half,
    update_weekly_km,
    update_fatigue,
    update_race_priority
)
from services.strava_service import get_strava_auth_url


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
    
        # WEEKLY KM
    if lower_text.startswith("weekly_km:"):

        weekly_km = text.split(":", 1)[1].strip()

        update_weekly_km(phone, weekly_km)

        return f"Weekly mileage updated to: {weekly_km}"

    # FATIGUE
    if lower_text.startswith("fatigue:"):

        fatigue = text.split(":", 1)[1].strip()

        update_fatigue(phone, fatigue)

        return f"Fatigue status updated to: {fatigue}"

    # RACE PRIORITY
    if lower_text.startswith("race_priority:"):

        race_priority = text.split(":", 1)[1].strip()

        update_race_priority(phone, race_priority)

        return f"Race priority updated to: {race_priority}"
    
        # HELP
    if lower_text == "/help":

        return (
            "🏃 Available Commands\n\n"

            "Profile & Goals\n"
            "goal: sub 50 10k\n"
            "race: Warsaw 10K May 23\n"
            "pb5k: 23:55\n"
            "pb10k: 50:12\n"
            "pbhalf: 1:58:43\n\n"

            "Training State\n"
            "weekly_km: 42\n"
            "fatigue: low / moderate / high\n"
            "race_priority: A / B / C\n\n"

            "Utilities\n"
            "/profile → show current profile\n"
            "/help → show available commands"
        )

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
            f"Weekly KM: {user['weekly_km'] or 'Not set'}\n"
            f"Fatigue: {user['fatigue'] or 'Not set'}\n"
            f"Race priority: {user['race_priority'] or 'Not set'}"
        )
    
    # CONNECT STRAVA
    if lower_text == "/connect_strava":

        auth_url = get_strava_auth_url(phone)

        return (
            "Connect your Strava account:\n\n"
            f"{auth_url}"
        )

    return None