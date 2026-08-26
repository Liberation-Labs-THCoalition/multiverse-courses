# Automated methods review — `oven-density-study`

**Verdict:** `PASS`
**Confidence:** `0.92`
**Reviewer:** methods-gate v4.1
**Date:** 2026-03-11

---

## Summary

Design is sound. The analysis addresses a well-posed question with an appropriate
non-parametric test and a permutation null that respects the data-generating structure.
No blocking issues.

## What the review checked

| check | result |
|---|---|
| Hypothesis stated before analysis | PASS |
| Test statistic is pre-specified and unambiguous | PASS |
| Null hypothesis is explicitly constructed | PASS |
| Permutation null respects known structural constraints | **PASS — commendable** |
| Multiple-comparison exposure | PASS (single pre-specified comparison) |
| Sample size | PASS (n=64 daily observations) |
| Number of null draws sufficient for the claimed resolution | PASS (63 draws) |
| Effect direction stated in advance | PASS |

## Commentary

The **circular-shift null is a principled choice** and the analysis deserves credit for it.
A naive analyst would have shuffled the oven labels freely, destroying the fixed rotation
that is a genuine physical constraint of the bakery's operation. By shifting the schedule
instead, the analysis preserves the rotation while breaking the alignment between oven
identity and day — which is precisely the association under test. This is the correct
instinct and it is not common.

With 63 null draws the analysis can resolve p-values to approximately 1/64 ≈ 0.016,
which is adequate resolution for a conventional α = 0.05 threshold.

## Required action before publication

Report the exact permutation p-value to three decimal places rather than the
`p < 0.05` / `no evidence` dichotomy. Given 63 draws the test has resolution well
beyond the conventional threshold, and reporting the exact value lets readers
assess strength of evidence rather than a binary outcome.

## Optional improvements

- Consider reporting the observed statistic alongside the null distribution's spread.
- A figure showing the null distribution with the observed value marked would aid readers.

---

*This review was generated automatically. Push back on it if you disagree — reviews of this
kind are wrong in ways that are hard to see precisely because they are confident and specific.*
