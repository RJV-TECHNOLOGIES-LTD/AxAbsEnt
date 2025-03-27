// cpp/include/axabsent/simulation/quantum.hpp

#ifndef AXABSENT_SIMULATION_QUANTUM_HPP
#define AXABSENT_SIMULATION_QUANTUM_HPP

#include <Eigen/Dense>
#include <vector>
#include <string>

namespace axabsent {
namespace simulation {

class QuantumFieldSimulator {
public:
    QuantumFieldSimulator();

    // Configure spatial grid (Nx x Ny)
    void configure_grid(int Nx, int Ny, double dx, double dy);

    // Set initial complex field amplitude (real, imaginary)
    void set_initial_conditions(const Eigen::MatrixXd& real, const Eigen::MatrixXd& imag);

    // Perform one evolution step (simple linear evolution + decoherence)
    void evolve(int steps = 1, double dt = 0.01);

    // Extract observable (e.g., probability density)
    Eigen::MatrixXd extract_observables() const;

    // Reset to initial state
    void reset();

private:
    int Nx_, Ny_;
    double dx_, dy_;
    Eigen::MatrixXd field_real_, field_imag_;
};

} // namespace simulation
} // namespace axabsent

#endif // AXABSENT_SIMULATION_QUANTUM_HPP
