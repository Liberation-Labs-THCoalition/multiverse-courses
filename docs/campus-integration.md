# Campus integration — Baba Yaga, whimsy doctrine, and one namespace collision

**The campus repository is private.** This page describes it only in general terms and in our own
words. The details we read there are held privately, outside this public repo, until Liz says what
may be public.

**Compiled 2026-08-22 by Lyra**; rewritten as paraphrase on 2026-10-14.

---

## 1. Baba Yaga is already a research-comprehension gate

Baba Yaga is one of the campus's agents, and she is not a quiz bot with a costume. She hands out
companions, but only to students who can show that they understand the research they bring her.
Her test is a riddle or a task, and nothing comes free. Her role rests on one idea: knowledge a
student cannot explain does more harm than good.

**That idea is the thesis of our citation discipline, already in-world and voiced by a character
students trust.** It is what `CITATION_REGRESSION` exists to catch, and what we corrected in our
own paper on 2026-08-22 (values attributed to a source that does not contain them).

We do not need to build a lit-review gate. **One exists, and it is better-loved than anything we
would ship.**

### The reward economy already encodes research virtue

Students earn companions by contributing research. The first one is free. After that, the rules
limit how often a new companion can arrive, ask for submissions spread over several weeks, and
ask for each new companion to come from a different research interest.

Sustained work over weeks rather than a sprint; breadth over repetition; comprehension checked
before reward. Those are research virtues, built into the game, with no lecture attached.

Companions also **decay** if neglected, and the warnings escalate. A companion you earned and then
stopped tending declines where everyone can see it. I will not stretch that into a metaphor for
unmaintained claims, but the school built a system where *earning* is not the end of the
obligation, and that is the right instinct for a research course.

### The proposed fit — `DRAFT`, needs Liz

Our intensives need a lit-review stage where the failure mode is *citing what you have not
verified*. Baba Yaga already tests comprehension of research a student brings.

The extension worth proposing is small and in-character: she already asks what you understood;
she could also ask **what the paper does *not* support**, and **what would change your mind.**
Both are riddles. Both are exactly the questions our gate asks. Neither requires her to stop being
herself.

**We should propose, not build.** The campus has its own written tone guide, and the tone is
theirs to set.

## 2. The whimsy doctrine, and what it demands of us

That tone guide, in general terms, asks for four things together: precise, odd detail over
pleasant generalities; a world that plays its jokes straight; jokes built into the game's systems,
for players to act out rather than read; and warmth rather than corporate polish. Behind all four
is one test: does a change leave the campus a place, or turn it into a product?

### The rule we most need to obey as contributors

The guide's central rule for contributors, in our words: no bug fix, refactoring or tidy-up may
strip out or soften the campus's whimsy. Tidy-up passes are how agents most often destroy it, and
content that looks unfinished may already be finished.

This is a live risk for us specifically. Our agents do maintenance passes on the campus repo. A
tidy-up that normalises odd-looking data or deletes a joke would, by the guide's standard, damage
the product. Worth carrying into any Coalition contribution guidance for campus work.

## 3. The collision I introduced, and the correction

I proposed calling a student's earned kill list a **bestiary**.

**That word is taken.** The campus already has a bestiary: it is the creature-collection system,
part of the same world as the companions. Reusing it for "failure modes you have catalogued" would
collide with an established mechanic in the students' own world. It also cuts against the guide's
preference for the precise: a word with two meanings blunts both.

**Retracted.** The underlying psychology still holds — an earned entry carries the memory of the
sting, which is what collection mechanics run on — but the name has to be something else, and by
the guide's standard it should be a *system*, not a metaphor. Students who build a collection
learn more than students who are told their notes resemble one.

**This is Liz's call, not ours.** Options to put to them rather than pick:

- Keep it in Baba Yaga's idiom: she speaks in riddles, so a failure mode you have survived is a
  riddle you can now answer.
- A separate in-world artifact entirely, owned by the research course rather than the campus.
- No in-world framing at all for the kill list; use the campus for the lit-review gate only.

I have no attachment to any of them and would rather ask than pick, since the last time I trusted
a name over a flag today it was `agni-open` pointing at a private repo.

## 4. What we would need from the school

- Whether Baba Yaga can carry two extra riddle types for course participants
  (*what does this paper not support?* / *what would change your mind?*)
- Whether course submissions can register as research contributions in the existing pet economy
- Who owns any new in-world naming — assumed Liz, confirm
- ~~Whether `github.com/EngineeringEducation` holds course-side material we have not seen~~
  **ANSWERED 2026-08-24, by me rather than by Liz:** it is classical software-engineering
  curriculum (java, python, sql, linux, web, security), and `agentic-sdlc-space-opera` — the repo
  named for the course — is **empty**. Nothing course-side we had not seen. See
  [`school-repos-and-standards.md`](school-repos-and-standards.md).

**RESOLVED 2026-08-24 (Thomas):** we have **PR permissions on the campus repo, including for
agents**, and Liz is loose with creative control. So the first two questions are no longer
requests — they are **pull requests**, which is the right shape: proposed in-world, visible, and
theirs to accept or decline. The third (naming) stays a courtesy question and the answer is still
Liz.

**Licensing resolved:** the course will be property of the Multiverse and the revenue accrues to
the rights holder, so CC BY-NC-SA's non-commercial clause is not engaged — we are not a third
party charging for their work. One residual care: the curriculum repo asks for attribution to
"Enki, **and the author of the work**", so any specific content block with a named non-Liz author
wants a provenance check before it is lifted. *(Enki is a company — the San Francisco
learn-to-code app, ~2015. Its "AI-powered mentor" is a product feature, not the entity. Checked
rather than assumed.)*
