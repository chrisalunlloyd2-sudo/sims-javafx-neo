import os
import sqlite3
import shutil
import platform

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

class DiscoveryModule:
    def __init__(self, db_path):
        self.db_path = db_path
        self.common_paths = []
        if platform.system() == "Windows":
            self.common_paths = [
                os.environ.get("SystemRoot", "C:\\Windows") + "\\System32",
                os.environ.get("ProgramFiles", "C:\\Program Files"),
                os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\WindowsApps")
            ]
        else:
            self.common_paths = ["/bin", "/usr/bin", "/usr/local/bin"]

    def sweep(self, limit=100):
        print(f"[*] Starting Brute-Force Discovery Sweep (Limit: {limit})...")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        found_count = 0
        for path in self.common_paths:
            if not os.path.exists(path):
                continue

            print(f"[*] Crawling: {path}")
            try:
                for entry in os.scandir(path):
                    if found_count >= limit:
                        break

                    if entry.is_file() and (entry.name.endswith(".exe") or entry.name.endswith(".com") or platform.system() != "Windows"):
                        # Check if already indexed
                        cursor.execute("SELECT id FROM performatives WHERE sentence = ?", (entry.name,))
                        if not cursor.fetchone():
                            # Auto-numbering and indexing
                            cursor.execute(
                                "INSERT INTO performatives (sentence, script_path, description) VALUES (?, ?, ?)",
                                (entry.name, entry.path, f"System binary discovered in {path}")
                            )
                            found_count += 1
            except PermissionError:
                continue

        conn.commit()
        conn.close()
        print(f"[+] Discovery complete. Indexed {found_count} new performatives.")

if __name__ == "__main__":
    discovery = DiscoveryModule(DB_PATH)
    discovery.sweep(limit=50) # Sweep 50 binaries for initial indexing
