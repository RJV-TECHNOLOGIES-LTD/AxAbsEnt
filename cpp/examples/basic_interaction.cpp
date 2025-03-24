// cpp/examples/basic_interaction.cpp

#include <iostream>
#include <Eigen/Dense>
#include "axabsent/core/absolute.hpp"
#include "axabsent/core/interaction.hpp"

using namespace axabsent::core;

int main() {
    std::cout << "[AxAbsEnt] Basic Interaction Example\n";

    // Create Absolute A
    Absolute A;
    Eigen::MatrixXd signatureA(2, 2);
    signatureA << 1, 0,
                  0, 1;
    A.set_signature(signatureA);

    Eigen::VectorXd stateA(2);
    stateA << 0.5, 0.8;
    A.set_state(stateA);
    A.set_property("mass", Eigen::VectorXd::Constant(1, 1.23));

    std::cout << "Absolute A created with state: " << A.get_state().transpose() << "\n";

    // Create Absolute B
    Absolute B;
    Eigen::MatrixXd signatureB(2, 2);
    signatureB << 2, 0,
                  0, 3;
    B.set_signature(signatureB);

    Eigen::VectorXd stateB(2);
    stateB << 0.0, 0.0;
    B.set_state(stateB);
    B.set_property("charge", Eigen::VectorXd::Constant(1, -0.42));

    std::cout << "Absolute B created with state: " << B.get_state().transpose() << "\n";

    // Define Interaction Operator (2x2)
    Eigen::MatrixXd interaction_matrix(2, 2);
    interaction_matrix << 1.0, -0.5,
                          0.3, 0.7;

    // Create Interaction
    Interaction AB(A, B, interaction_matrix);

    // Apply Interaction
    Eigen::VectorXd result = AB.apply();
    std::cout << "Projected result of A → B interaction: " << result.transpose() << "\n";

    // Action Cost (Entropy scalar)
    double action = AB.get_action_cost();
    std::cout << "Action cost (entropy signature): " << action << "\n";

    return 0;
}
