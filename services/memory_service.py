import sqlite3

conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT,
    role TEXT,
    content TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    phone TEXT PRIMARY KEY,
    goal TEXT,
    next_race TEXT,
    pb_5k TEXT,
    pb_10k TEXT,
    pb_half TEXT,
    weekly_km TEXT,
    fatigue TEXT,
    race_priority TEXT
)
""")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN weekly_km TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN fatigue TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN race_priority TEXT")
except:
    pass

conn.commit()

def save_message(phone, role, content):
    cursor.execute(
        "INSERT INTO messages (phone, role, content) VALUES (?, ?, ?)",
        (phone, role, content)
    )
    conn.commit()

def load_messages(phone, limit=10):
    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE phone = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (phone, limit)
    )

    rows = cursor.fetchall()
    rows.reverse()

    return [
        {"role": role, "content": content}
        for role, content in rows
    ]

def get_user(phone):
    cursor.execute(
        """
        SELECT
            goal,
            next_race,
            pb_5k,
            pb_10k,
            pb_half,
            weekly_km,
            fatigue,
            race_priority
        FROM users
        WHERE phone = ?
        """,
        (phone,)
    )

    row = cursor.fetchone()

    if not row:
        return None

    return {
        "goal": row[0],
        "next_race": row[1],
        "pb_5k": row[2],
        "pb_10k": row[3],
        "pb_half": row[4],
        "weekly_km": row[5],
        "fatigue": row[6],
        "race_priority": row[7]
    }

def create_user(phone):
    cursor.execute(
        """
        INSERT OR IGNORE INTO users (phone)
        VALUES (?)
        """,
        (phone,)
    )

    conn.commit()

def update_goal(phone, goal):
    cursor.execute(
        """
        UPDATE users
        SET goal = ?
        WHERE phone = ?
        """,
        (goal, phone)
    )

    conn.commit()

def update_next_race(phone, race):
    cursor.execute(
        """
        UPDATE users
        SET next_race = ?
        WHERE phone = ?
        """,
        (race, phone)
    )

    conn.commit()

def update_pb_5k(phone, pb):
    cursor.execute(
        """
        UPDATE users
        SET pb_5k = ?
        WHERE phone = ?
        """,
        (pb, phone)
    )

    conn.commit()

def update_pb_10k(phone, pb):
    cursor.execute(
        """
        UPDATE users
        SET pb_10k = ?
        WHERE phone = ?
        """,
        (pb, phone)
    )

    conn.commit()

def update_pb_half(phone, pb):
    cursor.execute(
        """
        UPDATE users
        SET pb_half = ?
        WHERE phone = ?
        """,
        (pb, phone)
    )

    conn.commit()

def update_weekly_km(phone, weekly_km):
    cursor.execute(
        """
        UPDATE users
        SET weekly_km = ?
        WHERE phone = ?
        """,
        (weekly_km, phone)
    )

    conn.commit()

def update_fatigue(phone, fatigue):
    cursor.execute(
        """
        UPDATE users
        SET fatigue = ?
        WHERE phone = ?
        """,
        (fatigue, phone)
    )

    conn.commit()

def update_race_priority(phone, race_priority):
    cursor.execute(
        """
        UPDATE users
        SET race_priority = ?
        WHERE phone = ?
        """,
        (race_priority, phone)
    )

    conn.commit()