import sqlite3
import os
import subprocess
import signal

class KernelOrchestrator:
    def __init__(self, db_path):
        self.db_path = db_path
        self.active_processes = {} # pid -> subprocess.Popen

    def run_command(self, cmd_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sentence, script_path FROM performatives WHERE id = ?", (cmd_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            sentence, script_path = row
            print(f"[ORCH] Spawning: {sentence}")
            py_exe = r"C:\Users\viper\python\python.exe"
            proc = subprocess.Popen([py_exe, script_path])
            self.active_processes[proc.pid] = proc
            return proc.pid
        return None

    def kill_process(self, pid):
        if pid in self.active_processes:
            print(f"[ORCH] Terminating PID {pid}")
            self.active_processes[pid].terminate()
            del self.active_processes[pid]
            return True
        return False

    def list_active(self):
        return self.active_processes.keys()

if __name__ == "__main__":
    DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")
    orch = KernelOrchestrator(DB_PATH)
    print("Sprite Kernel Orchestrator Ready.")
    # Example: Run heartbeat
    pid = orch.run_command(1)
    print(f"Heartbeat started with PID {pid}")
