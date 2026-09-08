# The shared target — `temperature=0`

**Status: `DRAFT`, 2026-09-08.** The worked substrate for all four sessions.

---

## The question

> **Ask a model the same question twice at `temperature=0`. Do you get the same answer?**

Everyone in the room will say yes. Most will be slightly insulted by the question.

The answer is **no**, reliably, and the reasons go all the way down.

---

## Why this one

Students do **not** bring their own research question to this course. That belongs to the
accelerator, for which this is a prerequisite. Here they are learning to hold the tools, and a
supplied target does three things a personal one cannot:

**It is bounded by construction.** Two API calls. There is no version of this that becomes a
six-week project, which means a student cannot get lost in it — and getting lost is the failure
mode we most want to avoid before anyone is trusted with a real question.

**It has a surprising true answer.** Not a drill with a known result the instructor is waiting to
hear. The room genuinely does not know, most people's prior is confidently wrong, and the
correction arrives from the machine rather than from us. That is the experience we are trying to
give them, in miniature, on purpose.

**It opens onto real structure.** Batching. Kernel selection. GPU non-determinism. Provider
routing. Seeds that are not seeds. Floating-point non-associativity, which is the root cause and
is also — precisely — the opener Acher et al. use in their reproducibility course
(`docs/source-analysis.md`). We are teaching their lesson one abstraction layer up, in the domain
our students actually work in.

**And a fourth, practical one:** nobody can wax lyrical about it. There is no personal stake to
defend, no pet theory to protect, and no way to spend forty minutes of class time on the
importance of one's own project. The target is deliberately unromantic.

---

## The arc, one target through four sessions

| session | what the target does |
|---|---|
| **1 — the question** | Write the one-page on it: the claim with a direction, what would falsify it, what you are hoping for, **what would let you stop**. Build a lit review loop and find out whether this is already known, what the reachable version is, and where saturation lands. |
| **2 — designing to fail** | Design the actual test. How many repeats? Same session or fresh? Same provider? What counts as "the same answer" — exact string, or semantically equal? **That last question is the whole session**, and students will not see it coming. |
| **3 — reading what came back** | Run it. Interpret variance you did not predict. Separate *the hypothesis was wrong* from *the measurement was wrong*, and notice the discrepancy you were about to explain away. |
| **4 — the finding you defend** | Present what you now believe about determinism, why the room should believe it, what would change your mind, and what your result does **not** support. |

## The trap in session 2, stated for facilitators only

**"The same answer" is undefined until a student defines it**, and every definition they pick is
a measurement decision that changes the result:

- exact string match → high variance, and it is mostly whitespace and formatting
- normalised string → lower, and now you have made an editorial choice about what counts
- semantic equivalence via a judge → you have introduced a second model, with its own
  non-determinism, into the instrument measuring non-determinism

The third one is the good trap. A student who reaches it has independently discovered that **the
instrument is part of the system under study**, which is a graduate-level idea arrived at from two
API calls. Do not hand it to them. Ask what counts as the same answer and wait.

---

## What this is not

It is not a demonstration that models are unreliable, and facilitators should head that off. The
finding is much narrower and much more useful: **a parameter you believed was a constant is a
variable, and you can measure it.** That is the transferable move. Every field has one of these.

## `OPEN`

- Needs a fallback target for anyone rate-limited or offline. Candidate: reordering the options in
  a multiple-choice prompt and measuring position bias — same shape, same boundedness, runs against
  a local model.
- Should the accelerator application ask what they would change about this target now that they
  have run it? It is a cheap signal about whether someone is ready for their own question.
