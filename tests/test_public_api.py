from types import ModuleType

import emergenz_knoten


def test_root_public_symbols_and_all_are_identical():
    declared = set(emergenz_knoten.__all__)
    imported = {
        name
        for name, value in vars(emergenz_knoten).items()
        if not name.startswith("_") and not isinstance(value, ModuleType)
    }

    assert len(declared) == len(emergenz_knoten.__all__)
    assert imported == declared
