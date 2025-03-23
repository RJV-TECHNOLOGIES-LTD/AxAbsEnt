# src/axabsent/simulation/results.py

import os
import json
from datetime import datetime
from typing import List, Dict, Any

RESULTS_DIR = os.path.join(os.getcwd(), "data", "simulation_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

def save_simulation_result(data: Dict[str, Any], label: str = "simulation"):
    """
    Saves simulation result as a JSON file in the results directory.
    The file is named with a timestamp and label.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{label}_{timestamp}.json"
    filepath = os.path.join(RESULTS_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return filename

def list_simulation_results() -> List[str]:
    """
    Returns a list of all result filenames in the simulation results directory.
    """
    if not os.path.exists(RESULTS_DIR):
        return []
    return sorted([
        f for f in os.listdir(RESULTS_DIR)
        if f.endswith(".json")
    ])

def load_simulation_result(filename: str) -> Dict[str, Any]:
    """
    Loads a specific simulation result file by name.
    Raises FileNotFoundError if the file does not exist.
    """
    filepath = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Result file not found: {filename}")

    with open(filepath, "r") as f:
        return json.load(f)
