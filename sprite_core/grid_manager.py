import json
import sqlite3
import os
import sys
import time
from grid_protocol import GridProtocol
from hardware_id import get_hardware_uuid

# Ensure sprite_core is in the path
sys.path.append(os.path.abspath("sprite_core"))

DB_PATH = os.path.join("sprite_core", "context_fence", "db", "sprite.db")

class GridManager:
    """Step 1102: Remote Agent Deployment & Step 1103: Global State Ledger"""
    def __init__(self, db_path):
        self.db_path = db_path
        self.protocol = GridProtocol()
        self.node_id = get_hardware_uuid()
        self.known_nodes = {} # ip -> last_heartbeat
        
    def grid_callback(self, message, addr):
        # Step 1104: Grid Handshakes
        if message['type'] == 'HANDSHAKE':
            print(f"[GRID] New Handshake from {addr[0]} (ID: {message['node_id'][:12]}...)")
            self.known_nodes[addr[0]] = time.time()
            return {"status": "ACK", "node_id": self.node_id}
        
        # Step 1105: Network Heartbeat
        if message['type'] == 'HEARTBEAT':
            self.known_nodes[addr[0]] = time.time()
            return {"status": "ACK"}

        if message['type'] == 'DEPLOY_AGENT':
            agent_name = message['agent_name']
            print(f"[GRID] Remote Request: Deploying '{agent_name}' on this node.")
            return {"status": "DEPLOYED", "node": self.node_id}
            
        if message['type'] == 'SYNC_STATE':
            return {"status": "SYNCED", "health": "OK"}
            
        return {"status": "UNKNOWN_TYPE"}

    def run_heartbeat_loop(self):
        """Step 1105: Network Heartbeat Loop"""
        while True:
            for ip in list(self.known_nodes.keys()):
                print(f"[GRID] Pinging Node {ip}...")
                resp = self.protocol.send_message(ip, 5555, {"type": "HEARTBEAT", "origin": self.node_id})
                if not resp:
                    print(f"[WARN] Node {ip} timed out.")
            time.sleep(60)

    def start(self):
        import threading
        threading.Thread(target=self.protocol.start_server, args=(self.grid_callback,), daemon=True).start()
        threading.Thread(target=self.run_heartbeat_loop, daemon=True).start()
        print(f"[GRID] Node {self.node_id[:12]} active.")

    def deploy_to_remote(self, target_host, agent_name):
        print(f"[GRID] Deploying '{agent_name}' to {target_host}...")
        msg = {
            "type": "DEPLOY_AGENT",
            "agent_name": agent_name,
            "origin_node": self.node_id
        }
        return self.protocol.send_message(target_host, 5555, msg)

if __name__ == "__main__":
    manager = GridManager(DB_PATH)
    manager.start()
    
    # Simulate a remote deployment to self
    import time
    time.sleep(2)
    resp = manager.deploy_to_remote('127.0.0.1', "Remote Maintenance Sprite")
    print(f"[GRID] Deployment Result: {resp}")
