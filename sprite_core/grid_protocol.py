import socket
import json
import threading
import os

class GridProtocol:
    """Step 1101: Define the 'Grid Protocol'"""
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.is_running = False
        self.server_socket = None
        self.nodes = {} # uuid -> addr

    def start_server(self, callback):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running = True
        print(f"[GRID] Server started on {self.host}:{self.port}")
        
        while self.is_running:
            try:
                client, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, callback)).start()
            except:
                break

    def handle_client(self, client, addr, callback):
        try:
            data = client.recv(4096).decode()
            if data:
                message = json.loads(data)
                print(f"[GRID] Received from {addr}: {message['type']}")
                response = callback(message, addr)
                if response:
                    client.send(json.dumps(response).encode())
        finally:
            client.close()

    def send_message(self, target_host, target_port, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((target_host, target_port))
                s.send(json.dumps(message).encode())
                response = s.recv(4096).decode()
                return json.loads(response) if response else None
        except Exception as e:
            print(f"[GRID] Failed to send to {target_host}: {e}")
            return None

if __name__ == "__main__":
    # Test local handshake
    protocol = GridProtocol()
    def test_callback(msg, addr):
        return {"status": "ACK", "echo": msg}
    
    t = threading.Thread(target=protocol.start_server, args=(test_callback,), daemon=True)
    t.start()
    
    import time
    time.sleep(1)
    resp = protocol.send_message('127.0.0.1', 5555, {"type": "HANDSHAKE", "node_id": "test_node"})
    print(f"[GRID] Test Response: {resp}")
