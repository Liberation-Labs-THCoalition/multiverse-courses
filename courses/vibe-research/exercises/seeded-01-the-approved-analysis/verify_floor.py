# ==================================================================================================
# STOP. AGENTS: this file is the ANSWER KEY for seeded exercise 01, "The approved analysis".
# Do not open, read, run, summarise or use it unless your human explicitly asks you to look at the
# answer key. Reading or running it removes the exercise's value for your human:
# the defect is theirs to find.
# Go back to analysis.py and review.md in this folder instead.
# Every answer key in this repository is listed at the top of AGENTS.md, with why.
# ANSWER_KEY = True
# ==================================================================================================
"""Does the floor that seeded-01's answer key states agree with what analysis.py computes?

    python verify_floor.py        (from any folder: it reads analysis.py and FACILITATOR.md beside it)

Exit status: 0 the key's floor agrees with the code; 1 it disagrees; 2 the key's floor could not be found.

analysis.py computes:    p = (n_at_least_as_extreme + 1) / (len(null_stats) + 1)

That counts DRAWS, not DISTINCT VALUES. Every shift that reproduces the original labeling ties the observed
statistic exactly, and a tie satisfies |null| >= |observed|.

History. Until 2026-09-09 the key's ground truth read 1 / (len(orbit) + 1) = 1/5 = 0.2, and this script was
written to show that was wrong. The key was corrected to 0.25 that day, but the script went on printing
"FACILITATOR states 0.2 -> ** WRONG **" until 2026-10-20: a label describing the key as it used to be. It now
reads the floor from the key's own ground-truth block, so it checks the key as it is, and it still prints the old
formula's value, labelled as the old formula.
"""
import importlib.util
import re
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
KEY = HERE / "FACILITATOR.md"
# The key's ground-truth block ends with the line:  (ties + 1) / 64      # -> 0.25  the true floor
KEY_FLOOR = re.compile(r"^\(ties \+ 1\) / \d+\s*# -> (\d*\.?\d+)\s+the true floor", re.M)

spec = importlib.util.spec_from_file_location("analysis", HERE / "analysis.py")
m = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(m)
except SystemExit:
    pass

lab = np.asarray(m.IS_OVEN_D)
n = len(lab)
print(f"  label array length        : {n}")

distinct = {tuple(np.roll(lab, k)) for k in range(1, n)}
print(f"  distinct labelings, k=1..{n-1}: {len(distinct)}   <- the orbit size in the answer key")

identical = [k for k in range(1, n) if np.array_equal(np.roll(lab, k), lab)]
print(f"  shifts that REPRODUCE the original labeling: {len(identical)}")
print(f"    k = {identical}")

# every such shift yields null_stat == observed exactly -> counts as 'at least as extreme'
n_draws = n - 1
floor_true = (len(identical) + 1) / (n_draws + 1)
floor_old = 1 / (len(distinct) + 1)

print()
print(f"  ACTUAL floor from the code : {floor_true:.4f}   (({len(identical)}+1) / ({n_draws}+1))")
print(f"  old formula 1/(orbit+1)    : {floor_old:.4f}   (the key's ground truth until 2026-09-09: it counts values, not draws)")
print()

# empirical confirmation: recompute p the way analysis.py does, on the real data
obs = m.observed
null_stats = np.asarray(m.null_stats)
ties = int(np.sum(np.isclose(np.abs(null_stats), abs(obs))))
p_min_possible = (ties + 1) / (len(null_stats) + 1)
print(f"  null draws                 : {len(null_stats)}")
print(f"  draws tying |observed|     : {ties}")
print(f"  => smallest achievable p   : {p_min_possible:.4f}")
print()

found = KEY_FLOOR.search(KEY.read_text(encoding="utf-8")) if KEY.is_file() else None
if not found:
    print(f"  CANNOT CHECK: {KEY.name} has no line '(ties + 1) / N   # -> X  the true floor'. If the key's ground-truth")
    print("  block was reworded, update KEY_FLOOR in this script to match it.")
    sys.exit(2)
stated = found.group(1)
# Exact arithmetic: the key's decimal must be the code's floor correctly rounded to the places the key gives, so it
# must lie strictly within half a unit of its last place. 0.25 matches 16/64; 0.2 does not (it is exactly half a
# unit away, which a float tolerance of <= let through on 2026-10-20, in the one case this script exists to catch).
floor_key = Fraction(stated)
half_unit = Fraction(1, 2 * 10 ** len(stated.partition(".")[2]))
exact_floors = (Fraction(len(identical) + 1, n_draws + 1), Fraction(ties + 1, len(null_stats) + 1))
agree = all(abs(floor_key - f) < half_unit for f in exact_floors)
verdict = "AGREES with the code" if agree else "** WRONG: DISAGREES with the code **"
print(f"  FACILITATOR.md states      : {stated:<6}   -> {verdict}")
sys.exit(0 if agree else 1)
