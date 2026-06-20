import os
import subprocess
import getpass

def inject_startup_hook():
    """Step 755: Inject Deep Init Hooks (Windows Startup Folder)"""
    user = getpass.getuser()
    startup_path = f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    shortcut_path = os.path.join(startup_path, "sprite_init.bat")

    py_exe = r"C:\Users\viper\python\python.exe"
    watchdog_script = os.path.abspath("sprite_core/sprite_watchdog.py")

    content = f"@echo off\nstart /B {py_exe} {watchdog_script}\n"

    try:
        with open(shortcut_path, "w") as f:
            f.write(content)
        print(f"[INIT] Deep Init Hook injected at {shortcut_path}")
    except Exception as e:
        print(f"[ERROR] Failed to inject hook: {e}")

if __name__ == "__main__":
    inject_startup_hook()
