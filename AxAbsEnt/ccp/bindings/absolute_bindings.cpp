#ifndef AXABSENT_ABSOLUTE_HPP
#define AXABSENT_ABSOLUTE_HPP

#include <string>
#include <unordered_map>
#include <Eigen/Dense>

namespace axabsent {
namespace core {

class Absolute {
public:
    Absolute();
    std::string get_id() const;

    Eigen::MatrixXd get_signature() const;
    void set_signature(const Eigen::MatrixXd& sig);

    Eigen::VectorXd get_state() const;
    void set_state(const Eigen::VectorXd& state);

    void set_property(const std::string& key, const Eigen::VectorXd& value);
    Eigen::VectorXd get_property(const std::string& key) const;

    Eigen::VectorXd project_state(const Eigen::MatrixXd& transform) const;
    double entropy_signature() const;

private:
    std::string id_;
    Eigen::MatrixXd signature_;
    Eigen::VectorXd state_;
    std::unordered_map<std::string, Eigen::VectorXd> properties_;
};

} // namespace core
} // namespace axabsent

#endif // AXABSENT_ABSOLUTE_HPP
