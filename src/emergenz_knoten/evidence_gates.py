"""Dependency-aware status objects for scientific evidence gates."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum


class GateStatus(StrEnum):
    """Machine-readable outcome of one scientific decision gate."""

    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    BLOCKED = "blocked"
    NOT_RUN = "not-run"


@dataclass(frozen=True)
class EvidenceGate:
    """One gate together with checks and unmet upstream dependencies."""

    name: str
    status: GateStatus
    passed_checks: tuple[str, ...] = ()
    failed_checks: tuple[str, ...] = ()
    blocked_by: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return self.status == GateStatus.PASS


def evaluate_evidence_gate(
    name: str,
    checks: Mapping[str, bool] | None,
    *,
    prerequisites: Sequence[EvidenceGate] = (),
    failed_status: GateStatus = GateStatus.FAIL,
) -> EvidenceGate:
    """Evaluate one gate without collapsing missing information into failure.

    ``checks=None`` denotes a gate that has not been run. A non-passing
    prerequisite blocks the gate before its own checks are interpreted.
    ``failed_status=INCONCLUSIVE`` is reserved for adequacy gates where a
    failed check means that the experiment cannot decide the physical claim.
    """

    if not name.strip():
        raise ValueError("gate name must not be empty")
    if failed_status not in (GateStatus.FAIL, GateStatus.INCONCLUSIVE):
        raise ValueError("failed_status must be fail or inconclusive")

    blocked_by = tuple(gate.name for gate in prerequisites if not gate.passed)
    if blocked_by:
        return EvidenceGate(
            name=name,
            status=GateStatus.BLOCKED,
            blocked_by=blocked_by,
        )
    if checks is None:
        return EvidenceGate(name=name, status=GateStatus.NOT_RUN)
    if not checks:
        raise ValueError("a tested gate must contain at least one check")

    invalid = [key for key, value in checks.items() if not isinstance(value, bool)]
    if invalid:
        raise TypeError(f"gate checks must be bool: {invalid}")
    passed = tuple(key for key, value in checks.items() if value)
    failed = tuple(key for key, value in checks.items() if not value)
    return EvidenceGate(
        name=name,
        status=GateStatus.PASS if not failed else failed_status,
        passed_checks=passed,
        failed_checks=failed,
    )
