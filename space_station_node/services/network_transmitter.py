import socket
import time
import sys
import os

# Add paths for constants and the C++ binaries
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../build/Debug')))
from core_shared.constants.network_config import GROUND_STATION_IP, GROUND_STATION_PORT
import quantum_crypto # type: ignore

def transmit_payload(raw_threat_batch): 
    print("\n   [NETWORK] Establishing Two-Way Socket to Earth Ground Station...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            time.sleep(1.5) 
            s.connect((GROUND_STATION_IP, GROUND_STATION_PORT))
            print(f"   [UPLINK] Connected to Ground Station on port {GROUND_STATION_PORT}.")
            
            # 1. Receive Earth's True Public Key
            # We receive it as raw bytes, NO decoding! (Removed .decode)
            earth_pk_bytes = s.recv(4096)
            print(f"   [KEY EXCHANGE] Received Earth's Public Key from Ground Control.")
            
            # 2. TRIGGER C++ CORE: Pass both the text and the raw bytes into the hybrid engine!
            print("   [ENCRYPTION] Handing Earth's Key and Threat Data to C++ Core...")
            hybrid_encrypted_package = quantum_crypto.secure_threat_payload(raw_threat_batch, earth_pk_bytes)
            
            # 3. Transmit the mathematically encrypted double payload
            print("   [TRANSMIT] Beaming Kyber Ciphertext & AES Payload to Earth...")
            s.sendall(hybrid_encrypted_package.encode('utf-8'))
            
    except ConnectionRefusedError:
        print("   [ERROR] Ground Station is currently OFFLINE. Transmission failed.")
    except Exception as e:
        print(f"   [ERROR] Network anomaly detected: {e}")
# import socket
# import time
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# from core_shared.constants.network_config import GROUND_STATION_IP, GROUND_STATION_PORT

# # Notice we are now passing the RAW text batch into the network layer!
# def transmit_payload(raw_threat_batch): 
#     print("\n   [NETWORK] Establishing Two-Way Socket to Earth Ground Station...")
#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             time.sleep(1.5) 
#             s.connect((GROUND_STATION_IP, GROUND_STATION_PORT))
#             print(f"   [UPLINK] Connected to Ground Station on port {GROUND_STATION_PORT}.")
            
#             # 1. NEW: Space receives Earth's Public Key
#             earth_pk = s.recv(4096).decode('utf-8')
#             print(f"   [KEY EXCHANGE] Received Earth's Public Key from Ground Control.")
            
#             # 2. (Coming Next) Space will pass this Public Key and the raw text into 
#             # our new C++ AES/Kyber bridge to generate the hybrid encrypted payload.
            
#             # 3. For now, we simulate the double payload transmission
#             dummy_encrypted_package = "0xQSEC_KYBER_CIPHERTEXT || 0xAES_ENCRYPTED_TEXT_DATA " + earth_pk
#             print("   [TRANSMIT] Beaming Kyber Ciphertext & AES Payload to Earth...")
#             s.sendall(dummy_encrypted_package.encode('utf-8'))
            
#     except ConnectionRefusedError:
#         print("   [ERROR] Ground Station is currently OFFLINE. Transmission failed.")
#     except Exception as e:
#         print(f"   [ERROR] Network anomaly detected: {e}")