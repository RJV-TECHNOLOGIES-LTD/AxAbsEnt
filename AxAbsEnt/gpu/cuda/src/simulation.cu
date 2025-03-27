/**
 * @file simulation.cu
 * @author Ricardo
 * @license AxAbsEnt-NC (Non-Commercial, Attribution Required)
 * @brief CUDA simulation implementation for CEFT-driven tensor evolution and gravitational collapse
 */

#include "axabsent_cuda/simulation.cuh"
#include <cmath>
#include <cstdio>

namespace axabsent {
namespace cuda {

__global__
void initialize_simulation_grid(SimulationCell* grid, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= size) return;

    SimulationCell& cell = grid[idx];

    // Initialize flattened 3x3 tensor with symmetry-breaking pattern
    for (int i = 0; i < 9; ++i) {
        cell.interaction_tensor[i] = (float)(i % 3) * 0.1f + (idx % 5) * 0.01f;
    }

    // CEFT baseline entropy distribution
    cell.curvature_entropy = 0.75f + 0.01f * (idx % 10);

    // Vacuum energy initialized between 0.0–1.0 with mild fluctuation
    cell.vacuum_state = 0.5f + 0.1f * sinf(idx * 0.07f);

    // Initial symmetry residue index
    cell.symmetry_index = 1.0f;
}

__global__
void evolve_simulation_step(
    SimulationCell* grid,
    int size,
    float time_step,
    float decay_coefficient
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= size) return;

    SimulationCell& cell = grid[idx];

    // CEFT entropy decays exponentially
    cell.curvature_entropy *= expf(-decay_coefficient * time_step);

    // Tensor elements mutate with vacuum fluctuations and symmetry index
    for (int i = 0; i < 9; ++i) {
        float delta = sinf(cell.vacuum_state + i * 0.3f) * time_step;
        cell.interaction_tensor[i] += delta * cell.symmetry_index;
    }

    // Symmetry index slowly decays
    cell.symmetry_index *= (1.0f - 0.01f * time_step);
}

__global__
void apply_gravitational_collapse(
    SimulationCell* grid,
    int size,
    float gravity_threshold
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= size) return;

    SimulationCell& cell = grid[idx];

    if (cell.curvature_entropy < gravity_threshold) {
        // Simulate curvature collapse by nullifying local interaction field
        for (int i = 0; i < 9; ++i) {
            cell.interaction_tensor[i] = 0.0f;
        }

        // Mark as collapsed
        cell.symmetry_index = 0.0f;
        cell.vacuum_state = 0.0f;
        cell.curvature_entropy = 0.0f;
    }
}

cudaError_t run_simulation_phase(
    SimulationCell* grid,
    int size,
    float time_step,
    float decay_coefficient,
    float collapse_threshold,
    int steps
) {
    int threads_per_block = 128;
    int blocks = (size + threads_per_block - 1) / threads_per_block;

    for (int step = 0; step < steps; ++step) {
        evolve_simulation_step<<<blocks, threads_per_block>>>(
            grid, size, time_step, decay_coefficient
        );
        cudaError_t err1 = cudaGetLastError();
        if (err1 != cudaSuccess) return err1;

        apply_gravitational_collapse<<<blocks, threads_per_block>>>(
            grid, size, collapse_threshold
        );
        cudaError_t err2 = cudaGetLastError();
        if (err2 != cudaSuccess) return err2;
    }

    return cudaSuccess;
}

}  // namespace cuda
}  // namespace axabsent
