# The four clocks

**Status: `DRAFT`, 2026-09-09.** Built from four independent facilitator run sheets plus an
adversarial cross-check. All four sessions in one file **on purpose** — four sessions running on
four different clocks is not a course, and that is exactly what the cross-check found.

> ## 🔴 PROVISIONAL, pending one decision
> These clocks assume the cuts listed under each session. **They do not solve the underlying
> problem**, which is not timing: four artifacts (a design, a chosen test, the pilot, a repository)
> are assumed by later sessions and scheduled by none. See
> [the audit](./audit-2026-09-09.md). **Sessions 2 and 3 reclaim 20–40 minutes each the moment that
> is settled**, because most of their overflow is regenerating what target rotation threw away.

---

## The house arithmetic

240 wall minutes. **Not four blocks of sixty.**

| | min |
|---|---|
| Opening | 5 |
| Two brain breaks | 10 |
| Transitions (3 × 3) | 9 |
| Overrun buffer | 10 |
| Close | 5 |
| **Content available** | **201** |

**A block that cannot be done in 50 minutes is cut or split.** And **the buffer is not a block** —
the moment you schedule work into it, it has stopped being a buffer. *(Session 2's first run sheet
did exactly that, scheduling "finish the pre-registration" into the overrun. That is a control that
cannot fail, committed on the run sheet for the session that teaches controls.)*

### ⚠ Session 4 was NOT the reference, and everyone inherited its error

Session 4 was written first and the other three were told to match it. **It does not satisfy the
house arithmetic**: six content blocks summing to **220 against 201**, with **zero minutes for
transitions and zero for overrun** — the 19 minutes the house explicitly budgets. Corrected below.

---

## Cohort cap: **8**, not 10 — and the evidence is session 4's own

`README.md` and session 4 say **ten, hard**, derived from hour 4 at five minutes per student. All
four facilitators independently arrived at **eight**, for a reason arithmetic misses:

- **Session 2** — hour 3 has every student running code against a live model API. At ~4–5 min of
  help per stuck student and a third of the room stuck, ten students is ~15 minutes of facilitator
  attention inside a 25-minute exercise.
- **Session 3** — three individual-work windows whose whole premise is *you cannot see your own
  error*, so someone else must look. At 8 you read every student's output; **at 10 you are
  sampling, in an exercise whose thesis is that sampling does not work.**
- **Session 4** — 10 × 5 min assumes zero handover between speakers. Real cap 8–9.
- **Session 3 adds: prefer an even number**, so the hour-4½ exchange pairs cleanly.

**Cap 10 hard, target 8, make it even. If you are given 10, get a second pair of hands for session
2 hour 3.**

---

## Session 1 — The question

*Needs ~211 as written. Cuts below bring it to 201.*

| clock | block | min |
|---|---|---|
| 0:00 | Opening — **plus course-level orientation** (only session 1 carries it) | 8 |
| 0:08 | **H1** — curiosity → a claim that can be wrong | 50 |
| 0:58 | **break** — "back at 1:03" | 5 |
| 1:03 | **H2** — the prediction game ⚠ *materials do not exist* | 40 |
| 1:43 | transition | 3 |
| 1:46 | **H3** — trace a number to its artifact ⚠ *materials do not exist* | 50 |
| 2:36 | **break** — post H4 pairs here | 5 |
| 2:41 | transition | 3 |
| 2:44 | **H4** — build the review loop, run it to saturation | 50 |
| 3:34 | **H4½** — the kill entry (continuous, no transition) | 11 |
| 3:45 | overrun buffer | 10 |
| 3:55 | close | 5 |

**Cuts required:** H1 −6 (fold the acceptance-test transfer into the finishability teach; debrief
5→3; analogy 6→5). H2 −5 (drop the drug-trial framing; move setup-reassignment to the break).
H4 −7 (move "what is the reachable version" to homework — it feeds `vr.bound`, assessed in session
2, not here; bound the citation trace to **exactly three citations** rather than "until one fails",
which is unbounded work inside a fixed block).

**Free improvement, no minutes:** the one-page is currently written 1–5, *then* line 5 is explained.
**Write 1–4, teach finishability, then write 5.** Line 5 stops being a guess.

⚠ **Pairs must be posted PRE-SESSION.** H1's pair exercise comes before any break, so the
"post at the previous break" rule has nothing to post at.

---

## Session 2 — Designing to fail

*Needs **247** as written — 46 over. The worst session, and the worst block is hour 4.*

| clock | block | min |
|---|---|---|
| 0:00 | Opening | 5 |
| 0:05 | **H1** — the confound that got there first | 50 |
| 0:55 | **break** — "back at 1:00" | 5 |
| 1:00 | **H2** — a control capable of failing | 42 |
| 1:42 | transition | 3 |
| 1:45 | **H3** — a test that cannot reject *(the centrepiece)* | 50 |
| 2:35 | **break** — "back at 2:40", **post H4 template here** | 5 |
| 2:40 | **H4** — pre-register, then have your agent attack it | 50 |
| 3:30 | **H4½** — the break log, and name the second kill | 10 |
| 3:40 | overrun buffer — **unspent** | 15 |
| 3:55 | close | 5 |

**Cuts required, and two are structural:**

- **H1 −15: move the design draft to pre-work.** Post the target + one-page template ~5 days out
  with *"arrive with a two-condition design."* This is a defect fix, not a time cut — **no block in
  the course ever schedules designing one**, and you cannot list what differs between conditions you
  have not written.
- **H3 — ordering defect.** The exercise says *"run your **planned test** on pure noise"*, but the
  planned test is specified in **hour 4's** pre-registration, which has not happened yet. Shrink to
  *"run a permutation null over your ordering labels and print `len(set(null))`"* — the deliverable
  is the **distinct-value count**, not a working analysis. Have the six-line skeleton written in
  advance and post it at minute 10 to anyone stuck.
- **H4 −23: the prereg is NOT completable in 50 minutes as written.** Seven bullets spanning
  `vr.prereg` 0–6, including three terms the novice audit names as the drop-out point — *estimator,
  sensitivity analysis, power.* **Power alone can eat 20 minutes** from someone who has never
  computed one. Post the template at the 2:35 break; teach only bullets 3–4 live; write the rest as
  a **skeleton**, with power reduced to two honest lines — *the smallest effect I could detect* and
  *what a null does and does not support.*

---

## Session 3 — Reading what came back

*Needs **252** as written — 51 over. Hour 2 is the single worst block in the course.*

| clock | block | min |
|---|---|---|
| 0:00 | Opening — *post orientation the night before; confirm, don't brief* | 5 |
| 0:05 | **H1** — the estimator measuring your sample size | 44 |
| 0:49 | transition | 3 |
| 0:52 | **break** — "back at 0:57" | 5 |
| 0:57 | **H2** — the statistic that is not what its name says | 50 |
| 1:47 | transition | 3 |
| 1:50 | **H3** — the hypothesis died, and that is interesting | 43 |
| 2:33 | **post the pairs** | 2 |
| 2:35 | **break** — "back at 2:43" | 5 |
| 2:43 | pairs to breakouts | 2 |
| 2:45 | **H4** — writing the limits section first *(taught)* | 30 |
| 3:15 | **H4½** — write it, hand it over, measure the gap | 30 |
| 3:45 | overrun buffer | 10 |
| 3:55 | close — **includes the third kill** | 5 |

**Cuts required:**

- **H1 −13, and (a) is a defect fix.** Replace *"list every statistic in your own analysis"* with a
  **supplied 8-statistic list, 4 safe / 4 unsafe.** A minimal option-order pilot contains 2–4
  statistics and **every one of them is a per-sample mean** — so the unsafe column stays empty for
  the whole room and the hour teaches a classifier against **zero instances.**
- **H2 −22.** The file budgets a 40-minute exercise, then puts a 10-minute opener in front and a
  22-minute "harder half" behind. It was never a 60-minute hour either. Exercise 40→30, harder half
  22→12. **Do not move the harder half into H3** — H3 is already over on its own.
- **H3** is 43–50 unbroken minutes of *telling*, remote, in hour three, right before a break — the
  session's lowest-attention stretch and its longest lecture. Convert ~6 minutes into a task.
- **Greenberg does not fit as written.** H4 was 64 minutes against 50 *before* it was added;
  Greenberg took it to 73. It fits only because H4 is split across two blocks — and 8 still comes
  out. Cut the facilitator "I did this" story: Greenberg carries the point, and the file's own
  warning (*check your own numbers before you tell it*) means the story also has a pre-session
  verification cost.
- ⚠ **The header promises three deliverables and the body budgets time for one.** The third kill
  is scheduled nowhere — it is in the close above, paid from the buffer.

---

## Session 4 — The gate, and the room *(corrected)*

*Was 220/201 with no transitions and no buffer.*

| clock | block | min |
|---|---|---|
| 0:00 | Opening | 5 |
| 0:05 | **H1** — build the gate from your own failures | 50 |
| 0:55 | **break** — "back at 1:00" | 5 |
| 1:00 | **H2** — the seeded exercise | 40 |
| 1:40 | transition | 3 |
| 1:43 | **H3** — defects that do not present as claims | 37 |
| 2:20 | **break** — **post handoff pairs here** | 5 |
| 2:25 | **H3½** — the handoff test | 20 |
| 2:45 | fix what the handoff found | 18 |
| 3:03 | transition | 3 |
| 3:06 | **H4** — the finding you will defend | 45 |
| 3:51 | overrun buffer | 4 |
| 3:55 | close | 5 |

**H4 at 45 minutes is 8 students at 5 minutes, or 9 at 5 with no handover.** This is the arithmetic
that sets the course cap — see above. Above 8, run two rooms for H4 or hold 4 minutes hard.

⚠ **`session-4:227` calls reproduction a *precondition* for hour 4, and `:228` then supplies a
fallback for when it fails. Pick one** — as written the precondition contradicts its own next
sentence.

---

## Prep — merged, deduplicated, all four sessions

**Needs a human decision or a budget:**
- **Model/API access per student, verified before the day.** Every target needs live inference —
  temperature control, repeated identical calls, multiple orderings, two judge models. Whose keys,
  what budget, what happens when a free tier throttles ten people at once. **Stated nowhere in the
  repo.**
- **Delivery platform** — named nowhere, yet the pairing rule requires "a channel or breakout per
  pair."
- **How students receive exercise files without the answer key**, which sits in the same directory.
- **A fallback dataset** for any student arriving without a pilot. Does not exist.

**Facilitator must author:**
- Session 1 H2's three claims + answers; session 1 H3's seeded claim set — **~10 distinct cases,
  not 5** (two students on one case means the second copies), each **one number, one named
  artifact, ≤2 files, traceable cold in under 18 minutes.**
- The six-line noise-run skeleton (session 2 H3), held in reserve.
- The prereg template as a fillable file + the agent-attack prompt, verbatim.
- **A glossary card**, posted not read: AUROC, confound, residualisation/FWL, permutation null,
  p-floor, alpha, estimator, power, confidence interval. *All used, none defined.*

**Every session:**
- Pairs list, pre-generated, repeater-aware, one named room per pair, facilitator takes any orphan.
  **Session 1's must be posted pre-session.**
- **Both break return times written down before you start.** You will not compute them at 0:55.
