import sys
import sqlite3
import os
import subprocess

# Ensure sprite_core is in the path
sys.path.append(os.path.abspath("sprite_core"))
from learning_engine import LearningEngine

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")
learning_engine = LearningEngine(DB_PATH)

def resolve_aliases(ids):
    """Step 702: Resolve aliases in the input sequence"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Simple recursive resolution could be added, but for now just one level
    sequence_str = " ".join(map(str, ids))
    cursor.execute("SELECT alias_id FROM aliases WHERE sequence = ?", (sequence_str,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return [row[0]]
    return ids

def execute_by_id(p_id, headless=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sentence, script_path FROM performatives WHERE id = ?", (p_id,))
    row = cursor.fetchone()
    
    if row:
        sentence, script_path = row
        if not headless:
            print(f"[!] Executing ID {p_id}: {sentence}")
        else:
            sys.stdout.write("!") # Step 701: Minimal character output
            sys.stdout.flush()

        if script_path and os.path.exists(script_path):
            try:
                py_exe = r"C:\Users\viper\python\python.exe"
                # For headless mode, we might want to suppress script output too
                subprocess.run([py_exe, script_path], check=True, capture_output=headless)
                
                cursor.execute("UPDATE performatives SET execution_count = execution_count + 1, last_success = CURRENT_TIMESTAMP WHERE id = ?", (p_id,))
                conn.commit()
            except Exception as e:
                if not headless:
                    print(f"[ERROR] Failed to execute {script_path}: {e}")
                else:
                    sys.stdout.write("?") # Failure indicator
                    sys.stdout.flush()
        else:
            if not headless:
                print(f"[WARN] Script path {script_path} not found or invalid.")
    else:
        if not headless:
            print(f"[?] ID {p_id} not found in database.")
    
    conn.close()

def process_input(user_input, headless=False):
    parts = user_input.strip().split()
    try:
        ids = [int(p) for p in parts]
        
        # Step 702: Resolve aliases
        ids = resolve_aliases(ids)
        
        prev_id = None
        for p_id in ids:
            if prev_id is not None:
                learning_engine.record_transition(prev_id, p_id)
            execute_by_id(p_id, headless=headless)
            prev_id = p_id
        
        if not headless:
            # Predictive prompt (Step 601 anticipation)
            if len(ids) > 0:
                last_id = ids[-1]
                pred = learning_engine.get_prediction(last_id)
                if pred and pred[1] > 0.5: # 50% threshold
                     print(f"[PROMPT] High probability next action: ID {pred[0]} ({pred[1]*100:.1f}%)")
        else:
            sys.stdout.write(".") # Success indicator
            sys.stdout.flush()
            
        return True
    except ValueError:
        return fallback_nlp(user_input)

def fallback_nlp(text):
    print(f"[*] NLP Fallback: Analyzing '{text}'...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Simple keyword match for now
    cursor.execute("SELECT id, sentence FROM performatives WHERE sentence LIKE ?", (f"%{text}%",))
    results = cursor.fetchall()
    
    if results:
        if len(results) == 1:
            p_id, sentence = results[0]
            print(f"[+] Found match: {sentence} (ID: {p_id})")
            execute_by_id(p_id)
        else:
            print("[?] Multiple matches found:")
            for p_id, sentence in results:
                print(f"  - {p_id}: {sentence}")
    else:
        print("[-] No matches found. Recording novel command.")
        # Step 504: Route novel text commands
        # In a real scenario, this would go to a LLM or heuristic builder
    
    conn.close()
    return False

if __name__ == "__main__":
    headless = "--headless" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--headless"]
    
    if args:
        process_input(" ".join(args), headless=headless)
    else:
        while True:
            try:
                prompt = "sprite> " if not headless else ""
                cmd = input(prompt)
                if cmd.lower() in ['exit', 'quit']:
                    break
                process_input(cmd, headless=headless)
            except KeyboardInterrupt:
                break
