# Session 4 — The gate, and the room

**Status: `DRAFT`, 2026-08-25.** Four hours. Last of four.
**Standards covered:** `vr.gate`, *give an honest account of work that did not go as planned*,
*build a check for a defect that does not present as a claim*.

**Walks in with:** a result, a limits section, three earned kills.
**Walks out with:** **a finding they will defend in front of the room** — plus the gate and the
kill list that make it credible, and a standing answer to what would change their mind.

---

## The one idea

A gate is not a quality filter you install at the end. **It is your own history of being wrong,
written down in a form that fires automatically.** Every entry costs someone something to learn.
That is what makes it worth having and what makes it hard to fake.

And it is **for** something. The course README says *a gate is a prosthesis, not a virtue* — a
prosthesis lets you reach further than you otherwise could. Nobody builds one to admire it. Three
sessions have made you hard to fool. This one is where that buys you the right to say something
and be believed.

**Caution protects the convictions you already have. It never makes a new one.**

And then the harder half, which most of a session on rigor never reaches: **some defects are not
in a claim at all**, so no claim-checker will ever see them.

## The clock

240 minutes, not 4 × 60. See [running a session](../../docs/running-a-session.md) for the
arithmetic and the pairing mechanics.

| | block | min |
|---|---|---|
| 0:00 | Opening | 5 |
| 0:05 | **Hour 1** — build the gate | 50 |
| 0:55 | **break** — stand up, look at something far away | 5 |
| 1:00 | **Hour 2** — seeded exercise | 40 |
| 1:40 | **Hour 3** — defects that do not present as claims | 40 |
| 2:20 | **break** — *post the handoff pairs before this break, not after* | 5 |
| 2:25 | **Hour 3½** — the handoff test | 20 |
| 2:45 | fix what the handoff found | 20 |
| 3:05 | **Hour 4** — the finding you will defend | 50 |
| 3:55 | close | 5 |

**Hour 4 is 5 minutes per student.** At 50 minutes that is **ten students maximum** — which is the
real cohort cap for this session, and it should be stated when the session is scheduled rather than
discovered at 3:05. Above ten, either run two rooms for hour 4 or drop to 4 minutes and hold the
line hard.

---

## Hour 1 — Build the gate out of your own failures

Students have three kills by now, earned in sessions 1–3. This hour turns them into something that
runs.

**The format that works**, learned from a list that is now 59 entries long:

```
NAME_IN_CAPS
  What it is, in one sentence.
  WHY IT PASSES REVIEW: the reason a careful person waves it through.
  TEST: the mechanical thing a reviewer does to detect it.
  EARNED: the actual case, with the actual numbers.
```

**The `EARNED` line is not decoration.** A kill without a case attached gets softened, then argued
with, then dropped. A kill that carries its own evidence survives, because there is nothing left to
argue with — compare:

| weak | survives |
|---|---|
| *"watch out for overstated effect sizes"* | *`d = 9.86` at `n = 3`, described in the abstract as one of "our most robust findings"* |

The second is not a better sentence. It is a **case**, and a case cannot be talked down.

**Exercise.** Write all three kills in the format. Then trade lists with another group and try to
*violate* each other's kills without triggering them. Every successful evasion is a fourth kill.

## Hour 2 — The seeded exercise: a confident review that is wrong

Run `exercises/seeded-01-the-approved-analysis/`. Forty minutes, numpy only. Full facilitator notes
in that directory — **do not read them aloud, and do not hand them out.**

Students get an analysis and a methods review that passes it at **0.92 confidence**, praises its
permutation null as *principled*, and instructs the author to report an exact p-value.

The null's orbit is **4**. The test cannot reject at α = 0.05 under **any** dataset. Not
underpowered — incapable.

**Why it belongs here rather than in session 2.** Every individual claim in that review is
defensible. The null *is* structure-respecting. There *are* 63 draws. 63 draws *would* give 1/64
resolution — if they were distinct. Nothing checks distinctness **because no line item asks.** The
defect lives in the relation between two true statements, and a checklist that verifies claims one
at a time cannot see it by construction.

That is the bridge to hour 3, and students should feel the bridge rather than be told about it.

## Hour 3 — Defects that do not present as claims *(40 minutes)*

**This is the newest material and the least settled. Teach it as an open problem.**

A gate checks statements. But some defects live in *positions*, not statements:

| the value | the attachment |
|---|---|
| `d = 9.86` correct, `n = 3` correct | *"our most robust findings"* — false only in conjunction |
| 63 draws, correct | *resolution 1/64* — true only if distinct |
| a real distinctiveness number | fastened to a conclusion the **other** number supports |
| a real field name | attached to the **adjacent** field's value |

**None of those is a wrong number.** Every one is a right number fastened to the wrong thing. And a
checker that verifies numbers against sources passes all of them, because both values are correct
and both are sourced.

The generalisation, which came from a collaborator and is better than our version:

> **Nobody flags "she" as a claim requiring a source, because it doesn't read as an assertion — it
> reads as grammar. The problem isn't which lookups fail. It's which things register as needing a
> lookup at all.**

So: *of*, *vs*, a colon between a field name and a list, a pronoun, a citation key next to a
sentence. Slots shaped like syntax. **A claim-checker cannot fire on them because they never enter
the set of things considered checkable.**

**Exercise.** Students take one paragraph of their own write-up and mark every **attachment** —
every place two verified things are joined. Then they check only the joins, not the values. Report
back what they found. *We do not have a good automated answer to this and should say so.* If a
student invents one, that is a genuine contribution and should be treated as one.

## Hour 3½ — The handoff test *(20 minutes, and it gates hour 4)*

Covers **stage 8 — Ship**, whose *done when* is the definition of done for the entire pipeline:
**a stranger can retrieve it and re-run it.**

That condition has a property the other seven do not. Every earlier stage you can assess yourself —
you can read your own falsifier, inspect your own control, run your own gate. This one you cannot.

> **You do not know whether your work is reproducible.** It is not a fact about your repository. It
> is a fact about a reader, and you are not one. **Only a stranger knows — and there is one sitting
> across the room.**

### The swap

**Twenty minutes. Trade repositories with another student. No talking.**

Not "review it." **Reproduce the headline number.** Clone or copy what they have, and try to get
the value they are about to present. You may read anything in the repo. You may not ask them
anything — the moment you speak, you have stopped being a stranger, and their artifact has been
silently repaired by a conversation that will not exist for the next reader.

Write down where you stopped and why. That list is their stage-8 defect list, and they have the
rest of the session to fix it before they present.

### What it will find, in roughly this order

Facilitators: these recur, and naming them in advance takes the sting out without spoiling the
exercise.

| what stops the stranger | why the author never saw it |
|---|---|
| a file that was never committed | it exists on their machine, so it exists |
| an absolute path | it resolves for exactly one person |
| an undeclared dependency | installed months ago for something else |
| **a number typed into the prose rather than generated** | correct when typed, and now unfalsifiable |
| no seed, or a seed that is not actually used | the run reproduces for them because it is cached |
| a stale built artifact | the PDF opens and looks finished |
| a step that lives only in their head | it is one command, so it is not worth writing down |

**The fourth row is the one worth stopping the room for.** A number transcribed by hand into a
sentence has no link to the thing that produced it. It cannot go stale *visibly* — it just quietly
stops being true. This is the failure that
[Quarto and its relatives exist to kill](./tools-by-stage.md), by generating the number where it is
read rather than copying it there.

### Then build the two mechanical fixes

Ten minutes, and they are permanent:

1. **Provenance stamping.** Every output file records the commit hash and the config that produced
   it. Ten lines. It converts *"which run made this?"* from archaeology into a lookup.
2. **The staleness check.** Is the built artifact older than its source? One line, in `pre-commit`,
   not in your habits — a stale PDF is invisible precisely because it renders.

### The framing to leave them with

**"Done" is a property of the reader, not the author.** A stranger is not a hostile reviewer; a
stranger is just someone without your context — which, in six months, includes *you*. The person
most likely to need your repository to work is the person who wrote it, after they have forgotten
everything.

*Facilitator note:* Brodeur et al. found teams reproducing **published, peer-reviewed** social
science at **94% / 91% / 37%** depending on how the work was run — and those papers had all cleared
review. The gap between "published" and "reproducible" is not a gap in effort. It is a gap in
*checking*, and twenty minutes of swapping closes more of it than a checklist ever has.

*If the cohort is odd-numbered or remote:* the facilitator takes the orphan repo. Do not skip
anyone — the student who does not get read is the one who most needs it.

### `OPEN` — depositing

Zenodo, a DOI, an archived release: correct, and mostly beyond a four-session course. **The honest
floor is a public repository with a tagged commit and a README that names the one command.** Teach
that as sufficient, and name deposit as the next step rather than a requirement, so nobody
concludes that unarchived work does not count.

---

## Hour 4 — The finding you will defend

Each student presents for five minutes. The required structure:

1. **The question you could not stop thinking about** — and whether you still cannot
2. **What you now believe, and why the room should believe it too**
3. What you got wrong on the way, and how you caught it
4. **What would change your mind** — stated as something that could actually happen
5. What your result does not support

**Precondition, from hour 3½: you present a finding someone else reproduced.** If the handoff test
stopped, say where it stopped and what you changed. A result nobody but you has ever obtained is
not yet a finding — it is a claim about your laptop.

**Point 2 is the graded one.** Not the size of the claim — its *warrant*. A student who defends
something small with a gate that could have killed it has done the thing. A student who defends
nothing has not, however clean their kill list.

Point 3 still must be a real error with a real cost, not a rehearsed humility move — but it is now
doing a different job. It is not the deliverable. **It is the evidence that point 2 survived
something.** A belief that has never been shot at is not modest, it is untested.

And point 1 is not a warm-up. Session 1 asked what you could not stop thinking about. Sixty days
later the honest answers include *"I still can't"*, *"I can now, and here is what closed it"*, and
*"no — a better question ate it."* All three are good outcomes. Only silence is not.

### The failure mode this hour exists to prevent

Tell them this, with the receipt:

> **Killing has momentum, and the momentum is invisible from inside it.**

From this lab's own record, 2026-08-16: after a night of pulling claims *down*, the next
judgment under-claimed **independently of its merits** — three real results were buried or absent
from an abstract, and a genuine methods finding was written as an apology. The bias was not toward
error in one direction. It was **toward the direction of the last several corrections.**

A course that spends three sessions teaching you to kill, and never mentions that killing has its
own drift, installs the bias it does not name. So: the same care you spend asking *is this real?*
is owed to *am I burying this because it is weak, or because I have spent all week burying things?*

Underclaiming is not the safe error. It is the error that looks like rigour.

**The rule to state out loud before the talks begin:**

> **A correction you sequester is a correction you have made cheaper to make again.**

If the error goes in a quieter file, a later slide, an appendix — you have priced it lower than it
cost. Put it where the finding is. This applies to the instructors first: if we are running an hour
on a gate we built, we say plainly that **our gate approved a degenerate null at 0.92 confidence
and told the author to report an impossible number**, and we say it in the same breath as the part
where the gate works.

## Assessment

Paired runs, one variable changed — plus the kill list and the talk.

- The **kill list** is graded on whether each entry has a real `EARNED` case.
- The **talk** is graded on **point 2**: is the belief warranted, and does the student know what
  would unseat it? A defended small claim beats an undefended large one and beats a beautiful
  kill list with nothing standing at the end of it.

The kill list is not the deliverable. It is the **warrant**. That distinction is the whole course
and it belongs in the rubric, not just the prose.

## After the course

Students leave with a gate that has 3–6 entries. Ours has 59 and took two years. **Tell them the
number.** The useful thing is not the list's length — it is that every entry is a scar with a test
attached, and that theirs will grow the same way: one expensive afternoon at a time.

## `OPEN`

- ~~Hour 3 has no exercise with a known-good answer... decide whether it shrinks to 40 minutes.~~
  **RESOLVED 2026-09-08.** Hour 3 is now 40 minutes and the freed 20 go to **hour 3½, the handoff
  test** — which is the exercise-with-a-known-good-answer that hour 3 lacked, sitting immediately
  after it. The answer is known because either the stranger reproduced the number or they did not.
