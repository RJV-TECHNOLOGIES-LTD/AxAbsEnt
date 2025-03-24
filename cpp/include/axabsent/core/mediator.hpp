// cpp/include/axabsent/core/mediator.hpp

#ifndef AXABSENT_CORE_MEDIATOR_HPP
#define AXABSENT_CORE_MEDIATOR_HPP

#include <Eigen/Dense>
#include "absolute.hpp"
#include "interaction.hpp"

namespace axabsent {
namespace core {

class Mediator {
public:
    Mediator();

    // Construct a mediator from two Absolutes using internal alignment logic
    Eigen::MatrixXd generate_operator(const Absolute& source, const Absolute& target) const;

    // Create an Interaction from the mediator's operator
    Interaction mediate(const Absolute& source, const Absolute& target) const;

    // Return the entropy of the mediator matrix used
    double compute_entropy(const Eigen::MatrixXd& operator_matrix) const;
};

} // namespace core
} // namespace axabsent

#endif // AXABSENT_CORE_MEDIATOR_HPP
