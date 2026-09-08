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

**The `EARNED` line is not decoration.** A kill without a case attached gets softened, then
argued with, then dropped. A kill with `d = 9.86, n = 3, and the phrase "most robust findings"`
attached to it survives, because there is nothing to argue with.

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

## Hour 3 — Defects that do not present as claims

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

## Hour 4 — The finding you will defend

Each student presents for five minutes. The required structure:

1. **The question you could not stop thinking about** — and whether you still cannot
2. **What you now believe, and why the room should believe it too**
3. What you got wrong on the way, and how you caught it
4. **What would change your mind** — stated as something that could actually happen
5. What your result does not support

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

- Hour 3 has no exercise with a known-good answer, unlike every other hour in the course. It is
  honest to teach an unsolved problem as unsolved, but four hours of solvable followed by one hour
  of open may read as the material running out. **Decide whether hour 3 shrinks to 40 minutes and
  hour 4 absorbs the rest.**
