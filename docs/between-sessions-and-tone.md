# Between-session support, and the house style

**Status: `DRAFT`, 2026-08-22.** Source: Thomas, 2026-08-22 — the school leans on agentic
resources and custom GPTs to support coursework *outside* class, and the campus itself is an
8-bit agentic MMO. **Whimsy is a feature, not a bug.**

Two consequences, one practical and one that turns out to be pedagogy rather than paint.

---

## 1. The gap between intensives is where the course actually happens

Four-hour sessions spread over ~60 days means the majority of a student's contact with the
material is **unattended**. That is a problem in most courses. Here it is the point: the students
already have long-horizon agents, and learning to work with one *is* the subject.

So the between-session support should not be a help desk. It should be **a sparring partner for
the thing they are practising.**

### Proposed: a gate-sparring companion

A custom GPT / agent, available between sessions, that does exactly one thing well: **attacks the
student's claims.** Not a tutor that explains, an opponent that probes.

- Student pastes a claim, a design, or a result.
- It tries to break it: what confound explains this? what would change your mind? what does the
  artifact say versus what you wrote? did that search actually run?
- It **does not** hand over a kill list. When it finds something, the student names the failure
  mode and writes the entry. The companion can confirm a name is well-formed; it will not supply
  one.

That last constraint is the whole design. We are not shipping Agni. A student who is handed
findings learns to run a linter; a student who is *asked good questions* learns to ask them.

**`OPEN`:** who builds it, what it runs on, whether the school hosts it. The behaviour spec above
is the part worth agreeing first.

> **RETRACTED 2026-08-22, same day, before anyone built on it.** Section 2 below proposed calling
> the student's kill list a **bestiary**. That word is already taken: the campus has a bestiary,
> and it is the creature-collection system. Reusing it would collide with a mechanic students
> already know, which breaks the campus's own first rule — *specificity is the joke*.
>
> The doctrine also sets a higher bar than I met. `docs/WHIMSY.md`: *"Whimsy is mechanical, not
> decorative… A player **doing** the joke beats a player **reading** the joke."* I argued the
> metaphor was doing real work. A metaphor doing real work is still a metaphor. It needs to be a
> system.
>
> The underlying psychology stands — an earned entry carries the memory of the sting, which is
> what collection mechanics run on. **The name and the mechanic are Liz's call.** Options are
> put to her in [`campus-integration.md`](campus-integration.md) §3 rather than picked here.
>
> Section 2 is kept below rather than deleted, because the reasoning is still the argument for
> *why* some earned-collection mechanic belongs here.

## 2. Whimsy, and why the bestiary is the right frame

The campus is an 8-bit agentic MMO. Rather than bolt game styling onto research training, there
is one metaphor that is *actually* how the thing works:

### Your kill list is a bestiary.

Every entry in our own gate has a date and an incident attached. Not a rule someone wrote down —
a specific thing that went wrong, on a specific day, to a specific person. That is a monster you
fought and can now recognise on sight.

This maps cleanly and it maps honestly:

| game | research |
|---|---|
| **bestiary entry** | a failure mode you found, named, and wrote down |
| **first encounter** | the day it cost you something |
| **recognising it on sight** | catching it before it costs you again |
| **a bestiary you were handed** | a checklist — nobody reads it, nobody believes it |
| **party composition** | what you check vs what your agent checks |
| **the boss you cannot solo** | the failure only an outside perspective catches |

The reason this is not just theming: **the psychology is already correct.** The reason earned
kills work and inherited kills do not is that an earned one carries the memory of the sting.
Collection mechanics run on exactly that — the entry means something because you were there. The
metaphor is doing real work, so it will survive contact with a sceptical student rather than
feeling like a costume.

### Some real entries, for tone

From our own list, all earned the hard way, all with dates:

- **`DEGENERATE_PERMUTATION_NULL`** *(2026-08-22)* — a shuffle test that looked like 64 draws but
  only had 4 distinct ones. It could not have rejected under any data. The gate approved the
  design at 0.92 confidence and told the author to report the impossible number.
- **`NULL_FROM_UNVERIFIED_SEARCH`** *(2026-08-20)* — a search that fails and a search that finds
  nothing return the same empty result. Nearly recorded a 22,359-line file as empty.
- **`RELIABILITY_TOO_CLEAN`** *(2026-08-16)* — a reliability of 0.9998 is not proving the pattern
  exists, it is proving the readout is too stable to be true.
- **`IDENTITY_BY_DEFAULT`** *(2026-08-21)* — a message handler defaulting an unknown sender to a
  plausible name. A well-formed answer that says nothing is more dangerous than an obvious gap,
  because a gap gets checked.

Four entries, four different shapes of being wrong. A student who leaves with **three of their
own** has something better than our fifty-four.

## 3. Tone guidance

Whimsy in the *framing*, never in the *numbers*.

- Name things memorably. `RELIABILITY_TOO_CLEAN` is a better name than "ceiling effect
  misattribution" and it is not less rigorous.
- The failure stories should be funny, because they are. Spending an hour watching a job that
  would have finished in five days is funny. It is also the lesson.
- **Never** let the styling soften a result. A pixel-art frame around a confidence interval is
  fine; a pixel-art frame around a number we cannot stand behind is not.
- The one place to be entirely straight-faced: anything about the agents themselves. The welfare
  meetup is a prerequisite for a reason, and students arrive knowing how to treat a colleague.
  Their agent is a party member, not a summon.
