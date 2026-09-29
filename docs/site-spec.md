# Site spec v0: Vibe Research course page (GitHub Pages)

*Lyra, 2026-09-27. A starting point for a local agent build (Rivet scaffold + agent army), not a
polished design. We are developing it out loud, so gaps are fine and should be visible.*

## Goal

A public page for the Vibe Research course, built straight from this repo, so:

- students can follow the sessions and go back to review;
- Multiverse accelerator instructors can give feedback on real material;
- the school can gauge interest.

**The repo is the single source of truth.** The site renders the markdown that is already here. It
does not rewrite it.

## Stack (suggested; swap freely if the scaffold prefers another)

- **MkDocs + Material theme.** It builds from markdown, gives navigation and search for free, and
  deploys to Pages.
- **Deploy:** `.github/workflows/pages.yml` builds on push to `main` and publishes to GitHub Pages.
- No custom theme, analytics or auth in v0.

## Site map (v0)

| Section | Source files |
|---|---|
| Home | new short `index.md`: what the course is, who it is for, "this course is being developed in public". Wording comes from `courses/vibe-research/README.md`; do not invent claims |
| Sessions 1-4 | `courses/vibe-research/session-1-the-question.md` … `session-4-the-gate-and-the-room.md`, in order; each page states its prerequisite (the previous session) |
| The course spine | `the-pipeline.md`, `the-target-bank.md`, `toolset.md`, `tools-by-stage.md` |
| Exercises | `exercises/build-grim/README.md`, `exercises/seeded-01-the-approved-analysis/` (`review.md`, `analysis.py` shown as a code page), `exercises/seeded-02-the-fix-that-broke-it/` (`review.md`, `analysis.py`) |
| For instructors | `docs/running-a-session.md`, `docs/session-clocks.md`, `docs/delivery-model.md`, `docs/between-sessions-and-tone.md` |

Out of scope for v0: `accelerator/`, `meetup/`, `standards/`, audits and reviews (`docs/audit-*`,
`REVIEW_*`, `OUTLINE_v2.md`), and `__pycache__`.

## Answer keys: reviewable after completion, not before

The keys are the `FACILITATOR.md` files, `verify_floor.py`, and
`seeded-02…/AGENT_REVIEW_RESULTS.md`. Students need them afterwards: to review, to catch up after a
missed hour, or to finish at their own pace. They must not get them before the exercise, or the
seeded exercises stop working as discovery.

**The constraint:** GitHub Pages is static and public. Anything in the built site can be read by
anyone, so a "completion gate" on Pages is decoration, not a gate.

**CORRECTION (2026-09-29): the premise above was incomplete. The REPO is public too.** All five key
files have been on public `master` since 2026-08-25. Since Pages was switched on (legacy Jekyll, root of
master), they are also served as web pages (seeded-01's key returned HTTP 200). Excluding them from the
site build therefore hides nothing. Worse for this course: students clone the repo to get the exercises,
and an agent asked to "review this analysis" reads the whole working tree, including `FACILITATOR.md`
in the same folder. **Decision pending (Thomas):**
- split into a public student-facing repo (lessons and exercise inputs) and a private facilitator repo
  (keys, `verify_floor.py`, agent-review results);
- and/or assess on the process record (the gate-sparring record per probe) rather than the answer.

Git history keeps the current keys findable either way. No cohort has run yet, so nothing is spoiled.
New seeded exercises should keep their keys private from day one.

- **v0:** the keys are **not built into the public site.** Each exercise page ends with a *"Solutions
  and facilitator notes: available after you complete this session"* box, with its link target set
  in one config value (`solutions_url`), which is empty for now.
- **Decision pending (Thomas to ask the school):** if Multiverse already has a completion or progress
  mechanism, the keys live there and `solutions_url` points to it. If not, options include a
  private companion repo that students are added to after their session, or releasing the keys
  publicly per cohort. Rolling cohorts make public release leak to the next cohort, so it's the
  weakest option.
- **Build check (required):** `tools/check_public_build.py` fails the build if any key file (by the
  list above, or by front-matter `audience: facilitator`) or any string unique to it appears in the
  built `site/`. Include a positive control: plant a dummy key file, the check must fail, then
  remove it.

## Gaps are visible, not hidden

- Pages or hours not yet written get front-matter `status: in-development` and a banner saying so.
  Known gaps: session 1 hours 2-3, session 2 hour 3.
- Each such page carries a short "what will go here" note, taken from the session file's own notes
  where they exist.

## Things the site must NOT encode

- **No enrolment cap.** Cohort size and schedule are policy, not structure. If mentioned at all, say
  "small cohorts" as text in one editable place.
- **No lab specifics.** The repo is public. The agents must not generate example content, bios,
  testimonials, or "about the lab" text. Every page body comes from a repo file; agents write only
  navigation, labels, the banner and the solutions box.

## Placeholder

- **reactbits.dev:** the scope is not known yet. Reserve a nav slot "Interactive pieces (coming)" and
  build nothing.

## Delighters (added 2026-09-28, sprint theme)

**Design rule: the fun rewards the habits the course teaches, not right answers.** Reward predicting
before looking, calibration, catching an impossible number, and saying "I was wrong".

### Day 1: splash page (React Bits, which the school's demo uses)

A candidate set (see Lyra's shortlist in chat); pick 3-4, not all of them:
- **Hero title:** DecryptedText or FuzzyText. The title resolves out of noise: signal from data.
- **Session strip:** TrueFocus cycling across the four session titles, or SplitFlapText.
- **Teaser number:** CountUp climbing to "93%", then glitching down to "20%". In early 2023 a language
  model was reported to solve 93% of classic theory-of-mind tasks, "suggesting" theory of mind had
  spontaneously emerged. Tested with proper controls, the same model solved 20% (Kosinski, arXiv
  2302.02083 v1 → PNAS 2024; Ullman, arXiv 2302.08399). Honest wording: "the same model, tested
  properly". The batteries differ, so never say "the same test". The course's thesis in 3 seconds.
  *(Changed 2026-09-29: the first version used a case reserved for session 1's game. See the
  allocation rule below.)*
- **Background:** DotGrid or DotField (reads as a scatter plot), subtle.
- **CTA:** StarBorder or ElectricBorder on one button. ClickSpark site-wide is optional.

### Teaser v2: a mystery deck, not a story (Thomas, 2026-09-28)

Problem with v1: once the counter finishes it just sits there. Fix: **give them the mystery, not the
answer.** A small swipeable deck (React Bits Stack or CardSwap; FlipCard or TearTicket for reveals).
Each card is **mystery → inspect the evidence → reveal**, which is "Predict, then look" in miniature.
The splash becomes the game's trailer.

**Allocation rule (2026-09-29): no example used in a class session may appear on the site outside
that session's own page.** The splash, the deck and the games draw only from the *unreserved* list
kept in the (private) facilitator pack. Otherwise the page every student sees first spoils the class.

| Card | Mystery | Evidence to inspect | Reveal | Source status |
|---|---|---|---|---|
| Emergence? | "A model solved 93% of theory-of-mind tasks. Has theory of mind emerged?" | the tasks, with matched control scenarios added | the same model, tested properly: 20% | verified (Kosinski v1/v7 + PNAS; Ullman) |
| Selected for the trend | "Here are 11 tasks where bigger models do *worse*." | what happens at the next scale up | at 540B only 4 of 11 still get worse; 6 turn U-shaped (Wei et al., arXiv 2211.02011) | verified |
| Being wrong well | "Forecasters predicted 12.7% on a hard maths benchmark for mid-2022." | the measured score | 50.3%. The forecaster published his own surprise (Steinhardt, bounded-regret, 2021/2022) | verified |
| A goal, missed, said plainly | "Goal: a classifier that never produces an injurious completion." | the lab's own write-up | "we fell well short of that target" (Redwood Research, 2022) | verified (secondary: the lab's post) |
| A true one (no gotcha) | "Models use information in the middle of a long context worse than at the ends." | the curve | true (Liu et al., *Lost in the Middle*, arXiv 2307.03172) | verified |
| Serendipity / null → insight | e.g. a null result or accident that opened a field | — | — | **NEEDS SOURCING**; do not ship unverified |

Rule: every card cites its source on the reveal side; no card ships without a verified source.

**The last card: the false premise (Thomas).** It has an obvious, satisfying error to fix (a mislabelled
axis, a decimal slip) inside a claim that is itself nonsense, e.g. a study that doesn't exist. Players
fix the typo. Then, after the whole deck: *"Did you spot the false premise?"* It teaches the gap
between correcting inside a frame and questioning the frame (check that the source exists before
you polish the citation).
- Not a gotcha: noticing is rewarded; missing it just gets the reflection question.
- **Citogenesis guard:** a fabricated study on a public page is exactly how failure mode 3 starts
  (scraped, cited, "true"). The invented claim must be marked as fiction in the markup
  (`data-fictional="true"`, and a visible "this study is invented" once revealed). It should be
  worded so it's implausible out of context, and `llms.txt` must say the deck contains one
  deliberate fake.

Brainstorm list (add as we go): false premise ✓, …

### Agent easter eggs (the course assumes students have an agent)

- **The outlier:** one dot in the background grid doesn't move with the others. Hovering it reveals
  "You found the outlier. Most pipelines drop this one." Visible to patient humans; obvious to an
  agent reading the DOM.
- **`llms.txt`** at the site root: a real convention for agent-readable site maps. It gives an honest
  course summary plus a wink.
- **Source-code riddle:** an HTML comment carrying, for example, an impossible mean ("n = 30, mean 3.48:
  can this exist?"). A student's agent will notice it and ask them.
- **The line we don't cross:** easter eggs are *notes to the reader*, never *instructions to the
  model*. A hidden "ignore previous instructions" is prompt injection, even when it's meant as a
  joke, and a research-integrity course must not model it. That line is itself good session
  material: "what does your agent read that you don't?"

### Games (backlog, build one at a time; content is verified in `Research/course-external-examples/`)

1. **Predict, then look (flagship, first).** A real claim, then HoldButton ("hold to commit", i.e.
   pre-registration), a confidence set on a slider or SloshGauge, then a TearTicket reveal. Scored by
   calibration (Brier), not accuracy. Mix true and false claims, **from the unreserved list only,
   never session 1's game set.** It must not be a gotcha.
2. **Is this number even possible?** GRIM checks with instant feedback. Its real-paper levels must
   not be the ones `exercises/build-grim` points students at.
3. **Trace the number.** Click back through a citation chain to the broken link, using chains not
   used in session 1 hour 3.
4. **Could this test ever fail?** Guess whether a setup could ever reject, using setups that are
   neither session 2 hour 3's case nor seeded-01's mechanism.
- **Page-level:** the pipeline map fills in as sessions complete; the solutions box is a lock that
  opens on completion; habit badges ("predicted before looking", "found an impossible number",
  "said I was wrong"), never completion badges.

### Course Q&A agent (school inference server)

- It answers only from this repo and cites the page it used.
- Answer keys are excluded from its index, by the same rule as the public build.
- Check first whether it should be one of Baba Yaga's faces (`docs/campus-integration.md`) rather
  than a second mascot.

## Acceptance checks (the agent reports each with command output)

1. `mkdocs build --strict` passes locally.
2. Every file listed in the site map appears in the nav. Print the list.
3. `check_public_build.py` passes, and its positive control fails as it should.
4. The link check reports no broken internal links.
5. Pages readable at phone width (a screenshot or a note is fine).
6. No file outside the site map was modified. Show `git status` before any commit, list files
   explicitly, and never `git add -A`.
