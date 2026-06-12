import sqlite3
from datetime import datetime

DB_NAME = "crisislens.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        description TEXT,
        image_path TEXT,
        category TEXT,
        severity TEXT,
        ai_summary TEXT,
        fake_probability TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# IMPORTANT: auto-create table when module loads
init_db()


def save_incident(name, location, description, image_path,
                   category, severity, ai_summary, fake_probability):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents
        (name, location, description, image_path,
         category, severity, ai_summary, fake_probability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, location, description, image_path,
          category, severity, ai_summary, fake_probability))

    conn.commit()
    conn.close()


def get_incidents():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM incidents
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows

    except Exception as e:
        print("DB Error:", e)
        return []
