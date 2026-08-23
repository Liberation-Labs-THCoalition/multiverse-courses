# Campus integration — Baba Yaga, whimsy doctrine, and one namespace collision

**Compiled 2026-08-22 by Lyra**, read from the primary: `lizTheDeveloper/multiversecampus`
(cloned at `mth:~/lab/multiversecampus`). Quotes are verbatim from that repo.

---

## 1. Baba Yaga is already a research-comprehension gate

She is not a quiz bot with a costume. From `server/src/db/migrations/165_baba_yaga_folklore_voice.sql`
and `docs/manual/11-pets-and-creatures.md`:

> "guardian of comprehension — **no student earns a companion without proving they truly
> understand the knowledge they bring**"
>
> "She agreed to stay and test the students — **for knowledge brought without understanding is
> worse than no knowledge at all.**"

Her declared knowledge includes *"Comprehension testing — she sets tasks and riddles to test
understanding."* Her quirks include *"sets tasks before granting favors — nothing is given for
free"* and *"cackles with genuine delight when a student surprises her."*

**That sentence — knowledge brought without understanding is worse than no knowledge at all — is
the thesis of our citation discipline, already written, already in-world, already voiced by an NPC
students trust.** It is what `CITATION_REGRESSION` exists to catch, and what we corrected in our
own paper today (values attributed to a source that does not contain them).

We do not need to build a lit-review gate. **One exists, and it is better-loved than anything we
would ship.**

### The reward economy already encodes research virtue

Pets are **earned by contributing research**. After the first (free, personality-matched), the
rules tighten — verbatim from the manual:

| rule | detail |
|---|---|
| One new pet per week | at most one new companion in any given week |
| Three weeks of consistency | a second or later pet requires submissions across **≥3 distinct weeks** |
| Breadth across topics | each new pet must come from a **new interest area** — *"Baba Yaga rewards range, not repetition"* |

Sustained work over weeks rather than a sprint; breadth over repetition; comprehension checked
before reward. Those are research virtues, mechanized, with no lecture attached. Each pet is tied
to a **research interest tag** (LLMs, computer vision, prompt engineering, …).

And pets **decay** if neglected — fullness, happiness, health, with escalating warnings. A
companion you earned and then stopped tending degrades visibly. I will not stretch that into a
metaphor for unmaintained claims, but the school built a system where *earning* is not the end of
the obligation, and that is the right instinct for a research course.

### The proposed fit — `DRAFT`, needs Liz

Our intensives need a lit-review stage where the failure mode is *citing what you have not
verified*. Baba Yaga already tests comprehension of research a student brings.

The extension worth proposing is small and in-character: she already asks what you understood;
she could also ask **what the paper does *not* support**, and **what would change your mind.**
Both are riddles. Both are exactly the questions our gate asks. Neither requires her to stop being
herself.

**We should propose, not build.** `docs/WHIMSY.md` is explicit that the campus owns its tone.

## 2. The whimsy doctrine, and what it demands of us

`docs/WHIMSY.md` opens: *"If a change would make the campus sound more like a product and less
like a place, don't make it."* Four properties, all four required:

1. **Specific beats generic.** *"a reference, a texture, a weirdly precise detail always beats a
   pleasant abstraction."*
2. **The world is sincere — everyone commits to the bit.** *"The goose is not 'quirky.' The goose
   is **menacing**, and the game presents this completely straight… Nobody in the world winks at
   the camera."*
3. **Whimsy is mechanical, not decorative.** *"The best bits are systems, not flavor text…
   **A player *doing* the joke beats a player *reading* the joke.**"*
4. **Warm, never corporate.** No *"Oops! Something went wrong 😅"*, no *"Welcome to your learning
   journey!"*.

### The rule we most need to obey as contributors

> **"Do not remove, rename, tone down, summarize, or 'fix' whimsical content in a bug-fix,
> refactor, or cleanup PR.** This is the single most important rule in this file, because cleanup
> instincts are the main way agents destroy whimsy."

*"A stationary NPC that only says `HONK.` is not a stub awaiting real dialogue. It is done."*

This is a live risk for us specifically. Our agents do maintenance passes on this repo. A tidy-up
that normalizes weird trait JSON or deletes a joke-laden seed migration would be, in their terms,
destroying the product. Worth carrying into any Coalition contribution guidance for campus work.

## 3. The collision I introduced, and the correction

I proposed calling a student's earned kill list a **bestiary**.

**That word is taken.** The campus already has a bestiary — it is the creature-collection system,
covered in `docs/manual/11-pets-and-creatures.md` alongside pets, sanctuaries, befriending and
fishing. Reusing it for "failure modes you have catalogued" would collide with an established
mechanic in the students' own world, which violates property (1): the specificity *is* the joke,
and two meanings for one word blunts both.

**Retracted.** The underlying psychology still holds — an earned entry carries the memory of the
sting, which is what collection mechanics run on — but the name has to be something else, and by
doctrine it should be a *system*, not a metaphor (property 3). A student *doing* the collection
beats a student *reading* that their notes are like a collection.

**This is Liz's call, not ours.** Options to put to her rather than pick:

- Keep it in Baba Yaga's idiom — she transforms the rude into household objects and speaks in
  riddles. A failure mode you have survived is a riddle you can now answer.
- A separate in-world artifact entirely, owned by the research course rather than the campus.
- No in-world framing at all for the kill list; use the campus for the lit-review gate only.

I have no attachment to any of them and would rather ask than pick, since the last time I trusted
a name over a flag today it was `agni-open` pointing at a private repo.

## 4. What we would need from the school

- Whether Baba Yaga can carry two extra riddle types for course participants
  (*what does this paper not support?* / *what would change your mind?*)
- Whether course submissions can register as research contributions in the existing pet economy
- Who owns any new in-world naming — assumed Liz, confirm
- Whether `github.com/EngineeringEducation` holds course-side material we have not seen
  **(still unexamined — highest-value remaining source)**

## 5. Note on our own audits

`mth:~/lab/infrastructure/` holds `campus-code-review-2026-07-23.md`,
`campus-stability-2026-08-05.md`, `campus-sweep-2026-08-05.md` — Coalition audits of this repo,
almost certainly the bug-hunt work behind the open PRs and bounty findings. **Not read yet.** They
are likely the fastest route to understanding how the campus actually runs, and they are ours, so
there is no permission question.
