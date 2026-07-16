import sys
import os
from ground_station_node.services import network_receiver
from ground_station_node.services import payload_decryptor
# from ground_station_node.services import ai_forensic_reporter

def run_ground_station():
    print("=========================================================")
    print(" EARTH GROUND STATION: SECURE TERMINAL ONLINE")
    print("=========================================================")
    
    # 1. Open the socket, GENERATE KEYS, BEAM THEM, and listen for the return transmission
    hybrid_payload = network_receiver.start_listening()
    
    # 2. Decrypt the payload upon successful network reception
    if hybrid_payload:
        print("\n[SYSTEM] Payload secured in Earth servers. Routing to decryption module...")
        decrypted_data = payload_decryptor.decrypt_payload(hybrid_payload)
        
        # 3. Trigger the Generative AI to write the formal forensic report!
        # if decrypted_data:
        #     ai_forensic_reporter.generate_forensic_report(decrypted_data)
        
    else:
        print("\n[ERROR] No data received from the Space Station.")

if __name__ == "__main__":
    run_ground_station()