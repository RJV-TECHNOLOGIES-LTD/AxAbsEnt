// cpp/src/core/mediator.cpp

#include "axabsent/core/mediator.hpp"
#include <stdexcept>
#include <cmath>

using namespace axabsent::core;

Mediator::Mediator() = default;

// Align signature spaces and generate a bridging operator
Eigen::MatrixXd Mediator::generate_operator(const Absolute& source, const Absolute& target) const {
    Eigen::MatrixXd S = source.get_signature();
    Eigen::MatrixXd T = target.get_signature();

    if (S.cols() != T.cols()) {
        throw std::invalid_argument("Mediator: Signature dimension mismatch between source and target.");
    }

    // Operator: normalized alignment of S and T
    Eigen::MatrixXd O = 0.5 * (T + S);
    return O;
}

// Wrap into an Interaction object
Interaction Mediator::mediate(const Absolute& source, const Absolute& target) const {
    Eigen::MatrixXd op = generate_operator(source, target);
    return Interaction(source, target, op);
}

// Compute entropy: Tr(O * O^T)
double Mediator::compute_entropy(const Eigen::MatrixXd& operator_matrix) const {
    return (operator_matrix * operator_matrix.transpose()).trace();
}
