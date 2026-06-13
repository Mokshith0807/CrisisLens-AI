import sqlite3

DB_NAME = "crisislens.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
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
        image_ai_analysis TEXT,
        emergency_recommendation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_incident(
    name,
    location,
    description,
    image_path,
    category,
    severity,
    ai_summary,
    fake_probability,
    image_ai_analysis,
    emergency_recommendation
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table if missing
    create_database()

    cursor.execute("""
    INSERT INTO incidents (
        name,
        location,
        description,
        image_path,
        category,
        severity,
        ai_summary,
        fake_probability,
        image_ai_analysis,
        emergency_recommendation
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        location,
        description,
        image_path,
        category,
        severity,
        ai_summary,
        fake_probability,
        image_ai_analysis,
        emergency_recommendation
    ))

    conn.commit()
    conn.close()


def get_incidents():
    create_database()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM incidents
    ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# Automatically create table on startup
create_database()
