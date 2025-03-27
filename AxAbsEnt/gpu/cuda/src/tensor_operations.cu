/**
 * @file tensor_operations.cu
 * @author Ricardo
 * @license AxAbsEnt-NC (Non-Commercial, Attribution Required)
 * @brief CUDA kernel implementation for CEFT-aligned tensor field operations
 */

#include "axabsent_cuda/tensor_operations.cuh"
#include <cmath>

namespace axabsent {
namespace cuda {

__global__
void tensor_add(
    const float* __restrict__ A,
    const float* __restrict__ B,
    float* __restrict__ result,
    int size
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= size) return;
    result[idx] = A[idx] + B[idx];
}

__global__
void tensor_contract(
    const float* __restrict__ A,
    float* __restrict__ result,
    int shape
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= shape) return;

    float sum = 0.0f;
    for (int i = 0; i < shape; ++i) {
        sum += A[i * shape + i];  // diagonal elements
    }
    result[idx] = sum;
}

__global__
void entropy_project_tensor(
    const float* __restrict__ tensor,
    const float* __restrict__ ceft,
    float* __restrict__ result,
    int size
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= size) return;

    result[idx] = tensor[idx] * ceft[idx];
}

__global__
void gradient_tensor_1d(
    const float* __restrict__ tensor,
    float* __restrict__ result,
    float spacing,
    int size
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= size || idx == 0 || idx == size - 1) {
        result[idx] = 0.0f;
        return;
    }

    float left = tensor[idx - 1];
    float right = tensor[idx + 1];
    result[idx] = (right - left) / (2.0f * spacing);
}

__global__
void divergence_vector_field(
    const float3* __restrict__ field,
    float* __restrict__ result,
    float spacing,
    int size
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= size || idx == 0 || idx == size - 1) {
        result[idx] = 0.0f;
        return;
    }

    float3 prev = field[idx - 1];
    float3 next = field[idx + 1];

    result[idx] = ((next.x - prev.x) +
                   (next.y - prev.y) +
                   (next.z - prev.z)) / (2.0f * spacing);
}

cudaError_t launch_tensor_operation(
    TensorOpType op,
    const void* input1,
    const void* input2,
    void* output,
    int size,
    float spacing
) {
    int threads = 128;
    int blocks = (size + threads - 1) / threads;

    switch (op) {
        case TensorOpType::ADD:
            tensor_add<<<blocks, threads>>>(
                static_cast<const float*>(input1),
                static_cast<const float*>(input2),
                static_cast<float*>(output),
                size
            );
            break;

        case TensorOpType::CONTRACT:
            tensor_contract<<<blocks, threads>>>(
                static_cast<const float*>(input1),
                static_cast<float*>(output),
                size
            );
            break;

        case TensorOpType::PROJECT_ENTROPY:
            entropy_project_tensor<<<blocks, threads>>>(
                static_cast<const float*>(input1),
                static_cast<const float*>(input2),
                static_cast<float*>(output),
                size
            );
            break;

        case TensorOpType::GRADIENT_1D:
            gradient_tensor_1d<<<blocks, threads>>>(
                static_cast<const float*>(input1),
                static_cast<float*>(output),
                spacing,
                size
            );
            break;

        case TensorOpType::DIVERGENCE:
            divergence_vector_field<<<blocks, threads>>>(
                static_cast<const float3*>(input1),
                static_cast<float*>(output),
                spacing,
                size
            );
            break;

        default:
            return cudaErrorInvalidValue;
    }

    return cudaGetLastError();
}

}  // namespace cuda
}  // namespace axabsent
