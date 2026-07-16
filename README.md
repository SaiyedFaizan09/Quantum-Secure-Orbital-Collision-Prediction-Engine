# Quantum-Secure Orbital Collision Prediction Engine 🛰️🔐

This project was developed for the **Def-Space Summer Internship 2026** at the **Bharat Space Education Research Centre (BSERC)**. It is a highly advanced, console-based simulation of an **Edge Computing Space Architecture**, specifically targeting the domains of Cyber Security, Digital Forensics, and Artificial Intelligence in Aerospace.

Instead of relying on Earth-based servers to calculate orbital threats, this software shifts the computational burden directly to a simulated Space Station (Edge Node). It ingests real-world orbital data, runs predictive spatial analytics, and secures the transmission of critical threat intelligence back to Earth using true hybrid Post-Quantum Cryptography.

## 🚀 Key Features

*   **Real-World Aerospace Data Ingestion:** Authenticates and pulls live "Two-Line Element" (TLE) orbital data for Low Earth Orbit (LEO) directly from the Space-Track.org API.
*   **Predictive Analytics (Spatial Proximity):** Parses TLE data to calculate exact X, Y, and Z spatial coordinates, applying mathematical distance filters to detect space debris entering the ISS "danger radius".
*   **True Hybrid Post-Quantum Cryptography:** Secures the telemetry downlink using **Kyber-768** (Key Encapsulation Mechanism) and **AES-256** (Symmetric Encryption) bridged natively in C++.
*   **Real-Time #SecOps Benchmarking:** Validates the system for radiation-hardened spacecraft hardware by actively tracking C++ execution time (in microseconds) and RAM footprints during quantum encryption.

## 📂 Architecture & Directory Structure

The system is split into two networked nodes communicating via local sockets to simulate the vast distance between Space and Earth:

*   **`space_station_node/`**: The Edge Node. Pulls API data, detects collisions, executes `#SecOps` hardware benchmarking, generates Kyber ciphertext, encrypts the payload with AES, and transmits.
*   **`ground_station_node/`**: The Receiving Node. Generates the initial Kyber key pair, decapsulates the matrix, decrypts the AES payload, and triggers the AI forensic reporter.
*   **`cpp_core/`**: Contains the raw C++ cryptographic algorithms (`liboqs` and `tiny-AES-c`) and the `pybind11` wrapper scripts.
*   **`data/`**: Caches the raw TLE JSON data locally to adhere to Space-Track API throttling limits (max 30 requests per minute).
*   **`logs/`**: Securely archives the Gemini-generated AI forensic reports.
*   **`build/`**: The CMake output directory for the compiled `.pyd` Python binaries.

## ⚙️ Prerequisites and Dependencies

To compile and run this true mathematical simulation on your local machine, you must have the following installed:

1. **Python 3.13** (or a compatible 3.x version)
2. **Microsoft Visual Studio Build Tools** (Requires the "x64 Native Tools Command Prompt for VS" for C++ compilation)
3. **CMake** (Added to your system PATH)
4. **C++ Libraries:**
    *   [liboqs](https://github.com/open-quantum-safe/liboqs): Open Quantum Safe library for the Kyber-768 algorithm (Must be compiled and linked on your system).
    *   [tiny-AES-c](https://github.com/kokke/tiny-AES-c): The `aes.h` and `aes.c` files must be placed inside the `cpp_core/` directories.
5. **API Accounts:**
    *   A registered account at [Space-Track.org](https://www.space-track.org/) for live orbital data.

## 🛠️ Setup and Installation Process

**1. Clone the Repository**
```bash
git clone https://github.com/YourUsername/quantum_orbital_engine.git
cd quantum_orbital_engine
2. Configure Environment Variables (.env) Create a .env file at the root of the project directory. Do not commit this file to GitHub! Add the following credentials:
# Space-Track Credentials
SPACE_TRACK_USERNAME=your_email@domain.com
SPACE_TRACK_PASSWORD=your_password

# Generative AI Key
GEMINI_API_KEY=your_gemini_key_here
3. Install Python Dependencies Install the necessary Python bridges and AI tools using PIP:
pip install python-dotenv google-generativeai pybind11
4. Compile the C++ Cryptographic Cores Because this architecture mixes pure C (tiny-AES-c) with C++ (liboqs and pybind11), the headers utilize extern "C" blocks to prevent C++ name mangling.
Open your x64 Native Tools Command Prompt for VS, navigate to the project's root build/ directory, and execute the CMake blueprint:
cd build
cmake ..
cmake --build .
(Note: This will generate quantum_crypto.pyd and quantum_earth.pyd inside build/Debug/).
🚀 How to Run the Simulation
To execute the end-to-end two-way cryptographic handshake, you must run both nodes simultaneously.
Terminal 1: Start Earth Ground Control
python -m ground_station_node.main_ground
Earth will stand by, generate the true Kyber-768 key matrix, and listen on the socket.
Terminal 2: Start the Space Station Edge Node
python -m space_station_node.main_edge
The Edge Node will ingest the TLE data, detect collisions, execute the true C++ hardware footprint benchmark, mathematically scramble the alert using Earth's key, and beam it down.
Once successfully decrypted, Ground Control will output the #ThreatIntelligence and save a newly generated Gemini AI Forensic Report directly to the logs/ directory!
