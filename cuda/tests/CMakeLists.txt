# CMake configuration for CUDA test suite (AxAbsEnt)

cmake_minimum_required(VERSION 3.21)

project(axabsent_cuda_tests LANGUAGES CXX CUDA)

# Enable CUDA
enable_language(CUDA)

# GoogleTest (optional: header-only mode or FetchContent)
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/release-1.12.1.zip
)
FetchContent_MakeAvailable(googletest)

include_directories(
  ${CMAKE_SOURCE_DIR}/include
  ${CMAKE_SOURCE_DIR}/../include
  ${CMAKE_SOURCE_DIR}/../lib/eigen
  ${CMAKE_SOURCE_DIR}/../lib/pybind11/include
)

# Set paths
set(TEST_SOURCES
  test_force_extraction.cu
  test_tensor_operations.cu
  test_simulation.cu
)

# Build test targets
foreach(TEST_FILE ${TEST_SOURCES})
  get_filename_component(TEST_NAME ${TEST_FILE} NAME_WE)
  add_executable(${TEST_NAME} ${TEST_FILE})

  target_link_libraries(${TEST_NAME}
    axabsent_cuda         # GPU logic
    axabsent_core_cpp     # Shared simulation logic
    gtest gtest_main
    cuda cudart
  )

  set_target_properties(${TEST_NAME} PROPERTIES
    CUDA_STANDARD 17
    CUDA_SEPARABLE_COMPILATION ON
    POSITION_INDEPENDENT_CODE ON
  )

  add_test(NAME ${TEST_NAME} COMMAND ${TEST_NAME})
endforeach()
