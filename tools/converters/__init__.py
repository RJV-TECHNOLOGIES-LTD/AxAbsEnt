# tools/converters/__init__.py

"""
AxAbsEnt Converters Package

This package provides tools to convert between raw data formats used across:
- Tensor representations
- Simulation output structures
- Experimental datasets
- Visualization export formats

All converters ensure structural and ontological consistency with the Enhanced Mathematical Ontology of Absolute Nothingness.
"""

from .tensor_formats import (
    tensor_from_json,
    tensor_to_json,
    tensor_from_csv,
    tensor_to_csv
)

from .simulation_formats import (
    load_simulation_state,
    save_simulation_state,
    flatten_simulation_log
)

from .experimental_data import (
    load_experimental_dataset,
    convert_experiment_to_dataframe
)

from .visualization_formats import (
    convert_tensor_to_heatmap,
    convert_interaction_graph_to_image
)

__all__ = [
    # Tensor
    "tensor_from_json",
    "tensor_to_json",
    "tensor_from_csv",
    "tensor_to_csv",

    # Simulation
    "load_simulation_state",
    "save_simulation_state",
    "flatten_simulation_log",

    # Experimental
    "load_experimental_dataset",
    "convert_experiment_to_dataframe",

    # Visualization
    "convert_tensor_to_heatmap",
    "convert_interaction_graph_to_image"
]
