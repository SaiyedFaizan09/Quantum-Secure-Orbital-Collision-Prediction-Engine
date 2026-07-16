import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../build/Debug')))
import quantum_earth #type: ignore

def decrypt_payload(hybrid_payload):
    print("\n=========================================================")
    print(" [GROUND SEC-OPS] TRUE HYBRID DECRYPTION INITIATED")
    print("=========================================================")
    
    # 1. Separate the Kyber Matrix (Key) from the AES Data (Text)
    try:
        kyber_hex, aes_data = hybrid_payload.split(" || ")
    except ValueError:
        print("[CRITICAL ERROR] Payload formatting corrupted during network transit!")
        return None

    # 2. TRIGGER C++ CORE: Mathematically unlock the payload!
    decrypted_data = quantum_earth.decrypt_hybrid_payload(kyber_hex, aes_data)
    
    print("   [DECRYPTED THREAT INTEL] Decoded Payload:")
    # Print the recovered batched threats
    for threat in decrypted_data.split(" || "):
        print(f"   -> {threat}")
        
    print("\n[GROUND CONTROL] Threat Intelligence successfully recovered from Edge Node.")
    return decrypted_data
# import time

# def decrypt_payload(encrypted_payload):
#     print("\n=========================================================")
#     print(" [GROUND SEC-OPS] POST-QUANTUM DECRYPTION INITIATED")
#     print("=========================================================")
    
#     # 1. Verify the payload has our secure quantum signature
#     if not (encrypted_payload.startswith("0xQSEC_") and encrypted_payload.endswith("_ENDQ")):
#         print("[CRITICAL ERROR] Payload signature invalid or corrupted during transmission!")
#         return None

#     print("[SYSTEM] Valid Kyber-768 quantum signature detected.")
#     print("[DECRYPTION] Loading Private Lattice Key to decapsulate matrix...")
    
#     # Simulate the heavy processing time of quantum decryption
#     time.sleep(1.2)
    
#     # 2. In a true hardware deployment, this is where the C++ liboqs decapsulation 
#     # would recover the exact shared secret. For our simulation, we will "unlock" the batch.
#     print("[DECRYPTION] Matrix decapsulation successful. Extracting threat batch...")
#     time.sleep(0.5)
    
#     print("=========================================================\n")
    
#     # Simulate the recovered payload (In reality, this data would be passed securely 
#     # from the Space Station's C++ core inside the network transmission)
#     print("   [DECRYPTED THREAT INTEL] Decoded Payload:")
#     print("   -> Target: ISS (ZARYA) | Distance: 0.0km")
#     print("   -> Status: CRITICAL COLLISION IMMINENT")
#     print("\n[GROUND CONTROL] Threat Intelligence successfully recovered from Edge Node.")
    
#     return "Target: ISS (ZARYA) | Distance: 0.0km"