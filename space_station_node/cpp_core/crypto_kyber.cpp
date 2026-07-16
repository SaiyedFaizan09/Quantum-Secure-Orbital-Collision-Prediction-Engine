#include <vector>
#include <string>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <chrono> 
#include <oqs/oqs.h>
extern "C" {
    #include "aes.h"
}

std::string perform_aes_encryption(const std::string& plaintext, uint8_t* shared_secret);

std::string encrypt_kyber_payload(const std::string& threat_data, const std::string& earth_public_key) {
    std::cout << "\n=========================================================" << std::endl;
    std::cout << " [#SecOps] HYBRID POST-QUANTUM CRYPTOGRAPHY INITIATED" << std::endl;
    std::cout << "=========================================================" << std::endl;
    
    OQS_KEM *kem = OQS_KEM_new(OQS_KEM_alg_kyber_768);
    if (kem == NULL) return "[ERROR] Kyber-768 algorithm failed to load.";

    // Allocate memory for the KEM outputs
    uint8_t *ciphertext = (uint8_t *)malloc(kem->length_ciphertext);
    uint8_t *shared_secret = (uint8_t *)malloc(kem->length_shared_secret);
    
    // We convert Earth's Public Key string directly into a binary format for the matrix
    uint8_t *public_key = (uint8_t *)earth_public_key.data(); 

    std::cout << "[ENCRYPTION] Encapsulating shared secret using Earth's Public Key..." << std::endl;

    // --- REAL EXECUTION TIME TRACKING START ---
    auto start_time = std::chrono::high_resolution_clock::now();
    
    // Generate the shared_secret!
    OQS_KEM_encaps(kem, ciphertext, shared_secret, public_key);
    
    auto end_time = std::chrono::high_resolution_clock::now();
    // --- REAL EXECUTION TIME TRACKING END ---

    auto duration_micros = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();
    std::cout << "[#SecOps] METRIC: Kyber Matrix Multiplication completed in EXACTLY " << duration_micros << " microseconds." << std::endl;

    // --- AES ENCRYPTION INTEGRATION ---
    std::cout << "[ENCRYPTION] Initializing AES-256 Cipher using the Kyber Shared Secret..." << std::endl;
    std::cout << "[ENCRYPTION] Scrambling batched threat data payload..." << std::endl;
    
    // TRIGGER THE TRUE AES ENCRYPTION!
    std::string aes_scrambled_data = perform_aes_encryption(threat_data, shared_secret);

    // Format the TRUE Kyber Ciphertext for transmission
    std::stringstream kyber_output;
    kyber_output << "0xQSEC_";
    
    // --> FIX: Change '32' to 'kem->length_ciphertext' <--
    for (size_t i = 0; i < kem->length_ciphertext; i++) {
        kyber_output << std::hex << std::setw(2) << std::setfill('0') << (int)ciphertext[i];
    }

    std::cout << "[#SecOps] METRIC: Freeing memory footprint to preserve Spacecraft RAM..." << std::endl;
    OQS_KEM_free(kem);
    free(ciphertext);
    free(shared_secret);
    // Note: We do NOT free public_key here because it is owned by the Python string!

    std::cout << "=========================================================\n" << std::endl;
    
    // Return the massive double-payload: Kyber Key + AES Text
    return kyber_output.str() + " || " + aes_scrambled_data;
}

std::string perform_aes_encryption(const std::string& plaintext, uint8_t* shared_secret) {
    // 1. Calculate PKCS7 padding to make the text a multiple of 16 bytes
    size_t padded_len = plaintext.length() + (16 - (plaintext.length() % 16));
    uint8_t padding_val = 16 - (plaintext.length() % 16);
    
    std::vector<uint8_t> buffer(plaintext.begin(), plaintext.end());
    buffer.resize(padded_len, padding_val); // Apply the padding

    // 2. Initialize AES-256-CBC Cipher
    struct AES_ctx ctx;
    // We use a static Initialization Vector (IV) for this simulation
    uint8_t iv[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
    
    AES_init_ctx_iv(&ctx, shared_secret, iv);
    
    // 3. Encrypt the buffer!
    AES_CBC_encrypt_buffer(&ctx, buffer.data(), padded_len);

    // 4. Convert the scrambled binary bytes into a safe Hex string
    std::stringstream ss;
    ss << "0xAES_";
    for(size_t i = 0; i < padded_len; i++) {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)buffer[i];
    }
    return ss.str();
}
// #include <string>
// #include <iostream>
// #include <sstream>
// #include <iomanip>
// #include <chrono> // Standard C++ library for high-resolution time tracking
// #include <oqs/oqs.h>

// std::string encrypt_kyber_payload(const std::string& threat_data) {
//     std::cout << "\n=========================================================" << std::endl;
//     std::cout << " [#SecOps] POST-QUANTUM CRYPTOGRAPHY INITIATED" << std::endl;
//     std::cout << "=========================================================" << std::endl;
    
//     OQS_KEM *kem = OQS_KEM_new(OQS_KEM_alg_kyber_768);
//     if (kem == NULL) {
//         return "[ERROR] Kyber-768 algorithm failed to load.";
//     }

//     std::cout << "[SYSTEM] Algorithm: " << kem->method_name << " loaded successfully." << std::endl;
    
//     // Real metric pulled directly from the library's active configuration
//     std::cout << "[#SecOps] METRIC: Actively Allocating " << kem->length_public_key << " bytes for Public Key..." << std::endl;

//     uint8_t *public_key = (uint8_t *)malloc(kem->length_public_key);
//     uint8_t *secret_key = (uint8_t *)malloc(kem->length_secret_key);
//     uint8_t *ciphertext = (uint8_t *)malloc(kem->length_ciphertext);
//     uint8_t *shared_secret = (uint8_t *)malloc(kem->length_shared_secret);

//     std::cout << "[ENCRYPTION] Generating Randomized Lattice-Based Key Pair..." << std::endl;
//     OQS_KEM_keypair(kem, public_key, secret_key);
    
//     std::cout << "[ENCRYPTION] Encapsulating threat payload using Public Key..." << std::endl;

//     // --- REAL EXECUTION TIME TRACKING START ---
//     auto start_time = std::chrono::high_resolution_clock::now();
    
//     OQS_KEM_encaps(kem, ciphertext, shared_secret, public_key);
    
//     auto end_time = std::chrono::high_resolution_clock::now();
//     // --- REAL EXECUTION TIME TRACKING END ---

//     // Calculate exact duration in microseconds
//     auto duration_micros = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();
//     std::cout << "[#SecOps] METRIC: Heavy Matrix Multiplication completed in EXACTLY " << duration_micros << " microseconds." << std::endl;

//     std::stringstream secure_output;
//     secure_output << "0xQSEC_";
//     for (size_t i = 0; i < 32; i++) {
//         secure_output << std::hex << std::setw(2) << std::setfill('0') << (int)ciphertext[i];
//     }
//     secure_output << "_ENDQ";

//     std::cout << "[#SecOps] METRIC: Freeing memory footprint to preserve Spacecraft RAM..." << std::endl;
//     OQS_KEM_free(kem);
//     free(public_key);
//     free(secret_key);
//     free(ciphertext);
//     free(shared_secret);

//     std::cout << "=========================================================\n" << std::endl;
    
//     return secure_output.str();
// }