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

## What will actually stop you — the barrier table

*The per-section tables below say what each tool is **for**. This one says what it **costs you to
start**, which is the thing that stops a student at 11pm on a Tuesday and is almost never written
down. Scan this to pick; read the sections to learn.*

**Columns.** `cost` is out-of-pocket. `account` is what you must create *before the tool does
anything* — the distinction that matters is whether an **agent can hold the credential**, because
a tool an agent cannot authenticate to is a tool the student has to babysit. `install` is the real
shape of getting it running, not a difficulty score. `hw` flags anything that is not "any laptop".

| tool | cost | account | install | hw | status |
|---|---|---|---|---|---|
| **Python 3.12+** | $0 | none | installer / `uv` / conda | any | `used` |
| **numpy**, **scipy** | $0 | none | `pip` | any | `used` |
| **git** | $0 | none for local; host acct to push | installer | any | `used` |
| **LaTeX** (TeX Live/MiKTeX) | $0 | none | **system install, multi-GB, slow** | any | `used` |
| **latexmk** | $0 | none | ships with TeX Live | any | `used` |
| **poppler** (`pdftotext`) | $0 | none | **system pkg**, not `pip` — `brew`/`apt`/`choco` | any | `used` |
| **pingouin** | $0 | none | `pip` | any | `known` |
| **statsmodels** | $0 | none | `pip` | any | `used` |
| **Quarto** | $0 | none | installer + a TeX for PDF | any | `known` |
| **Jupyter** + `papermill` | $0 | none | `pip` | any | `used` |
| **Zotero** (desktop) | $0 | **acct only for sync**; local works without | installer | any | `used` |
| **Better BibTeX** | $0 | none | drop-in plugin | any | `used` |
| **Zotero local API** | $0 | none — **no key at all** | **desktop app must be running** | any | `used` |
| **Zotero Web API** | $0 | acct + key | `pip` client | any | `used` |
| **OpenAlex** | $0 → **metered** | keyless works, then throttles | `pip`/HTTP | any | `used` |
| **OpenAlex S3 snapshot** | $0 | **none, no key** | S3 client + **disk** | any | `known` |
| **Semantic Scholar API** | $0 | key in practice — **429s on a first keyless call** | HTTP | any | `used` |
| **PubMed / E-utilities** | $0 | none; key raises rate | HTTP | any | `used` |
| **ClinicalTrials.gov API v2** | $0 | **none** | HTTP | any | `known` |
| **OSF** | $0 | acct + token | `pip` (`osfclient`) | any | `known` |
| **AsPredicted** | $0 | **email magic-link only — no credential exists** | web only | any | `known` |
| **Zenodo** | $0 | acct + token | HTTP | any | `known` |
| **DVC** | $0 | none for local remote | `pip` | any | `known` |
| **git-annex** | $0 | none | system pkg | any | `known` |
| **jamovi** + **jmv** | $0 | none | installer (GUI) / `R` pkg | any | `known` |
| **REDCap** | **$0 but not open** | **signed institutional licence** | server deploy | server | `known` |
| **torch** (CPU) | $0 | none | `pip` | any | `used` |
| **torch** + MPS | $0 | none | `pip` | **Apple Silicon** | `used` |
| **torch** + CUDA | $0 | none | `pip` w/ CUDA index | **NVIDIA GPU** | `known` |
| **MLX** | $0 | none | `pip` | **Apple Silicon** | **ruled out — see below** |

### Three rows that are the lesson

- **poppler is a system package, not `pip`.** The highest-yield tool on this page is the one most
  likely to fail at install for a student who only knows `pip`. Budget for it explicitly.
- **Zotero's local API needs no key and no account — and needs the desktop app open.** That is a
  strange, very good property: the agent authenticates to nothing, and the student can see every
  change land in a UI. It is the cheapest agentic surface in the whole stack.
- **AsPredicted has no credential to hold.** *"There are no userids nor passwords. All
  identification is done via email."* An agent cannot use it — not "has no API", but has nothing
  to authenticate **with**. Structural, not a gap.

### The cost column is mostly $0, and that is a claim about the field, not the list

Everything a student needs to do real, checkable, pre-registered research is free — and the two
non-free entries are instructive rather than annoying. **REDCap is free but not open** (signed
Vanderbilt licence, source not redistributable), which is where a clinical student meets *free is
not open*. **OpenAlex is free until it is metered**, which is where anyone meets *the terms moved
under a tool you already depend on*. Keep both in, precisely because they complicate the story.

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

## The search pass, and what it actually found

**Three parallel surveys, 2026-08-25**, briefed to return evidence with provenance tags rather
than recommendations. The headline is not a tool list.

### Finding: a tool's metadata is less reliable than the tool

Seven independent instances, across three surveys that never spoke to each other:

| tool | what the metadata said | what the artifact said |
|---|---|---|
| **OSF** | `developer.osf.io` documents no registration-submit endpoint | `POST /v2/registrations/` **exists**; two independent probes agree |
| **MLX** | docs describe `stream` as "the default device" | source: `"[SVD::eval_gpu] Metal SVD NYI"` plus a `check_cpu_stream` guard that **throws**, no fallback |
| **Zotero** | GitHub SPDX badge: `NOASSERTION` | `COPYING`: **AGPLv3** |
| **Taguette** | GitHub mirror's tags stop at 2019 — reads as abandoned | GitLab canonical, **active this month** |
| **revtools** | `pushed_at: 2026-07-07` | default-branch HEAD: **2020-01-10** |
| **Pweave** | PyPI classifier: `Development Status :: 5 - Production/Stable` | **fails at import**; no `requires_python`, no `requires_dist` |
| **Hatch** | widely repeated: "no lockfile support" | `hatch env lock` since **1.17.0**, emits PEP 751 `pylock.toml` |

**This is CHECK THE PRIMARY applied to software** — the same shape as *the paper says which model
→ read the shipped `config.json`*. It belongs in the course as a worked exercise, not a maxim:
give students a tool whose badge, `pushed_at` and classifiers all disagree with its source, and
let them find out.

**Corollary worth teaching:** `pushed_at` counts activity on *any* ref. A repo can look alive for
six years on the strength of a stale branch.

### Verified facts we are relying on

- **OpenAlex is now metered.** Confirmed live: `x-ratelimit-limit: 1000`, `limit-usd: 0.1`, one
  credit per list request. Keyless still returns data, then stops. **The CC0 S3 bulk snapshot
  remains free and unkeyed — teach the snapshot, not the live API.** Semantic Scholar 429s on a
  first keyless call.
- **MLX is irrelevant to an analysis course.** `eigvalsh` and `svd(compute_uv=False)` exist, and
  every decomposition **throws on GPU by design**. On CPU it calls the same `gesdd`/`syevd`
  through Accelerate that NumPy already calls on macOS 14+. *Verified on our own hardware:* torch
  2.13.0 raises `NotImplementedError` for `_linalg_eigh` on MPS at both 90x90 and 768x768 — not a
  size gate, the op is absent. Spectra work is CPU on both frameworks.
- **A lockfile buys "agrees to ~1e-13", not "bit-identical."** One `pixi.lock` resolved to three
  different BLAS libraries across platforms. Glatard et al. 2015 measured a one-bit `expf()`
  change between glibc versions moving FSL subcortical Dice from 0.99 to **0.59**. `glibc` is in
  no Python or R lockfile. *Checked on our box:* `d_eff` at L21 is **bit-identical across 1, 4 and
  12 threads** on Accelerate — the OpenBLAS thread-nondeterminism does not reproduce here, but
  that had to be measured rather than assumed.
- **Quarto's inline expressions are a CI gate.** `error: false` is the default and `quarto render`
  exits 1 on a failed expression. Stronger than any "typed number linter" — which does not exist —
  because a numeral that is never a literal cannot go stale.

### Pre-registration: what an agent can and cannot do

| | create by API | submit by API | gate |
|---|---|---|---|
| **Zenodo** | yes | **yes, immediate** | none — but **metadata stays editable indefinitely**, which defeats the purpose |
| **OSF** | yes | **yes, undocumented** | **~48-72h** auto-approve by daily cron, or a human clicks an email. No API path skips it. |
| **AsPredicted** | **no, structurally** | no | *"There are no userids nor passwords"* — magic-link only. **There is no credential an agent could hold.** |

The OSF wait is a **deliberate guard-rail, not a missing feature**, and worth presenting that way.

**Two traps for the syllabus:** the `prereg` R package depends only on `rmarkdown` — structurally
incapable of HTTP — and ships an `aspredicted_prereg` template with **no connection to
aspredicted.org**. And **OpenTimestamps proves timing, not commitment**: stamping is free and
unlimited, so one can stamp fifty contradictory hypotheses and reveal only the winner.

### The domain finding

> **The tooling gradient is not about field prestige, it is about workflow shape.** Standards
> describing a *single narrative document* (STROBE, STARD, CARE) stayed checklist-only. Standards
> describing a *pipeline with discrete steps* (PRISMA) grew real scriptable ecosystems.

A clinical or sociology student is **not short of rigor — they are short of workflows that
decompose.** That reframes the domain-widening problem: we are not bringing rigor to them, we are
bringing decomposition.

Best non-CS agent targets, each verified end-to-end: **ClinicalTrials.gov API v2** (open, no key,
600k studies), **Zotero's local write-capable API** at `localhost:23119/api/`, and the
**Nextflow / Snakemake / CWL** config-file family. **`jmv` + jamovi** is the cleanest
*GUI-for-the-student, script-for-the-agent* pairing found — same analyses, both ways, no
translation.

**REDCap is free but not open** — signed Vanderbilt license, source not redistributable. Keep it
as a teaching case: *free is not open* is a distinction a clinical student meets immediately.

### Still open

Nobody has benchmarked MLX against torch-MPS on linear algebra — **including Apple**. That is a
genuine null, not a search failure, and it is a publishable-sized gap if anyone wants it. Also
unmeasured anywhere: same code, same pinned versions, OpenBLAS vs MKL vs Accelerate — what is the
relative error? If the course needs that number, it must be produced.

## Original to-do (kept — the pass above covers categories, not sessions)

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
