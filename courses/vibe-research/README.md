# Vibe Research — intensive series

**Status: `DRAFT`.** Structure proposed 2026-08-22. **Session count SETTLED at 4** (Thomas, 2026-08-25) — *"stick with 4 until someone says otherwise."* Dates still `OPEN`.

**Names are ours to propose.** Liz has creative latitude over the campus. To save them time, we present finished names rather than options, and they change whatever they like. Everything below is a proposal, not a claim.

**Four** four-hour intensives, **fortnightly**, ≈ 56 days per cohort. Prerequisite: Multiverse agentic coursework, so
**every student arrives with an agent of their own.** We do **not** assume they have run a paired ablation: the school's
agent classes no longer include one, and Liz judged it too much to expect and likely to intimidate people (2026-10-13).
What else the prerequisite guarantees is `OPEN` until we have read the school's current curriculum.

---

## What the series is for

By the end, a student can take a curiosity — supplied here, their own in the accelerator — and drive it through a
full research cycle with their agent — **lit review → design → execution → analysis →
presentation** — with an adversarial gate at every step that they built themselves.

Not "here is our pipeline." The transferable claim is: *your team of two needs a gate, and it has
to be made of your own failures.*

## Running one

[`docs/running-a-session.md`](../../docs/running-a-session.md) — **the clock, the breaks, and the
pairing mechanics.** 240 minutes is not four blocks of sixty; a realistic "hour" here is **50
minutes** once you account for two brain breaks, transitions, and pairing. Also the rule that saves
the most dead air: **never ask a remote room to pair up — pre-assign and post the list at the
previous break.**

`DRAFT` — all four sessions have a per-block clock in [the four clocks](../../docs/session-clocks.md)
(2026-09-09, provisional). Session 1's page took its cuts on 2026-10-14. Sessions 2 and 3 still run
over (247 and 252 minutes against 201) until theirs are applied.

## Tooling

[`the-pipeline.md`](the-pipeline.md) — **the eight stages, named once.** Everything else points
here. Also carries **the entrustment ladder**: which stages a graduate may hand to their agent
unsupervised, and which three they never may.

[`tools-by-stage.md`](tools-by-stage.md) — **the selection view.** What to reach for at each of the
eight stages, the methods behind them, and what the student builds themselves. The distinction that
shapes the course lives here: *the mechanical stages have tools that do the work; the judgment
stages have tools that structure the judgment and hand it back to you.* It also carries a corrected
claim — we twice reported stages 1, 3 and 7 as having **no tools**, which was a fact about our
inventory, not about the field.

[`toolset.md`](toolset.md) — **the procurement view**: cost, credential, install shape, hardware.
Tools selected on one rule:
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
| 3 | **[Running it, and reading what came back](session-3-reading-what-came-back.md)** | execution + analysis | a result *and* an honest account of what it does not support |
| 4 | **[The gate, and the room](session-4-the-gate-and-the-room.md)** | gating; presentation; what to do when you were wrong | your own kill list, and a five-minute honest talk |

**Four sessions, not three.** The gap between *running it* and *the gate* is where the course actually lives — folding 4 into 3 would compress the two things students cannot get anywhere else (what a result does not support, and what to do when you were wrong) into a coda on an analysis session. They are the subject, not the wrap-up.

**Seeded material:** `exercises/seeded-01-the-approved-analysis/` — a confidently-approved analysis containing one fatal, findable defect. Synthetic reconstruction of a real gate failure in our own lab; runs in 40 minutes on numpy alone.

> ⚠ **Spoiler discipline.** The defect used to be described here in full. **It is a discovery exercise, and this is a student-reachable file** — the answer now lives only in that directory's `FACILITATOR.md`. Do not restate it in any file a student can open. Same rule for `seeded-02` and for the target bank's reveals; see [the audit](../../docs/audit-2026-09-09.md).

## Assessment — one comparison, predicted first

~~The Multiverse SDLC course assesses by paired runs with one variable changed … students will already have done
one … Adopting it is continuity, not imitation.~~ **Superseded 2026-10-13:** the school's agent classes no longer
include a paired ablation, and Liz judged it too much to expect and likely to intimidate people.

Keep the idea and drop the exam. Comparing two runs that differ in one thing is the heart of a test worth running, so
the course still teaches it, as something students learn here rather than something they must already know or
perform cold:

- **Predict first.** Before anything runs, the student writes down what they expect to change and what they expect
  to stay the same.
- **The agent runs both.** Same task, one thing changed: an analysis with the gate and without it (session 4), or two
  analysis choices on the same data (session 3). The mechanics are the agent's job.
- **Grade the prediction and the explanation, not the run.** Did they say beforehand what should differ, and can
  they explain what did? If the ungated run lets nothing through that the gated run catches, either the gate is not
  doing anything or they have not yet found a real failure mode, and *that* conversation is the assessment.
- **The first one is done together in class**, start to finish, before anyone does one alone. `OPEN`: which
  session's clock it goes in (session 2 hour 3, or the start of session 3).
- On student-facing pages it is a *comparison*, never an *ablation*.

If Liz would rather drop it entirely, session 4 still has the kill list and the talk, and session 3 has its
limits-first exercise. `OPEN`, Liz's call.

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

- ~~3 sessions or 4, and where the 60 days start~~ — **RESOLVED 2026-09-09 (Thomas).** Four, and the clock starts at the cohort's session 1. **Rolling cohorts:** a cohort runs 1→2→3→4 together, **fortnightly** (≈56 days, which is the "roughly 60"), and **each session is a formal prerequisite for the next** — nobody joins mid-arc. New cohort after; graduates may repeat the whole arc. *(An earlier line here read "3–4 … over roughly 60 days" while the status line above said `SETTLED at 4` — a claim that was simultaneously SETTLED and OPEN in one file, which is exactly what the marking scheme exists to prevent. Found by audit.)*
- **`OPEN`, needs Liz:** does fortnightly fit the wider school schedule?
- Cohort size, and whether sessions are live-only or recorded. **Ten students is the hard cap** — set by session 4 hour 4 at five minutes per student; see [the clock](./session-4-the-gate-and-the-room.md).
- ~~What students bring: their own question is assumed~~ — **RESOLVED 2026-09-08 (Thomas): the question is SUPPLIED.** Own questions are an accelerator requirement, not this course's. Rationale: this course teaches holding the tools on something basic, and a personal project invites burning class time defending it. See [the target bank](./the-target-bank.md).
- Whether Kavi's `kv_verify` battery can be taught with attribution (their call, and Dwayne's)
