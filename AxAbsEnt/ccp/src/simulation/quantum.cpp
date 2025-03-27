// cpp/src/simulation/quantum.cpp

#include "axabsent/simulation/quantum.hpp"
#include <cmath>
#include <stdexcept>

using namespace axabsent::simulation;

QuantumFieldSimulator::QuantumFieldSimulator()
    : Nx_(0), Ny_(0), dx_(1.0), dy_(1.0) {}

void QuantumFieldSimulator::configure_grid(int Nx, int Ny, double dx, double dy) {
    Nx_ = Nx;
    Ny_ = Ny;
    dx_ = dx;
    dy_ = dy;
    field_real_ = Eigen::MatrixXd::Zero(Nx_, Ny_);
    field_imag_ = Eigen::MatrixXd::Zero(Nx_, Ny_);
}

void QuantumFieldSimulator::set_initial_conditions(const Eigen::MatrixXd& real, const Eigen::MatrixXd& imag) {
    if (real.rows() != Nx_ || real.cols() != Ny_ ||
        imag.rows() != Nx_ || imag.cols() != Ny_) {
        throw std::invalid_argument("Initial condition dimensions do not match configured grid.");
    }
    field_real_ = real;
    field_imag_ = imag;
}

void QuantumFieldSimulator::evolve(int steps, double dt) {
    for (int step = 0; step < steps; ++step) {
        Eigen::MatrixXd real_next = field_real_;
        Eigen::MatrixXd imag_next = field_imag_;

        // Simple Laplacian-based evolution (non-relativistic Schrödinger-like)
        for (int i = 1; i < Nx_ - 1; ++i) {
            for (int j = 1; j < Ny_ - 1; ++j) {
                double laplacian_r =
                    (field_real_(i+1, j) + field_real_(i-1, j) - 2.0 * field_real_(i, j)) / (dx_ * dx_) +
                    (field_real_(i, j+1) + field_real_(i, j-1) - 2.0 * field_real_(i, j)) / (dy_ * dy_);
                double laplacian_i =
                    (field_imag_(i+1, j) + field_imag_(i-1, j) - 2.0 * field_imag_(i, j)) / (dx_ * dx_) +
                    (field_imag_(i, j+1) + field_imag_(i, j-1) - 2.0 * field_imag_(i, j)) / (dy_ * dy_);

                // Update rule (1st order time evolution, simplified Hamiltonian)
                real_next(i, j) += dt * laplacian_i;
                imag_next(i, j) -= dt * laplacian_r;
            }
        }

        // Swap fields
        field_real_ = real_next;
        field_imag_ = imag_next;
    }
}

Eigen::MatrixXd QuantumFieldSimulator::extract_observables() const {
    // Return probability density = |ψ|² = real² + imag²
    return field_real_.cwiseProduct(field_real_) + field_imag_.cwiseProduct(field_imag_);
}

void QuantumFieldSimulator::reset() {
    field_real_.setZero();
    field_imag_.setZero();
}
