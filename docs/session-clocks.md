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

## Cohort size: **target 8, hard cap 10**

**This is the one place the number lives;** other pages link here. An earlier derivation of "ten,
hard" from session 4 hour 4 at five minutes per student did not add up (10 × 5 = 50 minutes, in a
45-minute hour). All four facilitators independently arrived at **eight**, for a reason arithmetic
misses:

- **Session 2** — hour 3 has every student running code against a live model API. At ~4–5 min of
  help per stuck student and a third of the room stuck, ten students is ~15 minutes of facilitator
  attention inside a 25-minute exercise.
- **Session 3** — three individual-work windows whose whole premise is *you cannot see your own
  error*, so someone else must look. At 8 you read every student's output; **at 10 you are
  sampling, in an exercise whose thesis is that sampling does not work.**
- **Session 4** — 10 × 5 min assumes zero handover between speakers. Real cap 8–9.
- **Session 3 adds: prefer an even number**, so hour 4's hand-over pairs cleanly.

**Cap 10 hard, target 8, make it even. If you are given 10, get a second pair of hands for session
2 hour 3, and run session 4's hour 4 as two rooms or hold each talk to four minutes.**

---

## Session 1 — The question

*Needs ~211 as written. Cuts below bring it to 201.*

| clock | block | min |
|---|---|---|
| 0:00 | Opening — **plus course-level orientation** (only session 1 carries it) | 8 |
| 0:08 | **H1** — curiosity → a claim that can be wrong | 50 |
| 0:58 | **break** — "back at 1:03" | 5 |
| 1:03 | **H2** — the prediction game *materials: facilitator pack (private), 2026-09-29* | 40 |
| 1:43 | transition | 3 |
| 1:46 | **H3** — trace a number to its artifact *materials: facilitator pack (private), 2026-09-29* | 50 |
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

*Re-timed 2026-10-15 from the page as it stands: **200 against 201**, counting each hour at the
length its heading states. On 2026-09-09 it needed **247**, 46 over. Three fixes since then (hour 3
rewritten 2026-09-29, hour 1's design draft moved to pre-work 2026-09-30, hour 4's template and
skeleton 2026-10-14) and one `PROPOSED` cut on 2026-10-15 closed the gap. Not piloted: every number
here is a prediction.*

| clock | block | min |
|---|---|---|
| 0:00 | Opening — hour 1 pairs already posted | 5 |
| 0:05 | **H1** — the confound that got there first | 50 |
| 0:55 | **break** — "back at 1:00" | 5 |
| 1:00 | transition | 3 |
| 1:03 | **H2** — a control capable of failing | 42 |
| 1:45 | transition | 3 |
| 1:48 | **H3** — a test that cannot reject *(the centrepiece)* | 50 |
| 2:38 | **break** — "back at 2:43", **post H4 template here** | 5 |
| 2:43 | transition | 3 |
| 2:46 | **H4** — pre-register, then have your agent attack it | 48 |
| 3:34 | **H4½** — the break log, and name the second kill (continuous, no transition) | 10 |
| 3:44 | overrun buffer — 10, plus the one spare minute | 11 |
| 3:55 | close | 5 |

**Where the 200 comes from.** Line numbers are
[`session-2-designing-to-fail.md`](../courses/vibe-research/session-2-designing-to-fail.md) as of
2026-10-15. Each hour's heading states its length, and each block inside it states its own.

| block | heading says | line | its blocks | they add to |
|---|---|---|---|---|
| H1 | 50 | :54–55 | 3 + 8 + 6 + 6 + 5 + 17 + 5 (:62–110) | 50 |
| H2 | 42 | :123 | 4 + 8 + 8 + 4 + 8 + 10 (:132–168) | 42 |
| H3 | 50 | :184 | 5 + 12 + 8 + 15 + 7 + 3 (:194–224) | 50 |
| H4 | 48 | :241 | 12 + 13 + 23 (:260, :265, :282) | 48 |
| H4½ | 10 | :241, :320 | 10 | 10 |
| **total** | **200** | | | **200** |

Before the 2026-10-15 cut, the same count gave **202 by headings** (hour 4 at 50 = 12 + 15 + 23), one
over, and 197 by blocks.

- ~~`OPEN`: hour 1's heading says 50 and its blocks add to 45.~~ **Resolved 2026-10-15 (Lyra, from the
  private pack's clock):** the other 5 minutes are a scheduled read-out, each student reading out their
  top-ranked difference. Hour 1 keeps 50, and the session is 200. The read-out is now on the student
  page too, so the page's blocks add to 50.
- **The table that stood here on 2026-09-09 did not meet the house arithmetic either:** one
  transition, a 15-minute buffer, and 202 content minutes. It is replaced above.
- **The 247 is only partly traceable.** The two cuts named below account for 38 of its 46 minutes
  (15 + 23). The run sheet that gave the other 8 is not in this repository.

**Cuts, and where each stands:**

- **H1 −15: move the design draft to pre-work. APPLIED in two halves.** The hour stopped drafting a
  design when it was rewritten on 2026-09-30: it now opens with *"Bring the two-condition design you
  drafted as pre-work"* (:60), and its last block (17 min, :94) works on that draft. But until
  2026-10-15 no page told a student to draft one. Session 1's homework asks for two other things
  (`session-1:325–331`), and session 2 had no pre-work section. **`PROPOSED` 2026-10-15:** a *Before
  session 2* section (:18–37) asks for four lines (the claim, the two conditions, the items, the
  measurement), says not to run anything yet, and posts the hour 1 pairs in advance. The four lines
  stand in for the one-page template, which was never written. **Still `OPEN`:** which target the
  design is for, which waits on whether targets rotate within a cohort's arc, and who posts it, and
  where, about five days out. It is still a defect fix rather than a time cut: without the pre-work,
  hour 1's last block has nothing to work on, and drafting in the room takes the 15 minutes back.
- **H3 — ordering defect: FIXED 2026-09-29.** The old exercise ran a "planned test" that hour 4
  had not yet specified. The rewritten hour has students write a one-line *expected* test and build
  two small synthetic datasets for it (one that should make it reject, one that should not), so
  nothing depends on hour 4. It fits 50 minutes (5 + 12 + 8 + 15 + 7 + 3). **This doc must not state
  seeded-01's specific check**: session 4 depends on students discovering it.
- **H4 −23: the prereg is NOT completable in 50 minutes as written. APPLIED 2026-10-14.** Seven bullets spanning
  `vr.prereg` 0–6, including three terms the novice audit names as the drop-out point — *estimator,
  sensitivity analysis, power.* **Power alone can eat 20 minutes** from someone who has never
  computed one. Post the template at the second break; teach only bullets 3–4 live; write the rest as
  a **skeleton**, with power reduced to two honest lines — *the smallest effect I could detect* and
  *what a null does and does not support.* On the page: template at the break (:256), bullets 3–4
  taught live (:260), skeleton (:265), power in two lines (:275). That brought hour 4 to 50
  (12 + 15 + 23).
- **H4 −2: sensitivity analyses to homework. `PROPOSED`, applied 2026-10-15.** The 15-minute
  skeleton still covered five template sections, and two of them, sensitivity analysis and power,
  are the drop-out terms above, for students who arrive with **no statistics** (the prerequisites
  teach none; see the course README). Sensitivity analyses (`vr.prereg` objective 4) now come after
  the attack, as homework, before the pilot runs (:251, :340; template section 5). They are still
  committed before any real data, and the break log's checks give a student something concrete to
  start from. The skeleton keeps the test, the decision rule, power and the non-goal, in **13
  minutes** (:265–278). **Moved, not deleted.** Power stays in the room because the believe branch
  depends on it. If 13 minutes proves tight in a pilot, move the power arithmetic next, into the
  attack, which already asks the agent for it (:301). Don't move the believe branch.

**Still `OPEN` for session 2:**

- ~~Hour 1's five unassigned minutes~~: resolved (above). They are the read-out.
- **Hour 1 pairs must be posted pre-session**, as in session 1: hour 1 pairs up before any break.
  The page now says so (:37); *where* it is posted is open, as it is for session 1.
- **The believe step.** The page's own Open list wants a third synthetic dataset in hour 3: the claim
  true, at the effect you expect and the sample you plan. One spare minute does not pay for it, so it
  still needs a cut somewhere first.

---

## Session 3 — Reading what came back

> **Superseded 2026-10-14.** Session 3 was rebuilt, and its clock now lives on
> [its own page](../courses/vibe-research/session-3-reading-what-came-back.md#the-clock): 201 minutes of
> content in 240, not yet piloted. The plan below is the old one, kept for the record.

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
- ~~The six-line noise-run skeleton (session 2 H3), held in reserve.~~ **Superseded 2026-09-29:**
  hour 3 no longer has a noise run; students build their own two datasets with their agent.
- ~~The prereg template as a fillable file + the agent-attack prompt, verbatim.~~ **Done 2026-10-14:**
  [`templates/preregistration.md`](../courses/vibe-research/templates/preregistration.md); the prompt is
  in session 2, hour 4. Not yet piloted.
- **A glossary card**, posted not read: AUROC, confound, residualisation/FWL, permutation null,
  p-floor, alpha, estimator, power, confidence interval. *All used, none defined.*

**Every session:**
- Pairs list, pre-generated, repeater-aware, one named room per pair, facilitator takes any orphan.
  **Session 1's must be posted pre-session.**
- **Both break return times written down before you start.** You will not compute them at 0:55.
