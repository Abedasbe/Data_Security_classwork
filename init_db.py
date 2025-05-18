import sqlite3

DB = "users.db"

def init_db() -> None:
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT    NOT NULL,
                last_name  TEXT    NOT NULL,
                user_id    TEXT    UNIQUE NOT NULL,
                username   TEXT    UNIQUE NOT NULL,
                password   TEXT    NOT NULL,
                cc_number  TEXT    NOT NULL,
                cc_valid   TEXT    NOT NULL,
                cvc        TEXT    NOT NULL,
                is_admin   INTEGER DEFAULT 0
            );
        """)
    print("✅ users.db initialised.")

if __name__ == "__main__":
    init_db()