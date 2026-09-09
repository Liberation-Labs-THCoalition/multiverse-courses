"""GRIM — Granularity-Related Inconsistency of Means.  FACILITATOR REFERENCE ONLY.

>>> DO NOT GIVE THIS FILE TO STUDENTS. <<<

Building GRIM is the stage-7 exercise. It is ~15 lines of arithmetic, it detects real
errors in real published papers, and a student who writes it themselves owns a working
error detector by the end of an hour. Hand them this file and they own nothing.

This copy exists so a facilitator can (a) check a student's version against a known-good
one and (b) demo the tool live without writing it on the spot.

Method: Brown & Heathers 2017, "The GRIM Test: A Simple Technique Detects Numerous
Anomalies in the Reporting of Results in Psychology."

THE IDEA. If N observations are integers (Likert items, counts, sums of integer items),
their total is an integer, so the mean can only be one of N possible values -- k/N for
integer k. A reported mean that is not the rounded form of any k/N is arithmetically
impossible, whatever the data was. It is not a statistical argument and there is no
p-value: the number cannot exist.

SCOPE, and this is where students get it wrong:
  - Only for means of INTEGER-valued measures. A mean weight in kg tells you nothing.
  - Only useful when N < 10**decimals. With 2 decimals, GRIM has power below N=100;
    above that almost every value is reachable and "consistent" means nothing.
  - Inconsistency means the reported set (mean, N, decimals) cannot co-exist. It does
    NOT tell you which one is wrong, and it is not evidence of misconduct.
"""


def grim_consistent(mean: float, n: int, decimals: int = 2) -> bool:
    """Could `mean` arise from n integer observations, rounded to `decimals` places?"""
    if n <= 0:
        raise ValueError("n must be positive")
    # Candidate integer totals bracketing n*mean. Check a small window rather than one
    # value -- the reported mean is already rounded, so the true total may sit either side.
    approx = mean * n
    for total in range(int(approx) - 2, int(approx) + 3):
        if total < 0:
            continue
        if round(total / n, decimals) == round(mean, decimals):
            return True
    return False


def grim_has_power(n: int, decimals: int = 2) -> bool:
    """Below this threshold the test can discriminate; above it, nearly everything passes."""
    return n < 10 ** decimals


if __name__ == "__main__":
    # ---- CONTROLS FIRST -------------------------------------------------------
    # A detector that cannot fail is not a detector. These must BOTH hold, or the
    # implementation is broken and every downstream verdict is noise.
    cases = [
        # (mean,  n,  dec, expected, note)
        (3.44,   10, 2, False, "canonical impossible value: 34.4 is not an integer"),
        (3.40,   10, 2, True,  "canonical possible value: total 34"),
        (3.50,   10, 2, True,  "total 35"),
        (2.00,    7, 2, True,  "total 14, exact"),
        (2.10,    7, 2, False, "14.7 -- no integer total rounds to 2.10 at n=7"),
        (4.286,   7, 3, True,  "total 30 -> 4.2857 -> 4.286"),
    ]
    print("=== controls ===")
    failures = 0
    for mean, n, dec, expected, note in cases:
        got = grim_consistent(mean, n, dec)
        ok = got == expected
        failures += (not ok)
        print(f"  {'OK  ' if ok else '**FAIL**'} mean={mean} n={n} d={dec} "
              f"-> {'consistent' if got else 'IMPOSSIBLE'}  ({note})")

    print("\n=== power ceiling ===")
    for n in (20, 50, 99, 100, 250):
        print(f"  n={n:<4} decimals=2  discriminating: {grim_has_power(n, 2)}")

    print()
    if failures:
        raise SystemExit(f"** {failures} control(s) failed -- implementation is wrong **")
    print("all controls passed -- detector distinguishes possible from impossible")
