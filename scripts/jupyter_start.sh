#!/bin/bash
echo "🚀 Launching AxAbsEnt JupyterLab..."
jupyter lab --notebook-dir=notebooks --port=8888 --ip=0.0.0.0 --no-browser --allow-root
