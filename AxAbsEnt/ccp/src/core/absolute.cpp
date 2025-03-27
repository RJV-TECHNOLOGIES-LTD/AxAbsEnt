// cpp/src/core/absolute.cpp

#include "axabsent/core/absolute.hpp"
#include <stdexcept>
#include <uuid/uuid.h>  // Linux UUID generation
#include <cmath>

using namespace axabsent::core;

// Generate a UUIDv4 string
static std::string generate_uuid() {
    uuid_t id;
    uuid_generate(id);
    char buffer[37];
    uuid_unparse(id, buffer);
    return std::string(buffer);
}

// Constructor
Absolute::Absolute()
    : id_(generate_uuid()),
      signature_(Eigen::MatrixXd::Identity(1, 1)),
      state_(Eigen::VectorXd::Zero(1)) {}

// Get unique ID
std::string Absolute::get_id() const {
    return id_;
}

// Get and set signature matrix
Eigen::MatrixXd Absolute::get_signature() const {
    return signature_;
}

void Absolute::set_signature(const Eigen::MatrixXd& signature) {
    if (signature.rows() != signature.cols()) {
        throw std::invalid_argument("Signature matrix must be square.");
    }
    if (!signature.isApprox(signature.transpose())) {
        throw std::invalid_argument("Signature matrix must be symmetric.");
    }
    signature_ = signature;
}

// Get and set state
Eigen::VectorXd Absolute::get_state() const {
    return state_;
}

void Absolute::set_state(const Eigen::VectorXd& state) {
    if (signature_.rows() != state.size()) {
        throw std::invalid_argument("State dimension must match signature.");
    }
    state_ = state;
}

// Property interface
void Absolute::set_property(const std::string& key, const Eigen::VectorXd& value) {
    properties_[key] = value;
}

Eigen::VectorXd Absolute::get_property(const std::string& key) const {
    auto it = properties_.find(key);
    if (it == properties_.end()) {
        throw std::runtime_error("Property not found: " + key);
    }
    return it->second;
}

// Projection method (does not mutate internal state)
Eigen::VectorXd Absolute::project_state(const Eigen::MatrixXd& projection_matrix) const {
    if (projection_matrix.cols() != state_.size()) {
        throw std::invalid_argument("Projection matrix and state size mismatch.");
    }
    return projection_matrix * state_;
}

// Entropy scalar derived from the signature
double Absolute::entropy_signature() const {
    return (signature_ * signature_.transpose()).trace();
}
