# scripts/visualization/generate_visualizations.py

"""
AxAbsEnt Visualization Generator

Runs all visualization scripts to produce:
- Cross-absolute interaction diagrams
- Emergent force field maps
- Information flow networks
- Multidimensional PCA projections

All outputs saved to: results/diagrams/

Usage:
    python scripts/visualization/generate_visualizations.py [--all | --viz force_map]
"""

import os
import argparse
import subprocess
import datetime

# ----------------------------
# Script Map
# ----------------------------

VISUALIZATION_SCRIPTS = {
    "interaction_graph": "scripts/visualization/create_interaction_diagrams.py",
    "force_map": "scripts/visualization/generate_force_maps.py",
    "information_flow": "examples/visualization/information_flow_diagram.py",
    "multidimensional": "examples/visualization/multidimensional_visualization.py"
}

# ----------------------------
# Argument Parsing
# ----------------------------

parser = argparse.ArgumentParser(description="AxAbsEnt Visualization Runner")
parser.add_argument(
    "--all", action="store_true", help="Run all visualizations"
)
parser.add_argument(
    "--viz", choices=VISUALIZATION_SCRIPTS.keys(), help="Run a specific visualization"
)
args = parser.parse_args()

# ----------------------------
# Run Script
# ----------------------------

def run_visualization(script_path):
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return
    print(f"🖼️  Running: {script_path}")
    subprocess.run(["python", script_path])


# ----------------------------
# Main Execution
# ----------------------------

print("\n🎨 AxAbsEnt Unified Visualization Suite")
print("📂 Output Directory: results/diagrams/\n")

if args.all:
    for name, script in VISUALIZATION_SCRIPTS.items():
        run_visualization(script)
elif args.viz:
    run_visualization(VISUALIZATION_SCRIPTS[args.viz])
else:
    parser.print_help()
