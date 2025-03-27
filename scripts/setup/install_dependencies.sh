#!/bin/bash

################################################################################
# install_dependencies.sh — AxAbsEnt System Dependency Installer
#
# Installs all required Python, C++, GPU, and documentation dependencies
# for running, developing, and extending the AxAbsEnt Unified Framework.
#
# Supports:
# - Pip or Conda environments
# - GPU/CUDA optional dependencies
# - Scientific and simulation libraries
################################################################################

set -e

echo -e "\n🔧 Starting AxAbsEnt dependency installation...\n"

# ----------------------------
# Terminal color definitions
# ----------------------------
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# ----------------------------
# Detect Python environment
# ----------------------------
if command -v conda &> /dev/null; then
    echo -e "${GREEN}✔ Conda detected. Using Conda environment.${NC}"
    conda install -y --file requirements.txt
    conda install -y --file requirements-dev.txt
    conda install -y --file requirements-docs.txt
else
    echo -e "${YELLOW}⚠ Conda not found. Falling back to pip.${NC}"
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -r requirements-docs.txt
fi

# ----------------------------
# Install C++/CMake dependencies
# ----------------------------
echo -e "\n🔨 Installing C++ toolchain..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update
    sudo apt install -y build-essential cmake libeigen3-dev
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install cmake eigen
else
    echo -e "${RED}❌ Unsupported OS for C++ dependency setup.${NC}"
    exit 1
fi
echo -e "${GREEN}✔ C++ dependencies installed.${NC}"


# ----------------------------
# Optional: Check for GPU dependencies
# ----------------------------
if command -v nvidia-smi &> /dev/null; then
    echo -e "\n🧠 NVIDIA GPU detected. Verifying CUDA support..."

    if ! command -v nvcc &> /dev/null; then
        echo -e "${RED}❌ CUDA not found. Please install from https://developer.nvidia.com/cuda-downloads${NC}"
    else
        echo -e "${GREEN}✔ CUDA available. GPU acceleration supported.${NC}"
    fi
else
    echo -e "${YELLOW}⚠ No NVIDIA GPU detected. Skipping GPU-specific libraries.${NC}"
fi


# ----------------------------
# Success
# ----------------------------
echo -e "\n✅ ${GREEN}All AxAbsEnt dependencies installed successfully.${NC}"
