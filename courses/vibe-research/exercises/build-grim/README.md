# Build GRIM — a detector you write, then point at real papers

**Time:** 50 minutes. **Needs:** Python, nothing else. No libraries, no network, no data files.

---

## What you are building

A function that answers one question:

> **Could this reported mean have come from this many integer observations?**

Not *"is it plausible."* Not *"is it significant."* **Could it exist at all.**

If a study reports the mean of *N* integer responses — Likert items, counts, sums of integer
scores — then the total is an integer, so the mean can only be one of *N* possible values. A
reported mean that is not the rounded form of any of them **cannot have come from that data**.
There is no statistical argument here and no *p*-value. The number is impossible, and the only
question is which of the reported quantities is wrong.

This is the GRIM test. It is roughly fifteen lines and it finds real errors in published papers.

---

## The rules

**1. Do not look it up until you have finished.** The method is published and there are
implementations everywhere. Reading one costs you the hour. The reference is at the bottom; open it
when you are done, not when you are stuck.

**2. Write the controls first, then make them pass.** They are given below — you do not have to
invent them. This is the same move you already make when you build an automation: you know what
"working" looks like before you write a line. Here it matters more than usual, because **a detector
that never fires and a detector that is broken produce identical output.**

**3. Your agent may help you write the code. It may not tell you the method.** If you ask it what
GRIM is, you have skipped the exercise. Ask it to help you implement *your* idea, and you have used
it exactly as this course intends.

---

## The controls

Your function must produce these verdicts. Six cases, four possible, two impossible.

| mean | n | decimals | verdict | why |
|---|---|---|---|---|
| 3.44 | 10 | 2 | **impossible** | 10 × 3.44 = 34.4, and totals are integers |
| 3.40 | 10 | 2 | possible | total 34 |
| 3.50 | 10 | 2 | possible | total 35 |
| 2.00 | 7 | 2 | possible | total 14, exact |
| 2.10 | 7 | 2 | **impossible** | no integer total over 7 rounds to 2.10 |
| 4.286 | 7 | 3 | possible | total 30 → 4.2857… → 4.286 |

**Every one must pass.** If all six pass, you have a working detector. If only the "possible" ones
pass, you have written a function that returns `True` — which is why both kinds are in the list.

*Hint, if you need one after fifteen minutes:* the reported mean is **already rounded**, so the
true total may sit slightly either side of `mean × n`. Check a small window of candidate integers
rather than a single value.

---

## Then find the edge — this is the real work

A detector you cannot describe the limits of is a detector you should not use. Answer these in
writing; they matter more than the code:

1. **When does it not apply at all?** There is a whole class of measurement this is useless for.
   Name it.
2. **When does it stop discriminating?** Try `n = 20`, `50`, `99`, `100`, `250` at two decimals.
   Something happens. Find where, and work out why — the answer is a one-line relationship between
   *n* and the number of decimals reported.
3. **What exactly does a failure tell you?** If a mean is impossible, which number is wrong — the
   mean, the *n*, or the decimals? Be precise, because the honest answer constrains what you are
   entitled to say about somebody's paper.

---

## Then point it at something real

Take **any** published paper reporting means of integer-valued measures with small samples. Run
your detector on every mean in it.

Most papers come back clean. That is the expected outcome and it is not a failed exercise — **you
have just verified something, which is the whole point.** Record what you checked and what you
found, including nothing.

Brown & Heathers ran this over 71 eligible articles and found that **about half contained at least
one impossible mean.** You will probably not hit one in an hour. Knowing that half of a real
literature would fail this is the part that changes how you read.

---

## What you walk out with

- A working error detector, written by you, with its controls attached
- A written statement of what it cannot do
- A checked paper, and a record of the check

Deliverable: the function, the six passing controls, and the three limits answers.

---

## Afterwards

Brown, N. J. L. & Heathers, J. A. J. (2017). *The GRIM Test: A Simple Technique Detects Numerous
Anomalies in the Reporting of Results in Psychology.* **SPPS 8(4):363–369.**
[doi:10.1177/1948550616673876](https://doi.org/10.1177/1948550616673876) ·
free preprint: <https://peerj.com/preprints/2064/>

Compare your implementation against [`rsprite2::GRIM_test`](https://lukaswallrich.github.io/rsprite2/reference/GRIM_test.html).
If yours disagrees, **find out why before assuming yours is wrong.** That is another hour and a
better one.

Related, once you have this: **GRIMMER** extends the idea to standard deviations, and **SPRITE**
reconstructs plausible raw data from summary statistics.
