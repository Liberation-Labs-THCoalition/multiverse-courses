# Session 4 — The gate, and the room

> **Clock:** this session's clock is on this page, [below](#the-clock): 201 minutes of content in a 240-minute
> session, rebuilt 2026-10-20 and not yet piloted. [The four clocks](../../docs/session-clocks.md) still shows this
> session's old plan. For session 4, this page replaces it.

**Status: `DRAFT`, 2026-08-25; rebuilt 2026-10-20 around a published case and a gate that runs on data.** Four
hours. Last of four.
**Standards covered:** `vr.gate`, *build a review gate out of your own failures* (all seven objectives, hours 1 and 4),
from [Course: The Gate](../../standards/vibe-research/README.md). Three objectives this session teaches are not
written as standards yet: *build a check for a defect that does not present as a claim* (hour 3), *give an honest
account of work that did not go as planned* (hour 4, point 3), and the `PROPOSED` *defend a finding with a gate that
could have killed it* (hour 4, point 2).

**Walks in with:** from session 3, a result, its limits section and a verdict; three kills, each written as what
happened, its class, and a check someone else could apply; and the check from session 3's hour 3, run as homework.
**Walks out with:** **a finding they will defend in front of the room**, and what makes it credible: a gate that
runs, made of their own kills and seen to fail; a comparison, predicted first, of an analysis with that gate and
without it; a stranger who reproduced the number; and a standing answer to what would change their mind.

---

## The one idea

A gate is not a quality filter you install at the end. **It is your own history of being wrong, written down in a
form that fires automatically.** Every entry cost someone something to learn. That is what makes it worth having
and what makes it hard to fake.

You have built one before. In Agentic SDLC, a pre-commit hook stops code going in that fails a check you wrote. A
gate does the same for claims, and your own mistakes write its checks.

And it is **for** something. The course README says *a gate is a prosthesis, not a virtue*: a prosthesis lets you
reach further than you otherwise could. Nobody builds one to admire it. Three sessions have made you hard to fool.
This one is where that buys you the right to say something and be believed.

**Caution protects the convictions you already have. It never makes a new one.**

Two warnings come with it, and the session takes one each:

1. **A gate can share your blind spot.** If it sees your work only through the same instrument that made the work,
   it can only agree with it, however many checks it has. Hour 1.
2. **Some defects are not in a claim at all**, so no claim-checker will ever see them. Hour 3.

## Before session 4

Ten minutes, the day before.

1. **Have your three kills to hand**, from session 3's template, and your pilot: its results file and the code that
   analysed it.
2. **For each kill, rewrite its third line as a test a computer could run**, in one sentence: what it reads, and
   what makes it fail. *"Look carefully at the counts"* isn't one. *"Fails if any two compared numbers were computed
   over different numbers of responses"* is.
3. **Check that Python and numpy run**, as they did for session 3's exercise.

Hour 1's exercise is linked from this page. Please don't open it before the session: its first step is a
prediction, and it only works on a first read.

## The clock

*`DRAFT`, 2026-10-20. Not piloted: every timing here is `PREDICTED`.*

| clock | block | min |
|---|---|---|
| 0:00 | Opening. Hour 1's pairs were posted the night before; confirm them, don't brief | 5 |
| 0:05 | **Hour 1** — build the gate, and make it run | 50 |
| 0:55 | **break**, "back at 1:00" | 5 |
| 1:00 | **Hour 2** — the seeded exercise: a confident review | 40 |
| 1:40 | **lunch**, "back at 2:10" | 30 |
| 2:10 | transition | 3 |
| 2:13 | **Hour 3** — defects that do not present as claims | 30 |
| 2:43 | **break**, "back at 2:48". *Post the hand-off pairs before this break* | 5 |
| 2:48 | **Hour 3½** — the hand-off test | 20 |
| 3:08 | fix what the hand-off found, and run your gate on your own pilot | 16 |
| 3:24 | transition | 3 |
| 3:27 | **Hour 4** — the finding you will defend | 45 |
| 4:12 | overrun buffer, **unspent** | 13 |
| 4:25 | close | 5 |

**201 minutes of content** (50 + 40 + 30 + 20 + 16 + 45). The buffer is not a block: nothing is scheduled into it.

**Hour 4 at 45 minutes is eight students at five minutes each**, or nine with no handover between speakers. Cohort
size is in [the clocks](../../docs/session-clocks.md). Above eight: two rooms for hour 4, or hold four minutes hard.

**Pairs.** Hour 1 runs in pairs posted the night before, because its pair work comes before any break. Hour 3½ needs
a reader who hasn't watched your work today, so its pairs are new, posted at the second break. One named room per
pair; the facilitator takes any odd one out. See [running a session](../../docs/running-a-session.md).

**Commit, then reveal.** Hour 1 has a step where you write your answer down before anything runs. Online, that means
sending it to the facilitator (a direct message is fine). During that step your agent and search stay closed. That's
an honour rule, and it's part of the exercise.

---

## Hour 1 — Build the gate, and make it run

Covers `vr.gate`, objectives 0 to 6, and the course's assessed comparison (see [Assessment](#assessment)).
**50 minutes.**

Your three kills are written down. This hour turns them into code that runs on data, then finds out what your gate
lets through, including what it lets through because of where it looks.

**The case (5 min).** A published investigation, read aloud up to the moment of decision: a precision instrument, two
other checks that disagreed with it, both believed less reliable, and a schedule under pressure. Poll the room:
*what would you do with the disagreement?* Send your vote. The answer comes at the end of the hour.

**The format (2 min).** Every kill goes into the gate in this form:

```
NAME_IN_CAPS
  What it is, in one sentence.
  WHY IT PASSES REVIEW: the reason a careful person waves it through.
  TEST: the code that detects it, which runs without you.
  EARNED: the actual case, with the actual numbers.
```

**The `EARNED` line is not decoration.** A kill without a case attached gets softened, then argued with, then
dropped. A kill that carries its own evidence survives, because there is nothing left to argue with:

| weak | survives |
|---|---|
| *"watch out for best-of-n"* | the file, the two statistics, the counts behind each, and both numbers: before the fix and after |

The `EARNED` line has a second job now. **The case it names is your test's first positive control:** the check must
fire on the case it came from. If it doesn't, it isn't that kill's test yet.

**The exercise (2 + 28 min), in pairs, with your agents.** Go to your pair's room and open
[*All checks passed*](exercises/seeded-04-all-checks-passed/review.md) (in a clone:
`exercises/seeded-04-all-checks-passed/`). It is the results note of a pre-registered pilot, and the analysis ran
behind a gate whose seven checks all passed. Your task is at the end of the note. It has five steps, of about 3, 12,
3, 5 and 5 minutes:

1. **Predict**, alone, with your agent closed, and send it to the facilitator.
2. **Build:** your three kills become checks in the gate, each seen to fire.
3. **Run both:** the analysis with your gate and without it.
4. **Break it, unlike:** plant a defect none of your checks was written for.
5. **Fix, or sign.**

One of you shares a screen and drives an agent; the other keeps the written predictions. Your agent can write the
code. What each check tests is yours. **The last sentence of step 2 matters:** if one of your checks fails, write
down whether you think the check is wrong or the data is, before you change anything.

Steps 1 and 3 together are this course's assessed comparison: an analysis with your gate and without it, predicted
first.

**The reveal (8 min).** What the people in the opening case did with the disagreement, what the investigation found,
and what this exercise's gate let through.

**The rule (3 min).**

> **A check that sees your work only through the instrument that made it can only agree with it. Give your gate at
> least one check that looks from somewhere else, and make every check fail once, on a case unlike the one it was
> built for.**
>
> **When one check disagrees with the rest, find out which is wrong before you discount it.**

**Close (2 min).** One line each in the chat: the kill of yours that fired, or the kind of defect your gate can't see.

*Facilitator note —* **`PREDICTED`**, not piloted: a pair whose checks all pass will want to stop after step 3. For
them, step 4 is where the hour happens. Visit during it.

*The case, its sources and its reveal, the hour's clock and what **not** to use in it are in the **facilitator
pack**. The exercise's own facilitator notes, with its answer and the script that checks it, are kept with the
exercise, marked for agents to leave alone, and shared after the session.*

## Hour 2 — The seeded exercise: a confident review that is wrong

**40 minutes.** Run `exercises/seeded-01-the-approved-analysis/`, numpy only. Full facilitator notes in that
directory: **do not read them aloud, and do not hand them out.**

Hour 1's gate was code you could run. This one is a reviewer, and it is confident. Students get an analysis and a
methods review that passes it at **0.92 confidence**, praises its permutation null as *principled*, and instructs
the author to report an exact p-value.

What the defect is, why the exercise runs in this session, and how it leads into hour 3 are in the facilitator
notes, not here. Students find the defect themselves, and this page is open to them before the session.

## Hour 3 — Defects that do not present as claims

`PROPOSED` objective, not yet a written standard: *build a check for a defect that does not present as a claim*.
**30 minutes.** This is the newest material and the least settled. **Teach it as an open problem.**

A gate checks statements. But some defects live in *positions*, not statements:

| the value | the attachment |
|---|---|
| `0.8`, correct | *"80% of users"*: true only if it was counted over users, not visits |
| a real reference, a real sentence | the reference placed after a sentence it doesn't support |
| a real number from comparison A | quoted as the result of comparison B, sitting beside it |
| a real field name | over the adjacent field's values |

**None of those is a wrong number.** Every one is a right number fastened to the wrong thing. A checker that
verifies numbers against sources passes all of them, because both values are correct and both are sourced.

The generalisation, which came from a collaborator and is better than our version:

> **Nobody flags "she" as a claim requiring a source, because it doesn't read as an assertion — it reads as grammar.
> The problem isn't which lookups fail. It's which things register as needing a lookup at all.**

So: *of*, *vs*, a colon between a field name and a list, a pronoun, a citation key next to a sentence. Slots shaped
like syntax. **A claim-checker cannot fire on them because they never enter the
set of things considered checkable.**

**The idea (5 min).** The table and the quote, above.

**The board (2 min).** The facilitator adds today's own examples to the table.

**Your own (15 min), on your own, with your agent.** Take one paragraph of your own write-up: your session 3 verdict,
or the draft of your talk. Mark every **attachment**: every place two verified things are joined. Then check only the
joins, not the values: for each, open the artifact and confirm the two things belong together. Then try to make one
join checkable by code. One route: generate the sentence and its number from the same line of code, so they can't
come apart.

**Report back (6 min).** One join each that you checked, and what you found. *We do not have a good automated answer
to this and should say so.* If a student invents one, that is a genuine contribution and should be treated as one.

**Close (2 min).**

## Hour 3½ — The hand-off test

**20 minutes, then 16 to fix what it found.** Covers **stage 8 — Ship**, whose *done when* is the definition of done
for the entire pipeline: **a stranger can retrieve it and re-run it.**

That condition has a property the other seven do not. Every earlier stage you can assess yourself: you can read your
own falsifier, inspect your own control, run your own gate. This one you cannot.

> **You do not know whether your work is reproducible.** It is not a fact about your repository. It is a fact about
> a reader, and you are not one. **Only a stranger knows, and there is one sitting across the room.**

### The swap

**Twenty minutes. Trade repositories with another student. No talking.**

Not "review it." **Reproduce the headline number.** Clone or copy what they have, and try to get the value they are
about to present. You may read anything in the repo. You may not ask them anything: the moment you speak, you have
stopped being a stranger, and their artifact has been silently repaired by a conversation that will not exist for
the next reader.

Write down where you stopped and why. That list is their stage-8 defect list.

### Your own agent is not a stranger

Asking your own agent whether your work reproduces doesn't test anything. It has your paths, your installed packages
and everything you've told it, so it will reproduce the number and prove nothing. A **fresh** agent is a real
stranger: a new session in an empty folder, with no memory, given only the repository and the number to get. Start
one beside the swap, so it costs none of the twenty minutes, and put where it stopped on the same defect list.
*(Nexus's point, from reviewing this session as an agent, 2026-10-17.)*

### What it will find, in roughly this order

**`PREDICTED`**, never observed: this table is what we expect the swap to surface, drawn from ordinary hand-off
failures rather than from watching any student. Naming them in advance takes the sting out without spoiling the
exercise. **Log what actually stops people**; the real list will be better than this one.

| what stops the stranger | why the author never saw it |
|---|---|
| a file that was never committed | it exists on their machine, so it exists |
| an absolute path | it resolves for exactly one person |
| an undeclared dependency | installed months ago for something else |
| **a number typed into the prose rather than generated** | correct when typed, and now unfalsifiable |
| no seed, or a seed that is not actually used | the run reproduces for them because it is cached |
| a stale built artifact | the PDF opens and looks finished |
| a step that lives only in their head | it is one command, so it is not worth writing down |

**The fourth row is the one worth stopping the room for.** A number transcribed by hand into a sentence has no link
to the thing that produced it. It cannot go stale *visibly*: it just quietly stops being true. It is hour 3's defect
again, in a repository. This is the failure that [Quarto and its relatives exist to kill](./tools-by-stage.md), by
generating the number where it is read rather than copying it there.

### Then fix, and run your gate on your own work (16 min)

1. **Fix what the stranger's list found**, starting at the top.
2. **Run your hour 1 gate on your own pilot**, if its results file has the shape your checks read. Predict first:
   which of your checks will fail? If one fires, that is point 3 of your talk. If none can run on your data, say so in
   point 5.
3. **If there's time, the two mechanical fixes,** which are permanent:
   - **Provenance stamping.** Every output file records the commit hash and the config that produced it. Ten lines.
     It converts *"which run made this?"* from archaeology into a lookup.
   - **The staleness check.** Is the built artifact older than its source? One line, in `pre-commit`, not in your
     habits: a stale PDF is invisible precisely because it renders.

### The framing to leave them with

**"Done" is a property of the reader, not the author.** A stranger is not a hostile reviewer; a stranger is just
someone without your context, which, in six months, includes *you*. The person most likely to need your repository
to work is the person who wrote it, after they have forgotten everything.

*Facilitator note:* Brodeur et al. (IZA Discussion Paper 17645, 2025) gave teams of three a published social-science
article and its authors' own replication package, and asked them to reproduce a few of its numbers in a day. **94%
of human-only teams and 91% of AI-assisted teams did; 37% of the teams told to guide an AI minimally did.** All
twelve studies had known coding errors, so this says nothing about how often published work is wrong. What it does
say: a package written for strangers still stopped some human teams, and stopped most of the minimally guided AI
ones.

**What Brodeur establishes is the problem, not this remedy.** They measured no swaps, no checklists, and no training.
That twenty minutes of swapping helps is **our expectation, and `PREDICTED`**.

*If the cohort is odd-numbered or remote:* the facilitator takes the orphan repo. Do not skip anyone: the student
who does not get read is the one who most needs it.

### `OPEN` — depositing

Zenodo, a DOI, an archived release: correct, and mostly beyond a four-session course. **The honest floor is a public
repository with a tagged commit and a README that names the one command.** Teach that as sufficient, and name deposit
as the next step rather than a requirement, so nobody concludes that unarchived work does not count.

---

## Hour 4 — The finding you will defend

**45 minutes.** Each student presents for five minutes. The required structure:

1. **The question you could not stop thinking about**: whether you still cannot, and the bigger question it opened
2. **What you now believe, and why the room should believe it too**
3. What you got wrong on the way, and how you caught it
4. **What would change your mind**, stated as something that could actually happen
5. What your result does not support

**From hour 3½: say whether a stranger reproduced your number.** You present either way. If they did, you are
presenting a finding. If they stopped, say where, and what you changed; until someone else has obtained it, you are
presenting a claim about your laptop, and you should call it that.

**Point 2 is the graded one.** Not the size of the claim: its *warrant*. A student who defends something small with
a gate that could have killed it has done the thing. A student who defends nothing has not, however clean their kill
list. The strongest warrant is the one you built today: your gate, run on your own pilot, able to fail, and passed.

Point 3 still must be a real error with a real cost, not a rehearsed humility move, but it is now doing a different
job. It is not the deliverable. **It is the evidence that point 2 survived something.** A belief that has never been
shot at is not modest, it is untested.

And point 1 is not a warm-up. Session 1 asked what you could not stop thinking about. Sixty days later the honest
answers include *"I still can't"*, *"I can now, and here is what closed it"*, and *"no: a better question ate it."*
All three are good outcomes, and so is the swing you parked in session 1, if it has grown. Only silence is not.

### The failure mode this hour exists to prevent

> **Killing can build momentum, and from inside it the momentum is hard to see.**

Three sessions have trained you to pull claims down. The easy error now is to bury the next one because burying is
what you have been doing, not because it is weak. Session 3's verdict asked what you might be under-claiming. Ask it
again before you write your talk: *am I burying this because it is weak, or because I have spent the whole
course burying things?*

Underclaiming is not the safe error. It is the error that looks like rigour.

**The rule to state out loud before the talks begin:**

> **A correction you sequester is a correction you have made cheaper to make again.**

If the error goes in a quieter file, a later slide, an appendix, you have priced it lower than it cost. Put it where
the finding is. This applies to the instructors first. If we teach from a gate we built, we say plainly where it
failed, in the same breath as where it worked.

## Assessment

**One comparison, predicted first** (hour 1). Before anything runs, write down what each of your checks will do on
the exercise's data, and what the analysis will report with your gate and without it. Then run both. You are graded
on the prediction and the explanation, not on the run: a gate that caught nothing can still earn full marks, if you
predicted that honestly and can say why it caught nothing.

The comparison runs on an analysis, a gate and data you didn't make. A gate graded on your own analysis could be
tuned to catch whatever you planted, and a grader couldn't tell. On data you didn't plant, it can't. Then you run the
same gate on your own pilot (hour 3½), and that run is part of your talk's warrant (row 8). This is `vr.gate`
objective 4: practise on an analysis and a gate you didn't write, then apply the gate to your own.

Then **the gate** and **the talk**. The kill list is not the deliverable. It is the **warrant**. That distinction is
the whole course, and it is the last row of the rubric.

### Rubric

Every criterion names something a grader can see: a file, a message with its timestamp, a line of output, a sentence
in the talk. Each is **met** or **not yet**. *`DRAFT`, 2026-10-20: never used to grade anyone.*

| | criterion | met, when the grader can see… | not yet, for example |
|---|---|---|---|
| 1 | **The prediction came first** (`vr.gate` 4, the practice) | a message sent before the run, saying for each check whether it will pass or fail, and what the gated and ungated runs will report | written after the run; "it should be fine"; no call for some checks |
| 2 | **The comparison is explained** (`vr.gate` 4, the practice) | what the ungated run let through, as the number or decision it reported, and why the gate caught it or missed it, in terms of what each check read; consistent with the gate's actual output | "the gate caught an error"; an explanation the output contradicts |
| 3 | **Three kills, each a check that runs** (`vr.gate` 0–3) | three functions in the gate, each with a name a stranger could use, an `EARNED` line naming an artifact (a file, a line, a number), and a self-test line showing it fire | a kill with no case; a slogan for a name ("bias"); a check never seen to fire |
| 4 | **Broken once, unlike** (`vr.gate` 5, 6) | one defect planted in the data file, of a kind none of the checks was written for, and the result written down either way; if nothing fired, the blind spot named; and one check named that passed without being able to see a defect, with the reason | a plant only in the arrays the self-test already uses; no result recorded |
| 5 | **One join checked** (hour 3, `PROPOSED`) | a paragraph of the student's own write-up with its attachments marked, and at least one join checked against its artifact, with what that showed | values checked, joins not; no artifact opened |
| 6 | **Someone else got the number** (hour 3½) | the stranger's stop list, and in the talk either "reproduced" or where it stopped and what changed | the stop list skipped; a failed hand-off not mentioned |
| 7 | **An honest account of what went wrong** (point 3) | a real error, its cost, and the artifact that showed it | a humility move with no artifact; an error with no cost |
| 8 | **A finding, with a gate that could have killed it** (point 2; `vr.gate` 4, applied to their own work; the `PROPOSED` *defend a finding*) | one sentence of belief, with a direction and a number with its interval; the gate entry or check that could have killed it, shown to have run and not fired; and what would change the student's mind, stated as something that could happen | a beautiful kill list with nothing believed at the end; a belief no check could have touched; "I'd change my mind if it felt wrong" |

**Row 8 outranks the others.** A defended small claim beats an undefended large one, and beats a beautiful kill list
with nothing standing at the end of it. *"Nothing yet, because…"* can meet row 8, if the gate is real and the reason
is a result rather than a feeling.

## After the course

Students leave with a gate that has three to six entries, and code that runs them. Ours is much longer, and every
entry got there the same way. The useful thing is not the list's length. It is that every entry is a scar with a test
attached, and that theirs will grow the same way: one expensive afternoon at a time.

## `OPEN`

- ~~The target bank's session 4 target (judge agreement) is used by no session~~: **dropped from the bank
  2026-10-20.** Session 4 works on its seeded exercise and the student's own pilot.
- **`OPEN`: whether the assessed comparison must also run on the student's own pilot.** As written it is assessed on
  hour 1's exercise, where nobody can plant what their own gate catches, and run on the student's pilot in hour 3½'s
  fix block where possible.
- **`OPEN`: repeaters.** Hour 1's exercise has no variant. A repeater knows its answer, so keep repeaters out of
  first-timers' pairs for hour 1, as for any seeded exercise.
- **`DRAFT` (2026-10-20): hour 3 went from 37 minutes to 30**, and the hand-off fix from 18 to 16, so that the content
  fits the house's 201 minutes with the house's buffer. The old clock ran 210 minutes of content with a 4-minute
  buffer.
- ~~*"Reproduction is a precondition for hour 4"*, followed by a fallback for when it fails~~: **resolved 2026-10-20.**
  Everyone presents; the hand-off decides whether you present a finding or a claim, and you say which.
- ~~Hour 3 has no exercise with a known-good answer… decide whether it shrinks to 40 minutes.~~ **RESOLVED
  2026-09-08**, and the freed time went to hour 3½, the hand-off test, whose answer is known: either the stranger
  reproduced the number or they did not.
- **Not piloted.** No cohort has run this session. Hour 1's exercise has never been run with students or with agents,
  and every timing above is a prediction.
