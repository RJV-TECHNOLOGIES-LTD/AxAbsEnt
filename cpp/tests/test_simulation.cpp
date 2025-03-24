// cpp/tests/test_simulation.cpp

#include <gtest/gtest.h>
#include <Eigen/Dense>
#include "axabsent/core/absolute.hpp"
#include "axabsent/core/interaction.hpp"
#include "axabsent/simulation/dynamics.hpp"

using namespace axabsent::core;
using namespace axabsent::simulation;

// ------------------------------
// Dynamic Simulation Tests
// ------------------------------

TEST(SimulationTest, InitializationAndStepConsistency) {
    Absolute A, B;

    A.set_signature(Eigen::MatrixXd::Identity(2, 2));
    A.set_state((Eigen::VectorXd(2) << 1.0, 0.0).finished());

    B.set_signature(2.0 * Eigen::MatrixXd::Identity(2, 2));
    B.set_state((Eigen::VectorXd(2) << 0.0, 0.0).finished());

    Eigen::MatrixXd op(2, 2);
    op << 0.5, 0.5,
          0.0, 1.0;

    Interaction I(A, B, op);

    DynamicSimulator sim;
    sim.initialize({A, B}, I);

    sim.step();
    Eigen::VectorXd state = sim.get_state("target");
    EXPECT_GT(state.norm(), 0.0);  // State should have updated from 0
}

TEST(SimulationTest, RunMultipleStepsProducesProgressiveChange) {
    Absolute A, B;
    A.set_signature(Eigen::MatrixXd::Identity(2, 2));
    A.set_state((Eigen::VectorXd(2) << 1.0, 1.0).finished());
    B.set_signature(Eigen::MatrixXd::Identity(2, 2));
    B.set_state((Eigen::VectorXd(2) << 0.0, 0.0).finished());

    Eigen::MatrixXd op = Eigen::MatrixXd::Identity(2, 2);
    Interaction I(A, B, op);

    DynamicSimulator sim;
    sim.initialize({A, B}, I);
    sim.run(10);
    Eigen::VectorXd final_state = sim.get_state("target");

    // Expect state to have approached A's state
    EXPECT_NEAR(final_state(0), 1.0, 0.1);
    EXPECT_NEAR(final_state(1), 1.0, 0.1);
}

TEST(SimulationTest, EmergentForceReflectsStateDelta) {
    Absolute A, B;
    A.set_signature(Eigen::MatrixXd::Identity(2, 2));
    A.set_state((Eigen::VectorXd(2) << 2.0, 0.0).finished());
    B.set_signature(Eigen::MatrixXd::Identity(2, 2));
    B.set_state((Eigen::VectorXd(2) << 0.0, 0.0).finished());

    Eigen::MatrixXd op = Eigen::MatrixXd::Identity(2, 2);
    Interaction I(A, B, op);

    DynamicSimulator sim;
    sim.initialize({A, B}, I);
    sim.step();

    Eigen::VectorXd force = sim.get_emergent_force("target");

    // Force = projected - previous state
    EXPECT_NEAR(force(0), 2.0, 1e-6);
    EXPECT_NEAR(force(1), 0.0, 1e-6);
}

TEST(SimulationTest, ResonanceCoefficientIsNonZeroAfterMultipleSteps) {
    Absolute A, B;
    A.set_signature(Eigen::MatrixXd::Identity(2, 2));
    A.set_state((Eigen::VectorXd(2) << 0.5, -0.5).finished());
    B.set_signature(Eigen::MatrixXd::Identity(2, 2));
    B.set_state((Eigen::VectorXd(2) << 0.0, 0.0).finished());

    Eigen::MatrixXd op(2, 2);
    op << 1.0, 0.0,
          0.0, 1.0;

    Interaction I(A, B, op);

    DynamicSimulator sim;
    sim.initialize({A, B}, I);
    sim.run(5);

    double resonance = sim.get_resonance_signature("target");

    EXPECT_GT(resonance, 0.0);
}
