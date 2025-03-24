#!/bin/bash
# Universal Build Script for OmegaInfinity_CodexDecoder
echo "Starting build for all platforms..."

# Windows
echo "[Windows] Building .exe..."
pyinstaller --onefile --name OmegaInfinity_CodexDecoder ricardo_codex.py

# Linux
echo "[Linux] Building native ELF binary..."
pyinstaller --onefile --name OmegaInfinity_CodexDecoder_Linux ricardo_codex.py

# macOS
echo "[macOS] Building .command script..."
cp ricardo_codex.py OmegaInfinity_CodexDecoder_Mac.command
chmod +x OmegaInfinity_CodexDecoder_Mac.command

echo "Build complete."