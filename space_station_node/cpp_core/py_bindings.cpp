#include <pybind11/pybind11.h>
#include <string>
#include <iostream>

namespace py = pybind11;

// Forward declarations to link our other two C++ files
std::string encrypt_kyber_payload(const std::string& threat_data, const std::string& earth_public_key);
void run_secops_hardware_benchmark();

// The main bridge function now accepts TWO inputs
std::string secure_threat_payload(const std::string& threat_data, const std::string& earth_public_key) {
    std::cout << "\n[C++ CORE] Initiating True Two-Way Hybrid Encryption..." << std::endl;
    
    // 1. Trigger the Hardware Constraint Benchmarking (#SecOps)
    run_secops_hardware_benchmark();
    
    // 2. Execute the heavy Kyber encapsulation AND the AES encryption
    std::string hybrid_ciphertext = encrypt_kyber_payload(threat_data, earth_public_key);
    
    std::cout << "[C++ CORE] Hybrid Payload Encrypted Successfully." << std::endl;
    
    // 3. Return the massive double-payload back to Python
    return hybrid_ciphertext;
}

PYBIND11_MODULE(quantum_crypto, m) {
    m.doc() = "Quantum-Secure Cryptography and SecOps Benchmarking Core";
    
    // We use a lambda to accept Python bytes, convert to C++ string, and trigger the core
    m.def("secure_threat_payload", [](const std::string& threat_data, py::bytes earth_public_key) {
        std::string pk_str(earth_public_key);
        return secure_threat_payload(threat_data, pk_str);
    }, "Encrypts threat data using AES and Kyber.");
}
// #include <pybind11/pybind11.h>
// #include <string>
// #include <iostream>

// namespace py = pybind11;

// // Forward declarations to link our other two C++ files
// std::string encrypt_kyber_payload(const std::string& threat_data);
// void run_secops_hardware_benchmark();

// // The main bridge function called by your Python main_edge.py script
// std::string secure_threat_payload(const std::string& threat_data, const std::string& earth_public_key) {
//     std::cout << "\n[C++ CORE] Initiating Quantum-Resistant Encryption..." << std::endl;
    
//     // 1. Trigger the Hardware Constraint Benchmarking (#SecOps)
//     run_secops_hardware_benchmark();
    
//     // 2. Execute the heavy Kyber post-quantum cryptography
//     std::string ciphertext = encrypt_kyber_payload(threat_data);
    
//     std::cout << "[C++ CORE] Payload Encrypted Successfully." << std::endl;
    
//     // 3. Return the encrypted binary data to Python
//     return ciphertext;
// }

// // This macro creates the actual Python module named "quantum_crypto"
// PYBIND11_MODULE(quantum_crypto, m) {
//     m.doc() = "Quantum-Secure Cryptography and SecOps Benchmarking Core";
//     m.def("secure_threat_payload", &secure_threat_payload, "Encrypts collision threat data and benchmarks hardware.");
// }