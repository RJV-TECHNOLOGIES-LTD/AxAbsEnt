#!/bin/bash

################################################################################
# setup_environment.sh — AxAbsEnt Unified Setup Entrypoint
#
# This script initializes the development environment:
# - Creates and activates Python virtualenv or Conda env
# - Installs all project dependencies
# - Optionally configures GPU acceleration
# - Verifies that AxAbsEnt is ready for use
################################################################################

set -e

echo -e "\n🚀 Initializing AxAbsEnt Environment...\n"

# ----------------------------
# Configurable Parameters
# ----------------------------
ENV_NAME="axabsent"
PYTHON_VERSION="3.11"
USE_CONDA=false    # Set to true if you want to enforce conda
USE_GPU=true       # Set to false to skip GPU configuration


# ----------------------------
# Detect environment type
# ----------------------------

if command -v conda &> /dev/null && [ "$USE_CONDA" = true ]; then
    echo "📦 Conda detected. Creating environment: $ENV_NAME"
    conda create -y -n "$ENV_NAME" python="$PYTHON_VERSION"
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate "$ENV_NAME"
else
    echo "📦 Creating Python virtual environment: .venv"
    python"$PYTHON_VERSION" -m venv .venv
    source .venv/bin/activate
fi

echo "✅ Environment activated."


# ----------------------------
# Step 1: Install dependencies
# ----------------------------

echo -e "\n📦 Installing dependencies..."
bash scripts/setup/install_dependencies.sh


# ----------------------------
# Step 2: Optional GPU Configuration
# ----------------------------

if [ "$USE_GPU" = true ]; then
    echo -e "\n🔧 Configuring GPU (if available)..."
    bash scripts/setup/configure_gpu.sh
else
    echo "⚠️ GPU setup skipped (USE_GPU=false)"
fi


# ----------------------------
# Step 3: Environment Summary
# ----------------------------

echo -e "\n📄 Python Version:"
python --version

echo -e "\n📄 Installed Packages:"
pip list | grep -E 'torch|jax|tensorflow|axabsent' || echo "ℹ️  No major ML libs yet."

echo -e "\n✅ AxAbsEnt environment setup complete."
echo "You may now run: python -m axabsent"
