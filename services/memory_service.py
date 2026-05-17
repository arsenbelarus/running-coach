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