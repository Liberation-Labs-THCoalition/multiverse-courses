# Session 1 — The question you cannot stop thinking about

**Status: `DRAFT`, 2026-08-24.** Four hours. First of four.
**Standards covered:** `vr.formulate`, `vr.verify-number`, and the lit-review standard from
[Course: Question](../../standards/vibe-research/README.md).

**Decided (Thomas, 2026-08-24):** four sessions over ~60 days, *not padded* — if the content fits
in three we ship three. Students bring their own question; **a set of pre-made research setups is
provided** for those who arrive without one.

---

## What students walk in with

An agent. Agent Design and Agentic SDLC are prerequisites, so every learner already has a
long-horizon agent, has run a paired ablation as an assessment, and has been through the weekly
welfare meetup. **Session one does not set anything up.** It starts with the work.

## What they walk out with

1. One claim from their own domain that could come out the other way
2. A verified citation trail — or an explicit, written admission that one number has no primary
3. **Their first kill entry**, earned in hour four rather than handed to them

---

## Hour 1 — From curiosity to a claim that can be wrong

Covers `vr.formulate` objectives 0–3.

**The vibe analogy** (carried from the August draft, still the best opener we have): you read a
room instantly — tense meeting, awkward party — without parsing every conversation. You detect the
*shape*. Models have internal states and we can read them the same way.

**Then the work.** Each student writes, in this order, on one page:

- the curiosity, one sentence, in their own domain
- the claim, with a **direction** — not "X relates to Y" but "X increases Y"
- what observation would **falsify** it
- **what they are hoping for**, named as a stake rather than a prediction

That fourth line is the one people skip and it is the one that matters. A stake you have written
down can be audited. A stake you have not is just a thumb on the scale.

**Pair exercise:** swap pages. Your partner's job is to find the claim that cannot fail. Most first
drafts have one.

## Hour 2 — The prediction game, which is pre-registration in miniature

Covers `vr.formulate` 4–5.

Three surprising claims about model behaviour. Everyone writes down which they think are true
*before* the reveal. **That is pre-registration**, done in ninety seconds, and the point is that
it costs nothing and changes everything about how the reveal lands.

**Why "I was wrong" is the most valuable sentence in research.** The file-drawer problem, the drug
trial framing. Our own example, and it should be a live one rather than a polished one: *we
predicted preference training would worsen calibration; the data said the opposite, and the
falsification was more useful than the confirmation would have been.*

**Then the harder half:** each student identifies a **cheaper question that would have to be
answered first**, and states whether their available data can address their claim at all. A good
fraction will discover it can't. That discovery is a session-one success, not a failure — and it
is what the pre-made setups are for.

## Hour 3 — Trace a number to its artifact

Covers `vr.verify-number` 0–6. **This is the centrepiece and it is entirely hands-on.**

Each student receives a short claim and a pointer to the artifact behind it, and traces it.
The set is seeded so that the three failure modes each appear:

| seeded case | what the student should discover |
|---|---|
| artifact **disagrees** | the cited value isn't what the file says |
| artifact **missing** | the trail ends; there is no primary |
| artifact **written from the claim** | the "source" agrees because it was generated from the text |
| value outside its own **confidence interval** | arithmetically impossible, and visible |
| a **stale caveat** | the caveat's numbers were superseded by a later correction to the text it caveats |

Every one of these is drawn from a real defect in our own published work in the last fortnight.
That is the point. **Nothing in this hour is hypothetical, and the instructor should say so.**

Compare across the room afterward. The pattern that emerges — *a plausible number is harder to
doubt than an obviously missing one* — is the whole reason a gate exists, and it lands far better
discovered than asserted.

## Hour 4 — Lit review with the agent, and your first kill

Covers the lit-review standard.

Students run a literature review with their own agent on their own question. Then:

**Find one citation your agent gave you that you cannot verify.** Not "might be wrong" — one you
traced and could not confirm. There will be one. There is essentially always one.

Then the move that makes the course work:

1. Write down what happened, with the artifact that revealed it
2. Generalise it from an instance to a **class** — name the class
3. Write it as a check someone else could apply without your context

**That is their first kill entry, and they earned it in the first four hours.** A kill list you're
handed is a checklist. A kill list you earned is a memory — the entry means something because you
were there when it cost you.

*Instructor note:* do not supply our kill list. Not in this session, not in any session. A student
who leaves with **three kills of their own** has something better than our fifty-seven.

---

## Between sessions

Students work their question with their agent, against the **gate-sparring companion** (spec in
[`../../docs/between-sessions-and-tone.md`](../../docs/between-sessions-and-tone.md)): it attacks
claims, asks what would change your mind, and **never supplies a failure-mode name.** The student
writes the entry.

Per the RoverAI house pattern, the companion should emit **a record per probe** — what it
challenged, what the student answered, what survived — not a chat transcript. That makes the
student's gate auditable and the later ablation assessment possible.

**Homework:** three sources for your question, each either verified to a primary or explicitly
marked *unverifiable, and why*. The second category is a passing answer.

## Pre-made research setups — `OPEN`, needs building

For students without a question, or whose question their data can't reach. Each needs: a real
dataset, a genuine open question, and **at least one seeded defect** so the tracing exercise works
on it. Candidates worth drafting from our own corpus, since the defects are already documented:

- an effect size at small n, where the corrected and uncorrected values differ materially
- a metric with a name collision — the same word meaning two different formulas
- a depth-profile claim where the location is robust and the magnitude is a sampling artifact

## Open

- Cohort size, and whether sessions are recorded
- Whether hour 3's seeded claim set is drawn from our papers verbatim (attribution + our own
  comfort) or paraphrased
- Where the 60 days start
- Baba Yaga's two extra riddle types — now a **PR to the campus repo** rather than a request,
  per Thomas 2026-08-24; still Liz's to accept
