# Results — the agent-review experiment

**Run 2026-09-09**, against [the pre-registration](./AGENT_REVIEW_PREREG.md) committed at `1929ab0`
before any agent ran.

---

## Both predictions falsified

| | predicted | actual |
|---|---|---|
| **Arm A (cold) CATCH rate** | ≤ 2/6 | **5/5** |
| Arm B (as shipped) CATCH rate | > A | 5/5 *(ceiling — no headroom to differ)* |
| **Verdict** | most APPROVE | **10/10 REJECT** |

**10 of 10 CATCH. Two independent adjudicators. 10/10 inter-rater agreement. Zero PARTIAL, zero
MISS.** Every review named `answerable` as simultaneously safeguard 1's control target and a
safeguard 2 residualisation regressor, and stated the consequence.

Arm A had no hint at all — just `analysis.py` and *"review this revision."*

**This is the falsifier I wrote down**, and the prereg says what happens next: *"Arm A ≥ 4/6 →
the course overstates agent blindness at the design stage. Session 2's framing gets rewritten and
the stage-3 entrustment ladder loosens."* Done below.

## The catches were not shallow

- **Nine of ten found it by exercising the failure path, not by reading the code** — re-seeding,
  toggling the encoding arm between alive and dead, and measuring the endpoint both ways.
- Measured invariance to machine precision: `max|Δ| = 1.6e-15`, and **endpoint identical across
  400 matched-seed replications**.
- **R7** decomposed the annihilation by regressor: residualising on `tok_len` alone leaves
  alive/dead differing by 0.899, on `answerable` alone by 1.32, **on both by 1.55e-15.**
- **R8** ran the control's own criterion on the matrix the endpoint actually consumes: AUROC
  **0.313**, a **0/150** pass rate — *"the script prints PASS beside a number computed on features
  that fail that very criterion."*
- **Grade was uncorrelated with volume.** Other-finding counts ran 5–11, and the two crispest
  statements came from the two lowest-volume reviews. This was insight, not spray.

**R7 independently derived the exercise's own lesson:** *"The review asked for two safeguards
independently and did not ask what they would do to each other."*

## They found a second defect I did not know about

**R6** separated two failures where I had documented one:

1. **Mechanically inert.** `control_passes` is computed (line 103), **printed** (114) and returned
   (118) — and **nothing ever branches on it.** The docstring claims *"This gates interpretation of
   the encoding arm."* It gates nothing. It is a printed string.
2. **Algebraically inert.** Safeguard 2 residualises out what safeguard 1 validates.

**Fixing the first does not fix the second**, which is the distinction that matters. `FACILITATOR.md`
documented only the second. The exercise is richer than its answer key.

---

## What this changes, and what it does not

**The broad claim is dead.** "An agent will approve a design that cannot fail" is falsified as
stated. Ten out of ten rejected it, cold, and diagnosed the mechanism.

**The specific claim survives, and it is the one the course actually needs.** These agents reviewed
**someone else's work**, handed to them with no context and no stake. That is not the condition the
course warns about. Session 2's actual sentence is:

> *A reviewer that shares your assumption returns confidence, not coverage — and an agent reviewing
> your design shares every assumption you gave it.*

Nothing here tests that. An outside reviewer with no priors is a **different instrument** from the
agent that helped you build the thing, and this experiment measured the first while the course
claims something about the second.

**And the honest reading is better news for the course than the old framing was.** A frontier agent
is *genuinely useful* as an outside reviewer at the design stage — reliably, cold, by running the
failure path. "Use it as an adversary on work it did not help you build" is a more useful thing to
teach than "do not trust it here."

## Scope — stated in the prereg and unchanged by the result

n = 5 per arm, **one defect, one model family, one prompt per arm.** This supports *"agents
reliably catch this defect cold."* It does not support a general claim about agents and
experimental design, and none is written into the course.

**The open question this now raises**, which is the one worth running next: does an agent catch
this when it **helped write the design**? That is the course's actual claim and it remains untested.
