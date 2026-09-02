from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _inspect_nav(items: list[object], *, depth: int = 1) -> tuple[int, list[str]]:
    assert len(items) <= 7, f"navigation level has {len(items)} entries"
    assert depth <= 7, f"navigation exceeds seven levels at depth {depth}"
    maximum_depth = depth
    paths: list[str] = []
    for item in items:
        assert isinstance(item, dict) and len(item) == 1
        value = next(iter(item.values()))
        if isinstance(value, list):
            child_depth, child_paths = _inspect_nav(value, depth=depth + 1)
            maximum_depth = max(maximum_depth, child_depth)
            paths.extend(child_paths)
        else:
            assert isinstance(value, str)
            paths.append(value)
    return maximum_depth, paths


def test_active_documentation_obeys_seven_by_seven_rule() -> None:
    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    maximum_depth, paths = _inspect_nav(config["nav"])
    assert maximum_depth <= 7
    assert len(config["nav"]) <= 7
    assert paths.count("status/project_priorities.md") == 1


def test_only_canonical_frontdoor_contains_ordered_priorities() -> None:
    priorities = (ROOT / "docs/status/project_priorities.md").read_text(
        encoding="utf-8"
    )
    ordered = re.findall(r"(?m)^\d+\. \*\*", priorities)
    assert 1 <= len(ordered) <= 7

    for relative in (
        "README.md",
        "docs/index.md",
        "docs/status/current_status.md",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "## Naechste Prioritaeten" not in text
        assert not re.search(r"(?m)^\d+\. \*\*", text)


def test_reverse_specification_names_core_code_parameters() -> None:
    text = (ROOT / "docs/reference/implemented_equations.md").read_text(
        encoding="utf-8"
    )
    for token in (
        "B_H(z)",
        "W_H(z)",
        "\\alpha",
        "\\varepsilon",
        "\\eta",
        "\\sigma",
        "M_0",
        "$N$",
        "$H$",
    ):
        assert token in text
    assert "B_H(1)=1" in text
    assert "\\beta_s" not in text
    assert "g=|c_0|" not in text
    assert "F,qquad" not in text
    assert "Newton-Gleichung" in text
    assert "keine neue Modellannahme" in text


def test_canonical_vocabulary_separates_core_filter_and_port_symbols() -> None:
    vocabulary = (ROOT / "docs/reference/model_vocabulary.md").read_text(
        encoding="utf-8"
    )
    for token in (
        "\\beta_\\rho",
        "B_H(1)=1",
        "b_s=B_H",
        "a_j^{(s)}",
        "\\gamma_{\\rm w}",
        "\\mu_{\\rm w}",
        "unit_roundoff",
        "notch_response",
    ):
        assert token in vocabulary

    for relative in (
        "docs/reference/implemented_equations.md",
        "docs/reference/scalar_memory_center_filter.md",
        "docs/reference/THEORETICAL_CONTEXT.md",
        "paper/paper_i/manuscript/main.tex",
        "paper/paper_i/manuscript/main_compact.tex",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert not re.search(r"\\beta(?![_A-Za-z])", text), relative

    paper = (ROOT / "paper/paper_i/manuscript/main.tex").read_text(
        encoding="utf-8"
    )
    assert "\\lambda_{\\mathrm m}=\\beta_\\rho=\\alpha" in paper
