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

Ground truth:

```python
orbit = {tuple(np.roll(IS_OVEN_D, k)) for k in range(1, 64)}
len(orbit)                                                    # -> 4  distinct labelings

# The floor counts DRAWS THAT TIE, not distinct values:
ties = sum(np.array_equal(np.roll(IS_OVEN_D, k), IS_OVEN_D) for k in range(1, 64))
ties                                                          # -> 15  (k = 4, 8, ... 60)
(ties + 1) / 64                                               # -> 0.25  the true floor
```

**The test cannot reject at α = 0.05 under any dataset whatsoever.** Not underpowered —
*incapable*. No effect size, however enormous, lets this design produce p < 0.25.

> ### ⚠ This block was WRONG until 2026-09-09, and how it was wrong is worth an extra two minutes
>
> It read `1 / (len(orbit) + 1)` → **0.2**, and called that the floor. It is not. `analysis.py`
> computes `p = (n_at_least_as_extreme + 1) / (n_null + 1)`, which counts **draws**. Fifteen of the
> 63 shifts reproduce the original labeling exactly, each ties `|observed|`, and a tie is "at least
> as extreme." So the floor is **16/64 = 0.25**, which is what `session-2` said all along and what
> the code does.
>
> **Two true numbers — orbit size 4, and the p formula — joined by a false relation.** That is the
> defect class this very exercise teaches, committed in the line labelled *ground truth*, and it
> survived every review until a hostile audit recomputed it.
>
> **Why it hid:** the wrong formula and the right one **agree in every healthy case** (see the
> table below — 0.0161, 0.0159, 0.0154 in both) and diverge *only* in the degenerate case. The
> error was invisible except in exactly the situation the exercise exists to expose.
>
> Tell the room. It is the best available evidence for the course's own thesis, and it cost us
> nothing but embarrassment.

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
   wrong here?* Collect answers before anyone runs anything. **`PREDICTED`** (never observed):
   most groups defend the analysis, because the review is persuasive and the null genuinely is
   thoughtful. **If the room kills it in four minutes instead, that is a finding — write it
   down.** It would mean either the exercise is too easy or the room was pre-warned, and the two
   need different fixes.
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

  | `N_DAYS` | distinct labelings | shifts that tie | **p-floor** | |
  |---|---|---|---|---|
  | 60 | 4 | 14 | **0.2500** | degenerate |
  | **64** | **4** | **15** | **0.2500** | degenerate — *the exercise as shipped* |
  | 62 | 61 | 0 | 0.0161 | healthy |
  | **63** | **62** | **0** | **0.0159** | healthy |
  | 65 | 64 | 0 | 0.0154 | healthy |

  *(Recomputed 2026-09-09. The earlier version of this table used `1/(distinct+1)` and read 0.200
  for the degenerate rows. The healthy rows were unaffected — which is exactly why nobody caught
  it.)*

  The condition is exact: **the null is degenerate precisely when the schedule's period divides
  the series length.** 4 divides 60 and 64; it does not divide 62, 63 or 65.

  So **collecting one day less data takes this test from incapable to fine** — floor 0.2500 to
  0.0159, roughly a 16-fold change in resolution, with strictly less information. Nothing about
  the effect,
  the noise, the statistic or the sample size moved. Only the arithmetic relationship between
  two numbers nobody was looking at.

  Ask them what that implies about "more data is always better" as a heuristic. The honest answer
  is that power and *validity* are different axes, and this design failed on the second while
  looking fine on the first.
- **Session 4 tie-in:** this exercise generates the first entry in a student's own kill list.
  The rule they wrote in step 4 is the entry.
