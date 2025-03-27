// cpp/src/core/interaction.cpp

#include "axabsent/core/interaction.hpp"
#include <stdexcept>

using namespace axabsent::core;

Interaction::Interaction(const Absolute& source,
                         const Absolute& target,
                         const Eigen::MatrixXd& operator_matrix)
    : source_(source), target_(target), operator_(operator_matrix) {
    if (operator_.cols() != source_.get_state().size()) {
        throw std::invalid_argument("Operator columns must match source state size.");
    }
    if (operator_.rows() != target_.get_state().size()) {
        throw std::invalid_argument("Operator rows must match target state size.");
    }
}

Eigen::VectorXd Interaction::apply() const {
    return operator_ * source_.get_state();
}

Eigen::MatrixXd Interaction::get_operator() const {
    return operator_;
}

double Interaction::get_action_cost() const {
    // Action cost as entropy of projection: Tr(O * O^T)
    return (operator_ * operator_.transpose()).trace();
}

Interaction Interaction::compose(const Interaction& other) const {
    if (other.target_.get_state().size() != source_.get_state().size()) {
        throw std::invalid_argument("Cannot compose: dimension mismatch between interactions.");
    }

    Eigen::MatrixXd composed_op = operator_ * other.operator_;
    return Interaction(other.source_, target_, composed_op);
}
