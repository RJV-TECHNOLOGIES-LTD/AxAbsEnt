#!/bin/bash

################################################################################
# configure_gpu.sh — AxAbsEnt GPU Configuration Script
#
# This script detects NVIDIA GPUs, verifies CUDA & cuDNN installation,
# and configures environment variables for GPU acceleration.
#
# Supports: CUDA, cuDNN, PyTorch, TensorFlow, JAX
################################################################################

set -e

echo "🔧 Starting GPU configuration for AxAbsEnt..."

# ----------------------------
# Detect NVIDIA GPU presence
# ----------------------------

if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ NVIDIA GPU not detected (nvidia-smi not found)."
    echo "⚠️  Falling back to CPU-only mode."
    exit 0
fi

echo "✅ NVIDIA GPU detected:"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader


# ----------------------------
# Verify CUDA installation
# ----------------------------

if ! command -v nvcc &> /dev/null; then
    echo "❌ CUDA compiler (nvcc) not found."
    echo "➡️  Please install CUDA Toolkit from: https://developer.nvidia.com/cuda-downloads"
    exit 1
fi

CUDA_VERSION=$(nvcc --version | grep -o "release [0-9]*\.[0-9]*" | cut -d' ' -f2)
echo "✅ CUDA installed: v$CUDA_VERSION"


# ----------------------------
# Check cuDNN presence
# ----------------------------

CUDNN_PATH=$(find /usr/lib /usr/local/cuda/lib64 -name 'libcudnn*' 2>/dev/null | head -n 1)

if [ -z "$CUDNN_PATH" ]; then
    echo "❌ cuDNN not found in CUDA paths."
    echo "➡️  Please install cuDNN: https://developer.nvidia.com/cudnn"
    exit 1
else
    echo "✅ cuDNN found at: $CUDNN_PATH"
fi


# ----------------------------
# Set CUDA environment variables
# ----------------------------

export CUDA_HOME=/usr/local/cuda
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$CUDA_HOME/bin:$PATH

echo "🧠 CUDA environment variables configured."


# ----------------------------
# Run Python backend GPU check
# ----------------------------

echo -e "\n📦 Verifying Python GPU frameworks...\n"

python3 - <<EOF
import torch
import tensorflow as tf
import jax

print("PyTorch GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Not Available")
print("TensorFlow GPU:", tf.config.list_physical_devices('GPU'))
print("JAX GPU:", jax.devices())
EOF


# ----------------------------
# Final confirmation
# ----------------------------

echo -e "\n✅ AxAbsEnt GPU environment configured successfully."
