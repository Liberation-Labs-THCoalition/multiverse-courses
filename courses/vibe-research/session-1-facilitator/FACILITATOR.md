---
audience: facilitator
---

# Session 1 — facilitator notes

**Status: `DRAFT`, 2026-10-14.** These notes used to sit on the student page,
[`session-1-the-question.md`](../session-1-the-question.md), where they told students what they were
about to discover. They moved here so that the student page says only what to bring and what
they will do. Read this file alongside it.

**Who can see this file.** Its name, `FACILITATOR.md`, and its front matter, `audience:
facilitator`, each mark it as a key. `tools/build_site.py` never stages it, and
`tools/check_public_build.py` fails the build if a line unique to it turns up on the course site.
Agents helping students are told to leave `FACILITATOR.md` files alone (`AGENTS.md`). **The
repository itself is still public**, so anyone who clones it can read this file, as with the
exercise keys, until the public/private split is decided ([site spec](../../../docs/site-spec.md)).
So nothing that lives in the private facilitator pack goes in here: no claims, no cards, no
reveals.

---

## Before the session

- **The clock.** As written, session 1 needed about 211 minutes against 201
  ([the four clocks](../../../docs/session-clocks.md)). The student page took the clock's cuts on
  2026-10-14:
  - the one-page is written lines 1–4, then finishability is taught, then line 5 is written (the
    clock's "free improvement");
  - hour 2 no longer reassigns anyone to a pre-made setup (see the end of this file);
  - in hour 4, "what is the reachable version" moved to homework, and the citation trace is bounded
    to exactly three citations.

  Two cuts live only in your timing: hour 1's debrief goes from 5 minutes to 3, and the analogy
  from 6 to 5. Fold the "you already know how to do this" transfer into the finishability teach.
- **Pairs are posted before the session.** Hour 1's pair exercise comes before any break, so there
  is no earlier break to post them at. Give each pair a named room or thread, and take any orphan
  yourself ([running a session](../../../docs/running-a-session.md)).
- **Materials.** Hours 2 and 3 run from the private facilitator pack, which is kept outside this
  repository.
- **The supplied question** is the session-1 target in [the target bank](../the-target-bank.md).
  `OPEN`, and not fixed here: that page prints the answer, and it is on the public site. The
  student page no longer links to it.
- **What students bring.** The student page asks for two or three sentences on how they knew their
  agent was working. In hour 1, ask two or three people to read theirs during the finishability
  teach. It is the transfer the clock folds in there, already written.
- `OPEN`: the 8-minute opening, with its course orientation, has no written text yet.
- `OPEN`: model and API access per student (whose keys, what budget; see the prep list in the
  clocks). Until it is settled, the student page tells students not to buy anything.

## Running it online — `DRAFT`

The class meets on a video call (Livelink, with Google Meet as the fallback) with a Matrix room
alongside. *(Thomas, in a message, 2026-10-13. Not yet recorded in `session-clocks.md`, which
still lists the delivery platform as named nowhere.)*

- **Hour 2's commit-before-reveal.** Each student sends you their three verdicts and confidences
  before the first reveal. A direct message works, and its timestamp is the seal. `OPEN`: direct
  message or a form.
- **"No agent and no search" for the ninety seconds is an honour rule online.** Say so as part of
  the game, not as policing.
- **Hour 3's cards** go to each student privately at the start of each round, never posted to the
  whole room: the two tracers of a card must not see each other's notes. `OPEN`: Matrix direct
  messages or HedgeDoc notes.
- **Hour 3's piles** go on a shared board. `OPEN`: a HedgeDoc note or a Matrix thread.

## Hour 2 — the prediction game

- **How the claim set is chosen.** At least one false claim is one that was widely reported as
  true, and at least one true claim is one that sounds false. *(Changed 2026-10-14: the second
  criterion used to read "one that nobody predicted", which claims more than the sources show.)*
- **Check every key against the latest version of its primary before the session.** If a careful
  student could argue the other side from the primary, reword the claim or swap in a spare. In a
  game scored on confidence, a key that can be contested changes everyone's score.
- **Announcing the winner.** Show the winner's card next to the card with the most right answers.
  A right answer never costs more than a wrong one, so they are often the same student. When they
  are not, the two cards show why: the more accurate student was sure of something wrong, or
  unsure of things they got right. That is the conversation to have.
  - **CORRECTION, 2026-10-14.** The student page used to say, in hour 2, that the winner "will
    usually not be whoever got the most right". The arithmetic says the opposite. Three right
    answers at 72% or more total less than 0.25, the smallest possible cost of a single miss, so
    that card beats every card with a miss on it. In simulated rooms of 8 or 10 students, with
    confidences in 10-point steps and five different confidence habits, the winner was one of the
    most-right students in 79–100% of rooms, falling to about 60% only when everyone hedged at
    50–60%. Simulated, never observed.
- **`PREDICTED`**, never observed: the modal miss will be a confident *true* on the claim that was
  widely reported. **Record the confidences, not just the verdicts.** If the room is well
  calibrated from the start, the game needs harder claims, not easier ones.

## Hour 2 — the harder half

- Everyone works the supplied question, so the harder half asks whether the model access each
  student has could test their claim. If someone says *no* because they have no API access, point
  them to the local-model fallback in the target bank's `OPEN` list.
- *(Removed from the student page 2026-10-14: anyone whose data could not reach their question was
  to be "matched to a pre-made setup at the break before this hour". The setups do not exist, and
  the break came before the hour that would have shown who needed one.)*

## Hour 3 — the case cards

- **Open by saying it out loud:** every card is a real defect from published work, and most are
  still wrong where students will look first.
- **Line five of the record sheet** matters because, on more than one card, stopping one step
  early produces a confident *matches*.
- **Let the room name the piles.** They will arrive at something close to five failure modes:

  | what the room finds | the failure mode |
  |---|---|
  | the cited value is not what the artifact says | artifact **disagrees** |
  | the trail ends; there is no primary | artifact **missing** |
  | the "source" agrees because it was written from the claim | artifact **written from the claim** |
  | the number contradicts the paper's own other numbers | **arithmetically impossible** |
  | the number was corrected, but not where you read it | **superseded** |

- **The pattern that emerges**, *a plausible number is harder to doubt than an obviously missing
  one*, is the whole reason a gate exists, and it lands far better discovered than asserted. When
  you ask which cards anyone marked *matches*: those are the plausible ones, and they are the ones
  a gate is for.
- **`PREDICTED`**, never observed: the most *matches* verdicts will land on the cards where the
  printed number is faithfully copied from a source that is itself wrong. **Record which cards
  drew them.** If we are wrong about which cards fool people, the set needs a different trap.

## Hour 4 — the review, and the first kill

- **The sealed prediction comes back here** (added 2026-10-14). In job one, once the review has
  shown whether the question is already answered, students open the prediction they sealed in
  hour 2 and score it with the game's rule if the review settled the question. This replaces the
  old promise that they would "read it again in session 3", which nothing in session 3 kept, and
  which hour 4 would have answered weeks earlier anyway. Whether session 3 also comes back to it
  is `OPEN`, and is left to whoever rebuilds session 3.
- **`PREDICTED`**, never observed; this course has not run. We expect students to under-estimate
  saturation and to be startled by how early it arrives on a well-formed question. **Record what
  actually happens.** The reasoning behind the prediction is the part to trust: on a badly-formed
  question saturation never arrives, which is diagnostic rather than a failure of effort. A
  question that will not saturate is usually a topic wearing a question's clothes. Send them back
  to line two of their one-page.
- **The citation trace is bounded to three** (the clock's cut). With a bound, all three may check
  out, so the student page sends those students to the hour-3 card that fooled them, or nearly did.
- **Do not supply our kill list.** Not in this session, not in any session. **Three kills of
  their own beat fifty of anyone else's.**
- **The last question is the one to hold onto:** the same hour produced a boundary and a kill, and
  students are asked which one changed what they are going to do next.
- **`PREDICTED`:** they will report the kill, because it stung, and the answer that actually
  changed their next move will be the saturation number. Never observed. **This one is worth
  logging verbatim**, because if it is wrong the hour is structured around the wrong beat.

## Between sessions

- **The sparring prompt.** The student page gives students a prompt for their own agent, built
  from the gate-sparring spec in [`between-sessions-and-tone.md`](../../../docs/between-sessions-and-tone.md).
  `OPEN` there: who builds a hosted companion, what it runs on, and whether the school hosts it.
- **Why one record per probe** (the RoverAI house pattern): what it challenged, what the student
  answered, what survived. A record rather than a chat transcript makes the student's gate
  auditable, and makes the later comparison assessment possible.
- **Don't send students to `between-sessions-and-tone.md`.** It is an instructor planning page, and
  it carries entries from our own kill list, which this course does not hand to students.

## Pre-made research setups — `OPEN`, needs building

Moved from the student page 2026-10-14. They were meant for students without a question, or whose
question their data could not reach. Since the question became supplied (Thomas, 2026-09-08),
session 1 does not need them. `OPEN`: whether they are needed at all, or only for the carried
pipeline proposed in [`delivery-model.md`](../../../docs/delivery-model.md).

If they are built, each needs a real dataset, a genuine open question, and at least one seeded
defect so the tracing exercise works on it, drawn from **external, published** work (Thomas,
2026-09-24: external examples first; the repo is public). Defect types worth finding external
examples of:

- an effect size at small n, where the corrected and uncorrected values differ materially
- a metric with a name collision: the same word meaning two different formulas
- a depth-profile claim where the location is robust and the magnitude is a sampling artifact
