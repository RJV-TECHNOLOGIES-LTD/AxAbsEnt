#ifndef AXABSENT_CUDA_FORCE_EXTRACTION_CUH
#define AXABSENT_CUDA_FORCE_EXTRACTION_CUH

/**
 * @file force_extraction.cuh
 * @author Ricardo Jorge Do Vale
 * @license AxAbsEnt-NC (Non-Commercial, Attribution Required)
 * @brief CUDA kernel headers for force extraction from interaction tensors
 * @date 2025-03-23
 *
 * Description:
 * Implements CUDA-compatible kernel interfaces for decomposing interaction tensors
 * into fundamental force vectors (gravitational, electromagnetic, strong, weak)
 * based on the CEFT (Curvature Entropy Flux Tensor) and the SRI (Symmetry Residue Index).
 */

#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <math_constants.h>

namespace axabsent {
namespace cuda {

/**
 * @brief Enumerates available force types for extraction
 */
enum class ForceType : int {
    GRAVITATIONAL = 0,
    ELECTROMAGNETIC = 1,
    STRONG = 2,
    WEAK = 3
};

/**
 * @brief Kernel to extract force vectors from interaction tensors in parallel
 *
 * @param interaction_tensor [in] Raw flattened interaction tensor
 * @param curvature_entropy [in] CEFT component of each cell
 * @param output_vectors [out] Resulting force vectors per cell
 * @param tensor_size [in] Number of tensor elements
 * @param type [in] Force type to extract (enum)
 */
__global__ void extract_force_kernel(
    const float* __restrict__ interaction_tensor,
    const float* __restrict__ curvature_entropy,
    float3* __restrict__ output_vectors,
    const int tensor_size,
    const ForceType type
);

/**
 * @brief Launch wrapper for extract_force_kernel
 *
 * @param interaction_tensor Host pointer to tensor input (device must be set)
 * @param curvature_entropy Host pointer to CEFT values
 * @param output_vectors Host pointer to output buffer
 * @param tensor_size Number of elements in the tensor
 * @param type Desired force type to extract
 * @return cudaError_t
 */
cudaError_t launch_force_extraction(
    const float* interaction_tensor,
    const float* curvature_entropy,
    float3* output_vectors,
    int tensor_size,
    ForceType type
);

}  // namespace cuda
}  // namespace axabsent

#endif  // AXABSENT_CUDA_FORCE_EXTRACTION_CUH
