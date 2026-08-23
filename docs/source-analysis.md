# Source analysis — what exists, what we can adapt, what diverged

**Compiled:** 2026-08-22 by Lyra. Every claim below has a source; where I could not verify
something I have said so rather than filled the gap.

---

## 1. The Multiverse agentic SDLC course

Source: <https://themultiverse.school/classes/193> (also `/166`, `/182` — recurring offering),
fetched 2026-08-22.

| | |
|---|---|
| format | One-day intensive, online |
| prep load | ~40 hours of practice |
| audience | Developers and technically-minded product managers |
| prerequisites | none listed |
| instructor | Liz Howard (Future Infinitive), founder & professor |

### Learning outcomes, verbatim

> - "verify a program does what you claimed with a test"
> - "verify model written code against its specification"
> - **"design a review gate that catches what the doer cannot see"**
> - "reconcile an agents run with a tool that failed"
> - "reconcile what you built with what you can maintain alone"
> - "synthesise an accountability regime for an unattended agent"
> - "synthesise an agent that carries notes across its own runs"

### Two things worth stealing outright

**(a) Outcomes are competency verbs at ascending Bloom levels.** *verify* → *reconcile* →
*synthesise*. Not "understand X" or "be familiar with Y" — every outcome names something the
student can be observed doing. Our draft syllabus does not do this and should.

*(Tangentially: Bloom's cognitive level turns out to be linearly decodable from transformer
residual streams at ~95% via logistic probes, with separability onset around layer 5 —
Raimondi & Gabbrielli, arXiv 2602.17229. Cute, and probably a good hook for a session, but it
is not evidence that Bloom's is the right pedagogical frame. Do not let me use it as one.)*

**(b) Competency is demonstrated by an ablation.** Their assessment method, verbatim:

> "paired runs of the same multi-step task with the note store kept and cleared"
>
> — where the cleared iteration repeats a skipped step.

This is a controlled experiment used as an exam. The student runs their agent twice, changing one
variable, and the *difference* is the evidence. That is precisely the methodology the research
course teaches, so their assessment format **is** our subject matter. Strong continuity, and it
means students will already have done one before they reach us.

### The natural seam

`"design a review gate that catches what the doer cannot see"` is already in their catalogue —
for **code**. Our course is the same skill pointed at **research claims**. That is a clean
hand-off and an honest pitch: not a new idea, an extension of one they already teach.

## 2. Our own drafts, and how they have drifted

| file | date | state |
|---|---|---|
| `vibe_research_syllabus.md` | 2026-08-06 | the substantive draft — 4-hour intensive |
| `multiverse_fellowship_draft.md` | 2026-07-30 | superseded by v2 |
| `multiverse_fellowship_v2.md` | 2026-08-06 | fellowship framing |
| `Project-Oracle/docs/multiverse_training_spec.md` | 2026-07-07 | oldest |

### Four divergences from the current spec (Thomas, 2026-08-22)

| draft says | now |
|---|---|
| **one** 4-hour intensive | **3–4** intensives over ~60 days |
| "open enrollment, **no prerequisites**" | agentic coursework is a **prerequisite** |
| pathway = *"Agent Design → Agentic SDLC → Liberation Labs Research Fellowship"*, i.e. Multiverse agent courses come **after** | those courses come **before**; the accelerator is next year |
| red-teaming is **one principle in Hour 4** | adversarial gating is at **every step** |

The third is the significant one: **the funnel is inverted.** The draft treats the Multiverse
agent courses as the onward destination for people who catch the research bug. In the current
plan they are the entry requirement. Everything downstream of that — audience, assumed skill
level, what session one can take for granted — changes.

The fourth is a structural gap, not a wording issue. Gating cannot be a closing principle if it
is meant to run at every step; it has to be the spine the other content hangs on.

### What in the draft is still good

- The **vibe analogy** for internal states (you read a room without parsing every conversation).
- **Domain-tailored prompt sets** so a clinician, a lawyer and a journalist each break the model
  on their own material.
- **"Why 'I was wrong' is the most valuable sentence in research"**, with the file-drawer and
  drug-trial framing. This should probably get bigger, not smaller.
- The instructor notes, especially: *"Don't make it about Liberation Labs' research specifically.
  Make it about the METHOD. Our work is the example, not the subject."*

## 3. A caution about our own demo material

The draft's Hour 1 and Hour 3 depend on **pre-computed internal measurements**. As of 2026-08-22
we know that `d_eff` — the participation ratio we would most naturally demo — is **not converged
at n=90 prompts**: 95–98% of layers are still rising between m=80 and m=89, and the value at the
peak layer moves 14.6 → 39.5 as sample size goes 20 → 89.

The *peak location* is rock solid (layer 21 at every sample size, in both a hybrid and a dense
model). The *magnitude* is substantially a function of how many prompts we ran.

**So: demo the shape, not the number.** If we put "effective dimensionality ≈ 40" on a slide we
would be teaching students to quote a sampling artifact in the same session where we teach them
not to. Detail: `lyra-s-research-/experiment-designs/deff_convergence_results.md`.

## 4. External resources scanned

Thin pickings for direct reuse; nothing found that teaches adversarial gating for AI-assisted
research specifically. Useful adjacent material:

- **eLife, "Eleven strategies for making reproducible research and open science training the norm
  at research institutions"** — <https://elifesciences.org/articles/89736>. Institutional-adoption
  strategies; useful for the accelerator layer more than the intensives.
- **LMU Munich empirical-practice courses** — sample-size planning, power analysis,
  preregistration, open data, reproducible analysis scripts as a standard undergraduate sequence.
  Confirms the components are conventional; our contribution is the agent-in-the-loop framing,
  not the statistics.
- **`github.com/topics/research-methodology`** — grab-bag, nothing turnkey.
- **`github.com/EngineeringEducation`** — the Multiverse School's own GitHub org. **Not yet
  examined.** Likely the highest-value remaining source and the obvious next pull.

**Honest summary of the scan:** the pieces we would teach (pre-registration, power, honest nulls,
reproducibility) are standard and well-covered elsewhere. What is not covered anywhere I could
find is *how a human and a long-horizon agent divide the work of being rigorous* — who checks
what, what the agent can see that you cannot, what you can see that it cannot. That is the part
only we can write, and it should be the spine.
