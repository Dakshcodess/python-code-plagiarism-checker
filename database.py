import sqlite3


def connect_db():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file1 TEXT,
            file2 TEXT,
            score REAL,
            risk TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_result(file1, file2, score, risk):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history (file1, file2, score, risk)
        VALUES (?, ?, ?, ?)
    """, (file1, file2, score, risk))

    conn.commit()
    conn.close()


def fetch_history():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT file1, file2, score, risk FROM history ORDER BY id DESC")

    data = cursor.fetchall()

    conn.close()

    return data