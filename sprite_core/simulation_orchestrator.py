import time
import os
import sys
import subprocess
import sqlite3

# Ensure sprite_core is in the path
sys.path.append(os.path.abspath("sprite_core"))
from autonomous_controller import AutonomousController
from sprite_watchdog import maintain_persistence
from grid_manager import GridManager

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

class LivingSimulationOrchestrator:
    """Step 1003 & 1105: Finalize the 'Living Simulation' Orchestrator with Grid Support"""
    def __init__(self, db_path):
        self.db_path = db_path
        self.controller = AutonomousController(db_path)
        self.grid = GridManager(db_path)
        self.is_running = False

    def start_simulation(self):
        print("--- [SIMULATION ORCHESTRATOR] STARTING ---")
        print("[!] Synchronizing Background Sprite Engine with Visual JavaFX Bridge...")
        print("[!] Global Grid Protocol Active.")
        self.is_running = True
        
        # Start Grid Manager
        self.grid.start()
        
        # In a real scenario, this might start the JavaFX process too
        # subprocess.Popen(["mvn", "exec:java", "-Dexec.mainClass='com.simsneo.MainApp'"], cwd="C:/Users/viper/Desktop/Sims_JavaFX_Neo")
        
        try:
            while self.is_running:
                # Coordinate execution loop
                self.controller.check_environment_and_act()
                self.controller.self_modify()
                
                # Check for DePIN Reputation updates
                self.update_trust_scores()
                
                time.sleep(10)
        except KeyboardInterrupt:
            self.stop_simulation()

    def update_trust_scores(self):
        """Step 1002 logic integration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Simulate reputation gain for successful autonomous actions
        cursor.execute("UPDATE agent_profiles SET trust_score = MIN(1.0, trust_score + 0.001)")
        conn.commit()
        conn.close()

    def stop_simulation(self):
        print("\n--- [SIMULATION ORCHESTRATOR] STOPPING ---")
        self.is_running = False

if __name__ == "__main__":
    orch = LivingSimulationOrchestrator(DB_PATH)
    orch.start_simulation()
