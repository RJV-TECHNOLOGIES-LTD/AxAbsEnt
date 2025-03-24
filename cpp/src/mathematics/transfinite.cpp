// cpp/src/mathematics/transfinite.cpp

#include "axabsent/mathematics/transfinite.hpp"
#include <cmath>
#include <limits>
#include <stdexcept>

using namespace axabsent::mathematics;

Transfinite::Transfinite() = default;

// ------------------------------
// ω-symbolic representation
// ------------------------------

unsigned long long Transfinite::omega_symbol() {
    // Arbitrarily high integer to symbolically represent ω
    return static_cast<unsigned long long>(1e18);
}

bool Transfinite::is_finite(unsigned long long a) {
    return a < omega_symbol();
}

// ------------------------------
// ω-indexed summation: simulate convergence toward a limit
// ------------------------------

double Transfinite::omega_sum(const std::vector<double>& sequence, double threshold) {
    double sum = 0.0;
    double delta = 0.0;
    for (size_t i = 0; i < sequence.size(); ++i) {
        double term = sequence[i];
        sum += term;
        if (std::abs(term) < threshold) break;
    }
    return sum;
}

// ------------------------------
// Ordinal limit estimation
// ------------------------------

double Transfinite::ordinal_limit(const std::vector<double>& field, size_t max_steps) {
    if (field.empty()) {
        throw std::invalid_argument("Ordinal field is empty.");
    }

    double prev = field[0];
    for (size_t i = 1; i < std::min(field.size(), max_steps); ++i) {
        double current = field[i];
        if (std::abs(current - prev) < 1e-9) {
            return current;  // Converged
        }
        prev = current;
    }
    return prev;  // Approximate limit
}

// ------------------------------
// Normalize a vector across ω-index
// ------------------------------

Eigen::VectorXd Transfinite::omega_normalize(const Eigen::VectorXd& input) {
    if (input.norm() == 0.0) {
        throw std::runtime_error("Cannot normalize zero vector.");
    }
    return input / input.norm();  // Frobenius-normalize
}
