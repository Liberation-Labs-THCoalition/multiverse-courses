# Session 2 — Designing something that can fail

**Status: `DRAFT`, 2026-08-25.** Four hours. Second of four.
**Standards covered:** `vr.prereg`, *identify the confounds that separate your conditions before
your variable does*, *select a control that is capable of failing*.

**Walks in with:** a claim with a direction and a falsifier, a verified citation trail, and one
earned kill from session 1.
**Walks out with:** a pre-registration their agent has attacked, the break log, and a second kill.

---

## The one idea

Session 1 taught students to doubt a *number*. Session 2 teaches them to doubt a *design* — which
is harder, because a broken design produces numbers that look fine.

**Three ways a design fails before it runs**, and each gets an hour:

1. Something other than your variable separates your conditions
2. Your control cannot fail
3. Your test cannot reject

Every one of these produces clean, publishable-looking output. None is visible in the result.

## Hour 1 — The confound that got there first

Covers *identify the confounds that separate your conditions before your variable does*.

**Open with the number, not the concept.** In a dataset of ours, prompts were assigned to
conditions by design — grounded versus three flavours of confabulation. Then:

> **`prompt_len` alone classifies the arms at AUROC 0.9523.**
> 68% of confabulation prompts are longer than *every single* grounded prompt.

The two conditions were near-separable **from the prompt text, before the model ran.** Any
downstream feature correlated with length would have looked like a detector.

**The exercise.** Students take their own design and list everything that differs between their
conditions *other than* the variable of interest. Then they rank the list by "could this alone
produce my predicted result?" Most people find at least one candidate that could. The honest ones
find that their condition label is partly a *topic* label.

**The rule to leave with:** residualization removes the *linear part* of a confound. It does not
remove the fact that your conditions are different populations. We learned that one the expensive
way — FWL on length was applied, and the design still could not distinguish a detector from a
prompt-family classifier.

## Hour 2 — A control that is capable of failing

Covers *select a control that is capable of failing*.

**A control you expect to pass is not a control. It is a decoration.**

Worked example, ours, and it is the good kind of story because the control *worked*: testing
whether a hybrid model's depth profile carries a period-4 signature from its interleaved
architecture. The control was a **dense model with a sham period-4 mask** — a model with no such
structure, tested identically.

The dense control came back **significant**. Larger than the real model, opposite sign. Which meant
the *method* manufactured the structure, and the finding was dead. **That is a control doing its
job**, and it cost a result we wanted.

**The exercise, in pairs.** For each student's design: what is the control, and *what would it look
like if the control failed?* If they cannot describe the failure, they do not have a control.
Then: what would you conclude if the control fails? Write it down now, while it is cheap.

**A harder variant worth ten minutes:** a positive control proves the *instrument*. It cannot prove
the *scope*. We ran a positive control inside a directory that did not contain the target — it
passed, and the search was still worthless.

## Hour 3 — A test that cannot reject

Covers `vr.prereg` objectives 0–2, 5.

**The centrepiece, and the most uncomfortable teaching case we own.**

A pre-registered design specified a permutation null: shift a mask over the data, recompute the
statistic, compare. It stated a floor of `p = 1/64 = 0.016`.

**The mask had period 4. Shifting a period-4 mask gives four distinct masks, not sixty-four.** The
true floor was `p = 0.25`. The test could not have rejected under *any* data.

Two things make this worth an hour rather than an anecdote:

- **The gate approved it at 0.92 confidence**, called the null "principled," and issued a required
  change instructing the author to report the impossible floor. A reviewer that shares your
  assumption returns confidence, not coverage.
- **The tell was free and arrived before any interpretation**: the output contained nothing but
  multiples of 0.25.

**The exercise.** Every student runs their planned test on **pure noise** — shuffled labels, random
data, same pipeline. Two questions: does it ever reject? And **how many distinct values does the
null actually take?** Count them. A null with a handful of distinct values is not a null with a
thousand draws.

**The rule:** before reading any resampling p-value, print the number of unique values in the null.
It is one line and it would have saved the design above.

## Hour 4 — Pre-register, then have your agent attack it

Covers `vr.prereg` 3–4, 6.

Students write the real pre-registration. The house format:

- primary statistic, its estimator, **the exact formula**
- decision rule as branches: this result → this conclusion
- **the outcome you are hoping for, named as a stake**
- **what you have already seen**, and how it constrains what you may claim from it
- sensitivity analyses, committed to in advance, all of them reported
- power, honestly, including which direction a null does and does not support
- one **non-goal** — a nearby analysis you are choosing not to run, and why

Then they hand it to their agent with one instruction: **break this.** Not "review" — *find the
version of this design that produces my preferred answer regardless of the truth.*

The **break log** is the deliverable, and the second kill comes out of it.

*Instructor note:* the fourth bullet is the one people omit, and it is the one that makes a
pre-registration honest rather than merely early. A student who has already looked at their data
and does not say so has written a summary, not a prereg.

---

## Between sessions

The gate-sparring companion, now with two kills to work against. Students run their design past it
and log what it challenged.

**Homework:** execute a pilot — smallest version of your design that could produce a signal — and
bring both the result *and* the noise-run from hour 3.

## Open

- Whether hour 3's noise exercise needs a supplied harness or students build it (leaning: build
  it, it is six lines and building it is the lesson)
- **RESOLVED 2026-08-25 (Thomas):** no lab specifics. The failure state is reproduced
  synthetically instead — `exercises/seeded-01-the-approved-analysis/`, a 0.92-confidence review
  passing a null with an orbit of 4. Same shape, nothing of ours exposed, and students track it
  down rather than being shown it.
  Liberation Labs' internal output and Thomas should decide whether it leaves the building.
