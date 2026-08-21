import numpy as np
from mpmath import iv
import pytest

from emergenz_knoten.rotating_wave import finite_h_rotating_wave_residual
from emergenz_knoten.rotating_wave_interval import (
    IntervalRotatingWaveParameters,
    certify_rotating_wave_box,
    krawczyk_image,
    point_balance_and_jacobian,
)


def _parameters(horizon: int = 17) -> IntervalRotatingWaveParameters:
    return IntervalRotatingWaveParameters(
        alpha="0.07",
        horizon=horizon,
        memory_mass="1.2",
        eta="0.18",
        sigma_rep="1.0",
        sigma_att="3.0",
        amplitude_rep="1.0",
        amplitude_att="4.5",
    )


def _float_balance(radius: float, theta: float, horizon: int = 17) -> np.ndarray:
    value = finite_h_rotating_wave_residual(
        radius=radius,
        theta=theta,
        alpha=0.07,
        horizon=horizon,
        memory_mass=1.2,
        eta=0.18,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=4.5,
    )
    return np.asarray([-value.real, value.imag])


def test_point_balance_matches_native_residual_and_finite_difference_jacobian():
    radius = 1.1
    theta = 0.13
    evaluation = point_balance_and_jacobian(
        radius=str(radius),
        theta=str(theta),
        parameters=_parameters(),
        precision_dps=70,
    )
    balance = np.asarray([float(value) for value in evaluation["balance"]])
    jacobian = np.asarray(
        [[float(value) for value in row] for row in evaluation["jacobian"]]
    )
    expected = _float_balance(radius, theta)
    step = 1.0e-6
    finite_difference = np.column_stack(
        (
            (
                _float_balance(radius + step, theta)
                - _float_balance(radius - step, theta)
            )
            / (2.0 * step),
            (
                _float_balance(radius, theta + step)
                - _float_balance(radius, theta - step)
            )
            / (2.0 * step),
        )
    )

    np.testing.assert_allclose(balance, expected, rtol=0.0, atol=2.0e-16)
    np.testing.assert_allclose(
        jacobian,
        finite_difference,
        rtol=2.0e-9,
        atol=2.0e-10,
    )


def test_generic_krawczyk_image_lies_inside_known_root_box():
    previous_dps = iv.dps
    iv.dps = 60
    try:
        center = (iv.mpf("1.01"), iv.mpf("0.99"))
        box = (
            center[0] + iv.mpf(["-0.1", "0.1"]),
            center[1] + iv.mpf(["-0.1", "0.1"]),
        )
        function_at_center = (
            center[0] ** 2 + center[1] - 2,
            center[0] + center[1] ** 2 - 2,
        )
        jacobian_box = (
            (2 * box[0], iv.mpf(1)),
            (iv.mpf(1), 2 * box[1]),
        )
        determinant = iv.mpf("2.02") * iv.mpf("1.98") - 1
        inverse = (
            (iv.mpf("1.98") / determinant, -iv.mpf(1) / determinant),
            (-iv.mpf(1) / determinant, iv.mpf("2.02") / determinant),
        )

        image = krawczyk_image(
            center=center,
            box=box,
            function_at_center=function_at_center,
            jacobian_box=jacobian_box,
            inverse_point_jacobian=inverse,
        )

        for value, outer in zip(image, box, strict=True):
            assert float(value.a) > float(outer.a)
            assert float(value.b) < float(outer.b)
            assert float(value.a) < 1.0 < float(value.b)
    finally:
        iv.dps = previous_dps


def test_interval_evaluation_encloses_unrelated_point_evaluation():
    radius = "1.1"
    theta = "0.13"
    certificate = certify_rotating_wave_box(
        radius=radius,
        theta=theta,
        radius_half_width="1e-8",
        theta_half_width="1e-8",
        parameters=_parameters(),
        precision_dps=60,
    )
    point = point_balance_and_jacobian(
        radius=radius,
        theta=theta,
        parameters=_parameters(),
        precision_dps=70,
    )

    for interval, value in zip(
        certificate["function_box"], point["balance"], strict=True
    ):
        assert float(interval["lower"]) <= float(value) <= float(interval["upper"])
    for interval_row, point_row in zip(
        certificate["jacobian_box"], point["jacobian"], strict=True
    ):
        for interval, value in zip(interval_row, point_row, strict=True):
            assert (
                float(interval["lower"]) <= float(value) <= float(interval["upper"])
            )


@pytest.mark.parametrize(
    ("field", "value"),
    (("alpha", "0"), ("horizon", 1), ("eta", "nan")),
)
def test_interval_parameters_reject_invalid_values(field: str, value: object):
    values = {
        "alpha": "0.07",
        "horizon": 17,
        "memory_mass": "1.2",
        "eta": "0.18",
        "sigma_rep": "1.0",
        "sigma_att": "3.0",
        "amplitude_rep": "1.0",
        "amplitude_att": "4.5",
    }
    values[field] = value
    with pytest.raises(ValueError):
        IntervalRotatingWaveParameters(**values)
