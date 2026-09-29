# Session 2 — Designing something that can fail

> **Clock:** [the four clocks](../../docs/session-clocks.md) — S2 needs **247 min against 201**, the worst in the course. Hour 4's pre-registration is **not completable in 50 minutes as written**, Hour 3's old ordering defect (running a "planned test" that hour 4 had not yet specified) is fixed as of 2026-09-29: hour 3 uses a one-line *expected* test, and hour 4 formalises it.

**Status: `DRAFT`, 2026-08-25; hour 3 rewritten 2026-09-29 around an external case.** Four hours. Second of four.
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

Covers `vr.prereg` objectives 0–2, 5. **The centrepiece. 50 minutes.**

**The habit this hour installs:**

> **Before trusting any test, ask whether it could possibly have rejected, and prove that it could,
> by building the data that would make it.**

A test that cannot reject produces a perfectly ordinary number. Nothing about the output looks wrong.
The only way to find out is to try to make the test say *yes*.

**The case (5 min).** One sentence from a published paper, read aloud: a comparison between two
groups, a row of p-values, and a conclusion drawn from them. Poll the room: *is this evidence for
the conclusion?* Take the vote and don't discuss it yet.

**Make it reject (12 min), in pairs, with the paper open.** One question only: **what data would
have made this test come out the other way?** Build it. Describe it, sketch it, or have your agent
generate it, then check your agent's answer by running the test on it rather than taking its word.
Some pairs will find that no such data exists, and they should be able to say *why*.

**The contrast (8 min).** The same paper also contains a second test, run by the same authors on the
same data. Repeat the question for that one. **One of the two tests could have come out the other
way. Only one of them is evidence.** Then read the authors' own sentence about the first test, and
ask what the reader-facing conclusion claimed that the numbers never could.

**Your own test (15 min).** Hour 4 writes the formal pre-registration, so this is a draft. Write one
line: *the test I currently expect to use for my claim.* Then produce two datasets, synthetic, small
and made with your agent:

1. one that **should** make your test reject, and run the test on it;
2. one that **should not**, and run the test on it.

If the first one won't reject, however extreme you make it, you have found a test that cannot reject
before it cost you anything. That is a success. Hour 4 is where you replace it.

**Debrief (7 min).** Which tests in the room could not be made to reject? What was the mechanism in
each? Keep the list. **Don't name a rule for them.** The room should leave with the question, not a
checklist item, because the question transfers and the checklist doesn't.

**Close (3 min).** Your agent will review your design in hour 4. It shares every assumption you gave
it, including the one that says your test works. **A reviewer that shares your assumption returns
confidence, not coverage.** The only reviewer that doesn't share it is the data you built to break
the test.

*Facilitator note —* **`PREDICTED`**, never observed: most students' own tests *will* be able to
reject, and they'll be disappointed. Say plainly that this is the good outcome. The hour pays off for
the one or two students whose test cannot, and for everyone else it pays off later, the next time a
result looks clean.

*The case, its pointer, the reveal, and what **not** to use in this hour (one mechanism looks
tempting and would give away session 4's exercise) are in the **facilitator pack**, not in this
repository.*

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

- ~~Whether hour 3's noise exercise needs a supplied harness~~: superseded. The 2026-09-29 hour 3
  has students build their own two datasets with their agent; no harness is needed.
- **RESOLVED 2026-08-25 (Thomas):** no lab specifics. The failure state this hour originally used
  is reproduced synthetically in `exercises/seeded-01-the-approved-analysis/` for session 4, where
  students track it down rather than being shown it.
- ✅ **RESOLVED 2026-09-24 (Thomas): option (b).** Session 2 gives up that case, and session 4 keeps
  seeded-01 as the discovery it was built to be. Option (c) was never available: cohorts are rolling
  *and prereq-chained*, so every session-4 room has already taken session 2.
- ✅ **DONE 2026-09-29:** hour 3 is rewritten around an external, published test that cannot reject,
  one whose mechanism is **not** seeded-01's, and around the *habit* rather than a key (Thomas,
  2026-09-24: soften the closing rule). **This page must never state seeded-01's specific mechanism
  or check**: session 4 depends on students working it out. The case itself is in the facilitator
  pack.
- **`OPEN`, found 2026-09-29: hour 2's worked case is our own lab's research** (a hybrid model's
  period-4 mask), which the 2026-08-25 ruling excludes. It needs an external case, and it sits
  uncomfortably close to seeded-01's mechanism.
