// Declared in: cpp/include/axabsent/mathematics/tensor.hpp
#ifndef AXABSENT_MATHEMATICS_TENSOR_HPP
#define AXABSENT_MATHEMATICS_TENSOR_HPP

#include <Eigen/Dense>

namespace axabsent {
namespace mathematics {

class TensorOps {
public:
    // Contract 2D tensor along trace
    static double trace(const Eigen::MatrixXd& T);

    // Normalize tensor to unit Frobenius norm
    static Eigen::MatrixXd normalize(const Eigen::MatrixXd& T);

    // Outer product of two vectors
    static Eigen::MatrixXd outer(const Eigen::VectorXd& a, const Eigen::VectorXd& b);

    // Double contraction: Tr(A * B^T)
    static double double_contraction(const Eigen::MatrixXd& A, const Eigen::MatrixXd& B);
};

} // namespace mathematics
} // namespace axabsent

#endif // AXABSENT_MATHEMATICS_TENSOR_HPP
