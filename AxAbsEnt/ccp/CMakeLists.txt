# cpp/CMakeLists.txt

cmake_minimum_required(VERSION 3.18)
project(AxAbsEnt_CPP LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set output directories
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# ------------------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------------------

# Eigen (header-only)
find_package(Eigen3 REQUIRED)

# pybind11 for bindings
find_package(pybind11 REQUIRED)

# Python (for bindings)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# ------------------------------------------------------------------------------
# Include paths
# ------------------------------------------------------------------------------

include_directories(${CMAKE_SOURCE_DIR}/include)

# ------------------------------------------------------------------------------
# Core Library
# ------------------------------------------------------------------------------

file(GLOB_RECURSE CORE_SRC
    src/core/*.cpp
)
add_library(axabsent_core_lib STATIC ${CORE_SRC})
target_link_libraries(axabsent_core_lib PRIVATE Eigen3::Eigen)

# ------------------------------------------------------------------------------
# Simulation Library
# ------------------------------------------------------------------------------

file(GLOB_RECURSE SIM_SRC
    src/simulation/*.cpp
)
add_library(axabsent_simulation_lib STATIC ${SIM_SRC})
target_link_libraries(axabsent_simulation_lib PRIVATE axabsent_core_lib Eigen3::Eigen)

# ------------------------------------------------------------------------------
# Python Bindings
# ------------------------------------------------------------------------------

add_subdirectory(bindings)

# ------------------------------------------------------------------------------
# Examples
# ------------------------------------------------------------------------------

add_subdirectory(examples)

# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------

add_subdirectory(tests)

# ------------------------------------------------------------------------------
# Optional CUDA Build (if exists)
# ------------------------------------------------------------------------------

if(EXISTS "${CMAKE_SOURCE_DIR}/cuda/CMakeLists.txt")
    enable_language(CUDA)
    add_subdirectory(cuda)
endif()
