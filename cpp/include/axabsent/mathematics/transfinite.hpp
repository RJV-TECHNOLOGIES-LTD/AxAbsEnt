// cpp/include/axabsent/mathematics/transfinite.hpp

#ifndef AXABSENT_MATHEMATICS_TRANSFINITE_HPP
#define AXABSENT_MATHEMATICS_TRANSFINITE_HPP

#include <Eigen/Dense>
#include <vector>
#include <string>

namespace axabsent {
namespace mathematics {

class Transfinite {
public:
    Transfinite();

    /// Compute ω-indexed summation (symbolic ordinal limit convergence)
    static double omega_sum(const std::vector<double>& sequence, double threshold = 1e-6);

    /// Evaluate limit of an ordinal-indexed scalar field
    static double ordinal_limit(const std::vector<double>& field, size_t max_steps = 1000);

    /// Generate ω-normalized projection vector of arbitrary length
    static Eigen::VectorXd omega_normalize(const Eigen::VectorXd& input);

    /// Return symbolic ω (for mapping into higher abstraction layers)
    static unsigned long long omega_symbol();

    /// Symbolic transfinite compare: returns true if a < ω
    static bool is_finite(unsigned long long a);
};

} // namespace mathematics
} // namespace axabsent

#endif // AXABSENT_MATHEMATICS_TRANSFINITE_HPP
