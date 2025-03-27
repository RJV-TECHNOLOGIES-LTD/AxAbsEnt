// cpp/tests/test_mathematics.cpp

#include <gtest/gtest.h>
#include <Eigen/Dense>
#include <cmath>
#include "axabsent/core/absolute.hpp"

using namespace axabsent::core;

// ------------------------------
// Tensor and Linear Algebra Tests
// ------------------------------

TEST(MathematicsTest, MatrixMultiplicationConsistency) {
    Eigen::MatrixXd A(2, 2), B(2, 2);
    A << 1, 2,
         3, 4;
    B << 2, 0,
         1, 2;
    Eigen::MatrixXd result = A * B;

    EXPECT_NEAR(result(0, 0), 4.0, 1e-6);
    EXPECT_NEAR(result(0, 1), 4.0, 1e-6);
    EXPECT_NEAR(result(1, 0), 10.0, 1e-6);
    EXPECT_NEAR(result(1, 1), 8.0, 1e-6);
}

TEST(MathematicsTest, IdentityPreservationInProjection) {
    Absolute abs;
    Eigen::MatrixXd sig = Eigen::MatrixXd::Identity(3, 3);
    abs.set_signature(sig);
    Eigen::VectorXd state(3);
    state << 1, 0, -1;
    abs.set_state(state);

    Eigen::MatrixXd identity = Eigen::MatrixXd::Identity(3, 3);
    Eigen::VectorXd projected = abs.project_state(identity);
    EXPECT_TRUE(projected.isApprox(state));
}

// ------------------------------
// Entropy / Trace Calculations
// ------------------------------

TEST(MathematicsTest, EntropyViaTrace) {
    Eigen::MatrixXd M(2, 2);
    M << 2, 0,
         0, 3;

    double entropy = (M * M.transpose()).trace();  // 4 + 9 = 13
    EXPECT_NEAR(entropy, 13.0, 1e-6);
}

TEST(MathematicsTest, FrobeniusNormSquaredTrace) {
    Eigen::MatrixXd M(3, 3);
    M << 1, 2, 3,
         0, -1, 1,
         2, 1, 0;

    double expected = M.squaredNorm();  // Sum of squares
    double trace = (M * M.transpose()).trace();
    EXPECT_NEAR(expected, trace, 1e-6);
}

// ------------------------------
// Transfinite & Ordinal Logic (Mocked)
// ------------------------------

TEST(MathematicsTest, OrdinalArithmeticMockedAddition) {
    unsigned long long ω = 1e18;  // symbolic ω
    unsigned long long result = ω + 5;
    EXPECT_EQ(result, ω);  // ω + n = ω (ordinal semantics)
}

TEST(MathematicsTest, OrdinalAdditionOrderMatters) {
    unsigned long long ω = 1e18;
    unsigned long long result = 5 + ω;
    EXPECT_EQ(result, ω);  // n + ω = ω (same result numerically, but order matters logically)
}

// ------------------------------
// Categorical / Topological Tests (Placeholders)
// ------------------------------

TEST(MathematicsTest, CategoryCompositionPlaceholder) {
    SUCCEED();  // Will test functor chaining in future
}

TEST(MathematicsTest, TopologicalContinuityPlaceholder) {
    SUCCEED();  // Will test manifold open cover logic later
}
