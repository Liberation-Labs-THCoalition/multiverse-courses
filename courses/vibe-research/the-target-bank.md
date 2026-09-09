# The target bank — a different supplied problem per session

**Status: `DRAFT`, 2026-09-08.** Supersedes the single-target draft from earlier the same day.

---

## Why a bank and not one target

The first draft ran **one** target through all four sessions. That was a bug, and a specific one:

> Session 1's lit review asks *"has this already been answered?"* For any target good enough to
> open session 1, the answer is **yes** — that is what makes saturation reachable and the endpoint
> arrive in an hour. **So a competent session 1 kills the target for sessions 2–4.**

The fix is not a worse session 1. It is **one target per session**, each matched to the skill that
session teaches.

**And the cadence forces the same answer independently.** Sessions are monthly against a rolling
student body. Anyone who joins at session 2, or repeats a session, or talks to someone who took it
last month, arrives with the answer already. Self-contained sessions survive that; an arc does not.

**Targets rotate across cohorts too.** Four is the minimum, not the design. The bank should grow
to two or three per slot so a returning student meets a fresh one. Contributing a target that
worked is a legitimate way for a graduate to give back — it is also a strong signal they are ready
for the accelerator.

### What makes a target eligible

1. **Bounded by construction.** Runnable in an afternoon. No version of it becomes a project.
2. **A surprising true answer.** The room's prior is confidently wrong, and the correction comes
   from the machine, not from the facilitator.
3. **Opens onto real structure.** The shallow answer is one line; the reasons go down a long way.
4. **Unromantic.** Nothing here can be monologued about, and no one has a personal stake to defend.
5. **Exercises *this* session's skill specifically** — not research in general.

---

## Session 1 — *The question* · `temperature=0`

> **Ask a model the same question twice at `temperature=0`. Do you get the same answer?**

**`PREDICTED`** (never observed): most of the room says yes. The answer is **no**, and the root
cause is floating-point non-associativity —
which is precisely the opener Acher et al. use in their reproducibility course
(`docs/source-analysis.md`), one abstraction layer down, in the domain our students work in.

**Why it fits session 1:** the literature exists and **saturates fast**. That is the point. A
student runs their review loop and discovers the question is answered — in one hour instead of six
weeks. The endpoint arriving immediately *is* the lesson, and it is impossible to teach with an
open question.

Opens onto: batching, kernel selection, GPU non-determinism, provider routing, seeds that are not
seeds.

---

## Session 2 — *Designing to fail* · option order

> **Does changing the order of multiple-choice options change which one the model picks?**

Position bias is documented in general and **undocumented for their setup**, so the design work is
real rather than a re-derivation.

**Why it fits session 2:** the design decisions *are* the content, and there are more than students
expect. How many orderings — two, or all *n*!? How many items before the number means anything?
One model or three? And the one that eats the session:

> **What counts as "the same answer"?**

Exact string → high variance, mostly whitespace. Normalised → lower, and you have now made an
editorial choice about what counts. A judge model → **you have introduced a second model, with its
own non-determinism, into the instrument measuring non-determinism.**

*Facilitator note:* the third is the good trap. A student who reaches it has discovered that **the
instrument is part of the system under study** — a graduate-level idea, from a multiple-choice
prompt. Do not hand it over. Ask what counts as the same answer, and wait.

---

## Session 3 — *Reading what came back* · step-by-step

> **Does asking for step-by-step reasoning improve accuracy on a task you choose?**

**Why it fits session 3:** it reliably produces a *messy* result. Often null. Often confounded by
response length, output format, or the task being too easy to move. That is exactly the material
this session needs — a hypothesis that dies in an informative way, with the live question of
*whether the hypothesis failed or the measurement did*.

It also reliably generates a **discrepancy you are about to explain away** — usually a subgroup
where the effect reverses — which is the counterweight this session teaches.

---

## Session 4 — *The gate, and the room* · judge agreement

> **Given two answers to the same question, do two different judges agree on which is better?**

**Why it fits session 4:** it is inter-rater reliability, and it lands directly on the gate. A gate
containing a judge is only as good as that judge's agreement with itself and with anyone else — so
the student's measurement is *about their own instrument*, which is the session's subject.

It also produces something genuinely **defensible**: a number about their own setup that nobody
else has, that they can stand behind, and that has a clear "what would change my mind."

*Facilitator note:* this is where the course's own material becomes fair game. Our gate approved a
degenerate null at 0.92 confidence. Say so in the hour where students measure judges.

---

## `OPEN`

- **Offline / rate-limited fallbacks.** Sessions 1 and 2 can run against a local model. Sessions 3
  and 4 need a stated fallback; not yet written.
- **Bank depth.** Four targets is one cohort. Needs two–three per slot before a second cohort
  repeats a session.
- **Does the accelerator application ask what they would change about their target now?** Cheap
  signal about readiness for an own question.
