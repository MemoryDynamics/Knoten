from __future__ import annotations

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pyproject_discovers_markov_subpackage() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    find_config = data["tool"]["setuptools"]["packages"]["find"]

    assert find_config["where"] == ["src"]
    assert "emergenz_knoten*" in find_config["include"]
