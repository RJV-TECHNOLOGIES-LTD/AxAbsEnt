#ifndef AXABSENT_INTERACTION_HPP
#define AXABSENT_INTERACTION_HPP

#include "absolute.hpp"
#include <Eigen/Dense>

namespace axabsent {
namespace core {

class Interaction {
public:
    Interaction(const Absolute& source, const Absolute& target, const Eigen::MatrixXd& operator_matrix);

    Eigen::VectorXd apply() const;
    Eigen::MatrixXd get_operator() const;
    double get_action_cost() const;
    Interaction compose(const Interaction& other) const;

private:
    Absolute source_;
    Absolute target_;
    Eigen::MatrixXd operator_;
};

} // namespace core
} // namespace axabsent

#endif // AXABSENT_INTERACTION_HPP
