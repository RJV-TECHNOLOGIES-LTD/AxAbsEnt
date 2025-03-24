# cpp/bindings/CMakeLists.txt

cmake_minimum_required(VERSION 3.18)
project(axabsent_bindings LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python and pybind11
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

# Include core C++ headers
include_directories(${CMAKE_SOURCE_DIR}/include)

# Define binding targets
add_library(axabsent_core_bindings MODULE
    absolute_bindings.cpp
    interaction_bindings.cpp
    simulation_bindings.cpp
)

# Link with core AxAbsEnt C++ libraries
target_link_libraries(axabsent_core_bindings
    PRIVATE
    pybind11::module
    axabsent_core_lib             # Core C++ logic (absolute, interaction)
    axabsent_simulation_lib       # Simulation logic
)

# Set output properties
set_target_properties(axabsent_core_bindings PROPERTIES
    PREFIX ""                           # No 'lib' prefix
    SUFFIX "${Python3_EXTENSION_SUFFIX}"  # Use correct .so/.pyd extension
)

# Set RPATH for shared libraries
if(APPLE)
    set_target_properties(axabsent_core_bindings PROPERTIES INSTALL_RPATH "@loader_path")
else()
    set_target_properties(axabsent_core_bindings PROPERTIES INSTALL_RPATH "$ORIGIN")
endif()

# Output build info
message(STATUS "Binding module: axabsent_core_bindings")
message(STATUS "Python version: ${Python3_VERSION}")
