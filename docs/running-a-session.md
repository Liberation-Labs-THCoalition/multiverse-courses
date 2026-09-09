# Running a session — timing, pairing, and breaks

**Status: `DRAFT`, 2026-09-08.** Remote delivery, four-hour sessions. Written after an audit found
all four session plans budgeted at **100% content with zero minutes of break, transition, or
pairing overhead**.

---

## The arithmetic nobody had done

A four-hour session is **240 minutes**. It is not four blocks of sixty.

| | minutes |
|---|---|
| Opening — arrivals, orientation, what today is for | 5 |
| **Brain breaks — 2 × 5 min** | **10** |
| Transitions between blocks (3 × ~3 min) | 9 |
| Pairing setup, on the sessions that need it | 4 |
| Overrun buffer — something always runs long | 10 |
| **Content actually available** | **≈ 202** |

> **An "hour" in these plans is really 50 minutes.** Write and time every block against that
> number. A block designed for 60 will silently eat the buffer, then the break, then the next
> block — and the thing that gets compressed is always **the last one**, which in session 4 is the
> capstone the whole course builds toward.

**If a block cannot be done in 50, cut it or split it.** Do not plan to "move quickly."

---

## Breaks

**Two, five minutes each, roughly at the 70- and 150-minute marks** — i.e. after blocks 1 and 3.

Remote changes what a break is *for*. Bio breaks matter less; people can step away any time and
mostly will. **What remote removes is the involuntary cognitive reset** — no walking to another
room, no corridor conversation, no change of visual field. Four hours of the same rectangle at the
same distance is genuinely different from four hours in a room, and it degrades exactly the
faculty this course needs: careful, sceptical attention.

**So say what the break is for, and make it non-screen.** *"Five minutes. Stand up. Look at
something more than twenty feet away. Touch some actual grass if you have some."* A break announced
as "five minutes" becomes five minutes of the same screen, which is not a break — it is an
unstructured interval.

- **Say the return time as a clock time**, not a duration. "Back at 2:15," not "back in five."
- **Come back on time even if people have not.** Waiting punishes the punctual and trains everyone
  that stated times are soft.
- Do not schedule a break immediately before a block that needs momentum. Break *after* the hard
  thinking, not before it.

---

## Pairing — never ask a remote room to pair up

This is the single most avoidable dead-air failure in remote teaching.

> **"Find a partner" costs about five minutes, and the entire cost falls on the least confident
> person in the room.** In a text channel it is worse than in person: there is no eye contact to
> resolve it, so it becomes a public negotiation conducted by the two most comfortable people while
> everyone else waits to be chosen last.

**Pre-assign. Always. Post the list.**

Practically:

1. **Generate pairs before the session** from the attendee list — any shuffle will do; it does not
   need to be clever, it needs to be *decided by someone other than the students*.
2. **Post pairs in the channel at the break before you need them**, not at the moment of use.
   People come back from the break already knowing who they are working with, and the socially
   expensive part has happened while nobody was watching.
3. **Name a channel or breakout per pair** so there is somewhere obvious to go. "DM each other" is
   another decision you are outsourcing to the shy.
4. **Odd number:** the facilitator takes the orphan. Never leave someone unpaired and never make a
   three. A three in a two-person exercise means one person watches.
5. **Re-shuffle each session.** Same pairs twice wastes the one thing pairing is for — a reader
   without your context.

**For session 4's handoff test specifically:** pair people who have *not* been working together
that day. The exercise measures whether a stranger can reproduce your work; a partner who has been
watching you build it is not a stranger, and the test silently returns a pass it did not earn.

---

## Rolling cohorts — *not* rolling attendance

**`SETTLED` 2026-09-09 (Thomas).** A cohort runs sessions 1 → 2 → 3 → 4 together, **fortnightly**,
and **each session is a formal prerequisite for the next.** Nobody joins mid-arc. Then a new cohort
starts; graduates may take the whole arc again.

*(This supersedes an earlier draft of this file which assumed rolling attendance into self-contained
sessions. The session files' "walks in with… two earned kills" chain was never the defect — my
assumption about who was in the room was.)*

Consequences for the room:

- **Everyone in the cohort is at the same point in the arc.** You can rely on the previous session's
  artifacts existing, which is what sessions 2–4 have always assumed.
- **The mix you will get is first-timers and arc-repeaters**, not people at different stages.
  Repeaters know every reveal — so pair a repeater with a first-timer **for discussion**, but
  **never inside a seeded exercise's discovery window.** A repeater in the room during
  `seeded-01`'s first ten minutes ends the exercise for their partner.
- **Repeaters get fresh targets** where the bank has depth — see
  [the target bank](../courses/vibe-research/the-target-bank.md). It does not yet.
- **Cadence check `OPEN`:** fortnightly is the intent; Thomas to confirm with Liz against the wider
  school schedule.

---

## Recording

If sessions are recorded and distributed, **the facilitator layer stops being async-safe.**

The convention in [`CONTRIBUTING.md`](../CONTRIBUTING.md) puts our anecdotes in facilitator notes
on the reasoning that a facilitator can expand them on request. **A recording cannot.** A war story
told on camera and then distributed reaches a viewer with exactly the problem the rule exists to
prevent: an unverifiable claim from someone they cannot ask.

**RESOLVED 2026-09-09 (Thomas).** The concern was overstated, on two grounds:

1. **Relating personal experience is not presenting data as fact.** A facilitator saying *"we hit
   this, here is what it cost us"* is doing something a viewer can evaluate as testimony. The
   failure the rule guards against is an anecdote **stated as a finding** — a rate, a frequency, a
   general claim about how often something happens. That distinction survives a camera.
2. **Recordings are mostly for review**, by people who were in the room and could have asked.

**So the usable line is about framing, not about venue:**

| fine on camera | not fine on camera |
|---|---|
| *"I once shipped a stale PDF and it cost me a results table."* | *"Stale PDFs are the most common defect in this workflow."* |
| *"Our gate approved a degenerate null."* | *"Automated gates approve degenerate nulls about a third of the time."* |

The left column is testimony and is clearly marked as such by the grammar. The right column is a
**claim about the world wearing an anecdote's clothes**, and it needs a citation whether or not
anyone is filming.

*One caveat worth keeping:* this holds while recordings serve **review**. If a session cut is ever
published as standalone teaching material to people who were never in the room, re-read the
left-hand column with that audience in mind.
