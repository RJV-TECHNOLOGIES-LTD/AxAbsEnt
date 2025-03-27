# tools/exporters/data_exporter.py

"""
AxAbsEnt Data Exporter

This module handles structured export of simulation, experimental, and interaction data
into standardized formats including JSON, CSV, and HDF5. Metadata is injected automatically
to preserve ontological traceability and reproducibility.

All output conforms to the Enhanced Mathematical Ontology of Absolute Nothingness.
"""

import os
import json
import csv
import numpy as np
import h5py
from datetime import datetime
from typing import Any, Dict, List

EXPORT_METADATA = {
    "version": "1.0",
    "model": "AxAbsEnt Unified Ontology",
    "timestamp": lambda: datetime.utcnow().isoformat() + "Z"
}

def _inject_metadata(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Attach timestamped metadata to any export dictionary."""
    meta = {
        "exported_at": EXPORT_METADATA["timestamp"](),
        "model_version": EXPORT_METADATA["version"],
        "model_identifier": EXPORT_METADATA["model"]
    }
    return {**meta, "data": payload}


def export_to_json(data: Dict[str, Any], path: str) -> None:
    """Export data to a JSON file with metadata."""
    export_payload = _inject_metadata(data)
    with open(path, 'w') as f:
        json.dump(export_payload, f, indent=4)


def export_to_csv(data: List[Dict[str, Any]], path: str) -> None:
    """Export a list of dictionaries to CSV format."""
    if not data:
        raise ValueError("No data to export.")
    keys = data[0].keys()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def export_to_hdf5(data: Dict[str, Any], path: str) -> None:
    """
    Export structured numerical data to HDF5 format.

    Only numpy arrays and scalars are allowed in values.
    Nested dictionaries are ignored unless flat-mapped beforehand.
    """
    with h5py.File(path, 'w') as f:
        meta_grp = f.create_group('metadata')
        meta_grp.attrs['exported_at'] = EXPORT_METADATA["timestamp"]()
        meta_grp.attrs['model_version'] = EXPORT_METADATA["version"]
        meta_grp.attrs['model_identifier'] = EXPORT_METADATA["model"]

        data_grp = f.create_group('data')
        for key, value in data.items():
            if isinstance(value, (int, float)):
                data_grp.attrs[key] = value
            elif isinstance(value, np.ndarray):
                data_grp.create_dataset(key, data=value)
            else:
                continue  # Skip unsupported or nested types


def export_simulation_data(data: Dict[str, Any], output_dir: str, base_filename: str) -> None:
    """
    Export AxAbsEnt simulation data into all formats:
    - JSON: human-readable structured data
    - CSV: flattened time-series or summary
    - HDF5: tensor and entropy fields

    Args:
        data: Dictionary containing structured simulation data
        output_dir: Target directory path
        base_filename: Base name (without extension) for exported files
    """
    os.makedirs(output_dir, exist_ok=True)

    # JSON
    json_path = os.path.join(output_dir, f"{base_filename}.json")
    export_to_json(data, json_path)

    # CSV (only if "timeseries" is present)
    if "timeseries" in data and isinstance(data["timeseries"], list):
        csv_path = os.path.join(output_dir, f"{base_filename}.csv")
        export_to_csv(data["timeseries"], csv_path)

    # HDF5 (for tensors, entropy fields, curvature maps, etc.)
    hdf5_path = os.path.join(output_dir, f"{base_filename}.h5")
    export_to_hdf5(data, hdf5_path)
