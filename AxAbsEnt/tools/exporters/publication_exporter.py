# tools/exporters/publication_exporter.py

"""
AxAbsEnt Publication Exporter

Generates scientific publication-ready documents (LaTeX or Markdown) from theory,
simulation, and force emergence results. Integrates mathematical equations, tensor data,
and ontology-based interpretations in structured export format.
"""

import os
from datetime import datetime
from typing import Dict, Any
import numpy as np

LATEX_TEMPLATE = r"""
\documentclass[11pt]{article}
\usepackage{amsmath, amssymb, graphicx, geometry}
\geometry{margin=1in}
\title{%s}
\author{RJV Technologies Ltd \\ AxAbsEnt System}
\date{%s}

\begin{document}
\maketitle

\section*{Abstract}
%s

\section*{Tensor Summary}
\begin{center}
\includegraphics[width=0.8\textwidth]{%s}
\end{center}

\section*{Key Outputs}
\begin{itemize}
%s
\end{itemize}

\section*{Metadata}
\begin{verbatim}
%s
\end{verbatim}

\end{document}
"""

MARKDOWN_TEMPLATE = """
# {title}

**Generated:** {timestamp}  
**System:** AxAbsEnt Unified Engine  

## Abstract  
{abstract}

## Tensor Visualization  
![Tensor Field]({tensor_path})

## Key Outputs  
{output_list}

## Metadata  
"""

def _tensor_to_image(tensor: np.ndarray, output_path: str):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6, 5))
    plt.imshow(tensor, cmap='plasma', interpolation='nearest')
    plt.colorbar(label='Tensor Field Intensity')
    plt.title("Tensor Field Visualization")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def _format_outputs(outputs: Dict[str, Any]) -> str:
    return "\n".join(
        f"\\item \\textbf{{{k}}}: {v}" for k, v in outputs.items()
    )

def _format_outputs_md(outputs: Dict[str, Any]) -> str:
    return "\n".join(
        f"- **{k}**: {v}" for k, v in outputs.items()
    )

def export_publication(data: Dict[str, Any], output_dir: str, base_filename: str = "axabsent_paper") -> None:
    """
    Generates a .tex and .md file with all relevant scientific content.

    Args:
        data: {
            "title": str,
            "abstract": str,
            "tensor": np.ndarray,
            "outputs": dict (name → value),
        }
        output_dir: Target directory path
        base_filename: File prefix for all exported files
    """
    os.makedirs(output_dir, exist_ok=True)

    # Generate tensor image
    tensor_path = os.path.join(output_dir, f"{base_filename}_tensor.png")
    if "tensor" in data and isinstance(data["tensor"], np.ndarray):
        _tensor_to_image(data["tensor"], tensor_path)
    else:
        tensor_path = "tensor_placeholder.png"

    # Timestamp & metadata
    timestamp = datetime.utcnow().isoformat() + "Z"
    metadata = {
        "Generated": timestamp,
        "Ontology": "Enhanced Mathematical Ontology of Absolute Nothingness",
        "Version": "1.0"
    }

    # LaTeX export
    latex_content = LATEX_TEMPLATE % (
        data.get("title", "AxAbsEnt Unified Theory Publication"),
        timestamp,
        data.get("abstract", "No abstract provided."),
        os.path.basename(tensor_path),
        _format_outputs(data.get("outputs", {})),
        "\n".join([f"{k}: {v}" for k, v in metadata.items()])
    )

    with open(os.path.join(output_dir, f"{base_filename}.tex"), 'w') as f:
        f.write(latex_content)

    # Markdown export
    md_content = MARKDOWN_TEMPLATE.format(
        title=data.get("title", "AxAbsEnt Unified Theory"),
        timestamp=timestamp,
        abstract=data.get("abstract", "No abstract provided."),
        tensor_path=os.path.basename(tensor_path),
        output_list=_format_outputs_md(data.get("outputs", {})),
        metadata="\n".join([f"{k}: {v}" for k, v in metadata.items()])
    )

    with open(os.path.join(output_dir, f"{base_filename}.md"), 'w') as f:
        f.write(md_content)
