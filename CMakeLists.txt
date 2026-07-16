cmake_minimum_required(VERSION 3.14)
project(QuantumOrbitalEngine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

execute_process(
    COMMAND python -c "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
find_package(pybind11 CONFIG REQUIRED)

# --- NEW: LINK THE TRUE LIBOQS POST-QUANTUM LIBRARY ---
# Update this path to where your liboqs folder is located
set(OQS_DIR "C:/Faizan Document/BSERC/Def-Space Summer Internship 2026/Project/quantum_orbital_engine/liboqs")

# Tell CMake where the oqs.h header file is
include_directories(${OQS_DIR}/build/include)

# Tell CMake where the compiled static library is
link_directories(${OQS_DIR}/build/lib/Release)

pybind11_add_module(quantum_crypto 
    space_station_node/cpp_core/crypto_kyber.cpp
    space_station_node/cpp_core/hardware_monitor.cpp
    space_station_node/cpp_core/py_bindings.cpp
    space_station_node/cpp_core/aes.c
)
# Create the Python module for the Earth Ground Station
pybind11_add_module(quantum_earth 
    ground_station_node/cpp_core/py_bindings_earth.cpp 
    ground_station_node/cpp_core/crypto_earth.cpp
    ground_station_node/cpp_core/aes.c
)

# This tells the linker to attach the Kyber math library to the Earth module
target_link_libraries(quantum_earth PRIVATE oqs) 
# Link the OQS static library to your Python extension
target_link_libraries(quantum_crypto PRIVATE oqs)