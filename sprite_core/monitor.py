import sqlite3
import os
import time
import subprocess
import json

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

def get_system_metrics():
    # Simple metric collection for Windows
    # In a real scenario, use psutil
    try:
        # Get CPU load (basic)
        cpu_query = subprocess.check_output("wmic cpu get loadpercentage", shell=True).decode()
        cpu_load = float(cpu_query.split("\n")[1].strip())
        
        # Get Free Memory (basic)
        mem_query = subprocess.check_output("wmic OS get FreePhysicalMemory", shell=True).decode()
        mem_free = float(mem_query.split("\n")[1].strip()) / 1024.0 # MB
        
        # Get process count
        proc_query = subprocess.check_output("tasklist", shell=True).decode()
        proc_count = len(proc_query.split("\n")) - 3
        
        return cpu_load, mem_free, proc_count
    except Exception as e:
        # print(f"Error getting metrics: {e}")
        return 0.0, 0.0, 0
        
def log_metrics():
    cpu, mem, proc = get_system_metrics()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO environment_states (cpu_load, mem_free, active_processes) VALUES (?, ?, ?)", 
                   (cpu, mem, proc))
    conn.commit()
    conn.close()
    # Minimal output for headless operation (Step 701 anticipation)
    sys.stdout.write(".")
    sys.stdout.flush()

if __name__ == "__main__":
    import sys
    print("Sprite Environment Monitor Started [Headless Mode]")
    try:
        while True:
            log_metrics()
            time.sleep(10) # Log every 10 seconds
    except KeyboardInterrupt:
        print("\nMonitor Stopped.")
