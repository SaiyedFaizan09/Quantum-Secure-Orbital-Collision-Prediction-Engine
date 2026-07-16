#include <string>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <oqs/oqs.h>
extern "C" {
    #include "aes.h"
}

// We store the Earth's Private Key in local memory so it can be used later for decryption
static uint8_t *earth_secret_key = nullptr;
static OQS_KEM *kem = nullptr;

std::string perform_aes_decryption(std::string hex_ciphertext, uint8_t* shared_secret);
// 1. THE KEY GENERATOR
std::string generate_earth_keys() {
    std::cout << "\n=========================================================" << std::endl;
    std::cout << " [GROUND SEC-OPS] INITIALIZING KYBER-768 KEY EXCHANGE" << std::endl;
    std::cout << "=========================================================" << std::endl;

    kem = OQS_KEM_new(OQS_KEM_alg_kyber_768);
    if (kem == NULL) return "[ERROR] Kyber-768 algorithm failed to load.";

    uint8_t *public_key = (uint8_t *)malloc(kem->length_public_key);
    earth_secret_key = (uint8_t *)malloc(kem->length_secret_key);

    std::cout << "[SYSTEM] Generating Earth's Lattice-Based Key Pair..." << std::endl;
    
    // Mathematically generate the Public and Private keys
    OQS_KEM_keypair(kem, public_key, earth_secret_key);

    // Convert the Public Key to a string so Python can transmit it to Space
    std::string pk_string(reinterpret_cast<char*>(public_key), kem->length_public_key);
    
    free(public_key); // Free the public key from RAM, but keep the secret key!
    return pk_string;
}

// 2. THE PAYLOAD DECRYPTOR
std::string decrypt_hybrid_payload(const std::string& kyber_ciphertext_hex, const std::string& aes_payload) {
    std::cout << "\n[DECRYPTION] Hybrid Payload Received. Initiating Decapsulation..." << std::endl;

    if (earth_secret_key == nullptr || kem == nullptr) {
        return "[ERROR] Earth Private Key not found in memory!";
    }

    // Allocate memory for the recovered shared secret
    uint8_t *recovered_shared_secret = (uint8_t *)malloc(kem->length_shared_secret);
    
    // Note: In a true implementation, you must parse the hex string back into binary bytes here
    uint8_t *ciphertext_binary = (uint8_t *)kyber_ciphertext_hex.data();

    // --- TRUE QUANTUM DECAPSULATION MATH ---
    // 1. Remove the "0xQSEC_" prefix
    std::string clean_kyber_hex = kyber_ciphertext_hex;
    if(clean_kyber_hex.find("0xQSEC_") == 0) {
        clean_kyber_hex = clean_kyber_hex.substr(7);
    }
    
    // 2. Parse the Hex string back into the raw binary Matrix
    std::vector<uint8_t> kyber_binary_buffer;
    for(size_t i = 0; i < clean_kyber_hex.length(); i += 2) {
        std::string byteString = clean_kyber_hex.substr(i, 2);
        kyber_binary_buffer.push_back((uint8_t)strtol(byteString.c_str(), NULL, 16));
    }

    // 3. Decapsulate using the TRUE binary buffer!
    OQS_KEM_decaps(kem, recovered_shared_secret, kyber_binary_buffer.data(), earth_secret_key);

    std::cout << "[DECRYPTION] True Kyber Decapsulation Successful! Shared Secret Recovered." << std::endl;

    // --- AES DECRYPTION INTEGRATION ---
    std::cout << "[DECRYPTION] Initializing AES-256 Cipher using the recovered Shared Secret..." << std::endl;
    
    // TRIGGER THE TRUE AES DECRYPTION!
    std::string decrypted_threat_data = perform_aes_decryption(aes_payload, recovered_shared_secret);

    std::cout << "[SYSTEM] Freeing Earth Private Key to secure memory footprint..." << std::endl;
    free(earth_secret_key);
    free(recovered_shared_secret);
    OQS_KEM_free(kem);
    earth_secret_key = nullptr;

    std::cout << "=========================================================\n" << std::endl;
    
    return decrypted_threat_data;
}

std::string perform_aes_decryption(std::string hex_ciphertext, uint8_t* shared_secret) {
    // 1. Remove the "0xAES_" transmission prefix
    if(hex_ciphertext.find("0xAES_") == 0) {
        hex_ciphertext = hex_ciphertext.substr(6);
    }

    // 2. Convert the Hex string back into a binary buffer
    std::vector<uint8_t> buffer;
    for(size_t i = 0; i < hex_ciphertext.length(); i += 2) {
        std::string byteString = hex_ciphertext.substr(i, 2);
        buffer.push_back((uint8_t)strtol(byteString.c_str(), NULL, 16));
    }

    // 3. Initialize AES-256-CBC Cipher (Using the exact same IV as Space)
    struct AES_ctx ctx;
    uint8_t iv[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
    
    AES_init_ctx_iv(&ctx, shared_secret, iv);
    
    // 4. Decrypt the buffer!
    AES_CBC_decrypt_buffer(&ctx, buffer.data(), buffer.size());

    // 5. Remove the PKCS7 padding to reveal the true text
    uint8_t padding_val = buffer.back();
    buffer.resize(buffer.size() - padding_val);

    return std::string(buffer.begin(), buffer.end());
}