# cpp/examples/CMakeLists.txt

cmake_minimum_required(VERSION 3.18)
project(axabsent_examples LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include core headers
include_directories(${CMAKE_SOURCE_DIR}/include)

# Link to core and simulation libraries
link_directories(${CMAKE_BINARY_DIR}/lib)

# Absolute Interaction Example
add_executable(basic_interaction basic_interaction.cpp)
target_link_libraries(basic_interaction PRIVATE axabsent_core_lib)

# Force Emergence Example
add_executable(force_emergence force_emergence.cpp)
target_link_libraries(force_emergence PRIVATE axabsent_core_lib axabsent_simulation_lib)

# Set output directories
set_target_properties(basic_interaction PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

set_target_properties(force_emergence PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

# Print info
message(STATUS "C++ examples built: basic_interaction, force_emergence")
