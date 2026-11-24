"""Small algebraic controls for existing energy/infrared architectures.

No native trajectories, source motion, parameter fitting, or new field law.
"""

from dataclasses import replace
from fractions import Fraction

import numpy as np
import pytest

from emergenz_knoten.active_scalar_field import (
    ActiveScalarFieldConfig,
    scalar_field_linear_rate,
)
from emergenz_knoten.continuity_memory import (
    continuity_memory_mode_operator,
    memory_innovation_moments,
)
from emergenz_knoten.covariant_vector_field import (
    InertialVectorFieldDynamics,
    LocalVectorFieldExpansion,
    inertial_vector_frequency_response,
)
from emergenz_knoten.dynamic_gradient_mediator import (
    SecondOrderMediatorState,
    build_isotropic_mediator_modes,
    modal_source,
    modal_static_pair_energy,
    second_order_energy,
)
from emergenz_knoten.gradient_mediator import gradient_mediator_transfer
from emergenz_knoten.local_mediator import (
    RelaxationDiffusionMediator,
    TelegraphMediator,
    relaxation_diffusion_frequency_response,
    telegraph_frequency_response,
)
from emergenz_knoten.relaxation_diffusion_memory import (
    RelaxationDiffusionMemoryOperators,
)
from emergenz_knoten.spectral_memory_field import (
    SpectralMemoryConfig,
    zero_mean_attractive_kernel,
    kernel_transfer,
)
from emergenz_knoten.vector_memory import vector_gaussian_field, vector_memory_force


def test_spectral_relaxation_diffusion_fixed_point_includes_source_normalization():
    config = SpectralMemoryConfig(
        n_modes=5, box_length=8, lambda_value=0.2, memory_mass=1.7, deposition_sigma=0.1
    )
    operators = RelaxationDiffusionMemoryOperators(config, diffusion_per_update=0.3)
    deposition = operators.deposition(0.4)
    steady = (
        config.lambda_value
        * operators.heat_transfer
        * deposition
        / (1 - (1 - config.lambda_value) * operators.heat_transfer)
    )
    np.testing.assert_allclose(
        operators.update_rho(steady, deposited_at=0.4), steady, rtol=2e-15
    )
    assert steady[0].real * config.box_length == pytest.approx(config.memory_mass)


def test_zero_mean_compensation_removes_dc_instead_of_creating_a_pole():
    config = SpectralMemoryConfig(kernel=zero_mean_attractive_kernel())
    assert abs(kernel_transfer(config)[0]) < 1e-12
    assert np.isfinite(kernel_transfer(config)).all()


def test_normalized_forgetting_limit_loses_nonzero_mode_residue():
    # Exact rational heat multiplier, fixed nonzero mode; alpha tends to zero
    # with beta=alpha*M, unlike an independently sustained source beta.
    heat, mass = Fraction(4, 5), Fraction(3, 2)
    values = []
    for alpha in (Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000)):
        response = alpha * mass * heat / (1 - (1 - alpha) * heat)
        assert response <= alpha * mass * heat / (1 - heat)
        values.append(response)
    assert values[2] < values[1] < values[0]
    assert mass * heat / (1 - heat) > 0  # fixed-source limit would instead be nonzero


def test_existing_local_scalar_channels_allow_massless_response_but_not_automatically():
    k = np.array([0.1, 0.03, 0.01])
    for decay in (0.0, 0.2):
        diffusion = RelaxationDiffusionMediator(diffusivity=2, decay_rate=decay)
        response = relaxation_diffusion_frequency_response(k, 0, diffusion)
        np.testing.assert_allclose(response, 1 / (2 * k * k + decay))
        if decay == 0:
            np.testing.assert_allclose(k * k * response, 0.5)
        else:
            assert (k * k * response).real[-1] < (k * k * response).real[0]
    for damping in (0.0, 0.4):
        wave = TelegraphMediator(
            wave_speed=2, damping_rate=damping, natural_frequency=0
        )
        response = telegraph_frequency_response(k, 0, wave)
        np.testing.assert_allclose(k * k * response, 0.25)


def test_continuity_density_source_retains_its_numerator():
    k, stiffness = 0.2, 1.3
    for memory_decay, flux_decay in ((0.2, 0.4), (0, 0.4), (0.2, 0)):
        matrix = continuity_memory_mode_operator(
            k,
            memory_relaxation=memory_decay,
            flux_relaxation=flux_decay,
            stiffness=stiffness,
        )
        steady = np.linalg.solve(-matrix, np.array([1.0, 0.0]))
        assert steady[0] == pytest.approx(
            flux_decay / (memory_decay * flux_decay + stiffness * k * k)
        )
    # gamma=0 removes the static density numerator as well as the gap.
    assert steady[0] == 0


def test_gradient_mediator_read_write_geometry_changes_pole_order():
    parameters = dict(
        memory_decay=0.2,
        conjugate_decay=0.3,
        local_stiffness=1.2,
        gradient_stiffness=0.4,
        biharmonic_stiffness=0.7,
        coupling=0.6,
    )
    k = np.array([0, 0.1, 0.03])
    direct = gradient_mediator_transfer(
        k, coupling_geometry="direct_scalar", **parameters
    )
    gradient = gradient_mediator_transfer(k, **parameters)
    np.testing.assert_allclose(gradient, k * k * direct)
    assert direct[0] == pytest.approx(0.6**2 / (0.2 * 0.3))
    assert gradient[0] == 0
    # Even formally removing the gap leaves k^2/(a*k^2+...) finite.
    t = Fraction(1, 10000)
    gapless_gradient = t / (
        Fraction(6, 5) * t + Fraction(2, 5) * t * t + Fraction(7, 10) * t**3
    )
    assert gapless_gradient < Fraction(5, 6)
    assert t * gapless_gradient < Fraction(1, 10000)


@pytest.mark.parametrize(
    "override", [{"memory_decay": 0}, {"conjugate_decay": 0}, {"local_stiffness": 0}]
)
def test_gradient_mediator_critical_boundaries_are_not_existing_valid_parameters(
    override,
):
    parameters = dict(
        memory_decay=0.2,
        conjugate_decay=0.3,
        local_stiffness=1.2,
        gradient_stiffness=0.4,
        biharmonic_stiffness=0.7,
    )
    with pytest.raises(ValueError):
        gradient_mediator_transfer(0.1, **(parameters | override))


def test_active_vector_massless_boundary_is_distinct_from_gradient_source_port():
    energy = LocalVectorFieldExpansion(
        mass_coefficient=0,
        longitudinal_gradient_coefficient=2,
        transverse_gradient_coefficient=3,
        biharmonic_coefficient=0.4,
        cubic_saturation=0,
    )
    for damping in (0, 0.3):
        dynamics = InertialVectorFieldDynamics(
            energy=energy, inertia=1.4, damping=damping
        )
        for k in (0.1, 0.03):
            response = inertial_vector_frequency_response(
                0, k, dynamics, channel="longitudinal"
            )
            assert k * k * response == pytest.approx(1 / (2 + 0.4 * k * k))
            # Adjoint gradient source/readout adds k^2; the pair response
            # is bounded, despite the source-to-field pole.
            assert abs(k * k * response) <= 0.5


def test_active_scalar_zero_background_has_fixed_mass_term():
    config = ActiveScalarFieldConfig()
    assert scalar_field_linear_rate(config, np.array([0.0]))[0] == -1
    other = replace(config, gradient_coefficient=2.0)
    assert scalar_field_linear_rate(other, np.array([0.0]))[0] == -1


def test_oriented_gaussian_field_keeps_spatial_gaussian_decay():
    positions, orientations, weights = (
        np.zeros((1, 3)),
        np.array([[0, 1, 0]]),
        np.array([2.0]),
    )
    for distance in (1, 4):
        x = np.array([distance, 0, 0])
        value = vector_gaussian_field(x, positions, orientations, weights, sigma=1)
        np.testing.assert_allclose(value, [0, 2 * np.exp(-(distance**2) / 2), 0])
        np.testing.assert_array_equal(
            vector_memory_force(x, positions, orientations, weights, sigma=1), value
        )


def test_constructed_mediator_energy_completes_square_with_negative_source_term():
    modes = build_isotropic_mediator_modes(
        n_wavenumber=4, n_direction=4, k_max=2, spectral_shape=-1.0, memory_loading=0.3
    )
    source = modal_source(modes, 2.0)
    equilibrium = source / modes.restoring
    offset = np.linspace(-0.01, 0.01, modes.n_modes)
    velocity = 0.3 * offset
    state = SecondOrderMediatorState(2.0, equilibrium + offset, velocity)
    minimum = modal_static_pair_energy(modes, 2.0)
    assert minimum == pytest.approx(-0.5 * np.dot(source, equilibrium))
    assert second_order_energy(state, modes) - minimum == pytest.approx(
        0.5 * np.dot(modes.restoring * offset, offset)
        + 0.5 * np.dot(velocity, velocity)
    )


def test_equal_scalar_sources_have_opposite_cross_energy_to_gauss_constrained_flux():
    # A tiny positive Dirichlet Poisson matrix suffices to fix the energy sign;
    # this is not a 3D Coulomb approximation or a particle simulation.
    laplacian = np.array([[2.0, -1.0], [-1.0, 2.0]])
    inverse = np.linalg.inv(laplacian)
    source_a, source_b = np.eye(2)
    cross = source_a @ inverse @ source_b
    assert cross > 0
    for sign in (-1, 1):
        total = source_a + sign * source_b
        relaxation_energy = -0.5 * total @ inverse @ total
        gauss_energy = 0.5 * total @ inverse @ total
        scalar_cross = relaxation_energy + 0.5 * (inverse[0, 0] + inverse[1, 1])
        constrained_cross = gauss_energy - 0.5 * (inverse[0, 0] + inverse[1, 1])
        assert scalar_cross == pytest.approx(-sign * cross)
        assert constrained_cross == pytest.approx(sign * cross)


def test_memory_innovation_is_neutral_when_total_occupancy_is_balanced():
    result = memory_innovation_moments(
        memory_relaxation=0.2,
        target_mass=1,
        current_mass=1,
        current_centroid=np.zeros(3),
        deposited_position=np.ones(3),
    )
    assert result.monopole == 0
    np.testing.assert_allclose(result.first_moment, 0.2 * np.ones(3))
