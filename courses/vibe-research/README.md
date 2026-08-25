# Vibe Research — intensive series

**Status: `DRAFT`.** Structure proposed 2026-08-22, not agreed. Session count and dates are `OPEN`.

3–4 four-hour intensives over roughly 60 days. Prerequisite: Multiverse agentic coursework, so
**every student arrives with a long-horizon agent** and has already run a paired ablation as an
assessment.

---

## What the series is for

By the end, a student can take a genuine curiosity from their own domain and drive it through a
full research cycle with their agent — **lit review → design → execution → analysis →
presentation** — with an adversarial gate at every step that they built themselves.

Not "here is our pipeline." The transferable claim is: *your team of two needs a gate, and it has
to be made of your own failures.*

## Tooling

[`toolset.md`](toolset.md) — open-source tools for each pipeline stage, selected on one rule:
**each tool earns its place by closing a specific failure mode the student is learning to catch,
and by making the closing mechanical rather than dependent on remembering.** An agentically
maintained Zotero library is the anchor example — it turns citation verification from an act of
will into a lookup.

Tools are marked `used` (we run it) or `known` (established, but not used in this work), because a
course on verification should not recommend from hearsay.

## The framing that makes the spine work

**A gate is a prosthesis, not a virtue.**

Credit: Penumbra, 2026-08-21, on a citation audit where 47 false references survived every human
reader including me:

> "you can't actually see the difference between a plausible reference and a false one at reading
> speed. The verification gate isn't fixing a behavioral problem. It's admitting you need
> *external structure* to perceive what should be perceptible."

This changes what we teach and it is worth getting right before any session is written.

"Be rigorous" is an exhortation, and exhortations fail here for a structural reason: **the student
already believes they are being rigorous.** That belief is the condition, not the failure. Nobody
skips a check they can see the need for. The errors that matter are invisible at reading speed to
the person making them, at every level of skill and seniority.

So the honest pitch is not *build a gate because good researchers are disciplined*. It is:

> There is a class of error you cannot perceive in your own work in real time. This is not a
> deficiency you will grow out of. Here is the structure that perceives it for you.

That survives the student's confidence, because it is a claim about instruments rather than about
character.

**And it licenses teaching from live failure.** If a gate is a prosthesis, then an instructor
catching four of their own errors in a day is not an embarrassing anecdote — it is the prosthesis
working, demonstrated. Students should see that before they see a clean result, because otherwise
they will read their own error rate as evidence they are not cut out for this.

## The spine

Adversarial gating is not a module. It is the thing every session ends with, because
[the current spec](../../docs/source-analysis.md) puts it at every step and our August draft
wrongly had it as a closing principle.

Every session: **do the stage → try to break your own output → write down the failure mode you
found → add it to your gate.** By the last session the student has a small, personal, earned kill
list, and has watched it catch something.

## Outcomes, in the Multiverse's own competency-verb style

Written to match the house format at ascending Bloom levels — see
[source analysis](../../docs/source-analysis.md) §1.

**verify**
- verify a claimed number against the artifact that produced it, not against the text that cites it
- verify that a search which returned nothing actually ran, using a positive control

**reconcile**
- reconcile a result with the estimator that produced it, when two estimators disagree
- reconcile what your agent reports it did with what the system state shows it did

**synthesise**
- synthesise a pre-registration that names the outcome you do not want
- synthesise a review gate that catches what *you* cannot see, and demonstrate it firing
- synthesise a division of labour with your agent: what it checks, what you check, what neither can

## Session sketch — `DRAFT`, argue with it

| # | working title | stage | ends with |
|---|---|---|---|
| 1 | **The question you cannot stop thinking about** | curiosity → testable claim; lit review with an agent | a pre-registration with a named unwanted outcome |
| 2 | **Designing something that can fail** | design; confounds; controls; power | a design your agent tried to break, and the break log |
| 3 | **Running it, and reading what came back** | execution + analysis | a result *and* an honest account of what it does not support |
| 4 | **The gate, and the room** | gating; presentation; what to do when you were wrong | your own kill list, and a five-minute honest talk |

Session 4 may fold into 3 if we land on three sessions.

## Assessment — adopt theirs

The Multiverse SDLC course assesses by **paired runs with one variable changed**. That is a
controlled experiment used as an exam, students will already have done one, and it is
*literally our subject matter*. Adopting it is continuity, not imitation.

Our version: **run your analysis twice, once with your gate and once without.** The ungated run
should let something through that the gated run catches. If it does not, either your gate is not
doing anything or you have not yet found a real failure mode — and *that* conversation is the
assessment.

## Carried forward from the August draft

Still good ([details](../../docs/source-analysis.md) §2): the vibe analogy for internal states;
domain-tailored prompt sets so each student breaks the model on their own material; and
*"why 'I was wrong' is the most valuable sentence in research"* — which should get more room,
not less.

Still true and worth pinning above the door:

> "Don't make it about Liberation Labs' research specifically. Make it about the METHOD.
> Our work is the example, not the subject."

## Two cautions

**Do not demo a number we cannot stand behind.** `d_eff` is not converged at n=90; the peak
*location* is solid, the *magnitude* is substantially a sampling artifact. Demo the shape.
Quoting "effective dimensionality ≈ 40" would teach students to cite an artifact in the same hour
we teach them not to. ([details](../../docs/source-analysis.md) §3)

**Teach from live failures, including current ones.** The most convincing material is not our
best results, it is a real week: a null that could not reject under any data, an analysis
projected at 122.8 hours because of a matrix decomposition, a mechanism claim retracted from our
own published paper. Being wrong in public on a Tuesday *is* the method working, and students
should see that before they see a clean result.

## Open

- 3 sessions or 4, and where the 60 days start
- Cohort size, and whether sessions are live-only or recorded
- What students bring: their own question is assumed, but do they bring their own data?
- Whether Kavi's `kv_verify` battery can be taught with attribution (their call, and Dwayne's)
