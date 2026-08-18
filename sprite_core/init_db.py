import sqlite3
import os

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

def init_db():
    """Init db (function)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for mapping performative sentences to integer IDs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence TEXT UNIQUE NOT NULL,
            script_path TEXT,
            execution_count INTEGER DEFAULT 0,
            last_success DATETIME,
            description TEXT
        )
    ''')

    # Table for tracking environmental states during execution
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS environment_states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            performative_id INTEGER,
            cpu_load REAL,
            mem_free REAL,
            active_processes INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (performative_id) REFERENCES performatives(id)
        )
    ''')

    # Table for Markov Chain transitions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markov_transitions (
            from_id INTEGER,
            to_id INTEGER,
            transition_count INTEGER DEFAULT 1,
            probability REAL DEFAULT 1.0,
            PRIMARY KEY (from_id, to_id),
            FOREIGN KEY (from_id) REFERENCES performatives(id),
            FOREIGN KEY (to_id) REFERENCES performatives(id)
        )
    ''')

    # Initial seed data
    seed_data = [
        ("System Heartbeat Check", "scripts/heartbeat.py", "Checks if Sprite kernel is alive"),
        ("Environment Sweep", "scripts/sweep.py", "Scans system states"),
        ("Data Purge", "scripts/purge.py", "Cleans redundant logs")
    ]

    for sentence, script, desc in seed_data:
        try:
            cursor.execute("INSERT INTO performatives (sentence, script_path, description) VALUES (?, ?, ?)",
                           (sentence, script, desc))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
