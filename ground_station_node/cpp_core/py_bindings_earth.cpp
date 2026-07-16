#include <pybind11/pybind11.h>
#include <string>
#include <iostream>

namespace py = pybind11;

std::string generate_earth_keys();
std::string decrypt_hybrid_payload(const std::string& kyber_ciphertext_hex, const std::string& aes_payload);

PYBIND11_MODULE(quantum_earth, m) {
    m.doc() = "Earth Ground Station Quantum Decryption Core";
    
    // We use a lambda function to wrap the C++ string into a raw Python bytes object
    m.def("generate_earth_keys", []() {
        return py::bytes(generate_earth_keys());
    }, "Generates the Kyber-768 key pair and returns the Public Key.");
    
    m.def("decrypt_hybrid_payload", &decrypt_hybrid_payload, "Decapsulates the Kyber ciphertext and unlocks the AES payload.");
}