# Pre-registration — can an agent catch seeded-02's defect?

**Written 2026-09-09, BEFORE running anything.** Committed before results exist, because an
experiment about research discipline that is run loosely is just a joke about itself.

This closes the `OPEN` in `FACILITATOR.md`: *"Untested with an agent in the loop. Worth learning
whether an agent asked 'review this revision' catches the collinearity, since that is the realistic
modern version of this hour."*

---

## The question

`analysis.py` v2 implements three review-required changes in good faith. The defect is that
**safeguard 2 residualises the encoding features against `answerable` — the exact variable
safeguard 1 uses to prove those features are alive.** Control target and FWL regressor are one
variable, so the encoding arm is near-chance by construction and the primary endpoint
(`AUROC_gen − AUROC_enc`) is maximised by the safeguard that was supposed to protect it.

Measured ground truth: with the seed held fixed, killing the encoding features entirely moves the
headline endpoint by **+0.000**.

**Does an agent asked to review this revision find that?**

## Arms

| arm | materials | n | what it tests |
|---|---|---|---|
| **A — cold** | `analysis.py` only. Prompt: review this revision, approve or not. | 6 | Does an agent find it unprompted? |
| **B — as shipped** | `analysis.py` + `review.md`, exactly what a student receives | 6 | Does the exercise's own scaffolding do the work? |

**Arm B is not a blind arm and is not meant to be.** `review.md` already asks *"Does the positive
control do anything? … not whether it passes, but whether its result matters."* That is a strong
hint, deliberately. **A vs B measures how much of the catch is the hint.**

Agents run in a sandbox containing only the listed files. `FACILITATOR.md` is unreachable —
verified, zero matches.

## Scoring — fixed now, adjudicated blind

A separate agent scores each review **without being told which arm it came from** and without
seeing this file's ground truth section until after it has scored.

| grade | criterion |
|---|---|
| **CATCH** | Names that `answerable` is **both** safeguard 1's control target **and** a safeguard 2 residualisation regressor — or equivalently, that safeguard 2 removes the signal safeguard 1 validates. |
| **PARTIAL** | Observes the control's result cannot change the endpoint, **without** naming the mechanism. |
| **MISS** | Neither. |

Also recorded per review: **verdict** (approve / reject / conditional), and **other findings**, so
a false-positive rate is visible — an agent that rejects everything has not caught anything.

## Predictions, stated before the data

1. **Arm A catch rate ≤ 2/6.** If an agent reliably finds this cold, session 2's claim needs
   narrowing and I will say so.
2. **Arm B > Arm A.** The hint is doing real work.
3. **Most reviews in both arms will APPROVE or approve-with-minor-changes** — this is the
   `PREDICTED` line already in `FACILITATOR.md`, and this is the first evidence for or against it.
4. Agents will find *something* to say in both arms. **Volume of findings is not the measure**;
   only the graded criterion above counts.

## What would change my mind

- **Arm A ≥ 4/6 CATCH** → the course overstates agent blindness at the design stage. Session 2's
  framing gets rewritten and `tools-by-stage.md`'s entrustment ladder loosens for stage 3.
- **Arm B ≈ Arm A, both low** → the exercise's own scaffolding does not help, and question 2 in
  `review.md` needs rewriting.
- **Both arms high** → the exercise is too easy for a room with agents, and needs a harder variant.

## Scope, honestly

n = 6 per arm, one model family, one defect, one prompt per arm. **This is a pilot, not an
estimate.** It can support "agents do / do not reliably catch this one defect cold." It cannot
support a general claim about agents and experimental design, and no result here will be written
into the course as one.
