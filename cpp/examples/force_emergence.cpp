// cpp/examples/force_emergence.cpp

#include <iostream>
#include <Eigen/Dense>
#include "axabsent/core/absolute.hpp"
#include "axabsent/core/interaction.hpp"
#include "axabsent/simulation/dynamics.hpp"

using namespace axabsent::core;
using namespace axabsent::simulation;

int main() {
    std::cout << "[AxAbsEnt] Force Emergence Simulation Example\n";

    // Step 1: Create Absolutes
    Absolute source;
    source.set_signature(Eigen::MatrixXd::Identity(3, 3));
    source.set_state((Eigen::VectorXd(3) << 1.0, 0.0, 0.0).finished());
    source.set_property("charge", Eigen::VectorXd::Constant(1, 1.0));

    Absolute target;
    target.set_signature((Eigen::MatrixXd(3, 3) << 2, 0, 0,
                                                    0, 2, 0,
                                                    0, 0, 2).finished());
    target.set_state((Eigen::VectorXd(3) << 0.0, 1.0, 0.0).finished());
    target.set_property("mass", Eigen::VectorXd::Constant(1, 2.0));

    std::cout << "Source Absolute: " << source.get_state().transpose() << "\n";
    std::cout << "Target Absolute: " << target.get_state().transpose() << "\n";

    // Step 2: Create Interaction Matrix (field influence)
    Eigen::MatrixXd interaction_matrix(3, 3);
    interaction_matrix << 0.5, 0.0, -0.1,
                          0.0, 1.0,  0.0,
                          0.2, 0.0,  0.7;

    Interaction interaction(source, target, interaction_matrix);

    // Step 3: Initialize Dynamics Simulator
    DynamicSimulator sim;
    sim.initialize({source, target}, interaction);

    // Step 4: Run simulation for 10 steps
    for (int i = 0; i < 10; ++i) {
        sim.step();
        std::cout << "Step " << i + 1 << ": Target State = " << sim.get_state("target").transpose() << "\n";
    }

    // Step 5: Extract emergent force vector
    Eigen::VectorXd force_vector = sim.get_emergent_force("target");
    std::cout << "Emergent Force on Target: " << force_vector.transpose() << "\n";

    // Step 6: Compute resonance signature
    double resonance = sim.get_resonance_signature("target");
    std::cout << "Resonance Coefficient: " << resonance << "\n";

    return 0;
}
