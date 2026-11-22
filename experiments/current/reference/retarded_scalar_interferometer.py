"""Compact-source, free scalar interferometer in units c=hbar=1."""

from math import isfinite, pi, sin

from scipy.integrate import quad
from scipy.special import spherical_jn


def integrated_source_kernel(distance: float, radius: float, duration: float) -> float:
    """Time integral of one ball's step response, averaged over a second ball."""
    if not all(isfinite(value) for value in (distance, radius, duration)):
        raise ValueError("finite distances, radii and durations are required")
    if not (distance > 2 * radius > 0 and duration >= 0):
        raise ValueError("the identical balls must be disjoint and time nonnegative")
    if duration <= distance - 2 * radius:
        return 0.0
    volume = 4 * pi * radius**3 / 3

    def integrand(offset):
        if offset == 0:
            return 0.0
        overlap = pi * (4 * radius + offset) * (2 * radius - offset) ** 2 / 12
        density = 4 * pi * offset**2 * overlap / volume**2
        lower, upper = distance - offset, distance + offset
        length = max(0, min(duration, upper) - lower)
        angular_mean = (
            length * (duration - lower - length / 2) / (2 * distance * offset)
        )
        return density * angular_mean

    transition = abs(duration - distance)
    points = [transition] if 0 < transition < 2 * radius else None
    return quad(integrand, 0, 2 * radius, points=points)[0] / (4 * pi)


def _dephasing_weight(k, radius, separation):
    if k == 0:
        return 0.0
    ball = 3 * spherical_jn(1, k * radius) / (k * radius)
    x = k * separation
    angular = x * x / 6 if abs(x) < 1e-4 else 1 - sin(x) / x
    return ball * ball * angular / k


def vacuum_dephasing(
    radius: float, separation: float, charge: float, duration: float | None = None
) -> float:
    """Negative log visibility; duration=None gives the long-hold limit."""
    if not all(isfinite(value) for value in (radius, separation, charge)):
        raise ValueError("finite geometry and charge are required")
    if radius <= 0 or separation < 0:
        raise ValueError("radius must be positive and separation nonnegative")
    if duration is not None and (not isfinite(duration) or duration < 0):
        raise ValueError("duration must be finite and nonnegative")
    if separation == 0 or charge == 0 or duration == 0:
        return 0.0

    def weight(k):
        return _dephasing_weight(k, radius, separation)

    options = dict(epsabs=2e-9, limit=250)
    if duration is not None and duration < radius:
        # Avoid subtracting nearly equal integrals for a short hold.
        integral = quad(
            lambda k: 2 * weight(k) * sin(k * duration / 2) ** 2,
            0,
            float("inf"),
            **options,
        )[0]
        return charge**2 * integral / (2 * pi**2)
    integral = quad(weight, 0, float("inf"), **options)[0]
    if duration is not None:
        integral -= quad(
            weight, 0, float("inf"), weight="cos", wvar=duration, **options
        )[0]
    return charge**2 * integral / (2 * pi**2)
