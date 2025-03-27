// cpp/src/simulation/dynamics.cpp

#include "axabsent/simulation/dynamics.hpp"
#include <stdexcept>
#include <cmath>

using namespace axabsent::core;
using namespace axabsent::simulation;

DynamicSimulator::DynamicSimulator()
    : last_force_(Eigen::VectorXd::Zero(3)) {}

void DynamicSimulator::initialize(const std::vector<Absolute>& entities,
                                  const Interaction& interaction) {
    if (entities.size() != 2) {
        throw std::invalid_argument("Must provide exactly two Absolutes (source, target).");
    }
    source_ = entities[0];
    target_ = entities[1];
    interaction_ = interaction;
    target_state_history_.clear();
    last_force_ = Eigen::VectorXd::Zero(target_.get_state().size());
}

void DynamicSimulator::step() {
    Eigen::VectorXd projected = interaction_.apply();
    Eigen::VectorXd current = target_.get_state();
    Eigen::VectorXd delta = projected - current;

    Eigen::VectorXd new_state = current + 0.05 * delta;  // Simulation rate
    target_.set_state(new_state);

    target_state_history_.push_back(new_state);
    last_force_ = delta;
}

void DynamicSimulator::run(int steps) {
    for (int i = 0; i < steps; ++i) {
        step();
    }
}

Eigen::VectorXd DynamicSimulator::get_state(const std::string& name) const {
    if (name == "target") return target_.get_state();
    if (name == "source") return source_.get_state();
    throw std::invalid_argument("Unknown entity name: " + name);
}

Eigen::VectorXd DynamicSimulator::get_emergent_force(const std::string& name) const {
    if (name == "target") return last_force_;
    throw std::invalid_argument("Force only available for target.");
}

double DynamicSimulator::get_resonance_signature(const std::string& name) const {
    if (name != "target") throw std::invalid_argument("Resonance only available for target.");

    if (target_state_history_.size() < 2) return 0.0;

    double total = 0.0;
    for (size_t i = 1; i < target_state_history_.size(); ++i) {
        Eigen::VectorXd diff = target_state_history_[i] - target_state_history_[i - 1];
        total += diff.norm();
    }
    return total / static_cast<double>(target_state_history_.size() - 1);
}

void DynamicSimulator::reset() {
    target_state_history_.clear();
    last_force_ = Eigen::VectorXd::Zero(target_.get_state().size());
}
