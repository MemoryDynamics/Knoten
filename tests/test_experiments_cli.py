from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "experiments" / "cli.py"
SPEC = importlib.util.spec_from_file_location("experiments_cli", SCRIPT_PATH)
assert SPEC is not None
experiments_cli = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = experiments_cli
SPEC.loader.exec_module(experiments_cli)


def test_cli_catalog_contains_every_current_experiment_script() -> None:
    listed = {
        script
        for scripts in experiments_cli.CATEGORIES.values()
        for script in scripts
        if script.startswith("current/")
    }
    current = {
        path.relative_to(ROOT / "experiments").as_posix()
        for path in (ROOT / "experiments" / "current").rglob("*.py")
        if path.name != "__init__.py"
    }

    assert current <= listed
