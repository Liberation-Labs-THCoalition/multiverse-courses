"""Is seeded-01's stated floor of 0.2 correct, or is the true floor 0.25?

The FACILITATOR claims:  1 / (len(orbit) + 1) = 1/5 = 0.2
analysis.py computes:    p = (n_at_least_as_extreme + 1) / (len(null_stats) + 1)

Those are different quantities. p counts DRAWS, not DISTINCT VALUES.
Every shift that reproduces the original labeling ties the observed statistic
exactly, and a tie satisfies |null| >= |observed|.
"""
import sys, importlib.util
import numpy as np

sys.path.insert(0, ".")
spec = importlib.util.spec_from_file_location("a", "analysis.py")
m = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(m)
except SystemExit:
    pass

lab = np.asarray(m.IS_OVEN_D)
n = len(lab)
print(f"  label array length        : {n}")

distinct = {tuple(np.roll(lab, k)) for k in range(1, n)}
print(f"  distinct labelings, k=1..{n-1}: {len(distinct)}   <- the '4' in the answer key")

identical = [k for k in range(1, n) if np.array_equal(np.roll(lab, k), lab)]
print(f"  shifts that REPRODUCE the original labeling: {len(identical)}")
print(f"    k = {identical}")

# every such shift yields null_stat == observed exactly -> counts as 'at least as extreme'
n_draws = n - 1
floor_true = (len(identical) + 1) / (n_draws + 1)
floor_claimed = 1 / (len(distinct) + 1)

print()
print(f"  ANSWER KEY says floor      : {floor_claimed:.4f}   (1 / (distinct+1))")
print(f"  ACTUAL floor from the code : {floor_true:.4f}   (({len(identical)}+1) / ({n_draws}+1))")
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
print(f"  session-2 states the floor is 0.25 -> {'AGREES with the code' if abs(floor_true-0.25)<1e-9 else 'DISAGREES'}")
print(f"  FACILITATOR states 0.2      -> {'correct' if abs(floor_claimed-floor_true)<1e-9 else '** WRONG **'}")
