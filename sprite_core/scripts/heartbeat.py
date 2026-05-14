import os
import psutil # Assuming psutil is available or using alternative
import platform

print("--- SPRITE HEARTBEAT ---")
print(f"OS: {platform.system()} {platform.release()}")
print(f"Process ID: {os.getpid()}")
print("Status: ALIVE")
