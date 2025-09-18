import sqlite3
from flask import g
from backend.config import get_config

# Load configuration
cfg = get_config()


def get_db():
    """
    Get a database connection with timeout and WAL mode enabled.
    Uses Flask's `g` to reuse the same connection per request.
    """
    if "db" not in g:
        conn = sqlite3.connect(
            cfg.DB_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES,
            timeout=10  # ✅ wait up to 10s before giving up
        )
        conn.row_factory = sqlite3.Row

        # ✅ Enable WAL mode for better concurrency
        conn.execute("PRAGMA journal_mode=WAL;")

        g.db = conn
    return g.db


def get_conn():
    """Alias for get_db() to maintain compatibility with existing code."""
    return get_db()


def close_db(e=None):
    """
    Close the database connection at the end of the request.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """
    Initialize the database tables if they don't exist.
    Ensures 'drugs' and 'reports' tables are created with the correct schema.
    """
    conn = sqlite3.connect(cfg.DB_PATH)
    c = conn.cursor()

    # Create drugs table
    c.execute("""
        CREATE TABLE IF NOT EXISTS drugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            batch_number TEXT UNIQUE NOT NULL,
            mfg_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            manufacturer TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Create reports table
    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug_name TEXT,
            batch_number TEXT NOT NULL,
            location TEXT,
            note TEXT,
            reported_on TIMESTAMP DEFAULT (datetime('now')),
            status INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print(f"Initializing database at: {cfg.DB_PATH}")
    init_db()
    print("✅ Database initialized successfully with clean schema.")
