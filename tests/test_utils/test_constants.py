import pytest
from axabsent.utils.constants import (
    PHYSICAL_CONSTANTS,
    MATHEMATICAL_CONSTANTS,
    COUPLING_CONSTANTS,
    RESONANCE_FREQUENCIES
)


@pytest.mark.math
def test_physical_constants_correctness():
    """
    Validate essential physical constants against expected SI values.
    """
    assert "speed_of_light" in PHYSICAL_CONSTANTS
    assert pytest.approx(PHYSICAL_CONSTANTS["speed_of_light"], rel=1e-9) == 299_792_458.0

    assert "planck_constant" in PHYSICAL_CONSTANTS
    assert pytest.approx(PHYSICAL_CONSTANTS["planck_constant"], rel=1e-9) == 6.62607015e-34

    assert "gravitational_constant" in PHYSICAL_CONSTANTS
    assert pytest.approx(PHYSICAL_CONSTANTS["gravitational_constant"], rel=1e-9) == 6.67430e-11


@pytest.mark.math
def test_mathematical_constants_values():
    """
    Validate mathematical constants (e.g., π, e, φ).
    """
    assert "pi" in MATHEMATICAL_CONSTANTS
    assert pytest.approx(MATHEMATICAL_CONSTANTS["pi"], rel=1e-12) == 3.141592653589793

    assert "euler" in MATHEMATICAL_CONSTANTS
    assert pytest.approx(MATHEMATICAL_CONSTANTS["euler"], rel=1e-12) == 2.718281828459045

    assert "golden_ratio" in MATHEMATICAL_CONSTANTS
    φ = (1 + 5 ** 0.5) / 2
    assert pytest.approx(MATHEMATICAL_CONSTANTS["golden_ratio"], rel=1e-12) == φ


@pytest.mark.math
def test_coupling_constants_model_defined():
    """
    Check that theoretical coupling constants are defined and bounded.
    """
    assert "alpha_gravity" in COUPLING_CONSTANTS
    assert 0 < COUPLING_CONSTANTS["alpha_gravity"] < 1e-8

    assert "alpha_em" in COUPLING_CONSTANTS
    assert pytest.approx(COUPLING_CONSTANTS["alpha_em"], rel=1e-5) == 1 / 137


@pytest.mark.math
def test_resonance_frequencies_are_positive():
    """
    All resonance frequencies must be real, finite, and > 0.
    """
    for name, freq in RESONANCE_FREQUENCIES.items():
        assert isinstance(freq, float)
        assert freq > 0.0
        assert freq < 1e+30  # within physical meaning


@pytest.mark.math
def test_constants_are_readonly():
    """
    Constants must not be reassignable at runtime.
    """
    with pytest.raises(TypeError):
        PHYSICAL_CONSTANTS["speed_of_light"] = 123.456
