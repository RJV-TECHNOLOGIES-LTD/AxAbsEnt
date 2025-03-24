#!/bin/bash
# Unix build script for AxAbsEnt C++ code
mkdir -p build
cmake -S cpp -B build
cmake --build build --config Release
