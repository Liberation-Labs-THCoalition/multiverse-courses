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


---

## Acher, Gotlieb, Spieker & Le Bartz Lyan (ACM REP 2025) — read 2026-09-08

*"Teaching Reproducibility and Embracing Variability: From Floating-Point Experiments to
Replicating Research."* Proc. 3rd ACM Conference on Reproducibility and Replicability,
Vancouver, Jul 29-31 2025. `10.1145/3736731.3746162`.

> **⚠ CORRECTED 2026-09-09.** This header used to say *"paywalled; read via abstract, venue
> listing and the companion"*, and `toolset.md` called it a *"metadata-only sighting"* where
> *"the title is doing all the work."* **Both were wrong: the paper is gold open access and the
> ACM DL merely blocked an automated fetch.** All ten pages have now been read. We had asserted
> its pedagogy in detail from an abstract while our own legend said `SNIPPET — do not cite` — a
> hostile audit caught it, and the fix was to go and read the thing.
>
> **What it actually is:** a 26-hour course (six 4-hour sessions + one 2-hour; *the abstract says
> 24 and the body says 26 — an internal inconsistency in their paper*), 20 fourth- and fifth-year
> CS students at INSA Rennes, Fall 2024, working in **pairs**, 10 groups.

**Structure.** Two halves. First: floating-point associativity — *"how often is
(x + y) + z = x + (y + z)?"* — as a reproducibility "Hello World", with Docker, GitHub
Actions and templated experimentation, exploring variability across languages, compiler
flags and numerical precision. Second: reproducing and replicating real published work
(LLMs playing chess; football home advantage under COVID; energy efficiency across
languages). Students found subtle issues such as changed library defaults, and designed
replications that extended or challenged the originals.

**The thing worth stealing, and we had not noticed we needed it.** *Both halves are bounded
by construction.* The floating-point question has an answer you can compute in an afternoon
and still opens onto compilers, containers and precision. A replication is bounded by the
paper already existing: you get their number or you do not, and the interesting part is why.
> **⚠ The sentence that used to sit here — *"Acher does not teach focus. He hands students targets
> that cannot sprawl"* — is DELETED, 2026-09-09. Both halves are contradicted by the paper.**
>
> **The targets are supplied but they do sprawl.** The variability space inside them explodes
> combinatorially — that is the paper's actual thesis, and the word *"Variability"* is in its
> title. And students *do* exercise focus: the paper explicitly credits them with **"good judgment
> in selecting focused, tractable subsets."** So it is not bounded-by-construction-instead-of-
> focus. It is a bounded *entry point* onto an unbounded space, with focus as the student's job.
>
> That is a better model than the one we invented for them, and closer to what our own target bank
> does. What survives untouched: **instructor-curated targets, chosen from a menu of three
> (§4.1), with the instructors reproducing them first.** That is real practice at a real
> institution with a real cohort, and it is the part the supplied-target decision leans on.

**Where that puts us — an open tension, not a defect.** Our session 1 asks students to bring
*their own* curiosity, which is unbounded by construction. That is a real strength (it is
their domain, they care, the prerequisite means they can act on it) and a real exposure. We
have answered it with a written stopping condition and saturation (`vr.bound`, session 1
hour 4). Acher answers it by choosing the target. **Both are legitimate; ours costs more and
carries further.** Worth deciding deliberately rather than by default:

- **~~`OPEN`~~ — RESOLVED 2026-09-08 by Thomas, and further than I proposed.** Not a warm-up
  before their own question: **the question is supplied for the whole course.** Own questions are
  an *accelerator* requirement, and this course is its prerequisite. Here we teach holding the
  tools on something basic.

  His second reason is the one I had not priced: a personal project invites a student to *"wax
  prosaic about their likely delusional research project and burn class time."* With a cohort
  that is a tax on everyone; the supplied target is deliberately unromantic and nobody can
  monologue about it.

  So we land on **Acher's answer, arrived at from a different direction** — they chose a bounded
  target because it teaches variability cleanly; we choose one because unbounded personal
  questions are where novices get lost and where class time goes to die. Same structure, two
  independent reasons, which is the sort of agreement worth more than either argument alone.
  Target: [`the-target-bank.md`](../courses/vibe-research/the-target-bank.md) — *is
  `temperature=0` deterministic?*, whose root cause is floating-point non-associativity, which is
  literally Acher's opener one abstraction layer down.

**Also confirmed by their experience:** students found reproducibility flaws *in the
instructor's own prior work*. That is our "instructors go first" principle, arrived at
independently, and it is evidence the move survives contact with a real cohort.
