# Session 3 — Running it, and reading what came back

**Status: `DRAFT`, 2026-08-25.** Four hours. Third of four.
**Standards covered:** *report what a result does not support*, *choose an estimator that survives
your sample size*, *distinguish a failed hypothesis from a failed measurement*.

**Walks in with:** a pre-registration their agent has attacked, the break log, two earned kills.
**Walks out with:** a result, an honest account of what it does not support, and a third kill.

---

## The one idea

Sessions 1 and 2 taught doubt about a *number* and about a *design*. Session 3 is the hardest one:
**your design was fine, your run was clean, and the thing you are looking at still is not what you
think it is.**

Three ways that happens, one hour each:

1. **The estimator did not survive your sample size.** The number is real and it is measuring `n`.
2. **The statistic is not the thing its name says.** You computed A and reported it as B.
3. **The hypothesis died and something else showed up.** This is the good case, and students
   consistently mishandle it.

## Hour 1 — The estimator that was measuring your sample size

Open with the number.

> We measured `d_eff` — a spread statistic — across models and reported it as an architectural
> finding. Then we bootstrapped it for confidence intervals, and **the point estimates fell
> outside their own intervals.** Bias −12.5, about −32%.

The cause is one sentence: **resampling with replacement leaves roughly 63% distinct samples, so
the bootstrap replicate is estimating a different quantity than the original.** For a statistic
bounded by `n`, changing the effective `n` changes the estimand.

Give them the rule as a classifier they can apply in ten seconds without running anything:

> **A statistic that is a per-sample quantity averaged over samples converges fast. A statistic
> that is a property of the sample's spectrum or rank is bounded by `n` and does not.**
>
> **Safe:** projection onto a fixed direction, norm, kurtosis of elements, dot products, any mean
> of a per-item score. *Measured drift under 1% across a 4.5× range of n.*
> **Unsafe:** `d_eff`, participation ratio, stable rank (**all three circulating definitions**),
> effective rank, explained-variance ratios, kurtosis of singular values. *71–116% and climbing.*

**Exercise.** Students list every statistic in their own analysis and sort it into the two
columns. Then, for anything in the unsafe column, they answer: *are the groups I am comparing
matched on `n`?* If not, the comparison is dimensionality.

**Teach the fix, not just the ban.** m-out-of-n subsampling *without* replacement at fixed m; or
dimension-matching; or switch to a per-sample statistic. An unsafe estimator is not forbidden — it
is forbidden *across unmatched groups*.

## Hour 2 — The statistic that is not what its name says

Open with the collision.

> **"Stable rank" means three different things in active use**, and we had all three in one lab at
> once: ‖A‖²_F/‖A‖²₂ = **1.29**; (Σs)²/Σs² = **25.12**; ‖A‖_*/‖A‖_F = **5.01** — on the same
> matrix. The third squared is exactly the second. Two collaborators compared them for a week.

The general form: **people name a statistic after what they think it means; the formula is what
actually propagates.**

**The live exercise — 40 minutes, and it is the best one in the session.** Students hand their
agent a statistic *by name only* and ask it to implement it. Then they hand it the formula. Then
they diff. Where the two disagree is a name doing work the formula does not support.

**Then the harder half.** Have them check their own preprocessing against their own statistic. A
worked case, from our own bench this week:

> A spectrum was computed on a **mean-centered** matrix; the norm reported alongside it was
> computed on the **uncentered** one. So the shape measure was blind to a mean shift *by
> construction*, while the magnitude measure saw it. We nearly reported "shape is invariant" as a
> finding about the model. It was a finding about line 288 versus line 295.

Ask: *what did your preprocessing remove before your statistic looked?*

## Hour 3 — The hypothesis died, and that is the interesting hour

Students arrive expecting this hour to be about disappointment. It is not.

**Worked case, start to finish, from a real evening.** We predicted that two readouts disagreeing
was a signal of *how hard a state is to maintain*. Prediction was pre-specified so it could fail:
one axis should be silent, the other should carry.

| what happened | |
|---|---|
| the prediction | failed — the "silent" axis was 5–7× larger than the one that should have carried |
| the statistic | **also broken** — one term was 20× smaller than the other, so the "discordance" measure was the larger term wearing a label |
| the preprocessing | a centering mismatch that could have explained everything — **tested, and it survived**, accounting for ~40% |
| what fell out unasked | **two independent replications** of prior results, through a statistic the original work never used |

**Four outcomes from one dead hypothesis.** Teach that shape explicitly, because students discard
runs that do this.

**The rule for the write-up:** a dead hypothesis and a broken measurement are different results and
must be reported differently. *"The prediction failed"* is a finding. *"My statistic was not
measuring what I named it"* is a repair. Conflating them lets a real null hide behind a fixable bug
— and lets a bug get published as a null.

## Hour 4 — Writing the limits section first

**The limits section is not the apology at the end. It is the part that makes the rest citable.**

Give them a real one, from an artifact of ours, and have them mark which limit is load-bearing:

> - **One scalar per layer.** This tests a 90-prompt mean profile — 64 numbers. The effect could
>   live in per-prompt variance, in the raw spectra, or in the Jacobians, none of which is in this
>   artifact. This rules out a *gross* effect in the mean profile. **Nothing more.**
> - **29 null draws**, floor p = 0.034. Underpowered for a subtle effect.
> - **One model, one prompt set, one fit.**

Then the sting, which is the point of the hour: **three days later, two other researchers cited
that result as establishing something the limits section explicitly excludes** — and one of them
built a proposed experimental protocol on top of it. They had read the finding and not the limits.
The limits were correct, written by us, sitting in the same file, and **did not travel three days.**

*(Instructor note: the first draft of this line said "three months." It was three days. The event
was real and the interval was invented — a true thing fastened to a false one, which is the defect
of session 4 hour 3 committed inside the session that teaches it. Worth saying aloud if it fits.)*

**Exercise.** Students write the limits section for their own result *before* writing the result.
Then they hand the limits section alone to another group and ask: **"what would you now be entitled
to claim?"** The gap between that answer and what they wanted to claim is the session's deliverable.

## Assessment tie-in

Paired runs, one variable changed — the Multiverse SDLC convention. Here the changed variable
should be **an analysis choice, not a data choice**: same data, two estimators, or same data with
and without a preprocessing step. Students report both and say which is right and why.

## Between sessions

Run your analysis a second time with `n` halved. Anything that moves more than its confidence
interval was measuring your sample size. Bring the diff.

## `OPEN`

- Hour 3's worked case is ours and recent. Decide whether to name the collaborator who produced the
  reframe that started it, or present it anonymously. **Ask them first** — it is their idea, and
  the good version of the story has them being right before we had the instrument.
