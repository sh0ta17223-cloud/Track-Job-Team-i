import sqlite3
from datetime import date

DB_NAME = "officemeet.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        name TEXT PRIMARY KEY,
        dept TEXT,
        color TEXT,
        tags TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dept TEXT,
        color TEXT,
        date TEXT,
        start TEXT,
        end TEXT,
        tags TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_profile(profile):
    conn = get_connection()
    cur = conn.cursor()

    tags_str = "||".join(profile["tags"])

    cur.execute("""
    INSERT OR REPLACE INTO profiles (name, dept, color, tags)
    VALUES (?, ?, ?, ?)
    """, (profile["name"], profile["dept"], profile["color"], tags_str))

    conn.commit()
    conn.close()


def load_profile(name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name, dept, color, tags FROM profiles WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {
            "name": row[0],
            "dept": row[1],
            "color": row[2],
            "tags": row[3].split("||") if row[3] else []
        }

    return None


def add_attendance(item):
    conn = get_connection()
    cur = conn.cursor()

    tags_str = "||".join(item["tags"])

    cur.execute("""
    INSERT INTO attendances (name, dept, color, date, start, end, tags)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        item["name"],
        item["dept"],
        item["color"],
        item["date"].isoformat(),
        item["start"],
        item["end"],
        tags_str
    ))

    conn.commit()
    conn.close()


def get_attendances():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, name, dept, color, date, start, end, tags
    FROM attendances
    ORDER BY date, start
    """)
    rows = cur.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "dept": row[2],
            "color": row[3],
            "date": date.fromisoformat(row[4]),
            "start": row[5],
            "end": row[6],
            "tags": row[7].split("||") if row[7] else []
        })
    return result


def delete_attendance(attendance_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM attendances WHERE id = ?", (attendance_id,))

    conn.commit()
    conn.close()