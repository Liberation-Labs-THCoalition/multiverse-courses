# Session 3 — Running it, and reading what came back

> **Clock:** [the four clocks](../../docs/session-clocks.md) — S3 needs **252 min against 201**. Hour 2 is the single worst block in the course (72 against 50). The header promises three deliverables and the body budgets time for one.

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

### The other direction, which costs more to miss

Everything above is about not believing something false. The rest of this hour is about **not
discarding something true**, which no amount of scepticism will do for you.

**The discrepancy you are about to explain away.** From this lab, 2026-05: we had data showing a
gap between two conditions — honest answers about common things versus honest answers about rare
things. The gap was inconvenient. It was being treated as a confound, something to residualise out
and mention in the limitations. Thomas asked one question about it. The data rearranged, and the
"confound" turned out to be the finding — retrieval difficulty was the thing the geometry was
tracking all along.

Nothing about that was caught by rigour. Rigour was what was about to bury it.

> **Before you residualise a discrepancy out, say aloud what it would mean if it were real.**
> If the answer is interesting, it is a hypothesis, not a nuisance. You are allowed to run it.

**And immediately, the check that has to travel with it.** From the same store, 2026-07-07: in a
single session a paper was inflated (0.969 led instead of the defensible 0.707, twelve convergences
claimed where three held), a token list was cherry-picked 10-of-41 to build a narrative, and an
echo check shipped with a directional bug. Every one caught by the gate, none by the author.

> **The excitement of convergence is a confound on judgment, and it is strongest when the thing
> you want to be true actually might be true.**

That is the honest pair, and students should hold both:

| | the move | the failure it prevents | the failure it invites |
|---|---|---|---|
| **Look** | say what the discrepancy would mean if real | burying a finding as a nuisance | chasing noise you like |
| **Check** | run it as a claim that can fail | publishing what you hoped | burying it again |

Neither one is the safe one. **Scepticism has a cost and it is paid in findings you never made.**

## Hour 4 — Writing the limits section first

**The limits section is not the apology at the end. It is the part that makes the rest citable.**

Give them a real one, from an artifact of ours, and have them mark which limit is load-bearing:

> - **One scalar per layer.** This tests a 90-prompt mean profile — 64 numbers. The effect could
>   live in per-prompt variance, in the raw spectra, or in the Jacobians, none of which is in this
>   artifact. This rules out a *gross* effect in the mean profile. **Nothing more.**
> - **29 null draws**, floor p = 0.034. Underpowered for a subtle effect.
> - **One model, one prompt set, one fit.**

Then the sting, which is the point of the hour:

> **A finding travels. Its limits section does not.**

You can write a correct, complete, honest set of limits, put them in the same file as the result,
and watch the result be cited for something the limits explicitly exclude — sometimes within days.
Not by careless people. By people who read the finding, which is what a finding is *for*.

The mechanism has been measured. Greenberg (2009) reconstructed the full citation network behind a
single biomedical claim: **242 papers, 675 citations, and 220,553 citation paths supporting it.**
He identifies how the belief acquired authority it had not earned — **bias** (citing only
supportive work), **amplification** (citing reviews as if they were evidence), and **invention**
(citing papers for claims they do not make). The qualifications did not survive the journey; the
claim did.

> Greenberg, *BMJ* 2009;339:b2680 · free full text: <https://pmc.ncbi.nlm.nih.gov/articles/PMC2714656/>

**So the limits section is not a disclaimer, and writing it is not defensive.** It is the only part
of your paper that constrains what the next person is allowed to build on top of you — and it is
the part least likely to be read. Write it as though it will be the only thing that survives,
knowing it probably will not be.

*Facilitator note:* this is the hour to tell an "I did this" story if you have one — a result of
your own that got cited past its limits, or a citation you yourself made too generously. The
published network above carries the point for anyone taking this asynchronously, but a first-person
account lands harder in a room. **Check your own numbers before you tell it**: a true event
fastened to an invented detail is the exact defect of session 4, hour 3.

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
