# Tools by stage — what to reach for, and what to build instead

**Status: `DRAFT`, 2026-09-08.** The selection view of the toolset, ordered by
[the eight stages](./the-pipeline.md).

> **Two files, two questions.** This one answers *"what do I use at this stage, and what do I build
> myself?"* [`toolset.md`](./toolset.md) answers *"what will actually stop me installing it?"* —
> cost, credential, install shape, hardware. Pick here; check the barrier table there before you
> put anything in a syllabus.

---

## The finding, sharpened

The first pass said stages 1, 3 and 7 **have no tools**. True, and it undersold itself. The
accurate version:

> **Stages 1, 3 and 7 have no tool you can install. They have a check you can write.**

That is a better sentence for this course than the original, because a stage with no tooling reads
as a stage where you are on your own, and that is not what happens. What happens is that the
artifact is *yours* — a one-page, a design memo, a kill list — and the check on it is fifteen lines
you write in an afternoon. Nobody ships those as a package, because they only make sense against
your artifact.

**This is the whole course in one line, and it is the reason we do not hand out automation.** The
mechanical stages have mature tools you should absolutely use and mostly already know. The
judgment stages have checks that do not exist until you write them, and writing them is the skill.

**Legend.** `used` — we run it in the work this course draws on. `known` — established, but we have
not used it here; evaluate before adopting. **Build** — the student writes it; it is not a
download.

---

## 1 · Question — *no tool*

| | |
|---|---|
| **artifact** | the one-page: curiosity · directional claim · falsifier · stake · **stopping condition** |
| **agent can carry** | drafting variants, arguing the other side, spotting a vague predicate |
| **agent cannot carry** | whether *you* would accept the falsifier. It will accept anything you propose. |

**Build — the one-page linter.** Five required fields, and one real assertion: **line 3 (falsifier)
and line 5 (stopping condition) must name an observation, not a feeling.** A crude test that
catches most of it: does the line contain a number, a comparison, or a named artifact? "I would
stop when I am satisfied" fails. "I would stop when three more sources add nothing new" passes.

Fifteen minutes to write, and it is the first thing in the course that is *theirs*. Their partner's
read in the pair exercise is the other half — the linter catches empty, a human catches hollow.

*Why no tool exists:* a question is only well-formed relative to what you would do with the answer,
and no package knows that.

---

## 2 · Survey — the agent's best stage

| tool | status | what it closes |
|---|---|---|
| **Zotero** + **Better BibTeX** | `used` | Pinned citation keys and an auto-exported `.bib` that stays in sync. A citation with a resolvable key is checkable; one typed into a `.tex` is a claim. |
| **Zotero local API** | `used` | The agentic surface. **No key to read** — rare and cheap — but it is **off by default** (Settings ▸ Advanced) and returns `403` until switched on. The agent can fetch the stored PDF and check whether the claimed sentence is in it. |
| **OpenAlex** | `used` | Programmatic metadata at scale. **Now metered** — free key ≈ 10× the anonymous budget. |
| **Semantic Scholar API** | `used` | Keyless is a *shared* pool and routinely saturated; a key buys a private 1 RPS, not a bigger number. |
| **PubMed / E-utilities**, **ClinicalTrials.gov v2** | `used` / `known` | Domain coverage; both work keyless. |
| **unpaywall / DOI resolution** | `known` | Turns a DOI into a document you can read — the difference between verifying a citation and verifying a citation *record*. |

**Build — the review loop, with its termination clause.** A search, a log of what came back, a rule
for relevance, and **a condition under which it stops**. Four lines of scaffolding and one hard
decision. The stopping condition is **saturation**: the point where new sources stop changing the
picture. Write the number down.

> Your agent will find papers forever. That is what it is for, and it is not a flaw. It has no
> opinion about when you have enough. **Saturation is the opinion.**

---

## 3 · Design — *no tool*

| | |
|---|---|
| **artifact** | the design memo: the comparison, the controls, and what each control's failure would do |
| **agent can carry** | enumerating conditions, proposing controls, finding the confound you named |
| **agent cannot carry** | noticing that your control cannot fail. It will approve a design that must succeed. |

**Build — the null-data dry run.** Before any real data: generate data under the null, run the
*entire* analysis on it, and confirm it does **not** produce a positive. This is the single highest
-value thing a student can build in this course, and it is an afternoon.

It is also the operational definition of the stage's *done when*: **a control exists that is
capable of failing.** If your pipeline returns a result on noise, you have not built a control, you
have built a result generator — and you would have shipped it.

**Ask both questions of every control, not one:**

1. What does its **failure** do to my headline number?
2. What does its **success** do to my headline number?

We learned the second one the expensive way, four separate times, each after fixing the first. A
control whose failure is invisible is broken; a control whose success is *guaranteed* is decoration.

*Facilitator note:* two numbers that disagree are a fact; a reason they might disagree is a guess.
Watch for the student who has just explained an anomaly away in one sentence and moved on. That
sentence is a defence, not an inference, and this is the stage where it does the most damage.

---

## 4 · Pre-register — thin tools, real friction

| tool | status | what it closes |
|---|---|---|
| **OSF Preregistration** | `known` | Timestamped and immutable. The immutability *is* the feature. Read is keyless; write needs a PAT, which an agent can hold. |
| **AsPredicted** | `known` | Eight questions, right weight for a short session — **but there is no password field on the sign-in page at all.** An agent has nothing to authenticate with, and coauthor approval is a human email loop. Structurally human-in-the-path. |
| **a dated, pushed commit in your own repo** | `used` | What we actually do, and **the recommended path for a live session.** Weaker than OSF — you can rewrite history — so teach the weakness alongside it. `git tag` it and the weakness mostly closes. |

**Build — the prereg template, plus the split-sample drill.** Reproduce a result on half a randomly
split sample, commit your alternative model, *then* receive the second half. It is the cheapest
honest test of commitment-before-evidence we know of, and it fits inside one hour.
(Mechanism from Bauer et al. 2025 — see [prior art](../../docs/prior-art.md).)

**Do not make a hosted service the critical path in a four-hour class.** A magic link that lands in
a mailbox the student cannot reach from the room ends the session for them.

---

## 5 · Execute — mature tooling, use it

| tool | status | what it closes |
|---|---|---|
| **git** | `used` | Not collaboration — **dated, immutable evidence of what you believed when.** |
| **Jupyter + papermill** | `used` | Parameterised runs: the same analysis over conditions without copy-paste divergence. |
| **DVC** or **git-annex** | `known` | The artifact is versioned *alongside* the paper, so the number and the file it came from move together. |
| **Snakemake** / **Nextflow** | `known` | Declares the dependency graph, so "which step produced this file" is answerable. |
| **Docker / Apptainer** | `known` | The environment is an artifact too. |

**Build — provenance stamping.** Every output file records the commit hash and the config that
produced it. Ten lines, and it is what makes stage 6 possible at all.

**And the check that costs nothing:** `len(set(...))` on your conditions before you analyse
anything. A run that stopped early leaves an artifact **identical to a finished one** — the same
files, the same log, the same `Finished:` line, because the step that finished did finish. Count
unique values first. Read the log's *tail*, not its head.

---

## 6 · Analyse — where the tool choice does the work for you

| tool | status | what it closes |
|---|---|---|
| **pingouin** | `known` | Reports effect sizes **with confidence intervals by default**, and Hedges' *g* directly. We once headlined a *d* = 9.86 at n=3 with no CI and a ~20% small-sample inflation that lived in a commented-out caveat. A library whose default output includes the corrected statistic makes that error harder to make than to avoid. |
| **statsmodels**, **scipy.stats** | `used` | What we use. Powerful, and entirely willing to let you report an uncorrected *d* at n=3 without comment. |
| **`scipy.stats.bootstrap`** | `used` | Resampling with BCa. **Teach the trap**: refit any residualisation *inside* each replicate, or the interval comes out too narrow. |
| **jamovi** + **jmv** | `known` | GUI with a reproducible syntax trail — a real option for non-programmers. |

**Build — nothing new.** This stage is the one where the right *default* beats anything you would
write. That is itself the lesson: choosing pingouin over scipy is a methodological decision made
once, at import time, that removes a class of error permanently.

*The judgment that no library supplies:* **did the hypothesis die, or did the measurement?** Before
you residualise a discrepancy away, say out loud what it would mean if it were real.

---

## 7 · Gate — *no tool, deliberately*

| | |
|---|---|
| **artifact** | your kill list — your own failures, written as checks someone else could run |
| **host** | `pre-commit`, `pytest` — obvious homes for the checks *once they exist* |
| **agent can carry** | turning a described failure into a runnable check |
| **agent cannot carry** | knowing which failure was yours |

**We do not ship our kill list, in any session.** A kill list you are handed is a checklist. A kill
list you earned is a memory, and the entry means something because you were there when it cost you.
A student who leaves with **three of their own** has something better than our fifty-odd.

**Build — the check, and then the check on the check:**

> **Under what input does this check fail? If there is no such input, it is not a check.**

Then the inverse, which is the one that gets missed: **would this check print the same thing if the
artifact were correct and my pattern were wrong?** A broken check reports a *defect*, not an error
— it fails toward alarm, which looks like a finding and survives the glance a crash would not. Six
false alarms in one evening, all ours, the work clean every time.

*This stage is the course's reason for existing.* Brodeur et al. ran 288 researchers through
reproduction work and found that error detection was the capability that degraded — not just under
AI-led work, but measurably in the **assisted** arm too, where reproduction rates were otherwise
fine. The thing that quietly gets worse when you work with an agent is exactly this stage.

---

## 8 · Ship — under-taught, and cheap to fix

| tool | status | what it closes |
|---|---|---|
| **Quarto** | `known` | Prose and code in one document, so a number in the text is **generated rather than typed**. Kills transcription drift outright. `format: typst` gives PDF with no TeX install at all. |
| **LaTeX** + **latexmk** | `used` | The write-up rebuilds from source; `latexmk` resolves the multi-pass dance so "I forgot to rerun bibtex" stops being a class of error. |
| **`pdftotext`** (poppler) | `used` | **The highest-yield tool on this page.** It is how you check that the built artifact says what the source says. |
| **Zenodo** | `known` | A DOI and an archived copy. Read is keyless; deposit needs a token. |

**Build — the staleness hook.** Is the built PDF older than its source? One line, and it belongs in
`pre-commit` rather than in your habits. We hit that defect **five times in three days across three
people**, including a shipped paper missing six of eight rows of a results table.

*Done when a stranger can retrieve it and re-run it.* That is the definition of done for the whole
pipeline, and it currently gets one bullet in session 4. `OPEN`, and the cheapest fix is to make
the stage-8 hook the last thing every student builds.

---

## `OPEN`

- **Stage 6 has no build step.** That may be correct — it is the one stage where the library's
  default is the intervention — but it leaves session 3 lighter on construction than the others.
- **Stage 8 needs session time**, not a bullet. See above.
- **Offline / rate-limited fallbacks** for the stage-2 tools: OpenAlex is metered and Semantic
  Scholar's keyless pool is routinely saturated. A cohort of twenty hitting them at once in one
  room is a scenario nobody has tested.
