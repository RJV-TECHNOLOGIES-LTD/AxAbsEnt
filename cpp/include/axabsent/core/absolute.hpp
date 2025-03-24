// cpp/include/axabsent/core/absolute.hpp

#ifndef AXABSENT_CORE_ABSOLUTE_HPP
#define AXABSENT_CORE_ABSOLUTE_HPP

#include <string>
#include <unordered_map>
#include <Eigen/Dense>

namespace axabsent {
namespace core {

class Absolute {
public:
    // Constructor
    Absolute();

    // Getters
    std::string get_id() const;
    Eigen::MatrixXd get_signature() const;
    Eigen::VectorXd get_state() const;
    Eigen::VectorXd get_property(const std::string& key) const;

    // Setters
    void set_signature(const Eigen::MatrixXd& signature);
    void set_state(const Eigen::VectorXd& state);
    void set_property(const std::string& key, const Eigen::VectorXd& value);

    // Projection
    Eigen::VectorXd project_state(const Eigen::MatrixXd& projection_matrix) const;

    // Entropic selector (e.g. action scalar from signature)
    double entropy_signature() const;

private:
    std::string id_;
    Eigen::MatrixXd signature_;
    Eigen::VectorXd state_;
    std::unordered_map<std::string, Eigen::VectorXd> properties_;
};

} // namespace core
} // namespace axabsent

#endif // AXABSENT_CORE_ABSOLUTE_HPP
