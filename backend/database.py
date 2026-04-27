import sqlite3

DB_NAME = "scoutai.db"


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