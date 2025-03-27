#ifndef AXABSENT_CUDA_SIMULATION_CUH
#define AXABSENT_CUDA_SIMULATION_CUH

/**
 * @file simulation.cuh
 * @author Ricardo Jorge Do Vale
 * @license AxAbsEnt-NC (Non-Commercial, Attribution Required)
 * @brief CUDA simulation kernel declarations for transfinite dynamics and curvature evolution
 * @date 2025-03-23
 *
 * Description:
 * Declares GPU kernels and launch interfaces for executing time-evolution steps
 * of CEFT-based interaction fields across absolute domains. Includes curvature feedback,
 * symmetry decay integration, and vacuum fluctuation effects.
 */

#include <cuda_runtime.h>
#include <device_launch_parameters.h>

namespace axabsent {
namespace cuda {

/**
 * @brief Describes the state of a single simulation cell on the GPU
 */
struct SimulationCell {
    float interaction_tensor[9];    // 3x3 matrix flattened
    float curvature_entropy;        // CEFT
    float vacuum_state;             // Background energy potential
    float symmetry_index;           // SRI (Symmetry Residue Index)
};

/**
 * @brief Kernel to initialize the simulation grid with encoded CEFT and vacuum values
 *
 * @param grid Pointer to SimulationCell array
 * @param size Total number of simulation cells
 */
__global__ void initialize_simulation_grid(SimulationCell* grid, int size);

/**
 * @brief Main simulation kernel performing dynamic updates over time
 *
 * @param grid SimulationCell array
 * @param size Number of cells
 * @param time_step Current timestep size (Δt)
 * @param decay_coefficient CEFT-based entropy decay rate
 */
__global__ void evolve_simulation_step(
    SimulationCell* grid,
    int size,
    float time_step,
    float decay_coefficient
);

/**
 * @brief Optional kernel to apply gravitational collapse filtering
 *
 * @param grid SimulationCell array
 * @param size Number of cells
 * @param gravity_threshold Collapse threshold for curvature entropy
 */
__global__ void apply_gravitational_collapse(
    SimulationCell* grid,
    int size,
    float gravity_threshold
);

/**
 * @brief Host interface to launch a full simulation phase
 *
 * @param grid Device pointer to SimulationCell array
 * @param size Grid size
 * @param time_step Δt
 * @param decay_coefficient Curvature decay rate
 * @param collapse_threshold Threshold for gravitational collapse triggering
 * @param steps Number of simulation iterations
 * @return cudaError_t
 */
cudaError_t run_simulation_phase(
    SimulationCell* grid,
    int size,
    float time_step,
    float decay_coefficient,
    float collapse_threshold,
    int steps
);

}  // namespace cuda
}  // namespace axabsent

#endif  // AXABSENT_CUDA_SIMULATION_CUH
