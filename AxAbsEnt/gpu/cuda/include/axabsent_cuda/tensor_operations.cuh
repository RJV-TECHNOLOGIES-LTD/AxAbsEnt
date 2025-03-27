#ifndef AXABSENT_CUDA_TENSOR_OPERATIONS_CUH
#define AXABSENT_CUDA_TENSOR_OPERATIONS_CUH

/**
 * @file tensor_operations.cuh
 * @author Ricardo Jorge Do Vale
 * @license AxAbsEnt-NC (Non-Commercial, Attribution Required)
 * @brief CUDA declarations for tensor field operations in CEFT-based interaction modeling
 * @date 2025-03-23
 *
 * Description:
 * Provides kernel interfaces for performing core tensor operations on interaction grids,
 * including contraction, gradient estimation, divergence, and entropy-weighted projection.
 * These routines support high-dimensional quantum and classical tensors in AxAbsEnt.
 */

#include <cuda_runtime.h>
#include <device_launch_parameters.h>

namespace axabsent {
namespace cuda {

/**
 * @brief Element-wise tensor addition
 *
 * @param A First tensor input
 * @param B Second tensor input
 * @param result Output tensor
 * @param size Number of elements
 */
__global__ void tensor_add(
    const float* __restrict__ A,
    const float* __restrict__ B,
    float* __restrict__ result,
    int size
);

/**
 * @brief Tensor contraction kernel (summation along matched index)
 *
 * @param A Input tensor
 * @param shape Side length of square tensor (assumes NxN)
 * @param result Output vector (diagonal contraction)
 */
__global__ void tensor_contract(
    const float* __restrict__ A,
    float* __restrict__ result,
    int shape
);

/**
 * @brief Compute entropy-weighted projection of a tensor using CEFT weights
 *
 * @param tensor Input interaction tensor
 * @param ceft Entropy field (same dimension)
 * @param result Output tensor after projection
 * @param size Number of elements
 */
__global__ void entropy_project_tensor(
    const float* __restrict__ tensor,
    const float* __restrict__ ceft,
    float* __restrict__ result,
    int size
);

/**
 * @brief Compute gradient (finite diff) of tensor field in 1D layout
 *
 * @param tensor Input tensor
 * @param result Output gradient estimate
 * @param spacing Δx between tensor cells
 * @param size Total number of elements
 */
__global__ void gradient_tensor_1d(
    const float* __restrict__ tensor,
    float* __restrict__ result,
    float spacing,
    int size
);

/**
 * @brief Compute divergence of a vector field represented as float3*
 *
 * @param field Input vector field
 * @param result Output divergence scalar per cell
 * @param spacing Δx spacing
 * @param size Number of cells
 */
__global__ void divergence_vector_field(
    const float3* __restrict__ field,
    float* __restrict__ result,
    float spacing,
    int size
);

/**
 * @brief Launchable host-side interface to apply any of the above tensor operations
 * For dynamic runtime selection of operation type.
 */
enum class TensorOpType {
    ADD,
    CONTRACT,
    PROJECT_ENTROPY,
    GRADIENT_1D,
    DIVERGENCE
};

cudaError_t launch_tensor_operation(
    TensorOpType op,
    const void* input1,
    const void* input2,
    void* output,
    int size,
    float spacing = 1.0f
);

}  // namespace cuda
}  // namespace axabsent

#endif  // AXABSENT_CUDA_TENSOR_OPERATIONS_CUH
