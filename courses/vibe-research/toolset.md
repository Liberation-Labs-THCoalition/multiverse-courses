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
| **numpy**, **scipy** | $0 | none | `pip` (wheels for win/mac-arm/manylinux) | any | `used` |
| **git** | $0 | none for local; host acct to push | installer / `apt` / `brew` | any | `used` |
| **LaTeX** (TeX Live/MiKTeX) | $0 | none | **system install** — ~GB (scheme-full, the installer default) / ~few hundred MB (basic) / ~tens of MB (TinyTeX) | any | `used` |
| **latexmk** | $0 | none | in TeX Live **medium/full only** (`collection-binextra`) — **not** in scheme-basic, scheme-small or BasicTeX; MiKTeX on demand; in TinyTeX | **it is a Perl script** — TL/Windows bundles a minimal Perl, MiKTeX bundles none | `used` |
| **poppler** (`pdftotext`) | $0 | none | **CLI: system pkg or conda-forge — never pip.** PyPI `pdftotext` is sdist-only (needs `libpoppler-cpp` + a compiler); PyPI `poppler-utils` **ships no binaries at all**. Text-only alternative: `pypdfium2`, pure pip, every platform. | any | `used` |
| **pingouin** | $0 | none | `pip` (`py3-none-any`) | any | `known` |
| **statsmodels** | $0 | none | `pip` | any | `used` |
| **Quarto** | $0 | none | installer. LaTeX PDF needs a TeX (`quarto install tinytex`); **`format: typst` gives PDF with no TeX at all** — the Typst CLI is bundled. | any | `known` |
| **Jupyter** + `papermill` | $0 | none | `pip` | any | `used` |
| **Zotero** (desktop) | $0 | **acct only for sync**; local works without | installer | any | `used` |
| **Better BibTeX** | $0 | none | `.xpi` from GitHub releases → Tools ▸ Plugins ▸ Install From File (**not** a one-click store install) | any | `used` |
| **Zotero local API** | $0 | **no key to READ**; writes need a runtime-granted local key — agent *can* hold it, a human must grant it | desktop app running **and** local API switched on in Settings ▸ Advanced — **off by default, 403 until then** | any | `used` |
| **Zotero Web API** | $0 | acct + key (plain string, agent-holdable) | `pip` (`pyzotero`) | any | `used` |
| **OpenAlex** | $0 → **metered**; free key = **$1/day**, 10× the anonymous budget | keyless works, then throttles | `pip`/HTTP | any | `used` |
| **OpenAlex S3 snapshot** | $0 | **none — no AWS account** | S3 client + **~750 GB compressed, several TB open** | any | `known` |
| **Semantic Scholar API** | $0 | key needed in practice — keyless is a **shared** 1000 req/s pool across *all* anonymous users, routinely saturated (5/5 calls 429'd during our check). A key buys a **private 1 RPS**, not a bigger number. | HTTP | any | `used` |
| **PubMed / E-utilities** | $0 | none (3 req/s); key raises to 10 | HTTP | any | `used` |
| **ClinicalTrials.gov API v2** | $0 | **none** — verified 200 keyless | HTTP | any | `known` |
| **OSF** | $0 | **read public: none.** Write/private: acct + PAT (`OSF_TOKEN`), agent-holdable | `pip` (`osfclient`) | any | `known` |
| **AsPredicted** | $0 | **email magic-link only — no password field exists on the page.** An agent would need mailbox access, and coauthor approval is a human email loop regardless. | web only | any | `known` |
| **Zenodo** | $0 | **read public: none** (60/min). Deposit: acct + token w/ `deposit:write`+`deposit:actions` (100/min) | HTTP | any | `known` |
| **DVC** | $0 | **none** for a local/filesystem remote | `pip`; cloud remotes need extras (`dvc[s3]`…) | any | `known` |
| **git-annex** | $0 | none | **`pip` — real binary wheels** (linux x86_64/aarch64, macOS arm64/x86_64, win_amd64), or system pkg / conda-forge | any | `known` |
| **jamovi** + **jmv** | **$0 desktop**; Cloud has paid Priority/Teams tiers | none for desktop; acct for Cloud | installer (GUI) / CRAN pkg (needs R) | any | `known` |
| **REDCap** | **$0 for non-profit consortium members only** — commercial use is paid (REDCap Cloud) | **an executed EULA with Vanderbilt.** A human signature, not a credential. | server deploy | server | `known` |
| **torch** (CPU) | $0 | none | `pip` — **but on Linux plain `pip install torch` installs the CUDA build** and pulls ~2 GB of NVIDIA wheels onto a GPU-less box. Use `--index-url .../whl/cpu` for a real CPU install. | any | `used` |
| **torch** + MPS | $0 | none | `pip` | **Apple Silicon, macOS 14+** — no Intel-Mac wheels ship at all | `used` |
| **torch** + CUDA | $0 | none | Linux: plain `pip install torch`. **Windows: needs the CUDA index URL.** No macOS CUDA. | **NVIDIA GPU** | `known` |
| **MLX** | $0 | none | `pip`; CUDA backend on Linux via `pip install mlx[cuda]` | Apple Silicon — **or NVIDIA via the CUDA backend** | **not for this course — see below** |

### Four rows that are the lesson

- **poppler's CLI is genuinely un-`pip`-able, and PyPI actively misleads you about it.** The
  highest-yield tool on this page is the one most likely to stop a student who only knows `pip`.
  `pip install pdftotext` is source-only and needs a C++ toolchain; `pip install poppler-utils`
  succeeds and gives you **nothing** (see below). Route students to `conda-forge` or a system
  package, and budget for it out loud.
- **Zotero's local API is off by default.** It needs no key to read — genuinely rare, and the
  cheapest agentic surface in the stack — but until someone ticks a box in Settings ▸ Advanced it
  returns `403`, and *writes* need a key the user grants at runtime. "No credential" and "no setup"
  are not the same thing, and we had them conflated.
- **AsPredicted has no credential to hold.** The sign-in form has an email field and **no password
  field at all**. An agent cannot use it — not "has no API", but has nothing to authenticate
  *with*. Coauthor approval is an email loop too, so a human is structurally in the path.
- **Four rows we marked "any" are not.** `latexmk` (TeX Live scheme-dependent, and a Perl script
  where MiKTeX ships no Perl), `poppler` (a different package manager per OS), `torch`
  (**CUDA-by-default on Linux, CPU-by-default on Windows, arm64-only on macOS** — one `pip install`
  command, three different products), and MLX (Apple-only until recently, no longer). For a
  mixed-platform cohort, "any" was the single most error-prone cell in the table.

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

### Finding: hand-typed metadata lies; generated metadata does not

Eleven independent instances, across **four** surveys that never spoke to each other. The first
seven came from the toolset search pass. The last four were found while **fact-checking this
page's own barrier table**, which had been written partly from recall — so the finding reproduced
itself on us, one section below where we wrote it down.

| tool | what was claimed | what the artifact showed |
|---|---|---|
| **`poppler-utils`** (PyPI) | *"Precompiled command-line utilities… for manipulating PDF files"*, licence `GPL-2.0`, 18 KB LICENSE shipped | **9 KB wheel. Two Python files. Zero binaries, no CLI entry point.** Name, summary and licence each imply shipped binaries; `unzip -l` disproves all three in one command. |
| **OSF** | `developer.osf.io` documents no registration-submit endpoint | `POST /v2/registrations/` exists — two independent probes agree |
| **MLX** | PyPI summary: *"a framework for machine learning on Apple silicon"* | the **same release** ships manylinux x86_64/aarch64 and win_amd64/arm64 wheels and documents `pip install mlx[cuda]` |
| **MLX** (docs) | `stream` described as "the default device" | source: `"[SVD::eval_gpu] Metal SVD NYI"` + a `check_cpu_stream` guard that **throws**, no fallback |
| **Zotero** | GitHub SPDX badge: `NOASSERTION` | `COPYING`: **AGPLv3** |
| **jamovi** | GitHub metadata: `license: Other`, `spdx_id: NOASSERTION` | `LICENSE.md` is explicit and per-component: **AGPL3** for client/server, **GPL2+** for engine; `jmv` separately GPL-2 \| GPL-3 on CRAN |
| **Taguette** | GitHub mirror's tags stop at 2019 — reads abandoned | GitLab canonical, **active this month** |
| **revtools** | `pushed_at: 2026-07-07` | default-branch HEAD: **2020-01-10** |
| **Pweave** | PyPI classifier: `Development Status :: 5 - Production/Stable` | **fails at import**; no `requires_python`, no `requires_dist` |
| **Hatch** | widely repeated: "no lockfile support" | `hatch env lock` since **1.17.0**, emits PEP 751 `pylock.toml` |
| **PyTorch** | **no prose anywhere states the platform split** | `requires_dist` markers (`platform_system == "Linux"` on every NVIDIA dep) and a **502 MB vs 116 MB** wheel gap state it unambiguously |

### The rule this actually supports — and why "distrust metadata" is wrong

The PyTorch row is the reverse of the other ten, and it is the one that fixes the rule. There, the
machine-readable metadata is the **only** honest account and the human-written docs are silent. So
the lesson is not *distrust metadata*. It is:

> **Trust what the build generates. Distrust what a human typed once.**
>
> *Generated:* wheel filenames, dependency markers, file sizes, ZIP listings, `LICENSE` files, git
> HEAD dates, source code. These are produced by the thing itself, every release.
> *Hand-typed:* summaries, badges, classifiers, README prose, `pushed_at`-style aggregates. These
> are written once, at a moment that has passed, and nothing forces them to keep up.

Every one of the eleven fits. `poppler-utils`'s summary, MLX's summary, Pweave's classifier and
Zotero's and jamovi's SPDX badges are all hand-typed-or-inferred; the wheel contents, the wheel
filenames, the import failure and the `COPYING` files are all generated. **This is CHECK THE
PRIMARY applied to software**, with a usable test attached — *ask who wrote this string, and
whether anything would have forced them to revisit it.*

**Two corollaries worth teaching:**

- `pushed_at` counts activity on *any* ref. A repo can look alive for six years on a stale branch.
- A licence detector that fails degrades to `NOASSERTION`, which downstream tools then render as
  **"unknown licence"** — a materially different and much scarier claim than the truth. Zotero and
  jamovi are both AGPL3 and both read as unlicensed. Failure presenting as a finding is the same
  shape as a broken search returning zero results.

This goes in the course as a worked exercise, not a maxim: hand students `poppler-utils`, let them
read the name, the summary and the licence, then have them run `unzip -l` on the wheel.

### Verified facts we are relying on

- **OpenAlex is now metered.** Confirmed live: `x-ratelimit-limit: 1000`, `limit-usd: 0.1`, one
  credit per list request. Keyless still returns data, then stops. **The CC0 S3 bulk snapshot
  remains free and unkeyed — teach the snapshot, not the live API.** A free key raises the budget
  10× to **$1/day**; the snapshot is ~750 GB compressed.
- **Semantic Scholar's keyless tier is a shared pool, and that is the teachable part.** We first
  wrote "429s on a first keyless call" from a single observation. Re-checked: **5 of 5** keyless
  calls returned 429 while OSF, Zenodo, OpenAlex and ClinicalTrials.gov all returned 200 from the
  same host in the same session — so it is real and specific to S2, not our egress. But the
  documented mechanism is not a low per-user limit: unauthenticated traffic shares **one 1000
  req/s pool across every anonymous user on Earth**, and it is routinely saturated. A key does not
  buy a bigger number — it buys a **private 1 RPS**. *A symptom reproduced 5/5 still told us
  nothing about the cause; we had to read the terms for that.*
- **MLX buys an analysis course nothing *on Apple Silicon*, which is the only claim we can make.**
  `eigvalsh` and `svd(compute_uv=False)` exist, and every decomposition **throws on Metal by
  design** — `"[SVD::eval_gpu] Metal SVD NYI"` plus a `check_cpu_stream` guard with no fallback. On
  CPU it calls the same `gesdd`/`syevd` through Accelerate that NumPy already calls on macOS 14+.
  *Verified on our own hardware:* torch 2.13.0 raises `NotImplementedError` for `_linalg_eigh` on
  MPS at both 90x90 and 768x768 — not a size gate, the op is absent. **On Apple Silicon, spectra
  work is CPU on both frameworks.**
  **Correction, 2026-08-25:** we first wrote this as *"MLX is irrelevant to an analysis course"*,
  full stop. That was over-broad. MLX now ships manylinux and Windows wheels with a **CUDA
  backend** (`pip install mlx[cuda]`), and **we have not tested whether the decompositions throw
  there.** The Metal finding does not transfer, and we should not let it look like it does. The
  narrow claim survives; the general one was never tested. *(A student on NVIDIA would reach for
  torch anyway, so this changes no recommendation — it changes what we are entitled to say.)*
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
genuine null, not a search failure, and it is a publishable-sized gap if anyone wants it.

**Correction, 2026-08-25.** We also wrote here that *"same code, same pinned versions, OpenBLAS vs
MKL vs Accelerate — the relative error is unmeasured anywhere."* **That was half wrong, and the
half that was wrong is the half that mattered.** Whether numerical variation at the BLAS/LAPACK
level moves a downstream *scientific conclusion* has been asked and answered — repeatedly, for
eleven years, by Tristan Glatard's group. Most directly **Kiar et al. 2021** (*PLoS ONE*,
[10.1371/journal.pone.0250755](https://doi.org/10.1371/journal.pone.0250755)), whose "dense"
Monte-Carlo-arithmetic configuration instruments BLAS, LAPACK, NumPy and Cython and swings a
downstream classification accuracy from **0.520 to 0.716**. Graph features retained *under one
significant digit*. The reproducibility literature we did not know about is now the reason this
section is shorter.

What is genuinely open is narrower: that literature **perturbs arithmetic to simulate the gap**,
and nobody has swapped the backends that actually ship and measured the real disagreement. Worth
doing, but it is a fourth noise source to add to a known picture — **Vila et al. 2024**
([10.1145/3641525.3663626](https://doi.org/10.1145/3641525.3663626)) already showed hardware,
software packaging and rounding produce perturbations of *similar magnitude and uncorrelated*.

**This is the course's own lesson, arriving on schedule.** We claimed a null after three
independent surveys, and the null was an artifact of not knowing the field's vocabulary — the work
is indexed under *numerical reproducibility* and *stochastic arithmetic*, not under the tool names
we searched. *A search that fails and a search that finds nothing return the same empty result*,
and a search in the wrong vocabulary fails silently in exactly that way. **Three agreeing surveys
did not fix it, because they shared the vocabulary.** Session 1 gets this as a live example.

### One more thing, and it is for the syllabus rather than the toolset

**Acher, Gotlieb, Spieker & Lyan 2025**, *"Teaching Reproducibility and Embracing Variability: From
Floating-Point Experiments to Replicating Research"*
([10.1145/3736731.3746162](https://doi.org/10.1145/3736731.3746162), gold OA). Someone has already
published the pedagogy for the exact thing we are building a session around. **Read it before
writing that session.** Not yet read — ACM DL blocked automated fetching, so this is a metadata-
only sighting and the title is doing all the work in that sentence.

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
