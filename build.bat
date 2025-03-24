@echo off
REM Windows build script for AxAbsEnt C++ code
mkdir build
cmake -S cpp -B build
cmake --build build --config Release
