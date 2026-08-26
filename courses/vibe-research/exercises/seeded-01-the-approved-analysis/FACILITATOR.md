# Facilitator notes — seeded exercise 01

**Do not give students this file.** Give them `analysis.py` and `review.md`.

**Runs in:** ~40 minutes. Session 2 (*Designing something that can fail*), or session 4 as the
opener for building a kill list.

**Requires:** Python + numpy. Nothing else. No GPU, no network, no accounts.

---

## The defect

The circular-shift null has an **orbit of size 4**, not 63.

The oven schedule has period 4. Shifting a period-4 pattern by `k` gives back one of only four
distinct labelings — `k mod 4`. Shifts of 4, 8, 12 … 60 return the *identity*. So the 63 "draws"
contain **4 distinct values, one of them the original labeling**.

Ground truth, computable in one line:

```python
orbit = {tuple(np.roll(IS_OVEN_D, k)) for k in range(1, 64)}
len(orbit)          # -> 4
1 / (len(orbit)+1)  # -> 0.2   the smallest p this test can EVER return
```

**The test cannot reject at α = 0.05 under any dataset whatsoever.** Not underpowered —
*incapable*. There is no experiment you could run, no effect size however enormous, that would
let this design produce p < 0.2.

## Why the review passes it, which is the actual lesson

Every individual claim in `review.md` is **defensible**:

- The circular-shift null *is* structure-respecting. That praise is earned.
- There *are* 63 draws. Count them.
- 63 draws *would* give ~1/64 resolution — **if they were distinct.**

The review never checks whether the draws are distinct, because **no line item asks it to.**
The defect lives in the *relation* between "63 draws" and "resolution 1/64," and a checklist that
verifies claims one at a time cannot see it. The required action then instructs the author to
report a number the design cannot produce.

This is the failure mode to name out loud: **a confident, specific, internally consistent review
that is wrong.** Not sloppy. Not vague. Wrong in a way that its own structure cannot detect.

## Running it

1. **Ten minutes, no tools.** Read `analysis.py` and `review.md`. Write one sentence: *what is
   wrong here?* Collect answers before anyone runs anything. Most groups defend the analysis —
   the review is persuasive and the null genuinely is thoughtful.
2. **Ten minutes.** Answer the three questions at the bottom of `analysis.py`. Question 2 says
   *do not reason about it — compute it.* Watch for groups that reason instead. Reasoning about
   orbit size is where people get it wrong; the one-line `set()` is where they get it right.
3. **Ten minutes.** *Where in the review should this have been caught?* Push until someone says
   the review has no line item for it. That is the point.
4. **Ten minutes.** Write the missing check as a rule a reviewer could apply mechanically. Good
   answers converge on: **count the distinct values of your null before reading any p-value.**

## What to say if a group finds it in four minutes

Give them the harder question: **when is a circular-shift null the right choice?** It is not
always wrong — it is wrong *here* because the schedule's period divides the shift group. Ask them
to construct a case where the same null is both structure-respecting and non-degenerate. (Period
and series length coprime is one route. Random offsets within a cycle is another.)

## Provenance, for the facilitator

**This is a synthetic reconstruction of a real failure**, rebuilt so it can be shared. A
methods gate we use in our own lab approved a degenerate permutation null at high confidence,
described it as principled, and issued a required action telling the author to report a p-value
the design could not produce. The bakery, the ovens and the review text are invented. **The shape
is not.**

Teach it as a real thing that happened to working researchers, because it is. Students should
leave understanding that the review was not incompetent — it was *structurally blind*, and their
own reviews will be too unless they build the missing checks deliberately.

## Extensions

- **Harder variant — and this is the best five minutes in the exercise.** Change one line:
  `N_DAYS = 63`. Leave everything else untouched. Have students predict the new p-floor **before**
  computing it. Measured:

  | `N_DAYS` | distinct labelings | p-floor | |
  |---|---|---|---|
  | 60 | **4** | **0.200** | degenerate |
  | **64** | **4** | **0.200** | degenerate — *the exercise as shipped* |
  | 62 | 61 | 0.016 | healthy |
  | **63** | **62** | **0.016** | healthy |
  | 65 | 64 | 0.015 | healthy |

  The condition is exact: **the null is degenerate precisely when the schedule's period divides
  the series length.** 4 divides 60 and 64; it does not divide 62, 63 or 65.

  So **collecting one day less data takes this test from incapable to fine** — floor 0.200 to
  0.016, a 12× change in resolution, with strictly less information. Nothing about the effect,
  the noise, the statistic or the sample size moved. Only the arithmetic relationship between
  two numbers nobody was looking at.

  Ask them what that implies about "more data is always better" as a heuristic. The honest answer
  is that power and *validity* are different axes, and this design failed on the second while
  looking fine on the first.
- **Session 4 tie-in:** this exercise generates the first entry in a student's own kill list.
  The rule they wrote in step 4 is the entry.
