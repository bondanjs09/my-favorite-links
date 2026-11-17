import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS content_tbl (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                links TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                deleted_at TEXT
            )
        """)

        connection.commit()

    finally:
        connection.close()
