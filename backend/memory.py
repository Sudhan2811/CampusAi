import sqlite3
from pathlib import Path


DB_PATH = Path("backend/campusai.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_memory():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_message(session_id: str, role: str, message: str):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO conversations
        (session_id, role, message)
        VALUES (?, ?, ?)
        """,
        (session_id, role, message)
    )

    connection.commit()
    connection.close()


def get_history(session_id: str, limit=10):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM conversations
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (session_id, limit)
    )

    rows = cursor.fetchall()

    connection.close()

    # Reverse so the oldest message comes first
    rows.reverse()

    return [
        {
            "role": role,
            "message": message
        }
        for role, message in rows
    ]