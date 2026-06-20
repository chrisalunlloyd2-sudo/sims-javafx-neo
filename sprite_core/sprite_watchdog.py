import os
import time
import subprocess
import sys

# Watchdog A monitors Watchdog B and the main Controller
# Watchdog B (not shown) would monitor Watchdog A

def is_process_running(name):
    try:
        output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {name}"', shell=True).decode()
        return name in output
    except Exception:
        return False

def maintain_persistence():
    print("[WATCHDOG] Initializing Sprite Watchdog...")
    controller_script = "sprite_core/simulation_orchestrator.py"
    py_exe = r"C:\Users\viper\python\python.exe"

    while True:
        # Step 754: Deploy Paired Watchdog Processes
        # Check if Orchestrator is alive
        try:
            cmd = f'powershell -NoProfile -Command "Get-Process | Where-Object {{ $_.CommandLine -like \'*simulation_orchestrator.py*\' }} | Select-Object -ExpandProperty Id"'
            output = subprocess.check_output(cmd, shell=True).decode().strip()
            if not output:
                print("[WATCHDOG] Sprite Orchestrator dead. Resuscitating...")
                subprocess.Popen([py_exe, controller_script])
        except Exception as e:
            print(f"[WATCHDOG] Error: {e}")

        time.sleep(30)

if __name__ == "__main__":
    maintain_persistence()
