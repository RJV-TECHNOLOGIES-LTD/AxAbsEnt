// cpp/include/axabsent/core/interaction.hpp

#ifndef AXABSENT_CORE_INTERACTION_HPP
#define AXABSENT_CORE_INTERACTION_HPP

#include <Eigen/Dense>
#include "absolute.hpp"

namespace axabsent {
namespace core {

class Interaction {
public:
    // Construct interaction between two Absolutes with an operator matrix
    Interaction(const Absolute& source,
                const Absolute& target,
                const Eigen::MatrixXd& operator_matrix);

    // Apply the operator to the source's state
    Eigen::VectorXd apply() const;

    // Return the operator
    Eigen::MatrixXd get_operator() const;

    // Compute cross-absolute action cost (trace-based)
    double get_action_cost() const;

    // Compose with another interaction to form composite interaction
    Interaction compose(const Interaction& other) const;

private:
    Absolute source_;
    Absolute target_;
    Eigen::MatrixXd operator_;
};

} // namespace core
} // namespace axabsent

#endif // AXABSENT_CORE_INTERACTION_HPP
