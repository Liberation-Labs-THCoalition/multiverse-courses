# Facilitator notes — Build GRIM

**Do not hand this out.** Students get `README.md`. Working implementation for checking their work:
[`../../tools/grim_reference.py`](../../tools/grim_reference.py) — run it to see the controls pass.

**Time:** 50 minutes. **Stage:** 7 (gate). **Prereq:** none beyond Python.

---

## Why this exercise exists

Everything else in the gate session builds checks against **the student's own failures**, which is
right and is the harder skill. But it has a bootstrapping problem: **a student who has not yet
failed at anything has nothing to build from.**

This is the fix. GRIM is somebody else's check, fully specified, with a knowably correct answer —
so a student can experience *building a detector and verifying it* before they have any scars of
their own. Then hour 1's "build from your own failures" has something to be a variation on.

It is also the only hour in the course where they walk out holding a tool that works on other
people's published work. That lands.

---

## Where it fits

The session-4 clock is full ([running a session](../../../../docs/running-a-session.md)), so this
does not slot in for free. Options, in order of preference:

1. **Between sessions**, as the async task between 3 and 4. It needs no facilitator and it arms
   them for hour 1.
2. **Replacing session 4 hour 1** for a cohort with no prior sessions — a rolling-attendance room
   where most people have no failures of their own yet.
3. **Session 3**, if that room finishes its analysis work early.

**Do not run it in the same session as hour 1 as written.** Both are 50 minutes of building
checks, and the second one will feel like the first.

---

## The three things to protect

**1. Do not let anyone look it up.** The whole value is the derivation. Say this once at the start
and once at minute 10, then stop policing it — someone who looks it up has made a choice about
their own hour.

**2. The agent rule is the point, not a restriction.** *"Your agent may help you write the code. It
may not tell you the method."* This is the course's thesis in miniature — the mechanical part is
delegable, the judgment is not. Expect at least one person to ask the agent what GRIM is and say so
cheerfully. Ask them what they think they lost. There is no penalty; the answer is interesting.

**3. Controls before code.** The six controls are given precisely so nobody has to invent them —
the lesson is *making given controls pass*, not designing them. If someone writes the function
first and tests after, that is worth naming: they got a working answer by the route that usually
does not produce one.

---

## Timing

| min | |
|---|---|
| 0–5 | Frame it. Read the "could this exist at all" paragraph aloud. Do not explain the method. |
| 5–25 | Build. Circulate. **Hint at 15 if a pair is stuck**, not before. |
| 25–35 | The limits questions. This is the substantive half — hold the room to writing, not discussing. |
| 35–45 | Point it at a real paper. |
| 45–50 | Close on the generalisation below. |

**If they finish the code at minute 12** — some will — send them straight to the limits questions.
Do not let them polish. The code is not the deliverable.

---

## Answers to the limits questions

**1. When does it not apply?** Anything not integer-valued. Weights, times, reaction latencies,
already-averaged composites, percentages of a non-integer base. Students often say "continuous
data," which is close enough — but push once on **composites**: a mean of subscale means is not
integer data even though every underlying item was.

**2. When does it stop discriminating?** At **`n ≥ 10^decimals`**. Two decimals → no power at or
above `n = 100`, because by then every two-decimal value is reachable by some integer total. Have
them run the ladder and see it go flat; the reference implementation prints exactly this.

> This is the transferable half: **a detector has a domain, and outside it a "pass" means nothing
> at all.** A clean GRIM result at *n* = 400 is not evidence of anything. Silence outside the
> domain is indistinguishable from a clean bill of health.

**3. What does a failure tell you?** That the reported *set* — mean, *n*, decimals — cannot
co-exist. **Not which member is wrong.** The commonest real cause is benign: *n* differs from the
headline *n* because of missing data on that item. Be explicit that this is **not** evidence of
misconduct, and say why the distinction matters: a tool that finds real errors gets discredited
fast if it is used to make accusations it cannot support.

---

## What to listen for

- **"It always returns True"** — good, they found the failure mode the impossible-cases controls
  exist to catch. Ask what they would have concluded without those two rows.
- **Floating-point trouble** near exact boundaries (2.00, 3.50). Real, and a legitimate second
  hour if the room is enjoying itself. `round()` half-to-even bites here.
- **"Isn't this too easy to be useful?"** The best question in the hour. Answer with the Brown &
  Heathers number: about half of 71 eligible papers had at least one impossible mean. **Easy and
  useful are not opposites** — the check was always available and mostly nobody ran it.

---

## Close on this

> **You just built a check that cannot be argued with.** No assumptions, no model, no threshold,
> no *p*-value. It either fits or it does not.
>
> Most checks are not like that, and yours mostly will not be. But this is the shape to aim at:
> **a check earns its place by being able to fail, and by being cheap enough that you actually
> run it.**

Then the bridge to hour 1: *this one was handed to you, fully specified, with its controls
attached. The next one you build has to come from a failure of your own — and nobody will hand you
the controls.*
