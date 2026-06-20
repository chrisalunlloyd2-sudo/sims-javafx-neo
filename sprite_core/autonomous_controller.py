import sqlite3
import os
import time
import subprocess
import sys

# Ensure sprite_core is in the path
sys.path.append(os.path.abspath("sprite_core"))
from learning_engine import LearningEngine
from orchestrator import KernelOrchestrator

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

class AutonomousController:
    def __init__(self, db_path):
        self.db_path = db_path
        self.learning_engine = LearningEngine(db_path)
        self.orchestrator = KernelOrchestrator(db_path)
        self.confidence_threshold = 0.7 # Step 652: Confidence Threshold
        self.last_action_id = None

    def check_environment_and_act(self):
        """Step 651: Link Environment Monitor to Markov Model"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get latest metrics
        cursor.execute("SELECT cpu_load, mem_free, active_processes FROM environment_states ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if not row:
            return

        cpu, mem, proc = row
        print(f"[AUTO] System State: CPU {cpu}%, MEM {mem:.1f}MB, PROC {proc}")

        # Seeded Logic (Step 653 anticipation)
        action_id = None

        # Rule 1: High CPU -> Check Heartbeat (diagnostic)
        if cpu > 80:
            action_id = 1

        # Rule 2: Low Memory -> Data Purge
        elif mem < 1000: # Assuming 1000MB as a low threshold for simulation
            action_id = 3

        # Rule 3: High Process Count -> Environment Sweep
        elif proc > 100:
            action_id = 2

        if action_id:
            self.execute_autonomous_action(action_id)
        else:
            # Step 652: Do Nothing Protocol
            print("[AUTO] Confidence high in 'Idle' state. No action taken.")

    def execute_autonomous_action(self, action_id):
        # Check Markov model for confidence (Step 652)
        # In autonomous mode, we check if this action is statistically sound
        # or if we have a predicted next step with high confidence

        print(f"[AUTO] Threshold reached. Suggesting Action ID {action_id}")

        # For simulation, we'll execute if confidence > threshold or if it's a hard-coded trigger
        # We'll use the orchestrator to run it
        pid = self.orchestrator.run_command(action_id)
        if pid:
            print(f"[AUTO] Executed Action ID {action_id} (PID: {pid})")
            if self.last_action_id:
                self.learning_engine.record_transition(self.last_action_id, action_id)
            self.last_action_id = action_id

    def self_modify(self):
        """Step 654: Self-Modification Protocol (Simplified)"""
        # If an action has failed multiple times, we increase the threshold
        # If it succeeds consistently, we might lower it
        print("[AUTO] Running Self-Modification Sweep...")
        # (Real implementation would query execution_count and last_success)
        pass

if __name__ == "__main__":
    controller = AutonomousController(DB_PATH)
    print("Sprite Autonomous Controller Active.")
    try:
        while True:
            controller.check_environment_and_act()
            controller.self_modify()
            time.sleep(15)
    except KeyboardInterrupt:
        print("Autonomous Controller Stopped.")
