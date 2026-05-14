import json
import sqlite3
import os
import random
import sys

# Ensure sprite_core is in the path
sys.path.append(os.path.abspath("sprite_core"))
from hardware_id import get_hardware_uuid

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

class OpenClawProfileManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def generate_full_profile(self, name, anchor):
        """Step 801 & 1001: Hardware and Real-World Anchoring"""
        traits = {
            "behavioral": {
                "diligence": random.uniform(0, 1),
                "aggression": random.uniform(0, 1),
                "curiosity": random.uniform(0, 1),
                "loyalty": random.uniform(0, 1),
                "meticulousness": random.uniform(0, 1)
            },
            "technical": {
                "execution_speed": random.uniform(0, 1),
                "error_tolerance": random.uniform(0, 1),
                "optimization_bias": random.uniform(0, 1)
            }
        }

        # Step 1001: Link to Machine HW ID
        hw_uuid = get_hardware_uuid()

        # Step 1002: DePIN Trust Layer (Reputation Score)
        # In a real DePIN system, this would be retrieved from a blockchain
        trust_score = random.uniform(0.9, 1.0) # High initial trust for system sprites

        memory_silo = f"sprite_core/context_fence/memory_{name.lower().replace(' ', '_')}.json"
        if not os.path.exists(memory_silo):
            with open(memory_silo, 'w') as f:
                json.dump({"experiences": [], "shortcuts": {}}, f)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Update if exists, else insert
        cursor.execute("SELECT id FROM agent_profiles WHERE name = ?", (name,))
        row = cursor.fetchone()

        if row:
            cursor.execute(
                "UPDATE agent_profiles SET hardware_anchor = ?, traits = ?, hardware_uuid = ?, trust_score = ? WHERE name = ?",
                (anchor, json.dumps(traits), hw_uuid, trust_score, name)
            )
        else:
            cursor.execute(
                "INSERT INTO agent_profiles (name, hardware_anchor, traits, memory_silo_path, hardware_uuid, trust_score) VALUES (?, ?, ?, ?, ?, ?)",
                (name, anchor, json.dumps(traits), memory_silo, hw_uuid, trust_score)
            )

        conn.commit()
        conn.close()
        print(f"[DePIN] Agent {name} locked to Hardware: {hw_uuid[:12]}... Trust: {trust_score:.4f}")


if __name__ == "__main__":
    manager = OpenClawProfileManager(DB_PATH)
    # Step 802: Hardware Anchoring
    manager.generate_full_profile("Maintenance Sprite", "CPU_CORE_0")
    manager.generate_full_profile("Discovery Sprite", "DISK_PARTITION_C")
    manager.generate_full_profile("Security Sprite", "RAM_SEGMENT_A")
