"""Small standard-library validator for repository result contracts.

The contract language is intentionally narrower than JSON Schema.  It exists
to enforce exact object keys, native JSON scalars, fixed array cardinalities,
and registered constants without adding a runtime dependency.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
import math
import re
from typing import Any


_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_UUID4 = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z"
)


def _fail(path: str, expected: str, value: Any) -> None:
    raise ValueError(f"{path}: expected {expected}, got {type(value).__name__}")


def _primitive(value: Any, specification: str, *, path: str) -> None:
    if specification == "boolean":
        valid = type(value) is bool
    elif specification == "integer":
        valid = type(value) is int
    elif specification == "number":
        valid = type(value) in (int, float) and math.isfinite(value)
    elif specification == "string":
        valid = type(value) is str
    elif specification == "null":
        valid = value is None
    elif specification == "sha1":
        valid = type(value) is str and _SHA1.fullmatch(value) is not None
    elif specification == "sha256":
        valid = type(value) is str and _SHA256.fullmatch(value) is not None
    elif specification == "uuid4":
        valid = type(value) is str and _UUID4.fullmatch(value) is not None
    elif specification == "decimal":
        try:
            valid = type(value) is str and Decimal(value).is_finite()
        except InvalidOperation:
            valid = False
    else:
        raise ValueError(f"{path}: unknown primitive {specification!r}")
    if not valid:
        _fail(path, specification, value)


def validate_value(
    value: Any,
    specification: str,
    *,
    path: str,
    contract: dict[str, Any],
) -> None:
    """Validate one value and reject all unregistered fields and types."""

    if specification.startswith("nullable:"):
        if value is None:
            return
        specification = specification.split(":", 1)[1]
    if ":" not in specification:
        _primitive(value, specification, path=path)
        return

    namespace, name = specification.split(":", 1)
    if namespace == "const":
        if value != contract["constants"][name]:
            _fail(path, f"constant {name}", value)
        return
    if namespace == "enum":
        if value not in contract["enums"][name]:
            _fail(path, f"enum {name}", value)
        return
    if namespace == "object":
        rule = contract["objects"][name]
        if type(value) is not dict or set(value) != set(rule):
            _fail(path, f"exact object {name}", value)
        for key, child in rule.items():
            validate_value(
                value[key], child, path=f"{path}.{key}", contract=contract
            )
        return
    if namespace == "array":
        rule = contract["arrays"][name]
        if type(value) is not list:
            _fail(path, f"array {name}", value)
        if "length" in rule and len(value) != rule["length"]:
            _fail(path, f"array {name} of length {rule['length']}", value)
        if "min_length" in rule and len(value) < rule["min_length"]:
            _fail(path, f"array {name} with minimum length", value)
        if "max_length" in rule and len(value) > rule["max_length"]:
            _fail(path, f"array {name} with maximum length", value)
        for index, item in enumerate(value):
            validate_value(
                item,
                rule["item"],
                path=f"{path}[{index}]",
                contract=contract,
            )
        return
    raise ValueError(f"{path}: unknown contract namespace {namespace!r}")


def validate_payload(payload: Any, contract: dict[str, Any]) -> None:
    """Validate a complete payload against the contract root."""

    if type(contract) is not dict or set(contract) != {
        "arrays",
        "constants",
        "enums",
        "objects",
        "root",
        "schema",
    }:
        raise ValueError("$: malformed result contract")
    validate_value(payload, contract["root"], path="$", contract=contract)
