import sqlite3

DB_FILE = "vault.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    """Initialize database tables."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password BLOB NOT NULL
        )
    """)

    conn.commit()
    conn.close()
