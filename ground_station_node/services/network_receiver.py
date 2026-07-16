import socket
import sys
import os

# Add paths for constants and the new C++ binaries
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../build/Debug')))
from core_shared.constants.network_config import GROUND_STATION_IP, GROUND_STATION_PORT
import quantum_earth # type: ignore

def start_listening():
    print(f"\n[GROUND CONTROL] Starting two-way secure receiver on {GROUND_STATION_IP}:{GROUND_STATION_PORT}...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((GROUND_STATION_IP, GROUND_STATION_PORT))
        s.listen()
        print("[GROUND CONTROL] Listening for Space Station uplink...\n")
        
        conn, addr = s.accept()
        with conn:
            print(f"   [LINK ESTABLISHED] Secure connection from Space Station at {addr}")
            
            # 1. TRIGGER C++ CORE: Generate Earth's true Kyber Public Key!
            true_public_key_bytes = quantum_earth.generate_earth_keys()
            print("   [KEY EXCHANGE] Transmitting Earth's True Public Key to Space...")
            
            # Send the raw binary bytes directly!
            conn.sendall(true_public_key_bytes) 
            
            # 2. Wait for the double-payload to return
            data = conn.recv(8192) 
            if data:
                received_payload = data.decode('utf-8')
                print(f"   [ENCRYPTED UPLINK RECEIVED] {received_payload[:60]}... (truncated)")
                return received_payload