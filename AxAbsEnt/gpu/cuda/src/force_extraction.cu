/**
 * @file force_extraction.cu
 * @author Ricardo
 * @license AxAbsEnt-NC (Non-Commercial, Attribution Required)
 * @brief CUDA kernel implementation for extracting physical force vectors from interaction tensors
 */

#include "axabsent_cuda/force_extraction.cuh"
#include <cmath>
#include <cstdio>

namespace axabsent {
namespace cuda {

__device__ __forceinline__
float3 normalize_vector(float3 v) {
    float mag = sqrtf(v.x * v.x + v.y * v.y + v.z * v.z + 1e-9f); // Prevent divide by 0
    return make_float3(v.x / mag, v.y / mag, v.z / mag);
}

__device__ __forceinline__
float3 extract_force_from_tensor(const float* tensor, float entropy, ForceType type) {
    float3 f;

    switch (type) {
        case ForceType::GRAVITATIONAL:
            f = make_float3(
                -tensor[0] * entropy,
                -tensor[4] * entropy,
                -tensor[8] * entropy
            );
            break;

        case ForceType::ELECTROMAGNETIC:
            f = make_float3(
                tensor[1] - tensor[3],
                tensor[2] - tensor[6],
                tensor[5] - tensor[7]
            );
            break;

        case ForceType::STRONG:
            f = make_float3(
                tensor[0] + tensor[1],
                tensor[3] + tensor[4],
                tensor[6] + tensor[8]
            );
            break;

        case ForceType::WEAK:
            f = make_float3(
                entropy * (tensor[2] - tensor[1]),
                entropy * (tensor[5] - tensor[3]),
                entropy * (tensor[7] - tensor[6])
            );
            break;
    }

    return normalize_vector(f);
}

__global__
void extract_force_kernel(
    const float* __restrict__ interaction_tensor,
    const float* __restrict__ curvature_entropy,
    float3* __restrict__ output_vectors,
    const int tensor_size,
    const ForceType type
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= tensor_size) return;

    const float* tensor = &interaction_tensor[idx * 9];
    float entropy = curvature_entropy[idx];
    float3 force = extract_force_from_tensor(tensor, entropy, type);
    output_vectors[idx] = force;
}

cudaError_t launch_force_extraction(
    const float* interaction_tensor,
    const float* curvature_entropy,
    float3* output_vectors,
    int tensor_size,
    ForceType type
) {
    int threads_per_block = 128;
    int blocks = (tensor_size + threads_per_block - 1) / threads_per_block;

    extract_force_kernel<<<blocks, threads_per_block>>>(
        interaction_tensor,
        curvature_entropy,
        output_vectors,
        tensor_size,
        type
    );

    return cudaGetLastError();
}

}  // namespace cuda
}  // namespace axabsent
