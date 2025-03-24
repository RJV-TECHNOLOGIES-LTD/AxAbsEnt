# cpp/tests/CMakeLists.txt

cmake_minimum_required(VERSION 3.18)

project(AxAbsEnt_Tests LANGUAGES CXX)

enable_testing()

# ------------------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------------------

# Find GoogleTest (required for C++ unit testing)
find_package(GTest REQUIRED)

# ------------------------------------------------------------------------------
# Include Paths
# ------------------------------------------------------------------------------

include_directories(
    ${CMAKE_SOURCE_DIR}/include
)

# ------------------------------------------------------------------------------
# Test Sources
# ------------------------------------------------------------------------------

file(GLOB_RECURSE TEST_SOURCES
    test_core.cpp
    test_mathematics.cpp
    test_simulation.cpp
)

# ------------------------------------------------------------------------------
# Test Executable
# ------------------------------------------------------------------------------

add_executable(axabsent_cpp_tests ${TEST_SOURCES})

target_link_libraries(axabsent_cpp_tests
    PRIVATE
    GTest::gtest
    GTest::gtest_main
    axabsent_core_lib
    axabsent_simulation_lib
    Eigen3::Eigen
)

# ------------------------------------------------------------------------------
# Register Tests
# ------------------------------------------------------------------------------

include(GoogleTest)
gtest_discover_tests(axabsent_cpp_tests)

# ------------------------------------------------------------------------------
# Output Info
# ------------------------------------------------------------------------------

message(STATUS "AxAbsEnt C++ tests enabled")
