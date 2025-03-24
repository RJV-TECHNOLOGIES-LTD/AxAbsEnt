// cpp/tests/test_core.cpp

#include <gtest/gtest.h>
#include "axabsent/core/absolute.hpp"
#include "axabsent/core/interaction.hpp"

using namespace axabsent::core;

// ------------------------------
// Absolute Tests
// ------------------------------

TEST(AbsoluteTest, UUID_IsNotEmpty) {
    Absolute abs;
    EXPECT_FALSE(abs.get_id().empty());
}

TEST(AbsoluteTest, SignatureAssignmentAndValidation) {
    Absolute abs;
    Eigen::MatrixXd sig(2, 2);
    sig << 1.0, 0.0,
           0.0, 1.0;
    abs.set_signature(sig);
    EXPECT_TRUE(abs.get_signature().isApprox(sig));
}

TEST(AbsoluteTest, StateAssignment) {
    Absolute abs;
    abs.set_signature(Eigen::MatrixXd::Identity(2, 2));
    Eigen::VectorXd state(2);
    state << 0.5, -1.0;
    abs.set_state(state);
    EXPECT_TRUE(abs.get_state().isApprox(state));
}

TEST(AbsoluteTest, PropertyMapAccess) {
    Absolute abs;
    Eigen::VectorXd mass(1);
    mass << 1.23;
    abs.set_property("mass", mass);
    EXPECT_TRUE(abs.get_property("mass").isApprox(mass));
}

TEST(AbsoluteTest, ProjectState) {
    Absolute abs;
    abs.set_signature(Eigen::MatrixXd::Identity(2, 2));
    abs.set_state((Eigen::VectorXd(2) << 1.0, 2.0).finished());

    Eigen::MatrixXd P(1, 2);
    P << 0.5, 0.5;

    Eigen::VectorXd projected = abs.project_state(P);
    EXPECT_NEAR(projected(0), 1.5, 1e-6);
}

TEST(AbsoluteTest, EntropySignatureCalculation) {
    Absolute abs;
    Eigen::MatrixXd sig(2, 2);
    sig << 1, 0,
           0, 2;
    abs.set_signature(sig);
    EXPECT_NEAR(abs.entropy_signature(), 5.0, 1e-6);
}

// ------------------------------
// Interaction Tests
// ------------------------------

TEST(InteractionTest, ApplyProjection) {
    Absolute A, B;
    A.set_signature(Eigen::MatrixXd::Identity(2, 2));
    A.set_state((Eigen::VectorXd(2) << 1.0, 3.0).finished());

    B.set_signature(2 * Eigen::MatrixXd::Identity(2, 2));
    B.set_state((Eigen::VectorXd(2) << 0.0, 0.0).finished());

    Eigen::MatrixXd op(2, 2);
    op << 0.1, 0.2,
          0.3, 0.4;

    Interaction I(A, B, op);
    Eigen::VectorXd result = I.apply();

    EXPECT_NEAR(result(0), 0.1 + 0.6, 1e-6);  // 0.1*1.0 + 0.2*3.0
    EXPECT_NEAR(result(1), 0.3 + 1.2, 1e-6);  // 0.3*1.0 + 0.4*3.0
}

TEST(InteractionTest, ActionCostCalculation) {
    Absolute A, B;
    A.set_signature(Eigen::MatrixXd::Identity(2, 2));
    A.set_state((Eigen::VectorXd(2) << 0, 0).finished());
    B.set_signature(Eigen::MatrixXd::Identity(2, 2));
    B.set_state((Eigen::VectorXd(2) << 0, 0).finished());

    Eigen::MatrixXd op(2, 2);
    op << 1, 2,
          3, 4;

    Interaction I(A, B, op);
    double action = I.get_action_cost();  // Tr(O O^T)
    EXPECT_NEAR(action, 30.0, 1e-6);      // [[5, 11], [11, 25]] → 5 + 25
}

TEST(InteractionTest, CompositionProducesCorrectOperator) {
    Absolute A, B, C;
    A.set_signature(Eigen::MatrixXd::Identity(2, 2));
    A.set_state((Eigen::VectorXd(2) << 1.0, 0.0).finished());
    B.set_signature(Eigen::MatrixXd::Identity(2, 2));
    B.set_state((Eigen::VectorXd(2) << 0.0, 0.0).finished());
    C.set_signature(Eigen::MatrixXd::Identity(2, 2));
    C.set_state((Eigen::VectorXd(2) << 0.0, 0.0).finished());

    Eigen::MatrixXd opAB(2, 2);
    opAB << 0, 1,
            1, 0;

    Eigen::MatrixXd opBC(2, 2);
    opBC << 2, 0,
            0, 3;

    Interaction AB(A, B, opAB);
    Interaction BC(B, C, opBC);
    Interaction AC = BC.compose(AB);

    Eigen::MatrixXd expected = opBC * opAB;
    EXPECT_TRUE(AC.get_operator().isApprox(expected));
}
