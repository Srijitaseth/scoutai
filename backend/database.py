import os
import sqlite3
from pathlib import Path


def get_default_db_path():
    if os.getenv("VERCEL"):
        return "/tmp/scoutai.db"

    return str(Path(__file__).with_name("scoutai.db"))


DB_NAME = os.getenv("SCOUTAI_DB_PATH", get_default_db_path())


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        resume_text TEXT,
        match_score REAL,
        interest_score REAL,
        final_score REAL,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        feedback_type TEXT,
        comment TEXT
    )
    """)

    conn.commit()
    conn.close()
