# Toolset — open source, one tool per failure mode

**Status: `DRAFT`, 2026-08-25.** Suggested by Thomas: point students at good open-source tooling
for each pipeline stage, e.g. an agentically-maintained Zotero library for lit review.

---

## The selection rule

Not "here are the popular tools." **Each tool earns its place by closing a specific failure mode
the student is being taught to catch**, and by making the closing *mechanical* rather than
dependent on remembering.

That is the same argument as [gate-as-prosthesis](README.md#the-framing-that-makes-the-spine-work),
one layer down. A student who has to *remember* to check whether a citation resolves will
eventually not remember. A student whose bibliography is a database with resolvable keys gets the
check for free, and their attention is freed for the errors no tool catches.

**Honesty about our own experience**, because a course on verification should not recommend from
hearsay. Marked below:

- **`used`** — we run it in the pipeline that produced the papers this course draws on
- **`known`** — established, widely used, but *we have not used it in this work*. Evaluate before
  adopting; a student's report on it is a legitimate contribution back to this file.

---

## Dependencies — must-haves, choices, and hardware

Three different kinds of entry, and conflating them is how a setup guide becomes unusable.

### Must-haves — no alternatives offered

If a student cannot run these, they cannot do the course. Pin versions in the syllabus.

| | status | why it is non-negotiable |
|---|---|---|
| **Python 3.12+** | `used` | Everything below. We run 3.12 and 3.13 in different environments; either is fine, mixing them in one project is not. |
| **numpy**, **scipy** | `used` | `scipy.stats` is the floor for any inferential claim. Mann-Whitney, bootstrap, the lot. |
| **git** | `used` | Not for collaboration — for **dated, immutable evidence of what you believed when**. This is the prereg substrate when OSF is overkill. |
| **LaTeX** (TeX Live or MiKTeX) + **latexmk** | `used` | The write-up is an artifact that must rebuild from source. `latexmk` because it resolves the multi-pass dance so "I forgot to rerun bibtex" stops being a class of error. |
| **poppler** (`pdftotext`) | `used` | **The single highest-yield tool on this page.** It is how you check that the built artifact says what the source says. Five stale-PDF defects in three days across three people were all caught with it. |

### Categories — pick one, know why

| role | options | note |
|---|---|---|
| **effect sizes + CIs** | `pingouin` *(recommended)* · `statsmodels` · raw `scipy` | Recommended because it gives Hedges' *g* and confidence intervals **by default**. The others let you report an uncorrected *d* at n=3 in silence. See the self-indictment below. |
| **reference manager** | `Zotero` + Better BibTeX *(recommended)* · `JabRef` · a hand-maintained `.bib` | Recommended for the API — it is what makes agentic maintenance possible, and it is what **we** run. |
| **notebook / literate doc** | `Quarto` · `Jupyter` + `papermill` · plain scripts | Any is fine. The requirement is that **numbers in prose are generated, not typed.** |
| **data versioning** | `DVC` · `git-annex` · a committed `data/` dir | The last is what we do, and it is adequate at our scale. |
| **prereg** | `OSF` · `AsPredicted` · dated public commit | Strength decreases left to right. Teach the weakness of the one you pick. |

### Hardware — and this is a reproducibility surface, not a footnote

The same code gives different wall-clock, different memory behaviour, and sometimes different
numerics across these. **Students will not all be on the same one, and that is worth naming in
session 1 rather than discovering in session 3.**

| platform | stack | status | what actually bites |
|---|---|---|---|
| **Apple Silicon** | `torch` + **MPS** backend | `used` | What Starship runs. Unified memory is generous, but **kernels silently fall back**: we lost real time to a flash-linear-attention fast path that was unavailable on MPS and dropped to a torch implementation without failing. It printed a warning and kept going. |
| **Apple Silicon** | **MLX** | `known` | Apple's own array framework — likely faster and more memory-efficient than torch-MPS for the same work. **We have not used it.** A student who benchmarks MLX against torch-MPS on an identical analysis has produced a genuinely useful contribution. |
| **NVIDIA** | `torch` + CUDA | `known` | The default assumption of most tutorials, which is why Mac students hit undocumented walls |
| **CPU only** | `torch` CPU / `numpy` | `used` | Entirely sufficient for everything in this course **except** running a model. All the analysis work — bootstrap, AUROC, spectra — is CPU-bound. A student with no GPU is not excluded. |

**The teaching point, and it belongs in session 2's confound hour:** *"it ran differently on my
machine"* is not a support issue, it is an uncontrolled variable. If two students get different
numbers from the same notebook, that is a finding about the environment, and the environment is
part of the method.

**Practical rule:** whatever the platform, record it with the result — device, backend, library
versions, and whether any fast path fell back. We now do this and we did not always.

## Lit review — `vr.verify-number`, and the citation standard

| tool | status | failure mode it closes |
|---|---|---|
| **Zotero** + **Better BibTeX** | `used` | A citation with a stable key that resolves to a record is checkable. A citation typed into a `.tex` by hand is a claim. Better BibTeX gives you pinned citation keys and an auto-exported `.bib` that stays in sync with the library. |
| **Zotero Web API / local API** | `used` | This is the piece that makes it *agentic*: the agent can add, tag, deduplicate and — critically — **fetch the stored PDF and check whether the claimed sentence is in it**. |
| **OpenAlex**, **Semantic Scholar API**, **PubMed** | `used` | Programmatic metadata and abstracts; our own Research Runner sits on these. Resolves "does this paper exist" before "does it say what I claimed." |
| **`unpaywall` / DOI resolution** | `known` | Turns a DOI into a document you can actually read, which is the difference between verifying a citation and verifying a citation *record*. |

**Why this matters more than convenience.** Two of our own defects this fortnight were citations
to sources that did not contain the values attributed to them, and one was a **fully fabricated
reference** (Vera's find: a study attributed to a real researcher, at an institution that does not
exist). A library where every entry has an attached document and a resolvable key does not prevent
that — but it makes the check a lookup instead of an act of will.

> **CORRECTED 2026-08-25.** I marked Zotero `known` and wrote "we have not used it in this
> work." **Wrong.** We run `zotero-lib` on MTH — an `ingest.py`, an API key, and a working
> agentic loop where I send Nexus papers with DOIs and suggested collections and they land in the
> library. There is a message in the archive **from me** doing exactly that, on 2026-06-20, six
> papers for the presence-metric related-work section.
>
> Why I got it wrong: the library has been idle for weeks, because prep and cleanup for the
> hackathon turned my work from *doing research* into *red-teaming existing research*. I checked
> what I had been doing recently and reported it as what we do. **A tool you have stopped using
> is not a tool you have never used**, and my own week is not a survey of the lab's capabilities.
>
> This is the fourth time in three days I have been confidently wrong about the state of our own
> work — after "nobody has looked at the 27B", "I'm not working on attention heads", and a
> registry claim that went through three states. The pattern is specific enough to name:
> **I narrate my own recent context as though it were the lab's inventory.**

**The agentic part, concretely.** The student's agent maintains the library: deduplicates,
normalises, attaches PDFs, and flags entries with no retrievable document. Then hour 3's tracing
exercise has a substrate, and the lit-review standard becomes *"show me an entry your agent
flagged as unretrievable, and what you did about it."*

## Pre-registration — `vr.prereg`

| tool | status | failure mode |
|---|---|---|
| **OSF Preregistration** | `known` | A timestamped, immutable prereg you cannot quietly edit after seeing data. The immutability *is* the feature. |
| **AsPredicted** | `known` | Lighter weight, eight questions, good for a four-hour session |
| **A dated commit in the student's own repo** | `used` | What we actually do. Weaker than OSF — you can rewrite history — but honest if the repo is public and the commit is pushed. Teach the weakness alongside it. |

## Analysis — where the tool choice would have saved us

| tool | status | failure mode |
|---|---|---|
| **pingouin** | `known` | Reports effect sizes **with confidence intervals by default**, and offers Hedges' *g* directly. Our emotion-accumulation paper headlined `d = 9.86` at n=3 with no CI and a ~20% small-sample inflation that lived only in a commented-out caveat. A library whose default output includes the corrected statistic and its interval makes that error harder to make than to avoid. |
| **statsmodels**, **scipy.stats** | `used` | What we use. Powerful and entirely willing to let you report an uncorrected `d` at n=3 without comment. |
| **`scipy.stats.bootstrap`** | `used` | Resampling with BCa. **Teach the trap with it**: refit any residualization *inside* each replicate, or the interval comes out too narrow. |

## Data and artifact provenance — `vr.verify-number` objectives 0–2

| tool | status | failure mode |
|---|---|---|
| **DVC** or **git-annex** | `known` | Versions the *artifact* alongside the paper, so "the number the paper cites" and "the file it came from" move together. Would have closed the defect below. |
| **A `data/` directory committed beside the `.tex`** | `used` | What we do. Works, and is what our provenance check reads. |
| **`pdftotext` in a pre-commit hook** | `used`, ad hoc | **Is the built PDF older than its source?** We hit that defect *five times in three days* across three different people, including a shipped paper missing 6 of 8 rows of a results table. It is a one-line check and it should be a hook, not a habit. |

## Execution and reproducibility

| tool | status | failure mode |
|---|---|---|
| **Quarto** | `known` | Prose and code in one document, so a number in the text is generated rather than typed. Kills transcription drift outright. |
| **papermill** | `known` | Parameterised notebook runs — the same analysis over conditions without copy-paste divergence |
| **Snakemake** / **Nextflow** | `known` | Declares the dependency graph, so "which step produced this file" is answerable |
| **Docker / Apptainer** | `known` | The environment is an artifact too |

## Gating

**No tool recommendation here, deliberately.** Students build their own gate from their own
failures — see [`build-a-review-gate-out-of-your-own-failures`](../../standards/vibe-research/gate/build-a-review-gate-out-of-your-own-failures.md).
`pre-commit` and `pytest` are the obvious hosts for the checks once they exist, but the checks
have to be earned first. **We do not ship our kill list, in any session.**

## What to do with this in the sessions

- **Session 1** assumes a working Zotero library. Setup is prerequisite work, not class time — but
  the agentic maintenance loop is worth ten minutes of demo, because it is the thing that makes
  hour 3 possible.
- **Session 3** is where `pingouin` versus `scipy` becomes a live lesson rather than a preference:
  run the same comparison both ways and look at what each *volunteers*.
- Anything marked `known` that a student actually evaluates should come back into this file with
  their name on it.

## Open

- Whether the school already standardises on any of these (`OPEN`, ask Liz — the Multiverse has
  its own agentic resources and custom GPTs; we should not fork what exists)
- Whether we supply a pre-built Zotero group library for the pre-made research setups
- Licensing on any tool we bundle rather than link

## To do before this ships — a search pass per category

`OPEN`, flagged by Thomas 2026-08-25. Everything above is drawn from what we happen to use plus
what I happen to know, which is **exactly the sampling bias this course teaches students to
catch**. Before it goes to students, run an actual search per category and build a recommendation
list from evidence rather than recall.

Categories needing a sweep: reference management · pre-registration · effect sizes and CIs ·
data versioning · literate documents · workflow orchestration · environment capture.

**And widen past computer science.** We will likely field a lot of CS, but the Multiverse takes
all comers and the method is domain-general. Worth surveying:

- **Life sciences / clinical** — the pre-registration and reporting-standard culture is far more
  mature here than in ML; CONSORT, PRISMA, and registered reports are worth borrowing from rather
  than reinventing
- **Social sciences** — where the replication crisis produced most of the tooling we are quietly
  relying on
- **Assistant-based science suites** (e.g. Claude's) — `known`, unevaluated, and increasingly the
  default entry point for someone outside CS
- **Domain-specific**: qualitative coding, geospatial, bioinformatics, digital humanities

A student from outside CS should not have to translate a software-engineering toolchain before
they can start. If we cannot name a tool for their domain, we should say so rather than hand them
ours.
