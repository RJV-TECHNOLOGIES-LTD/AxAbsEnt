# scripts/simulation/run_simulations.py

"""
AxAbsEnt Simulation Runner

Executes selected simulation modules in batch:
- Parameter Sweep
- Particle Collision
- Resonance Detection
- Quantum Field Propagation
- Cosmological Simulation (optional)

Supports:
- Local or distributed execution
- GPU acceleration where available
- Logging and CSV export of results
"""

import os
import subprocess
import argparse
import datetime

# ----------------------------
# Available Simulations
# ----------------------------

SIMULATION_SCRIPTS = {
    "parameter_sweep": "scripts/simulation/parameter_sweep.py",
    "particle_collision": "examples/simulation/particle_collision.py",
    "resonance_detection": "examples/simulation/resonance_detection.py",
    "quantum_field": "examples/simulation/quantum_field_simulation.py",
    "cosmological": "examples/simulation/cosmological_simulation.py"
}

# ----------------------------
# Argument Parser
# ----------------------------

parser = argparse.ArgumentParser(description="AxAbsEnt Simulation Runner")
parser.add_argument(
    "--all", action="store_true", help="Run all simulations in order"
)
parser.add_argument(
    "--sim", choices=SIMULATION_SCRIPTS.keys(), help="Run a specific simulation"
)
parser.add_argument(
    "--log", action="store_true", help="Log outputs to file (in ./logs/)"
)
args = parser.parse_args()


# ----------------------------
# Setup Output Logging
# ----------------------------

def get_log_path(script_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name = os.path.basename(script_name).replace(".py", "")
    os.makedirs("logs", exist_ok=True)
    return f"logs/{name}_{timestamp}.log"


# ----------------------------
# Execute Simulation Script
# ----------------------------

def run_script(script_path):
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return

    log_file = get_log_path(script_path) if args.log else None
    command = ["python", script_path]

    print(f"\n🚀 Running: {script_path}")
    if log_file:
        print(f"📝 Logging to: {log_file}")
        with open(log_file, "w") as f:
            subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)
    else:
        subprocess.run(command)


# ----------------------------
# Run All or Selected Simulations
# ----------------------------

if args.all:
    for sim_name, sim_path in SIMULATION_SCRIPTS.items():
        run_script(sim_path)
elif args.sim:
    run_script(SIMULATION_SCRIPTS[args.sim])
else:
    parser.print_help()
