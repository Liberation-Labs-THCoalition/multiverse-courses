# The pipeline — eight stages, named once

**Status: `DRAFT`, 2026-09-08.** The canonical decomposition. Everything else in this repo —
sessions, standards, toolset — should point here rather than re-cutting it.

---

## Why this file exists

The course is *about* building a research pipeline. Until today the repo contained **three
different decompositions of it and no canonical one**:

| where | segments |
|---|---|
| `standards/vibe-research/` | question · design · execution-and-analysis · gate (4) |
| the four sessions | the question · designing to fail · reading what came back · the gate (4) |
| `toolset.md` section headings | lit review · pre-registration · analysis · data-and-provenance · execution-and-reproducibility · gating (6) |

None of them reconciled, and the tool table contained Quarto, LaTeX and Zenodo — **write-up and
deposit tooling for a stage that appeared in none of the three.** You cannot select "one tool per
stage" against a stage list that does not exist.

---

## The eight stages

| # | stage | the move | done when |
|---|---|---|---|
| 1 | **Question** | curiosity → a claim with a direction, a falsifier, and a stopping condition | the one-page is written, including line five |
| 2 | **Survey** | find out whether it is answered, what the reachable version is, and where saturation lands | new sources stop changing the picture |
| 3 | **Design** | the comparison, the controls, the thing that would refute you | a control exists that is *capable* of failing |
| 4 | **Pre-register** | lock the analysis, including the outcome you do not want | it is timestamped somewhere you cannot edit |
| 5 | **Execute** | run it, capture provenance as you go | the artifact records what produced it |
| 6 | **Analyse** | read what came back, separate dead hypothesis from broken measurement | the limits section is written |
| 7 | **Gate** | check it with something that can fail | the gate fires on a known-bad input |
| 8 | **Ship** | write it, deposit it, make it reachable by someone who is not you | a stranger can retrieve it and re-run it |

---

## The observation that should shape the tools list

Map every tool in `toolset.md` onto that table and a pattern falls out immediately:

| stage | tools |
|---|---|
| 1 Question | **none** |
| 2 Survey | Zotero, Better BibTeX, Zotero API, OpenAlex, Semantic Scholar, PubMed, ClinicalTrials.gov |
| 3 Design | **none** |
| 4 Pre-register | OSF, AsPredicted |
| 5 Execute | Jupyter + papermill, git, DVC, git-annex |
| 6 Analyse | numpy, scipy, statsmodels, pingouin, jamovi |
| 7 Gate | **none — ours is bespoke** |
| 8 Ship | Quarto, LaTeX, Zenodo |

**Stages 1, 3 and 7 have no tools.** They are the judgment stages — and they are exactly the
stages that decide whether the other five were worth doing.

That is not a gap in the tool list. It is the shape of the work, and it is worth saying out loud
in session 1:

> **Your agent is strongest where the work is mechanical and weakest where it is decisive.**
> Survey, execute, analyse and ship are the stages it can carry almost alone. Question, design
> and gate are the stages where it will confidently produce something plausible and you are the
> only one who can tell.

This is also why the prerequisite matters. Students arrive able to automate stages 2, 5, 6 and 8 —
that is what the agentic coursework taught them. **This course is about 1, 3 and 7.**

---

## Mapping to what already exists

**Sessions** cover the stages unevenly on purpose — four sessions, eight stages:

| session | stages |
|---|---|
| 1 — the question | **1**, **2** |
| 2 — designing to fail | **3**, **4** |
| 3 — reading what came back | **5**, **6** |
| 4 — the gate, and the room | **7**, **8** |

Two stages per session, and each session pairs one judgment stage with one mechanical one. That
was not designed; it fell out of the mapping, and it is a good enough reason to keep the
four-session shape.

**Standards** should be re-tagged against this list. Current courses (`question`, `design`,
`execution`, `gate`) collapse eight stages into four folders, which is fine as a *course*
grouping but should not be mistaken for the pipeline. `vr.bound` belongs to stage 1;
`vr.verify-number` spans 2 and 5.

---

## `OPEN`

- **Re-tag `toolset.md` by stage.** It is currently organised by tool with stage names appearing
  as incidental headings. One table, stage-ordered, is the more useful artifact — and it makes
  the three empty rows visible, which is the point.
- **Stage 8 is under-taught.** We have tools for it and no session hour. "A stranger can retrieve
  it and re-run it" is the definition of done for the whole pipeline, and it is currently one
  bullet in session 4.
- **Should stage 4 (pre-register) exist for a four-hour session?** AsPredicted needs an email
  magic-link and coauthor approval; OSF needs a token. Both are friction inside a live class.
  Possible answer: a timestamped commit to their own repo is a legitimate pre-registration and
  costs nothing — worth saying explicitly rather than treating the hosted services as the only
  option.
