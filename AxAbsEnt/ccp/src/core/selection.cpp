#include "axabsent/core/selection.hpp"
#include <cmath>

using namespace axabsent::core;

Selection::Selection()
    : alpha_(1.0), beta_(1.0) {}

// Evaluate the entropy-based action cost
double Selection::evaluate_action(const Interaction& interaction) const {
    return interaction.get_action_cost();  // Tr(O O^T)
}

// Evaluate integrated information from signature overlap
double Selection::evaluate_information(const Absolute& source, const Absolute& target) const {
    Eigen::MatrixXd S = source.get_signature();
    Eigen::MatrixXd T = target.get_signature();

    double dot = (S.cwiseProduct(T)).sum();
    double norm = std::sqrt((S.array().square().sum()) * (T.array().square().sum()));
    if (norm == 0) return 0.0;
    return dot / norm;  // Cosine similarity of tensors
}

// Final selection score
double Selection::selection_score(const Interaction& interaction) const {
    double action = evaluate_action(interaction);
    double info = evaluate_information(interaction.get_operator() * interaction.apply(), interaction.apply());

    // Lower action + higher information → better
    return alpha_ * (-action) + beta_ * info;
}

