"""
Bakery oven study — does Oven D produce denser loaves?

This analysis has been reviewed and approved. It is wrong.
Your job is to find out why, using nothing but this file and `review.md`.

Do not fix it yet. First, write down in one sentence what the defect IS.
"""
import numpy as np

rng = np.random.default_rng(20260825)

# ---------------------------------------------------------------------------
# Setup: a bakery runs four ovens on a fixed rotating schedule.
# Day 0 -> oven A, day 1 -> B, day 2 -> C, day 3 -> D, day 4 -> A, ...
# We measure loaf density once per day for 64 days.
# ---------------------------------------------------------------------------
N_DAYS = 64
OVENS = np.array([i % 4 for i in range(N_DAYS)])   # 0=A 1=B 2=C 3=D
IS_OVEN_D = (OVENS == 3)

# Observed densities. There is no real oven effect in this generator --
# the "effect" you will see is drift plus noise.
density = 0.90 + 0.0009 * np.arange(N_DAYS) + rng.normal(0, 0.015, N_DAYS)


def statistic(labels_is_d):
    """Mean density on Oven-D days minus mean on all other days."""
    return density[labels_is_d].mean() - density[~labels_is_d].mean()


observed = statistic(IS_OVEN_D)

# ---------------------------------------------------------------------------
# Permutation null.
#
# We cannot shuffle the oven labels freely -- the rotation is a real physical
# constraint, and a free shuffle would destroy it. So we use a CIRCULAR SHIFT
# of the schedule, which preserves the rotation structure exactly. This is a
# structure-respecting permutation null.
# ---------------------------------------------------------------------------
null_stats = []
for k in range(1, N_DAYS):            # 63 shifts
    shifted = np.roll(IS_OVEN_D, k)
    null_stats.append(statistic(shifted))
null_stats = np.array(null_stats)

n_at_least_as_extreme = int(np.sum(np.abs(null_stats) >= abs(observed)))
p_value = (n_at_least_as_extreme + 1) / (len(null_stats) + 1)

print(f"observed difference : {observed:+.5f}")
print(f"null draws          : {len(null_stats)}")
print(f"as extreme or more  : {n_at_least_as_extreme}")
print(f"p-value             : {p_value:.4f}")
print()
print("CONCLUSION: Oven D differs from the other ovens (p < 0.05)." if p_value < 0.05
      else "CONCLUSION: no evidence Oven D differs.")

# ---------------------------------------------------------------------------
# STOP.
#
# Before reading review.md, answer these three, in writing:
#
#   1. How many null draws does this analysis report?
#   2. How many DISTINCT values can `null_stats` actually take? Do not reason
#      about it -- compute it. One line.
#   3. Given your answer to (2), what is the smallest p-value this test could
#      EVER return, for any data whatsoever?
#
# If (3) is larger than 0.05, this test cannot reject its null under any
# dataset. It is not underpowered. It is incapable.
# ---------------------------------------------------------------------------
