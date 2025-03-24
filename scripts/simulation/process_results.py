# scripts/simulation/process_results.py

"""
Simulation Results Processor (AxAbsEnt Unified Theory)

Processes CSV results from simulations (e.g. parameter sweep, Monte Carlo),
computing:

- Aggregate statistics
- Entropy–amplitude correlations
- Directional vector clustering (via PCA)
- Filtered datasets for falsifiability or plotting

Outputs summary files and logs.
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import os

# ----------------------------
# Configuration
# ----------------------------

INPUT_CSV = "results/parameter_sweep_results.csv"
SUMMARY_CSV = "results/summary_stats.csv"
PCA_CSV = "results/direction_pca.csv"

if not os.path.exists(INPUT_CSV):
    raise FileNotFoundError(f"❌ Input file not found: {INPUT_CSV}")

print(f"📂 Loading simulation data from {INPUT_CSV}")
df = pd.read_csv(INPUT_CSV)


# ----------------------------
# Basic Statistics
# ----------------------------

print("\n📊 Computing aggregate statistics...\n")

summary = df.groupby(["dimension", "signature_scale", "chain_length"]).agg({
    "sdi_trace": ["mean", "std", "min", "max"],
    "amplitude": ["mean", "std", "min", "max"]
})

summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
summary.reset_index(inplace=True)

summary.to_csv(SUMMARY_CSV, index=False)
print(f"✅ Summary statistics saved to {SUMMARY_CSV}")


# ----------------------------
# Direction Vector PCA (optional)
# ----------------------------

if "direction_vector" in df.columns:
    print("🧠 Performing PCA on direction vectors...")

    directions = df["direction_vector"].apply(lambda x: np.array(eval(x)))
    direction_matrix = np.vstack(directions.values)
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(direction_matrix)

    df["pca_x"] = reduced[:, 0]
    df["pca_y"] = reduced[:, 1]

    df[["dimension", "signature_scale", "chain_length", "
