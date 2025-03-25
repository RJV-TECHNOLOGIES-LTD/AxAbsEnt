# tools/exporters/report_generator.py

"""
AxAbsEnt Report Generator

Generates multi-section scientific reports from simulation or theoretical output.
Supports Markdown (.md) format for integration into publications, pipelines, or versioned archives.

Includes:
- Simulation config summary
- Force decomposition
- Entropy & curvature field stats
- Optional tensor visualization
"""

import os
import numpy as np
from datetime import datetime
from typing import Dict, Any
import matplotlib.pyplot as plt

def _generate_tensor_image(tensor: np.ndarray, path: str):
    plt.figure(figsize=(6, 4.5))
    plt.imshow(tensor, cmap='inferno', interpolation='nearest')
    plt.colorbar(label='Tensor Magnitude')
    plt.title("Tensor Field Visualization")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _format_table(title: str, data: Dict[str, Any]) -> str:
    output = [f"### {title}", "", "| Metric | Value |", "|--------|-------|"]
    for k, v in data.items():
        output.append(f"| {k} | {v} |")
    return "\n".join(output)


def generate_analysis_report(data: Dict[str, Any], output_path: str) -> None:
    """
    Generate a Markdown report file from unified model results.

    Args:
        data: {
            "title": str,
            "description": str,
            "config": dict,
            "results": dict,
            "tensor": np.ndarray (optional),
            "force_components": dict (optional),
            "entropy": float (optional),
            "curvature_trace": float (optional),
        }
        output_path: Target .md file path
    """
    lines = []

    title = data.get("title", "AxAbsEnt Simulation Report")
    desc = data.get("description", "This report summarizes the results of a simulation or force analysis.")
    timestamp = datetime.utcnow().isoformat() + "Z"

    lines.append(f"# {title}\n")
    lines.append(f"**Generated:** {timestamp}")
    lines.append(f"\n**Model:** Enhanced Mathematical Ontology of Absolute Nothingness\n")
    lines.append(f"## Description\n{desc}\n")

    # Configuration
    if "config" in data:
        lines.append(_format_table("Simulation Configuration", data["config"]))

    # Results
    if "results" in data:
        lines.append(_format_table("Results Summary", data["results"]))

    # Force components
    if "force_components" in data:
        lines.append(_format_table("Force Decomposition", data["force_components"]))

    # Optional entropy and curvature
    if "entropy" in data or "curvature_trace" in data:
        lines.append("## Projection Metrics")
        if "entropy" in data:
            lines.append(f"- **Entropy**: {data['entropy']:.6f}")
        if "curvature_trace" in data:
            lines.append(f"- **Curvature Trace**: {data['curvature_trace']:.6f}")
        lines.append("")

    # Tensor visualization
    if "tensor" in data and isinstance(data["tensor"], np.ndarray):
        image_path = output_path.replace(".md", "_tensor.png")
        _generate_tensor_image(data["tensor"], image_path)
        lines.append("## Tensor Visualization")
        lines.append(f"![Tensor Field]({os.path.basename(image_path)})\n")

    # Metadata
    lines.append("## Metadata")
    lines.append("```")
    lines.append(f"Generated: {timestamp}")
    lines.append("Ontology: Enhanced Mathematical Ontology of Absolute Nothingness")
    lines.append("Version: 1.0")
    lines.append("```")

    # Write to file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))
