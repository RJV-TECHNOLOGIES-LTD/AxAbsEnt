#include "axabsent/mathematics/tensor.hpp"
#include <stdexcept>
#include <cmath>

using namespace axabsent::mathematics;

// Trace of square matrix
double TensorOps::trace(const Eigen::MatrixXd& T) {
    if (T.rows() != T.cols()) {
        throw std::invalid_argument("Trace requires a square matrix.");
    }
    return T.trace();
}

// Normalize to unit Frobenius norm
Eigen::MatrixXd TensorOps::normalize(const Eigen::MatrixXd& T) {
    double norm = T.norm();
    if (norm == 0.0) {
        throw std::runtime_error("Cannot normalize a zero tensor.");
    }
    return T / norm;
}

// Outer product: a ⊗ b
Eigen::MatrixXd TensorOps::outer(const Eigen::VectorXd& a, const Eigen::VectorXd& b) {
    return a * b.transpose();
}

// Double contraction: Tr(A * B^T)
double TensorOps::double_contraction(const Eigen::MatrixXd& A, const Eigen::MatrixXd& B) {
    if (A.rows() != B.rows() || A.cols() != B.cols()) {
        throw std::invalid_argument("Double contraction requires matrices of the same shape.");
    }
    return (A * B.transpose()).trace();
}
