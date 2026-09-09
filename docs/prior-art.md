# Prior art — what else teaches this, and what we take from it

**Status: `DRAFT`, 2026-09-08.** A scan for comparable courses, run by a Fable subagent at
Thomas's request, then curated and partly re-verified here.

---

## How to read this file

**This is an agent scan, and it is labelled as one.** The subagent kept a verification key and it
is preserved below, because a prior-art file that launders search results into settled fact is the
exact failure this course teaches students to catch.

- **`READ`** — the page or PDF was fetched and read.
- **`SNIPPET`** — known only from a search result. Details unconfirmed. Do not cite.
- **`LYRA-VERIFIED`** — I went to the primary myself and checked the specific numbers quoted.

Two things worth recording about the scan itself, because they *are* course material:

1. The subagent's summariser **invented a "three conditions" list** for the Brodeur PDF. The agent
   caught it, went to the saved PDF, and reported the primary instead. That is the loop we teach,
   performed unprompted by a subagent, and it belongs in session 3.
2. My own follow-up search returned a summary saying both arms reproduced at **91%**. The primary
   says **94% vs. 91%**. The snippet was the loose one. *Two numbers that disagree are a fact; a
   reason they might is a guess.*

---

## The headline, stated at its true strength

**One scan, run across several phrasings, found no semester-length course that teaches research
*methodology* with a long-horizon agent as working partner.** The nearest things are a one-week
residential institute and a three-day seminar, neither with a supplied problem and neither
assessing anything.

**That is a bounded claim about a search, not a fact about the world.** A search that fails and a
search that finds nothing return the same empty result. What it licenses: we are not duplicating
an existing course, and we should stop looking for one to copy wholesale. What it does not
license: any "first of its kind" language in public materials.

---

## What we take, in priority order

### 1. Brodeur et al. 2026 — the empirical justification for the whole course

`LYRA-VERIFIED` · PNAS 123(22) e2524747123 · OA PDF: <https://eprints.whiterose.ac.uk/id/eprint/241548/>

A three-arm RCT: **288 researchers, 103 teams**, reproducing published social-science results
under human-only, AI-assisted (ChatGPT as collaborator), and AI-led (minimal human oversight).

| arm | reproduced | major errors found |
|---|---|---|
| human-only | **94%** (31/33) | **1.70** |
| AI-assisted | **91%** | **0.74** |
| AI-led | **37%** (13/35) | **0.23** |

Human-only vs. the other two on major errors: **P = 0.006 and P < 0.001**. The paper's own summary
line is that AI assistance had "no measurable advantages and was associated with **reduced
detection of major errors**."

**Why this is the citation that matters.** The capability that degrades first — and degrades even
in the *assisted* arm, where reproduction rates held up fine — is **error detection**. That is not
a side finding for us; it is the entire subject of sessions 3 and 4.

> **Scope, corrected 2026-09-09 after audit.** Brodeur establishes the **problem statement**, not
> our pedagogy. They tested no training, no gates, and no intervention of any kind. What is
> supported: *error detection degrades when you work with an agent, measurably, even when the work
> otherwise looks fine.* What is **not** supported: that a student-built gate restores it. That is
> our claim and it is currently untested. Citing Brodeur for the remedy is amplification — one of
> the three mechanisms [Greenberg names](../courses/vibe-research/session-3-reading-what-came-back.md),
> which we teach one session earlier.

> There is a **correction** to this paper, [10.1073/pnas.2621051123](https://doi.org/10.1073/pnas.2621051123),
> July 2026. I checked it: **affiliation only**, three authors, production error. **No finding,
> figure, table or conclusion changed.** Recorded because the next person should not have to
> re-derive that, and because citing a corrected paper without having read the correction is a
> defect we have shipped before.

### 2. Bauer et al. 2025 — grade the rigour, never the outcome

`READ` · *Teaching of Psychology* 52(1):117–123 · OA: <https://madoc.bib.uni-mannheim.de/66489/> ·
companion + syllabus: <https://osf.io/g3k5t/>

Three mechanisms, all directly usable:

- **A portfolio of prescreened targets the instructor has already run.** Their stated rationale —
  supervision load, fairness of difficulty, and no dead ends for the students least equipped to
  absorb one — is **independent published support for the target bank**, arrived at from a
  different direction. They also record the honest counterpoint: self-selected targets produce
  more ownership and motivation. We are trading that away deliberately, and now we can say who
  else made the same trade and why.
- **"Grading should not be influenced by replication success."** Grade rigour, documentation and
  literature knowledge. This belongs in `FACILITATOR.md` for every seeded exercise — a student
  whose careful work produces a null has met the standard completely.
- **Split-sample pre-registration** (their cite: Blincoe & Buchert 2020): reproduce a result, then
  commit to an alternative model *before* being handed the second half of a randomly split sample.
  Cheap, bounded, and it is the nearest published mechanism to assessing **commitment before
  evidence** — which is stage 4 of our pipeline and currently the hardest thing we assess.

### 3. The EPA ladder, inverted — `READ`, and the best structural fit found

Entrustable Professional Activities (ten Cate; medical education) ·
<https://www.ncbi.nlm.nih.gov/books/NBK619385/>

The unit of assessment is a **task**, not a trait, and the grade is a **supervision level**:
observe only → direct supervision → indirect supervision → distant supervision → ready to
supervise others. Competence is level 4 *on that specific task*.

**The inversion is the idea.** Our course's real graduation question is not what the student can do
unsupervised. It is:

> **Which pipeline stages may this student now entrust to their agent unsupervised, and which
> never?**

That is an entrustment decision in exactly ten Cate's sense, pointed the other way — and it lands
on the eight stages we just made canonical. Drafted as the entrustment ladder in
[the pipeline](../courses/vibe-research/the-pipeline.md).

### 4. Vilhuber et al. 2022 — the QA structure, and a thing we already built

`READ` · *J. Stat. & Data Science Education* 30(3) · <https://arxiv.org/abs/2204.01540>

The AEA Data Editor's replication lab runs ~50 undergraduates a year against real
conditionally-accepted manuscripts. **~14 hours of onboarding plus three graded synthetic test
cases with known planted defects before any student touches live work**, then a tiered review chain
(student → experienced-undergraduate pre-approver → Data Editor).

**We independently built the first half of this.** `seeded-01-the-approved-analysis` and
`seeded-02-the-fix-that-broke-it` are exactly graded synthetic cases with planted defects. That is
convergence rather than borrowing, and it is worth knowing that the largest operating instance of
this pedagogy made the same call.

**What we have not built is the tiered review**, and with one facilitator over four sessions we
probably cannot. The cheap version is peer pre-approval: no artifact counts until a second student
has signed it off. Costs one exchange, and it is the structure Berkeley's Stat 159 gets for free by
submitting all homework as pull requests with **graded peer code review** (`READ`,
<https://stat159.berkeley.edu/fall-2025/overview/syllabus>).

### 5. Smaller takes, worth one line each

- **CASBS/Stanford AIMS** (`READ`) — their five-role taxonomy of AI in research is a clean way to
  open session 1: *what is the agent, in this loop, right now?*
- **Agents4Science** (`READ`) — mandatory disclosure of AI involvement, review prompts published.
  **Make the agent's role log a graded deliverable**, not an afterthought. Already half of
  `vr.bound` objective 2.
- **Calling Bullshit** (`READ`) — the one concrete exercise on their public syllabus is a
  week-long **diary of encounters**. That is the live-logged version of our kill list, same shape
  as `vr.bound` objective 2, which is reassuring about that objective.
- **Apart Research sprints** (`READ`) — the same three-layer funnel as the Multiverse
  (sprint → fellowship), running at scale, and they **release the bounded problem materials about a
  week early**. Cheap to copy, and it protects class time.
- **CURE literature** (`SNIPPET`) — five criteria for course-based research. Overlaps our target
  eligibility list; worth a look when the bank grows, not before.
- **CREP** (`READ`) and **I4R Replication Games** (`READ`) — curated target pools with external
  sign-off. The Replication Games shape (pre-read, one day, same-day written report) is close to a
  drop-in if we ever want a fifth session.

---

## The negatives, and what to do with each

| the scan found no… | our position |
|---|---|
| semester-length agent-partnered methodology course | Do not copy; do not claim primacy either. |
| course that assesses **knowing when to stop** | `vr.bound` may be genuinely new. Hold that lightly — it is one scan. It does mean nobody has debugged this for us, so the standard needs its own scrutiny rather than a reference implementation. |
| curriculum teaching statistics via error-hunting tools (statcheck, GRIM) | An opportunity we are **not** taking this cycle. Recorded so it stops resurfacing as a fresh idea. |
| course running **ablation-as-exam** | Brodeur proves the design works as a *measurement instrument*. Using it as an *assessment* would be novel — and is a bigger swing than a four-session prerequisite should take. Park it; it is accelerator-shaped. |

`OPEN` — **ReplicationWiki's "Replication in teaching" portal returned HTTP 500** during the scan.
It is the natural directory for this category and it was never read. Recheck before treating this
scan as saturated.
