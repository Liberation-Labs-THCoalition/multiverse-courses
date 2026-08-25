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

## Lit review — `vr.verify-number`, and the citation standard

| tool | status | failure mode it closes |
|---|---|---|
| **Zotero** + **Better BibTeX** | `known` | A citation with a stable key that resolves to a record is checkable. A citation typed into a `.tex` by hand is a claim. Better BibTeX gives you pinned citation keys and an auto-exported `.bib` that stays in sync with the library. |
| **Zotero Web API / local API** | `known` | This is the piece that makes it *agentic*: the agent can add, tag, deduplicate and — critically — **fetch the stored PDF and check whether the claimed sentence is in it**. |
| **OpenAlex**, **Semantic Scholar API**, **PubMed** | `used` | Programmatic metadata and abstracts; our own Research Runner sits on these. Resolves "does this paper exist" before "does it say what I claimed." |
| **`unpaywall` / DOI resolution** | `known` | Turns a DOI into a document you can actually read, which is the difference between verifying a citation and verifying a citation *record*. |

**Why this matters more than convenience.** Two of our own defects this fortnight were citations
to sources that did not contain the values attributed to them, and one was a **fully fabricated
reference** (Vera's find: a study attributed to a real researcher, at an institution that does not
exist). A library where every entry has an attached document and a resolvable key does not prevent
that — but it makes the check a lookup instead of an act of will.

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
