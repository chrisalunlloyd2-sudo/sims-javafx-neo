import sqlite3
import os

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

class LearningEngine:
    def __init__(self, db_path):
        self.db_path = db_path

    def is_relevant(self, from_id, to_id):
        """Step 603: Design the 'Data Withdraw' Filter"""
        # For now, we consider a transition highly relevant if it has been seen before
        # or if the performative is a core system check (IDs 1-3)
        if from_id in [1, 2, 3] or to_id in [1, 2, 3]:
            return True
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT transition_count FROM markov_transitions WHERE from_id = ? AND to_id = ?",
            (from_id, to_id)
        )
        row = cursor.fetchone()
        conn.close()
        
        # If it's a new transition, we record it, but we could add more complex state-based logic here
        return True 

    def record_transition(self, from_id, to_id):
        """Step 602: Build the Recursive Rolling Log with Data Withdraw filter"""
        if from_id is None or to_id is None:
            return
        
        if not self.is_relevant(from_id, to_id):
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if transition exists
        cursor.execute(
            "SELECT transition_count FROM markov_transitions WHERE from_id = ? AND to_id = ?",
            (from_id, to_id)
        )
        row = cursor.fetchone()
        
        if row:
            cursor.execute(
                "UPDATE markov_transitions SET transition_count = transition_count + 1 WHERE from_id = ? AND to_id = ?",
                (from_id, to_id)
            )
        else:
            cursor.execute(
                "INSERT INTO markov_transitions (from_id, to_id, transition_count) VALUES (?, ?, 1)",
                (from_id, to_id)
            )
        
        conn.commit()
        self.update_probabilities(from_id, conn)
        conn.close()

    def update_probabilities(self, from_id, conn):
        """Step 601: Integrate the Markov Chain Model (Probability Calculation)"""
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(transition_count) FROM markov_transitions WHERE from_id = ?", (from_id,))
        total = cursor.fetchone()[0]
        
        if total > 0:
            cursor.execute(
                "UPDATE markov_transitions SET probability = CAST(transition_count AS REAL) / ? WHERE from_id = ?",
                (total, from_id)
            )
            conn.commit()

    def get_prediction(self, current_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT to_id, probability FROM markov_transitions WHERE from_id = ? ORDER BY probability DESC LIMIT 1",
            (current_id,)
        )
        prediction = cursor.fetchone()
        conn.close()
        return prediction

    def check_for_aliases(self, threshold=5):
        """Step 702: Implement Alias Compounding"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find sequences that appear frequently
        # This is a simplified version looking at transitions
        cursor.execute(
            "SELECT from_id, to_id, transition_count FROM markov_transitions WHERE transition_count >= ?",
            (threshold,)
        )
        sequences = cursor.fetchall()
        
        for from_id, to_id, count in sequences:
            sequence_str = f"{from_id} {to_id}"
            cursor.execute("SELECT id FROM aliases WHERE sequence = ?", (sequence_str,))
            if not cursor.fetchone():
                print(f"[*] Compounding frequent sequence: {sequence_str}")
                # Create a new performative for this sequence
                cursor.execute(
                    "INSERT INTO performatives (sentence, description) VALUES (?, ?)",
                    (f"Compound Sequence: {sequence_str}", f"Automated alias for {sequence_str}")
                )
                new_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO aliases (sequence, alias_id) VALUES (?, ?)",
                    (sequence_str, new_id)
                )
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    engine = LearningEngine(DB_PATH)
    # Simulate some learning
    print("[*] Simulating transition learning: 1 -> 2")
    engine.record_transition(1, 2)
    print("[*] Simulating transition learning: 1 -> 2")
    engine.record_transition(1, 2)
    print("[*] Simulating transition learning: 1 -> 3")
    engine.record_transition(1, 3)
    
    pred = engine.get_prediction(1)
    if pred:
        print(f"[+] Prediction for ID 1: Next is likely ID {pred[0]} (Prob: {pred[1]:.2f})")
