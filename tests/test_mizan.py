#!/usr/bin/env python3
"""One runnable check for evals/mizan.py scoring, no CLI calls.
python3 tests/test_mizan.py"""
import importlib.util, sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("mizan", Path(__file__).resolve().parents[1] / "evals/mizan.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

assert m.REF.search("/x/skills/black-iris/references/athar.md").group(1) == "athar"
assert m.REF.search("/x/black-iris/1.15.0/skills/black-iris/references/naming.md").group(1) == "naming"
assert not m.REF.search("/x/references/athar.md.bak")
assert m.score({"mode": "athar"}, ["athar"]) == "hit"
assert m.score({"mode": "athar"}, ["dabke", "athar"]) == "extra"
assert m.score({"mode": "athar"}, ["dabke"]) == "wrong"
assert m.score({"mode": "athar"}, [], loaded=True) == "miss"
assert m.score({"mode": "athar"}, []) == "skip"
assert m.score({"mode": "name"}, ["naming"]) == "hit"
assert m.score({"mode": "none"}, []) == "hit" and m.score({"mode": "shape"}, ["deslop"]) == "false fire"
print("mizan: pass")
