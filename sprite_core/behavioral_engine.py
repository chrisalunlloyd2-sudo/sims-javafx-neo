import json
import sqlite3
import os

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

class BehavioralEngine:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_execution_priority(self, agent_name):
        """Step 803: Link traits to execution priority"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT traits FROM agent_profiles WHERE name = ?", (agent_name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            traits = json.loads(row[0])
            # High Diligence + High Execution Speed = High Priority (Simplified)
            priority = (traits["behavioral"]["diligence"] + traits["technical"]["execution_speed"]) / 2
            return priority
        return 0.5

class IACProtocol:
    """Step 805: Inter-Agent Communication"""
    def __init__(self):
        self.message_queue = []

    def send_handover(self, from_agent, to_agent, task_data):
        msg = {
            "from": from_agent,
            "to": to_agent,
            "data": task_data,
            "status": "PENDING"
        }
        self.message_queue.append(msg)
        print(f"[IAC] Handover: {from_agent} -> {to_agent} (Task: {task_data['action']})")
        return True

if __name__ == "__main__":
    be = BehavioralEngine(DB_PATH)
    prio = be.get_execution_priority("Maintenance Sprite")
    print(f"[BEHAVIOR] Maintenance Sprite Priority: {prio:.2f}")
    
    iac = IACProtocol()
    iac.send_handover("Discovery Sprite", "Maintenance Sprite", {"action": "Optimizing discovered path", "path": "C:/Windows/Temp"})
