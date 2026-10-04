import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "requirements-lock.txt"


def _locked_requirements() -> dict[str, tuple[str, int]]:
    lines = LOCK.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str, str]] = []
    pattern = re.compile(r"^([A-Za-z0-9_.-]+)==([^ \\]+) \\$")
    for index, line in enumerate(lines):
        match = pattern.fullmatch(line)
        if match:
            starts.append((index, match.group(1).lower().replace("_", "-"), match.group(2)))

    locked: dict[str, tuple[str, int]] = {}
    for position, (start, name, version) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        hash_count = sum("--hash=sha256:" in line for line in lines[start:stop])
        assert hash_count > 0, name
        locked[name] = (version, hash_count)
    return locked


def test_transitive_lock_is_complete_and_hashed() -> None:
    lock_text = LOCK.read_text(encoding="utf-8")
    locked = _locked_requirements()
    expected_direct = {
        "numpy": "2.3.5",
        "matplotlib": "3.10.8",
        "numba": "0.63.1",
        "scipy": "1.17.1",
        "pandas": "3.0.3",
        "mpmath": "1.3.0",
        "pytest": "9.0.3",
        "ripser": "0.6.15",
        "ruff": "0.15.21",
        "mkdocs": "1.6.1",
        "pymdown-extensions": "10.21.3",
        "setuptools": "84.0.0",
        "wheel": "0.48.0",
    }

    assert {name: locked[name][0] for name in expected_direct} == expected_direct
    assert len(locked) == 50
    assert sum(hash_count for _, hash_count in locked.values()) == 1219
    assert "--no-index" not in lock_text
    assert "--emit-index-url" in lock_text


def test_ci_installs_the_lock_without_dependency_reresolution() -> None:
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "pip install --require-hashes -r requirements-lock.txt" in workflow
    assert "pip install --no-deps --no-build-isolation -e ." in workflow
    assert "pip install -r requirements.txt" not in workflow
    assert "pip install -r requirements-dev.txt" not in workflow


def test_citation_metadata_matches_the_manuscript_and_package() -> None:
    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    manuscript = (ROOT / "paper/paper_i/manuscript/main.tex").read_text(
        encoding="utf-8"
    )
    package = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert citation["cff-version"] == "1.2.0"
    assert "date-released" not in citation
    assert citation["authors"] == [{"family-names": "Horn", "given-names": "H."}]
    assert citation["preferred-citation"]["authors"] == citation["authors"]
    assert citation["preferred-citation"]["year"] == 2026
    assert r"\author{H. Horn}" in manuscript
    assert citation["preferred-citation"]["title"] in manuscript
    assert '{ name = "H. Horn" }' in package


def test_release_blockers_remain_narrow_and_scientific() -> None:
    manifest = yaml.safe_load(
        (ROOT / "paper/paper_i/supplement/evidence_manifest.json").read_text(
            encoding="utf-8"
        )
    )

    assert manifest["release_blockers"] == [
        "Independent replication of the interval certificates with a second backend is absent.",
        "No archival release identifier or DOI has been minted.",
    ]
