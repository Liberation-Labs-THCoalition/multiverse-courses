# Tools by stage — what to reach for, and what to build instead

**Status: `DRAFT`, 2026-09-08.** The selection view of the toolset, ordered by
[the eight stages](./the-pipeline.md).

> **Two files, two questions.** This one answers *"what do I use at this stage, and what do I build
> myself?"* [`toolset.md`](./toolset.md) answers *"what will actually stop me installing it?"* —
> cost, credential, install shape, hardware. Pick here; check the barrier table there before you
> put anything in a syllabus.

---

## The finding, corrected twice

**First pass:** stages 1, 3 and 7 *have no tools*.
**Second pass:** they have *no tool you can install, but a check you can write*.
**Both were wrong**, and the way they were wrong is worth more to this course than the claim was.

What actually happened: I mapped `toolset.md` — a list assembled for **our** pipeline, by us, for
our work — found three empty rows, and reported that as a fact about the field. It is a fact about
our list. There is a large, mature literature on question formation, experimental design and
adversarial review, most of it older than any of us, some of it packaged as software.

> **An absence in your own inventory is not an absence in the world.** The gap you find by reading
> your own notes is a gap in your notes.

That is now the honest version, and it changes what the course teaches at these three stages. Not
*"you are on your own here, go build something"* — which would have sent students to reinvent
`DeclareDesign` badly, exactly as I did. Instead:

> **These stages have methods, and the methods are old. What they do not have is anything that
> will make the judgment for you.** A design package will tell you your design's properties; it
> will not tell you the comparison was the wrong one. A question framework will tell you your
> question is unfalsifiable; it will not tell you it is boring.

**The mechanical stages have tools that do the work. The judgment stages have tools that structure
the judgment and then hand it back to you.** That distinction survives contact with the literature,
which the previous one did not.

*What follows is verified — primary sources checked, and the places I got it wrong left visible.*

**Legend.** `used` — we run it in the work this course draws on. `known` — established, but we have
not used it here; evaluate before adopting. **Build** — the student writes it; it is not a
download.

---

## 1 · Question

| | |
|---|---|
| **artifact** | the one-page: curiosity · directional claim · falsifier · stake · **stopping condition** |
| **agent can carry** | drafting variants, arguing the other side, spotting a vague predicate, surfacing candidate connections at scale |
| **agent cannot carry** | whether *you* would accept the falsifier — it will accept anything you propose — and, per below, it cannot problematize |

### Methods, and they are not new

| method | what it does |
|---|---|
| **FINER** (Cummings, Browner & Hulley, ch. 2 of Hulley et al., *Designing Clinical Research*, **4th ed. 2013, p. 17**; in print since 1988) | Feasible · Interesting · Novel · Ethical · Relevant. It **intersects** our one-page rather than containing it: *Interesting* ≈ curiosity, *Relevant* ≈ stake. It adds two we omit (*Novel*, *Ethical*) plus a feasibility bundle — subjects, expertise, cost, scope, fundability. **It has no falsifier and no stopping condition.** Its "confirms, refutes, or extends" is about refuting *the literature*, not naming what would kill your own claim; its cost/scope bullets are pre-study resource bounds, not a stopping rule. **FINER asks whether the study should exist; our one-page asks what would make you drop it.** |
| **PICO / PICOT** | Population · Intervention · Comparison · Outcome (· Time). **Prompts** you to name the comparison — it does not force anything, and the *C* is explicitly optional in the original ("the comparison intervention or exposure, *if relevant*"). Worth teaching anyway, because the omission is measured: Huang et al. found **2 of 59** clinical questions carried all four elements, and *C* is the routinely empty slot. |
| **Problematization** (Alvesson & Sandberg 2011, *AMR* 36(2):247–271; Sandberg & Alvesson 2011, *Organization* 18:23–44) | A published method for generating questions by identifying and **challenging an assumption the literature shares**. Five assumption types to interrogate: in-house, root metaphor, paradigm, ideology, field. |
| **Strong inference** (Platt 1964, *Science*) | Multiple competing hypotheses, then design the experiment that *excludes* some. Question and design in one move. |

### The one that is about agents

Alvesson & Sandberg's whole argument is a contrast between **gap-spotting** — finding what the
literature has not covered — and **problematization** — challenging what it assumes. They observe
that gap-spotting dominates, and that it reliably produces uninteresting questions.

> **Gap-spotting is an agent's native mode.** Ask an agent *"what's missing in this literature?"*
> and it will answer, forever, fluently, and mostly with questions nobody needed answered. It is
> extremely good at the operation that produces boring research.

Problematization requires holding a position about what the field takes for granted — which is a
stance, not a retrieval. Your agent can *help you test* an assumption once you have named it. It
will not name one for you, because naming one means disagreeing with the corpus it learned from.

### Tools, which do exist

| tool | what it does |
|---|---|
| **Literature-based discovery** (Swanson's ABC, 1986) | A–B known in one literature, B–C in another, A–C never tested. This is *"a string of things that seem connected"* formalised. **Open** discovery: given A, find candidate Cs. **Closed**: given a known A–C, find the B that explains it. Swanson's fish-oil/Raynaud's link came out of abstracts alone. |
| **Citation-graph mapping** — Connected Papers, Litmaps, Inciteful, VOSviewer, CiteSpace | Renders the structural holes visible. You look at a map and see the sparse region between two dense clusters. Cheapest possible version of the above, and browser-based. |
| **OpenAlex + embeddings** | Roll your own LBD. Genuinely buildable in a session, and the students already have the skills. |

**The honest caveat, and it is good teaching material:** LBD is a *candidate generator*. Most of
what it emits is junk. It relocates the judgment rather than removing it — which is a more
interesting thing to teach than "no tools exist," and it is the same shape as every other stage.

**Still build the one-page linter.** Five required fields, one real assertion: **the falsifier and
the stopping condition must name an observation, not a feeling.** Crude test that catches most of
it — does the line contain a number, a comparison, or a named artifact? *"I would stop when I am
satisfied"* fails. *"I would stop when three more sources add nothing new"* passes. It is fifteen
minutes and it is downstream of a method now, rather than a substitute for one.

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

## 3 · Design — the most mature of the three, and the one I called empty

| | |
|---|---|
| **artifact** | the design memo: the comparison, the controls, and what each control's failure would do |
| **agent can carry** | enumerating conditions, proposing controls, finding the confound you named, running the diagnosis |
| **agent cannot carry** | noticing that your control cannot fail. It will approve a design that must succeed. |

### Tools, and there are good ones

| tool | what it does |
|---|---|
| **DeclareDesign** (R) | Declare a design as a code object under **MIDA** — Model, Inquiry, Data strategy, Answer strategy — then `diagnose_design()` **simulates it and reports its statistical properties before you run it**. Companions: `randomizr` (assignment), `fabricatr` ("imagining your data before you collect it"), `DesignLibrary` (templates). Covers observational and experimental, causal and descriptive. |
| **dagitty** (browser **and** R, free, no account, runs offline from a downloaded zip), **dowhy** (Python) | Draw the causal structure and it computes minimal sufficient adjustment sets — **and shows you what adjusting for would break.** Biasing paths turn red; force adjustment on a descendant of the exposure and it reports that no valid set exists. Collider bias becomes mechanical. **The authors' own limit, which matters more in a room than anywhere else: it is mechanical *given your DAG*. Whether the collider is in the diagram at all is still something you have to have thought of.** |
| **Design analysis** (Gelman & Carlin) | Type **S** (sign) and Type **M** (magnitude) errors instead of plain power. Far more useful at small *n*: it tells you that *conditional on reaching significance*, an underpowered study's effect size is inflated — so a huge *d* from a tiny sample is evidence of low power, not of a huge effect. |
| **Specification-curve / multiverse analysis** (Steegen et al. 2016; Simonsohn et al.) — `specr`, `multiverse` (R) | Enumerate every defensible analytic choice and report the whole distribution. The formalisation of researcher degrees of freedom. |
| **Classical DOE** (Box, Hunter & Hunter) — `pyDOE3`, `statsmodels` | Factorial, fractional factorial, blocking, confounding structure, resolution. |
| **Power** — G\*Power, `statsmodels.stats.power`, `pingouin.power_*` | Sample size at design time rather than as a post-hoc apology. |

> **A correction worth keeping in the syllabus.** The first version of this file told students to
> **build a null-data dry run** — generate data under the null, run the whole analysis, confirm it
> does not produce a positive — and called it the highest-value thing they could build here.
>
> That is `diagnose_design()`, with less rigour, ten years late. I proposed it having declared the
> stage tool-less *without checking*. The exercise is still worth doing deliberately if you are
> staying in Python and want to feel the mechanism in your hands — but **do it knowing you are
> reimplementing a known thing, not inventing one.** That distinction is most of what separates
> learning from wasted evenings, and it is a distinction your agent will never draw for you,
> because it will happily help you build either.

**The stage's *done when* is unchanged: a control exists that is capable of failing.** If your
pipeline returns a result on noise, you have not built a control, you have built a result
generator — and you would have shipped it.

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
| **pingouin** | `known`, **installed 2026-09-08** (0.6.1) — demo-able, but not used in the work this course draws on | Reports effect sizes **with confidence intervals by default**, and Hedges' *g* directly. Cohen's *d* at small *n* is upward-biased by roughly `1 − 3/(4df−1)`; at *n* = 3 that is about 20%, and a bare *d* with no interval hides both the bias and the width. A library whose default output includes the corrected statistic and its CI makes that error **harder to make than to avoid** — which is a better safeguard than remembering. |
| **statsmodels**, **scipy.stats** | `used` | What we use. Powerful, and entirely willing to let you report an uncorrected *d* at n=3 without comment. |
| **`scipy.stats.bootstrap`** | `used` | Resampling with BCa. **Teach the trap**: refit any residualisation *inside* each replicate, or the interval comes out too narrow. |
| **jamovi** + **jmv** | `known` | GUI with a reproducible syntax trail — a real option for non-programmers. |

**Build — nothing new.** This stage is the one where the right *default* beats anything you would
write. That is itself the lesson: choosing pingouin over scipy is a methodological decision made
once, at import time, that removes a class of error permanently.

*The judgment that no library supplies:* **did the hypothesis die, or did the measurement?** Before
you residualise a discrepancy away, say out loud what it would mean if it were real.

---

## 7 · Gate — methods aplenty; the kill list is still yours

| | |
|---|---|
| **artifact** | your kill list — your own failures, written as checks someone else could run |
| **host** | `pre-commit`, `pytest` — obvious homes for the checks *once they exist* |
| **agent can carry** | turning a described failure into a runnable check; running the mechanical detectors |
| **agent cannot carry** | knowing which failure was yours |

### Methods

| method | what it gives you |
|---|---|
| **Severe testing** (Mayo, *Statistical Inference as Severe Testing*, 2018) | A claim passes only if it survived a test it would **probably have failed had the claim been false**. This is the principled statement of our own rule below — same idea, better formulation, with a literature behind it. |
| **Adversarial collaboration** (Kahneman; Mellers, Hertwig & Kahneman 2001) | Two parties who disagree design the test *together* and pre-commit to what each outcome means. The formal protocol for what we do informally. |
| **Pre-mortem** (Klein, *HBR* 2007) | Assume it already failed; explain why. Fifteen minutes, no tooling, and it belongs in **session 2**, not here. |
| **Many-analysts** (Silberzahn et al. 2018) | Same data, 29 teams, divergent results. The cheap classroom version is two students, one dataset. |

### The Red Team Challenge, and its numbers

Lakens & Tiokhin ran a **paid red team** on a submission-ready manuscript in 2020. Five reviewers,
three weeks, $200 each, plus a donation per issue on a severity tier set by a **neutral arbiter**
(Ruben Arslan): **$100** major · **$20** minor-computational-reproducibility · **$10** minor.

> **107 reports submitted → 18 unique critical issues → 5 major.** Final donation: $660.

Two things to steal, and the second is the one students need:

1. **The arbiter is a distinct role.** Neither the author nor the red team decides what counts.
   In a classroom that is a third student, and it costs nothing.
2. **107 → 5.** That is the yield of a real adversarial pass, published, by careful people. Tell
   students this *before* their first review, because otherwise the first false alarm reads as a
   finding and the tenth reads as despair. **Most of what an adversarial pass produces does not
   survive arbitration, and that is the process working, not failing.**

*Facilitator note:* we have hit this ratio from the inside more than once — an evening's worth of
findings, every one of them an instrument fault, the work clean throughout. Tell that story here if
the room needs it; the published number above carries the point on its own for anyone reading this
asynchronously.

### Mechanical detectors

**statcheck** — recomputes a reported *p*-value from the reported test statistic **and df**, and
flags mismatches. Handles *t, F, r, z, χ², Q* only, and only in APA style. Canonical implementation
is an R package (Nuijten & Epskamp), **but there is a free zero-install web app at `statcheck.io`
that takes PDF/DOCX/HTML**, plus an unofficial Python port on PyPI that lags the R release.
*(Corrected 2026-09-09 — this row said "R" flatly, which for a Python cohort means "skip it." It is
a browser tool in thirty seconds.)* It checks **internal consistency only** — never whether the
analysis was right. Then **GRIM** and **GRIMMER**
(whether a reported mean/SD is arithmetically possible for the stated *n*), **SPRITE**
(reconstructs plausible raw distributions). Free, fast, and — per the prior-art scan — **no
published curriculum teaches with them**, which is an opening rather than a curiosity.

> **GRIM is the build exercise for this stage, and it is the best one in the course.**
> **`used` — upgraded 2026-09-09. We ran it over our own published corpus before recommending it,
> and it found a real defect on the first pass.**
>
> *`kv-cloak-defense-paper` reports **7%** confabulation in a table captioned **"50 prompts per
> model."** At n=50 only even percentages are reachable — 7% would need 3.5 confabulations. The
> paper's own body says `n=7` and "50–100 prompts each", so the data was right and **the caption's
> N was wrong**; it shipped in three files. The neighbouring rows (12%, 26%) are reachable at 50,
> which is exactly why nothing ever looked odd.*
>
> That is the argument for this exercise, and we did not have to borrow anyone else's example.
>
> It is **fifteen lines of arithmetic** with no
> dependencies: if *N* observations are integers their total is an integer, so the mean can only be
> one of *N* values. A reported mean that is not the rounded form of any of them **cannot exist**,
> whatever the data was. No statistics, no *p*-value, no judgement call.
>
> A student writes it in an hour, and walks out owning a working error detector they can point at
> real published papers. That is the entire philosophy of this course in one exercise: **they build
> the instrument, then use it on something real.**
>
> Teach the limits in the same hour, because they are where the thinking is. GRIM applies **only**
> to integer-valued measures, and it goes blind once *N* ≥ 10^decimals — at two decimals it has no
> power above *N* = 100. An inconsistency says the reported *set* cannot co-exist; it does not say
> **which** number is wrong, and it is not evidence of misconduct.
>
> **Why it lands:** Brown & Heathers tested 71 eligible articles and found that **about half (36)
> contained at least one impossible mean**, with 16 carrying multiple. A student who has just
> written the detector themselves, and then reads that number, has understood something about
> published literature that no lecture delivers.
>
> Brown & Heathers 2017, *SPPS* 8(4):363–369, [doi:10.1177/1948550616673876](https://doi.org/10.1177/1948550616673876).
> **Free preprint:** <https://peerj.com/preprints/2064/> — send students this one, not the paywall.
> Check their implementations against [`rsprite2::GRIM_test`](https://lukaswallrich.github.io/rsprite2/reference/GRIM_test.html).
>
> Facilitator reference implementation (do **not** distribute): `tools/grim_reference.py`.

### And the kill list is still yours

**No course ships you one, this one included.** A kill list you are handed is a checklist. A kill
list you earned is a memory, and the entry means something because you were there when it cost you.
**Three of your own beat fifty of anyone else's.** The methods above tell you how to *run* a gate;
only your own failures tell you what to put in it.

**Build — the check, and then the check on the check:**

> **Under what input does this check fail? If there is no such input, it is not a check.**

Then the inverse, which is the one that gets missed: **would this check print the same thing if the
artifact were correct and my pattern were wrong?** A broken check reports a *defect*, not an error
— **it fails toward alarm.** That is the dangerous direction, because an alarm looks like a finding
and survives the glance a crash would never survive. A check that crashes gets fixed in a minute; a
check that cries wolf gets believed.

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
`pre-commit` rather than in your habits. This is among the most common defects in any
build-a-document workflow, and among the least visible: the PDF opens, it looks finished, and the
table in it is two revisions old. Nothing about a stale artifact announces itself.

*Done when a stranger can retrieve it and re-run it.* That is the definition of done for the whole
pipeline — and it is the one condition **you cannot assess yourself**. Every other stage you can
check alone; this one is a fact about a reader.

**Taught as [session 4, hour 3½ — the handoff test](./session-4-the-gate-and-the-room.md):** repos
swapped, twenty minutes, no talking, reproduce the other student's headline number from the repo
alone. Whatever stops them is the defect list. Then build the two permanent fixes — provenance
stamping and the staleness hook — and present a finding somebody else has actually obtained.

---

## Sources

Verified 2026-09-08 against primaries, not summaries. Where a search summary and the primary
disagreed, the primary is what is written above — the Red Team numbers reconcile only from the
source (a summary gave "18 critical" and "5 major / $660" as if they were the same figure; they are
different tiers of the same tally).

- Alvesson & Sandberg 2011, *AMR* 36(2):247–271 · Sandberg & Alvesson 2011, *Organization* 18:23–44
- Swanson 1986, literature-based discovery (fish oil / Raynaud's)
- DeclareDesign — <https://declaredesign.org/> · CRAN · Blair, Coppock, Humphreys, *APSR*
- Lakens & Tiokhin, Red Team Challenge 2020 — <https://www.the100.ci/2020/07/01/red-team-part-3/>
- Mayo 2018, *Statistical Inference as Severe Testing*
- Steegen et al. 2016 (multiverse) · Gelman & Carlin (Type S/M) · Platt 1964 (strong inference)
- Klein 2007 (pre-mortem) · Silberzahn et al. 2018 (many analysts)
- Brodeur et al. 2026, *PNAS* 123(22) — see [prior art](../../docs/prior-art.md)

**`SNIPPET` list cleared 2026-09-09.** All five were checked against primaries, and **the debt was
not cosmetic — two of the five were wrong:**

| source | verdict | what changed |
|---|---|---|
| **FINER** | **WRONG** | "superset of our one-page" was false *in both directions* — FINER has no falsifier and no stopping condition, and adds two criteria we lack. Rewritten as an intersection. |
| **Acher et al.** | **WRONG** | Not paywalled; gold OA, ten pages, now read. The pedagogy sentence we asserted is contradicted by the text. → [source analysis](../../docs/source-analysis.md) |
| **statcheck** | stretched | "R" was the load-bearing error for a Python cohort — there is a free zero-install web app. |
| **PICO/PICOT** | stretched | "Forces" fails; the *C* is optional in the original. The omission claim survives and is now measured. |
| **dagitty** | **supported** | Every checkable assertion held. Added the authors' own limit: mechanical *given your DAG*. |

*A `SNIPPET` flag is not a formality. Two of five named-from-memory claims did not survive contact
with the source, and one of them was load-bearing in a session.*

---

## `OPEN`

- **We should actually adopt two of these before teaching them.** `DeclareDesign` is R and our
  stack is Python — either accept the R dependency for one session or find the honest Python
  equivalent. `dagitty` runs in a browser and costs nothing, so that one is close to free.
- **Run `statcheck`/`GRIM` over our own corpus before recommending them.** Recommending a detector
  we have never pointed at ourselves is exactly the `known`/`used` distinction this repo exists to
  respect.
- **Stage 6 has no build step.** That may be correct — it is the one stage where the library's
  default is the intervention — but it leaves session 3 lighter on construction than the others.
- ~~**Stage 8 needs session time**, not a bullet.~~ **RESOLVED 2026-09-08** — hour 3½, the handoff
  test. Twenty minutes, taken from hour 3.
- **Offline / rate-limited fallbacks** for the stage-2 tools: OpenAlex is metered and Semantic
  Scholar's keyless pool is routinely saturated. A cohort of twenty hitting them at once in one
  room is a scenario nobody has tested.
