# Vibe Research Standards

topic-namespace: vr

---

**Status: `DRAFT`, 2026-08-24, authored by Lyra.** Written in the Multiverse `standards` schema
(Topic → Course → Standard → Objective, each with a slug, scoreable) so it can slot into the
school's existing structure and its XP economy rather than sitting beside them. Format matched
from `EngineeringEducation/standards/python/` — see
[`../../docs/school-repos-and-standards.md`](../../docs/school-repos-and-standards.md).

**Offered upstream, not assumed.** Naming, course boundaries, and whether this belongs in the
school's repo or ours are Liz's call.

Prerequisite: the Multiverse agentic coursework. Every learner arrives owning a long-horizon
agent and has already run a paired ablation as an assessment.

---
## Course: Question

- [Formulate a testable claim from a domain curiosity](./question/formulate-a-testable-claim-from-a-domain-curiosity.md)
- [Verify a claimed number against the artifact that produced it](./question/verify-a-claimed-number-against-the-artifact-that-produced-it.md)
- Conduct an agent-assisted literature review without inheriting its errors

---
## Course: Design

- [Pre-register an analysis, including the outcome you do not want](./design/pre-register-an-analysis-including-the-outcome-you-do-not-want.md)
- Identify the confounds that separate your conditions before your variable does
- Select a control that is capable of failing

---
## Course: Execution and Analysis

- [Bound an inquiry so it can end](./execution/bound-an-inquiry-so-it-can-end.md)
- Verify that a search which returned nothing actually ran
- Reconcile a result with the estimator that produced it
- Distinguish a per-sample statistic from a rank-bounded one

---
## Course: The Gate

- [Build a review gate out of your own failures](./gate/build-a-review-gate-out-of-your-own-failures.md)
- Demonstrate your gate catching something you could not see unaided
- Divide verification labour with a long-horizon agent

---

## Note on the four Standards written out in full

Thirteen are listed; five are authored. That is deliberate — enough to judge the shape and the
level, not so much that it presumes agreement on the structure. If the shape is right the
remaining eight are mechanical.

**`vr.bound` was added 2026-09-08** and is the only one not in the original twelve. It exists
because a gap was found by asking what the course defends against: every other standard here
guards against believing something *false*, and none guarded against an inquiry that is
perfectly sound and simply never ends. That failure is produced by a *good* collaborator
rather than a bad one, which is why a course built around agentic partners needs it named.
`vr.formulate` objective 6 authors the stopping condition; `vr.bound` assesses whether it was
honoured or revised in the open.
