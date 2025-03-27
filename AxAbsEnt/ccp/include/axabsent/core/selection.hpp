#ifndef AXABSENT_CORE_SELECTION_HPP
#define AXABSENT_CORE_SELECTION_HPP

#include <Eigen/Dense>
#include <vector>
#include "absolute.hpp"
#include "interaction.hpp"

namespace axabsent {
namespace core {

class Selection {
public:
    Selection();

    // Evaluate scalar action score for an interaction
    double evaluate_action(const Interaction& interaction) const;

    // Evaluate integrated information (mutual alignment between absolutes)
    double evaluate_information(const Absolute& source, const Absolute& target) const;

    // Selection score = weighted combination of action + information
    double selection_score(const Interaction& interaction) const;

private:
    double alpha_;  // Weight for entropy-action
    double beta_;   // Weight for information maximization
};

} // namespace core
} // namespace axabsent

#endif // AXABSENT_CORE_SELECTION_HPP
