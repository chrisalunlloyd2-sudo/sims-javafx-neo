import subprocess
import hashlib
import platform

def get_hardware_uuid():
    """Step 1001: Implement 'Real-World Anchoring'"""
    try:
        if platform.system() == "Windows":
            # Get CPU ID via PowerShell
            cpu_cmd = "powershell -NoProfile -Command \"(Get-WmiObject -Class Win32_Processor).ProcessorId\""
            cpu_id = subprocess.check_output(cpu_cmd, shell=True).decode().strip()

            # Get Disk Serial via PowerShell
            disk_cmd = "powershell -NoProfile -Command \"(Get-WmiObject -Class Win32_DiskDrive).SerialNumber\""
            disk_id = subprocess.check_output(disk_cmd, shell=True).decode().strip()

            raw_id = f"{cpu_id}-{disk_id}"
            hardware_hash = hashlib.sha256(raw_id.encode()).hexdigest()
            return hardware_hash
        else:
            return "NON_WINDOWS_HW_ID"
    except Exception as e:
        return "HARDWARE_ID_FETCH_FAILED"

if __name__ == "__main__":
    print(f"[HW] Machine Hardware UUID: {get_hardware_uuid()}")
