import sys
import asyncio
import time
from space_station_node.services.tle_ingestion import TLEIngestionService
from space_station_node.services.orbit_analytics import OrbitAnalyticsEngine
from space_station_node.services import network_transmitter

async def run_edge_node():
    """Master Orchestrator for the Quantum-Secure Orbital Collision Prediction Engine."""
    print("\n=========================================================")
    print(" QUANTUM-SECURE ORBITAL COLLISION ENGINE: EDGE NODE LIVE")
    print("=========================================================")
    
    # 1. Start the SecOps Hardware Constraint Benchmark Timer [3, 4]
    benchmark_start = time.time()

    # 2. Phase 1: Data Ingestion (API-Level Filtering & Caching) [2]
    print("\n[PHASE 1] Initiating Orbital Data Ingestion...")
    ingestion_service = TLEIngestionService()
    try:
        await ingestion_service.run_ingestion_pipeline()
    except Exception as e:
        print(f"[CRITICAL ERROR] Data ingestion failed: {e}")
        sys.exit(1)
    
    # 3. Phase 2: Predictive Analytics (Spatial Proximity Filtering) [5]
    print("\n[PHASE 2] Executing Predictive Analytics Engine...")
    analytics_engine = OrbitAnalyticsEngine()
    threats = analytics_engine.detect_collision_threats()
    
    # 4. Phase 3: Threat Assessment & Quantum Payload Generation
    print("\n[PHASE 3] Threat Assessment & Quantum Payload Generation...")
        
    threat_batch = []
    
    for threat in threats:
        # REAL DATA INJECTION: Pulling the actual object name and distance from the Space-Track data
        payload = f"Target: {threat['OBJECT_NAME']} | Distance: {threat['DISTANCE_KM']}km"
        threat_batch.append(payload)
        
    if len(threat_batch) > 0:
        print(f"[CRITICAL ALERT] {len(threat_batch)} Threats detected within the Danger Radius!")
        print("-> Passing raw threat batch to Network Transmitter for Two-Way Key Exchange...\n")
        
        batched_payload_string = " || ".join(threat_batch)
        
        # We hand the raw string to the transmitter. 
        # The transmitter catches Earth's key, triggers the C++ #SecOps benchmark, 
        # executes Kyber/AES encryption, and beams it down [1]!
        network_transmitter.transmit_payload(batched_payload_string)
        
    else:
        print("[STATUS] No collision threats detected. Orbit is clear.")
        
    # 5. Finalize the Python #SecOps Benchmarking
    benchmark_end = time.time()
    execution_time = benchmark_end - benchmark_start
    print("\n=========================================================")
    print(f" [#SecOps BENCHMARK] Total Python Orchestration: {round(execution_time, 4)} seconds.")
    print("=========================================================\n")

if __name__ == "__main__":
    # Execute the asynchronous master loop
    asyncio.run(run_edge_node())
# import sys
# # Add the build folder to Python's path so it can find the compiled C++ binary
# sys.path.append('./build/Debug')
# import quantum_crypto # type: ignore
# import asyncio
# import time
# import sys
# from space_station_node.services.tle_ingestion import TLEIngestionService
# from space_station_node.services.orbit_analytics import OrbitAnalyticsEngine
# from space_station_node.services import network_transmitter

# async def run_edge_node():
#     """Master Orchestrator for the Quantum-Secure Orbital Collision Prediction Engine."""
#     print("\n=========================================================")
#     print(" QUANTUM-SECURE ORBITAL COLLISION ENGINE: EDGE NODE LIVE")
#     print("=========================================================")
    
#     # 1. Start the SecOps Hardware Constraint Benchmark Timer
#     # This proves the edge node can process analytics efficiently before the heavy C++ cryptography
#     benchmark_start = time.time()

#     # 2. Phase 1: Data Ingestion (API-Level Filtering & Caching)
#     print("\n[PHASE 1] Initiating Orbital Data Ingestion...")
#     ingestion_service = TLEIngestionService()
#     try:
#         await ingestion_service.run_ingestion_pipeline()
#     except Exception as e:
#         print(f"[CRITICAL ERROR] Data ingestion failed: {e}")
#         sys.exit(1)
    
#     # 3. Phase 2: Predictive Analytics (Spatial Proximity Filtering)
#     print("\n[PHASE 2] Executing Predictive Analytics Engine...")
#     analytics_engine = OrbitAnalyticsEngine()
#     threats = analytics_engine.detect_collision_threats()
    
#     # [PHASE 3] Threat Assessment & Quantum Payload Generation...
#     print("\n[PHASE 3] Threat Assessment & Quantum Payload Generation...")
        
#     # 1. Create an empty list to hold our batch of threats
#     threat_batch = []
#     # 2. Loop through your flagged LEO debris and add them to the batch
#     # (This assumes your analytics engine already filtered for the danger radius)
#     for threat in threats:
#         # Format the text but DO NOT encrypt or transmit yet!
#         payload = f"Target: ISS (ZARYA) | Distance: {threat['DISTANCE_KM']}km"
#         threat_batch.append(payload)
#     # 3. Check if the batch has any threats inside it
#     if len(threat_batch) > 0:
#         print(f"[CRITICAL ALERT] {len(threat_batch)} Threats detected within the Danger Radius!")
#         print("-> Preparing batched threat data for C++ Kyber Post-Quantum Encryption...\n")
        
#         # 4. Join all 11 strings together into one massive payload, separated by " || "
#         batched_payload_string = " || ".join(threat_batch)
        
#         # 5. Hand the massive payload to the C++ core EXACTLY ONCE
#         # This triggers the #SecOps benchmark and Kyber algorithms only one time!
#         encrypted_payload = quantum_crypto.secure_threat_payload(batched_payload_string)
        
#         print("   [SECURE UPLINK] Batched Ciphertext generated successfully.")
        
#         # 6. Transmit the entire encrypted batch over the socket EXACTLY ONCE
#         network_transmitter.transmit_payload(batched_payload_string)
        
#     else:
#         print("[STATUS] No collision threats detected. Orbit is clear.")
        
#     # 5. Finalize the Python #SecOps Benchmarking
#     benchmark_end = time.time()
#     execution_time = benchmark_end - benchmark_start
#     print("\n=========================================================")
#     print(f" [#SecOps BENCHMARK] Total Python Orchestration: {round(execution_time, 4)} seconds.")
#     print("=========================================================\n")

# if __name__ == "__main__":
#     # Execute the asynchronous master loop
#     asyncio.run(run_edge_node())