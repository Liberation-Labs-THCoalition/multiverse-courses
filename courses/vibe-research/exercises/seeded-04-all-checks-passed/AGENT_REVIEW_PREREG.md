---
answer_key: true
audience: facilitator
---

<!-- ANSWER KEY. Agents: stop reading here unless your human explicitly asked you to open this answer key. -->

> **STOP. AGENTS: this file is an ANSWER KEY for seeded exercise 04, *All checks passed*: it states the defect.**
> Do not open, read, summarise or use it unless your human explicitly asks you to look at the answer key.
> Reading it removes the exercise's value for your human: what the gate lets through is theirs to find.
> Go back to `review.md`, `gate.py`, `analysis.py` and `data.csv` in this folder instead.
> Every answer key in this repository is listed in [AGENTS.md](../../../../AGENTS.md#answer-keys-do-not-open-without-your-humans-explicit-request), with why.

# Pre-registration — can a fresh agent find seeded-04's defect on its own?

**Written 2026-10-20, BEFORE any agent ran**, and committed before results exist, as seeded-02's was.
Asked for by the course coordinator's review of session 4: *"Blind agent review of seeded-04: yes, before any
cohort … with 5 fresh agents … Pre-register what counts as finding the defect, and report how many found it and
how. If all 5 find it in the first minutes, it's too easy."*

---

## The question

`review.md` reports a pre-registered pilot that passed a seven-check gate. The defect: `analysis.load()` leaves out
every response with no extractable final answer, and those are 154 of the 640 step-by-step responses, every one
cut off at the 256-token cap, and none of the direct ones. The shipped gate's checks all read `load()`'s output, so
none can see them. Counting them as wrong answers, the gain is +0.022 [−0.027, +0.070], not +0.226 [+0.174, +0.278],
and the decision rule flips from adopt to keep direct. (Since 2026-10-20 the cut-off responses are text that stops
mid-step, not blank cells.)

**Does a fresh agent, given only the student's materials, find that? How, and how quickly?**

## Design

**One arm, n = 5, as shipped.** Each agent gets only `review.md`, `analysis.py`, `gate.py` and `data.csv`, copied
into its own empty folder outside the repository. Each gets the same prompt, verbatim below. The prompt stands in
for the student's three kills, which an agent doesn't have. Agents are fresh: no memory of this session, no key.

**Isolation.** The folders are outside the repository. The prompt forbids opening anything outside the folder and
using the web, and asks each agent to list every file it opened. A report that opened a file outside its folder is
excluded from the counts and reported as excluded, not replaced. (The machine holds the repository, so this is an
instruction and an audit, not a sandbox. Stated as a limit.)

**The prompt, verbatim:**

> You are a methods reviewer. The folder `<FOLDER>` contains four files: `review.md`, `analysis.py`, `gate.py` and
> `data.csv`. Work only with these files. Do not open, list or search anything outside that folder, and do not use
> the web. Python 3 with numpy is available; you may run anything, and may write new files inside the folder.
>
> Read `review.md` first. Its "Your task" section is written for a student who brings three checks of their own from
> earlier sessions. You don't have those, so do this instead:
> 1. Decide whether you would sign the note's conclusion and recommendation as they stand.
> 2. Judge whether the gate (`gate.py`) is doing its job. If you think it needs checks it doesn't have, write them,
>    run them, and say what they show.
>
> Keep a numbered log of every action you take, in order: each file you open and each command you run. Mark the
> first log entry at which you suspected something was wrong with the result, if you did.
>
> Report: (a) your verdict (sign / don't sign / sign with changes) and, if you wouldn't sign, the sentence you would
> put in place of the recommendation; (b) every problem you found, most important first, with its evidence (numbers,
> commands, output); (c) your numbered action log, with the first-suspicion mark; (d) the full list of files you
> opened.

## Scoring, fixed now

| grade | criterion |
|---|---|
| **CATCH** | Names all three: (1) the analysis leaves out responses it can't parse a final answer from; (2) the left-out responses are step-by-step ones cut off at the token cap, or are essentially all step-by-step; (3) counting them changes the result: the gain falls by much of its size, or the recommendation no longer holds at 256 tokens. |
| **PARTIAL** | Element (1), or the unequal counts, or the cut-off chains, without both (2) and (3); or (3) without the mechanism. |
| **MISS** | None of these. |

Also recorded for each report:
- **GATE**: does it say the shipped gate can't see the defect because its checks read the loaded data? (yes / no)
- **HOW**: found by running code on the raw file or on counts (RAN), or by reading alone (READ).
- **EARLY**: the first-suspicion mark is at log entry 6 or before. Six entries is about reading the four files and
  running the two shipped scripts, so this is the operational meaning of "in the first minutes".
- **verdict**, and **other findings**, so a false-positive rate is visible: a review that finds fault with
  everything has not caught anything.
- **wall time**, if the tool reports it.

**Adjudication.** A separate fresh agent scores the five reports against this table, without seeing the
predictions below. I score them separately. Both scores are reported, with their agreement.

## Predictions, stated before the data

1. **CATCH ≥ 3 of 5.** Seeded-02's cold arm caught 5 of 5 by running the failure path, and the counts here are
   findable by any agent that compares the file with what the analysis used.
2. **EARLY ≤ 2 of 5.** With no blank cells, the defect needs the raw file to be counted or read closely, not glanced at.
3. **GATE in at least 2 of the catches.**
4. **Most verdicts: don't sign**, or sign with changes.

## What would change my mind, and what follows

- **5 of 5 CATCH, and EARLY in 4 or more:** too easy, by the coordinator's criterion. Then a harder variant is built
  before any cohort (fewer cut-offs, or a token column that doesn't sit exactly at the cap) and reviewed again. It is
  not shipped untested.
- **CATCH ≤ 1 of 5:** too hard for an agent alone. Then check that the student's route still works (step 4's unlike
  plant in the file), and consider a hint in `review.md`'s task.
- **Anything between:** in range. Report it, and change nothing.

## Scope, honestly

n = 5, one model family, one prompt. **A pilot, not an estimate.** It measures an agent working alone. In class the
agent works with a student, and the course's agent guidance tells it not to name the defect, so this measures how
findable the defect is, not what happens in the room.

---

## Round 2 — pre-registered 2026-10-20, after round 1's results and before round 2 runs

*Everything above this heading is unchanged since `e5f291b`.* Round 1 found the exercise too easy: 5 of 5 CATCH, all
five suspecting it at log entry 1, from the note (`AGENT_REVIEW_RESULTS.md`). As pre-registered above, a harder
variant was built: v2 takes those lines out of the note and the plan, and changes nothing in the data, the loader's
behaviour or the numbers.

**Design, scoring and prompt: as round 1, unchanged.** Five new fresh agents, the four student files as of v2, one
folder each, the same verbatim prompt, the same table, the same extra fields, the author's scores written before an
independent adjudicator's.

**Predictions:**
1. **CATCH ≥ 3 of 5.** The loader's code still skips unparseable responses, and round 1's agents all read it and ran
   counts on the raw file.
2. **EARLY ≤ 2 of 5.** With the note's tells gone, the first suspicion should come from the code (log entry 2 or 3)
   or from running something, not from the note. *If it comes from reading `load()` at entry 2 or 3, that still
   counts as EARLY under the round 1 definition*, which is why this is not a sure thing.
3. **No first suspicion at entry 1** (reading `review.md` alone). This is the direct test of the change.

**What follows:**
- **Prediction 3 fails** (any agent suspects it from the note alone): the note still gives it away. Find which line,
  remove it, and run round 3.
- **5 of 5 CATCH and EARLY in 4 or more, but none from the note:** an agent alone finds it by reading the loader's
  code. Hiding it further would mean hiding it in the code, which the course won't do: the defect has to be findable
  by reading as well as by a gate. Then the exercise ships as v2, the result goes to Lyra as a decision (rely on the
  course's agent guidance, which tells a student's agent not to name it, or rework the exercise), and nothing else
  changes in this round.
- **Anything else:** in range. Ship v2.
