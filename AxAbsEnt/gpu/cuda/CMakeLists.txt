cmake_minimum_required(VERSION 3.21)
project(axabsent_cuda LANGUAGES C CXX CUDA)

# Set CUDA Architecture for A100/H100 and fallback GPUs
set(CMAKE_CUDA_ARCHITECTURES 75 80 86)

# CUDA Requirements
enable_language(CUDA)
find_package(CUDA REQUIRED)

# Output directories
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Include paths
include_directories(
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/../cpp/include
    ${CMAKE_SOURCE_DIR}/../cpp/lib/eigen
    ${CMAKE_SOURCE_DIR}/../cpp/lib/pybind11/include
)

# Source files
file(GLOB_RECURSE CUDA_SOURCES
    ${CMAKE_SOURCE_DIR}/src/*.cu
)

file(GLOB_RECURSE CUDA_HEADERS
    ${CMAKE_SOURCE_DIR}/include/axabsent_cuda/*.cuh
)

# Shared CUDA Library
add_library(axabsent_cuda SHARED ${CUDA_SOURCES} ${CUDA_HEADERS})

# Compiler flags
set_target_properties(axabsent_cuda PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
    CUDA_STANDARD 17
    POSITION_INDEPENDENT_CODE ON
)

# CUDA-specific flags
target_compile_options(axabsent_cuda PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:
        -O3
        --use_fast_math
        -Xcompiler=-fPIC
    >
)

# Link with required C++ simulation and tensor logic
target_link_libraries(axabsent_cuda
    axabsent_core_cpp       # From cpp/src/core/
    axabsent_tensor_cpp     # From cpp/src/mathematics/
)

# Installation targets
install(TARGETS axabsent_cuda
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# Export include headers
install(DIRECTORY include/ DESTINATION include FILES_MATCHING PATTERN "*.cuh")
