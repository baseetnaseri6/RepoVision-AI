import sqlite3
from datetime import datetime

DB_NAME = "reviews.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_name TEXT,
            repo_url TEXT,
            language TEXT,
            stars INTEGER,
            forks INTEGER,
            overall_score INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_review(repo, scores):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reviews (
            repo_name,
            repo_url,
            language,
            stars,
            forks,
            overall_score,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        repo.get("full_name"),
        repo.get("html_url"),
        repo.get("language"),
        repo.get("stars"),
        repo.get("forks"),
        scores.get("overall"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_recent_reviews(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT repo_name, repo_url, language, stars, forks, overall_score, created_at
        FROM reviews
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows