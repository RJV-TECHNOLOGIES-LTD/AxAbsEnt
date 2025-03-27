/**
 * @file test_tensor_operations.cu
 * @author Ricardo
 * @license AxAbsEnt-NC (Non-Commercial, Attribution Required)
 * @brief Unit tests for CUDA tensor operations
 */

#include <gtest/gtest.h>
#include <cuda_runtime.h>
#include <cmath>
#include <vector>
#include "axabsent_cuda/tensor_operations.cuh"

using namespace axabsent::cuda;

const float EPSILON = 1e-5f;

// Utility: Compare two float arrays
void assertArrayNear(const float* a, const float* b, int size, float epsilon = EPSILON) {
    for (int i = 0; i < size; ++i) {
        ASSERT_NEAR(a[i], b[i], epsilon) << "Mismatch at index " << i;
    }
}

// === TEST CASES ===

TEST(TensorOps, TensorAdd) {
    int size = 8;
    std::vector<float> h_a(size, 1.0f);
    std::vector<float> h_b(size, 2.0f);
    std::vector<float> h_out(size, 0.0f);
    std::vector<float> expected(size, 3.0f);

    float *d_a, *d_b, *d_out;
    cudaMalloc(&d_a, size * sizeof(float));
    cudaMalloc(&d_b, size * sizeof(float));
    cudaMalloc(&d_out, size * sizeof(float));

    cudaMemcpy(d_a, h_a.data(), size * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b.data(), size * sizeof(float), cudaMemcpyHostToDevice);

    tensor_add<<<1, size>>>(d_a, d_b, d_out, size);
    cudaMemcpy(h_out.data(), d_out, size * sizeof(float), cudaMemcpyDeviceToHost);

    assertArrayNear(h_out.data(), expected.data(), size);

    cudaFree(d_a); cudaFree(d_b); cudaFree(d_out);
}

TEST(TensorOps, TensorContract) {
    int shape = 3;
    int size = shape * shape;
    std::vector<float> h_tensor = {
        1.0f, 0.2f, 0.3f,
        0.4f, 2.0f, 0.6f,
        0.7f, 0.8f, 3.0f
    };
    std::vector<float> h_result(1, 0.0f);
    float expected = 1.0f + 2.0f + 3.0f;

    float *d_tensor, *d_result;
    cudaMalloc(&d_tensor, size * sizeof(float));
    cudaMalloc(&d_result, sizeof(float));

    cudaMemcpy(d_tensor, h_tensor.data(), size * sizeof(float), cudaMemcpyHostToDevice);
    tensor_contract<<<1, 1>>>(d_tensor, d_result, shape);
    cudaMemcpy(h_result.data(), d_result, sizeof(float), cudaMemcpyDeviceToHost);

    ASSERT_NEAR(h_result[0], expected, EPSILON);

    cudaFree(d_tensor); cudaFree(d_result);
}

TEST(TensorOps, EntropyProjection) {
    int size = 4;
    std::vector<float> h_tensor = { 1.0f, 2.0f, 3.0f, 4.0f };
    std::vector<float> h_ceft   = { 0.1f, 0.2f, 0.3f, 0.4f };
    std::vector<float> h_out(size, 0.0f);
    std::vector<float> expected = { 0.1f, 0.4f, 0.9f, 1.6f };

    float *d_tensor, *d_ceft, *d_out;
    cudaMalloc(&d_tensor, size * sizeof(float));
    cudaMalloc(&d_ceft,   size * sizeof(float));
    cudaMalloc(&d_out,    size * sizeof(float));

    cudaMemcpy(d_tensor, h_tensor.data(), size * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_ceft,   h_ceft.data(),   size * sizeof(float), cudaMemcpyHostToDevice);

    entropy_project_tensor<<<1, size>>>(d_tensor, d_ceft, d_out, size);
    cudaMemcpy(h_out.data(), d_out, size * sizeof(float), cudaMemcpyDeviceToHost);

    assertArrayNear(h_out.data(), expected.data(), size);

    cudaFree(d_tensor); cudaFree(d_ceft); cudaFree(d_out);
}

TEST(TensorOps, Gradient1D) {
    int size = 5;
    float dx = 1.0f;
    std::vector<float> h_tensor = { 1.0f, 2.0f, 4.0f, 8.0f, 16.0f };
    std::vector<float> h_out(size, 0.0f);
    std::vector<float> expected = { 0.0f, 1.5f, 3.0f, 6.0f, 0.0f };

    float *d_tensor, *d_out;
    cudaMalloc(&d_tensor, size * sizeof(float));
    cudaMalloc(&d_out,    size * sizeof(float));

    cudaMemcpy(d_tensor, h_tensor.data(), size * sizeof(float), cudaMemcpyHostToDevice);

    gradient_tensor_1d<<<1, size>>>(d_tensor, d_out, dx, size);
    cudaMemcpy(h_out.data(), d_out, size * sizeof(float), cudaMemcpyDeviceToHost);

    assertArrayNear(h_out.data(), expected.data(), size);

    cudaFree(d_tensor); cudaFree(d_out);
}

TEST(TensorOps, DivergenceVectorField) {
    int size = 5;
    float dx = 1.0f;
    std::vector<float3> h_field = {
        {1, 1, 1},
        {2, 2, 2},
        {4, 4, 4},
        {8, 8, 8},
        {16, 16, 16}
    };
    std::vector<float> h_out(size, 0.0f);
    std::vector<float> expected = {
        0.0f,
        4.5f,  // (4-1)*3 / 2
        9.0f,  // (8-2)*3 / 2
        18.0f, // (16-4)*3 / 2
        0.0f
    };

    float3* d_field;
    float* d_out;
    cudaMalloc(&d_field, size * sizeof(float3));
    cudaMalloc(&d_out,   size * sizeof(float));

    cudaMemcpy(d_field, h_field.data(), size * sizeof(float3), cudaMemcpyHostToDevice);

    divergence_vector_field<<<1, size>>>(d_field, d_out, dx, size);
    cudaMemcpy(h_out.data(), d_out, size * sizeof(float), cudaMemcpyDeviceToHost);

    assertArrayNear(h_out.data(), expected.data(), size);

    cudaFree(d_field); cudaFree(d_out);
}
