import os
import sqlite3
import subprocess

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

class PerformativeInterpreter:
    def __init__(self, db_path):
        self.db_path = db_path

    def translate(self, text):
        print(f"[*] Interpreting: '{text}'")
        # Logic to decide if we should create a new script or find existing
        # For Step 551, we translate directives into functional shell commands

        # Simple heuristic: if it looks like a system command we already have, return it
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, sentence FROM performatives WHERE sentence LIKE ?", (f"%{text}%",))
        match = cursor.fetchone()

        if match:
            print(f"[+] Match found in index: {match[1]} (ID: {match[0]})")
            return match[0]

        # If no match, we "generate" a new performative (simulated Step 552)
        print(f"[-] No direct match. Generating new performative for '{text}'...")
        new_id = self.allocate_new(text)
        return new_id

    def allocate_new(self, sentence):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Step 552: Auto-Numbering Allocation
        cursor.execute(
            "INSERT INTO performatives (sentence, description) VALUES (?, ?)",
            (sentence, "User-defined or AI-generated performative")
        )
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"[+] Allocated ID {new_id} for '{sentence}'")
        return new_id

if __name__ == "__main__":
    interpreter = PerformativeInterpreter(DB_PATH)
    interpreter.translate("calc")
    interpreter.translate("Open Notepad")
