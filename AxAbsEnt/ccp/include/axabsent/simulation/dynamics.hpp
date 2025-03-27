// cpp/include/axabsent/simulation/dynamics.hpp

#ifndef AXABSENT_SIMULATION_DYNAMICS_HPP
#define AXABSENT_SIMULATION_DYNAMICS_HPP

#include <Eigen/Dense>
#include <string>
#include <unordered_map>
#include <vector>
#include "axabsent/core/absolute.hpp"
#include "axabsent/core/interaction.hpp"

namespace axabsent {
namespace simulation {

class DynamicSimulator {
public:
    DynamicSimulator();

    // Initialize simulation with source, target, and interaction
    void initialize(const std::vector<axabsent::core::Absolute>& entities,
                    const axabsent::core::Interaction& interaction);

    // Advance one timestep
    void step();

    // Run for N steps
    void run(int steps);

    // Get current state of named entity
    Eigen::VectorXd get_state(const std::string& name) const;

    // Get emergent force vector on target
    Eigen::VectorXd get_emergent_force(const std::string& name) const;

    // Get resonance signature
    double get_resonance_signature(const std::string& name) const;

    // Reset internal state
    void reset();

private:
    axabsent::core::Absolute source_;
    axabsent::core::Absolute target_;
    axabsent::core::Interaction interaction_;

    std::vector<Eigen::VectorXd> target_state_history_;
    Eigen::VectorXd last_force_;
};

} // namespace simulation
} // namespace axabsent

#endif // AXABSENT_SIMULATION_DYNAMICS_HPP
