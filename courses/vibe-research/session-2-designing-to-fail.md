# Session 2 — Designing something that can fail

> **Clock:** [the four clocks](../../docs/session-clocks.md) — S2 needs **247 min against 201**, the worst in the course. Hour 4's pre-registration is **not completable in 50 minutes as written**, Hour 3's old ordering defect (running a "planned test" that hour 4 had not yet specified) is fixed as of 2026-09-29: hour 3 uses a one-line *expected* test, and hour 4 formalises it.

**Status: `DRAFT`, 2026-08-25; hour 3 rewritten 2026-09-29, and hours 1 and 2 rewritten 2026-09-30, each around an external case.** Four hours. Second of four.
**Standards covered:** `vr.prereg`, *identify the confounds that separate your conditions before
your variable does*, *select a control that is capable of failing*.

**Walks in with:** a claim with a direction and a falsifier, a verified citation trail, and one
earned kill from session 1, plus a two-condition design for this session's target, drafted as
pre-work (not yet written: see Open).
**Walks out with:** a pre-registration their agent has attacked, the break log, and a second kill.

---

## The one idea

Session 1 taught students to doubt a *number*. Session 2 teaches them to doubt a *design* — which
is harder, because a broken design produces numbers that look fine.

**Three ways a design fails before it runs**, and each gets an hour:

1. Something other than your variable separates your conditions
2. Your control cannot fail
3. Your test cannot reject

Every one of these produces clean, publishable-looking output. None is visible in the result.

## Hour 1 — The confound that got there first

Covers *identify the confounds that separate your conditions before your variable does*. **50
minutes.**

**If something other than your variable can tell your conditions apart, it can produce your result
on its own.** That something is a *confound*. The output it produces looks exactly like a finding.

Bring the two-condition design you drafted as pre-work. The last block runs on it.

**The case (3 min).** A published result, read aloud: a large dataset whose conditions were
assigned by design, and the score a model reached on it. Poll the room: *does the score show that
the model can do the task the dataset was built to test?* Take the vote and don't discuss it yet.

**What else separates the conditions? (8 min), in pairs, with the first handout.** It gives you
the instructions that each condition's items were produced under, exactly as printed, and nothing
else. Before you see a single item, write down:

1. every way the conditions could differ *other than* the thing the dataset is meant to test;
2. for each one, whether it alone could let a reader get the label right;
3. the one you would bet on, and why.

Rank the list and commit to it on paper. The next handout tests it.

**Label it blind (6 min), second handout.** Items from the case, each with part of it withheld.
Label every item on your own, without talking. Then score yourself against the key and put your
count on the board. The room's pooled count is the number that matters, not anyone's own score.

**The reveal (6 min), third handout.** What the published analysis found. Check it against the list
you wrote. Then ask the question this hour adds: **what does this do to the headline score?**
Answer with numbers, not adjectives.

**The rule to leave with (5 min), fourth handout.** If time is short, this block shrinks to the
rule itself:

> **Adjusting for a difference is not the same as removing it.**

You can filter out the items that show a difference. You can *residualise* it: subtract from your
measurement the part that the difference predicts, usually by fitting a straight line. Either way
you remove what that adjustment can see. You do not make your conditions the same population.
After any adjustment, ask again whether something could still tell your conditions apart.

**Your own design (17 min).** Take your design and write:

- **how each condition is produced:** who or what makes its items, from what, and in what order.
  Then how each is run: when, on what machine, with which model version and settings. *"It ran
  differently on my machine"* is not a support issue. It is an uncontrolled variable;
- **every difference between your conditions other than the variable**, including differences in
  how they are run and recorded, such as file names, IDs and order;
- **the rank:** for each difference, *could this alone produce my predicted result?* Most people
  find at least one that could. The honest ones find that their condition label is partly a
  *topic* label;
- **the blind test for your top candidate:** could a reader, or your agent, tell which condition
  an item came from without the variable? If you plan to adjust for it, what would the adjustment
  leave behind?

Keep the list. You will need it again today.

*Facilitator note —* **`PREDICTED`**, not piloted: most pairs will write a list of differences and
no ranking. Push each pair to commit to a ranking, with a reason for the top item, before the second
handout lands. The hour pays off when the second handout is scored, and only for the pairs who
ranked first.

*The case, its sources, the handouts, the key, the reveal, the clock, and what **not** to use in
this hour are in the **facilitator pack**, not in this repository. Learners get full citations for
every source at the reveal, once their own answers are on paper.*

## Hour 2 — A control that is capable of failing

Covers *select a control that is capable of failing*. **42 minutes.**

**A control you expect to pass is not a control. It is a decoration.**

A negative control is a run with everything except the thing you think you are measuring, put
through the identical pipeline. Its whole value is that it *can* come back positive. So the question
to ask of a control is not "did it pass?" It is **"what would its failure have looked like, and
would anyone have been able to see it?"**

**The case (4 min).** A published claim, read aloud: a striking finding from a large, carefully
collected sample, and the one sentence in which the authors report their negative control. The
control is reported as passing. Poll the room: *does the passing control make you more confident in
the finding?* Take the vote and don't discuss it yet.

**What would failure look like? (8 min), in pairs, with the first handout.** It gives you the claim,
the control sentence exactly as printed, and a table of measurements with one column left blank:
the controls. Before anything else is handed out, write down:

1. what the negative control is: what goes through the pipeline, and what is left out;
2. what its failure would look like **in these columns**, as numbers rather than adjectives;
3. what you would conclude about the headline if it failed;
4. whether the published report lets a reader see which of those happened.

Write it now, while it is cheap. Once the next handout lands, you can no longer write it honestly.

**The blank column (8 min), second handout.** It fills in the controls. Check them against what you
wrote for (2). Then ask the question this hour adds: **what does the control's failure do to my
headline number?** Answer with the number, not with an adjective.

**What a control's success buys (4 min), third handout.** A later design, with controls built in
from the start, each of which could have failed. Ask the second question: **what does the control's
success do to my headline number?** Find out whether anything is left standing, and why you are
allowed to believe it.

**Your own control (8 min).** Take your own design and, for its control, write:

- what the control is, and what it leaves out;
- what its failure would look like in your output, as numbers;
- what its failure does to your headline number;
- what its success does to it.

Then the question the case turned on: **what is the blank for your pipeline?** It is the run that
has everything except the thing you think you are measuring. If you cannot describe its failure, you
do not have a control. If its success is guaranteed, you have a decoration.

**A harder variant (10 min, the first thing to cut).** A positive control proves the *instrument*.
It cannot prove the *scope*. The last handout shows one positive control run under more than one
condition. Ask of it, and then of your own: **under what conditions did you check your positive
control, and are those the conditions your real data lives in?**

*Facilitator note —* **`PREDICTED`**, not piloted: most pairs will write a vague (2) the first time,
something like "the control would show something". Push for a number in a column. The hour pays off
when the second handout lands, and only for the pairs who committed on paper first.

*The case, its sources, the handouts, the reveal, the clock, and what **not** to use in this hour
are in the **facilitator pack**, not in this repository. Learners get full citations for every source
at the reveal, once their own answers are on paper.*

## Hour 3 — A test that cannot reject

Covers `vr.prereg` objectives 0–2, 5. **The centrepiece. 50 minutes.**

**The habit this hour installs:**

> **Before trusting any test, ask whether it could possibly have rejected, and prove that it could,
> by building the data that would make it.**

A test that cannot reject produces a perfectly ordinary number. Nothing about the output looks wrong.
The only way to find out is to try to make the test say *yes*.

**The case (5 min).** One sentence from a published paper, read aloud: a comparison between two
groups, a row of p-values, and a conclusion drawn from them. Poll the room: *is this evidence for
the conclusion?* Take the vote and don't discuss it yet.

**Make it reject (12 min), in pairs, with the paper open.** One question only: **what data would
have made this test come out the other way?** Build it. Describe it, sketch it, or have your agent
generate it, then check your agent's answer by running the test on it rather than taking its word.
Some pairs will find that no such data exists, and they should be able to say *why*.

**The contrast (8 min).** The same paper also contains a second test, run by the same authors on the
same data. Repeat the question for that one. **One of the two tests could have come out the other
way. Only one of them is evidence.** Then read the authors' own sentence about the first test, and
ask what the reader-facing conclusion claimed that the numbers never could.

**Your own test (15 min).** Hour 4 writes the formal pre-registration, so this is a draft. Write one
line: *the test I currently expect to use for my claim.* Then produce two datasets, synthetic, small
and made with your agent:

1. one that **should** make your test reject, and run the test on it;
2. one that **should not**, and run the test on it.

If the first one won't reject, however extreme you make it, you have found a test that cannot reject
before it cost you anything. That is a success. Hour 4 is where you replace it.

**Debrief (7 min).** Which tests in the room could not be made to reject? What was the mechanism in
each? Keep the list. **Don't name a rule for them.** The room should leave with the question, not a
checklist item, because the question transfers and the checklist doesn't.

**Close (3 min).** Your agent will review your design in hour 4. It shares every assumption you gave
it, including the one that says your test works. **A reviewer that shares your assumption returns
confidence, not coverage.** The only reviewer that doesn't share it is the data you built to break
the test.

*Facilitator note —* **`PREDICTED`**, never observed: most students' own tests *will* be able to
reject, and they'll be disappointed. Say plainly that this is the good outcome. The hour pays off for
the one or two students whose test cannot, and for everyone else it pays off later, the next time a
result looks clean.

*The case, its pointer, the reveal, and what **not** to use in this hour (one mechanism looks
tempting and would give away session 4's exercise) are in the **facilitator pack**, not in this
repository.*

## Hour 4 — Pre-register, then have your agent attack it

Covers `vr.prereg` 3–4, 6.

Students write the real pre-registration. The house format:

- primary statistic, its estimator, **the exact formula**
- decision rule as branches: this result → this conclusion
- **the outcome you are hoping for, named as a stake**
- **what you have already seen**, and how it constrains what you may claim from it
- sensitivity analyses, committed to in advance, all of them reported
- power, honestly, including which direction a null does and does not support
- one **non-goal** — a nearby analysis you are choosing not to run, and why

Then they hand it to their agent with one instruction: **break this.** Not "review" — *find the
version of this design that produces my preferred answer regardless of the truth.*

The **break log** is the deliverable, and the second kill comes out of it.

*Instructor note:* the fourth bullet is the one people omit, and it is the one that makes a
pre-registration honest rather than merely early. A student who has already looked at their data
and does not say so has written a summary, not a prereg.

---

## Between sessions

The gate-sparring companion, now with two kills to work against. Students run their design past it
and log what it challenged.

**Homework:** execute a pilot — smallest version of your design that could produce a signal — and
bring both the result *and* the noise-run from hour 3.

## Open

- ~~Whether hour 3's noise exercise needs a supplied harness~~: superseded. The 2026-09-29 hour 3
  has students build their own two datasets with their agent; no harness is needed.
- **RESOLVED 2026-08-25 (Thomas):** no lab specifics. The failure state this hour originally used
  is reproduced synthetically in `exercises/seeded-01-the-approved-analysis/` for session 4, where
  students track it down rather than being shown it.
- ✅ **RESOLVED 2026-09-24 (Thomas): option (b).** Session 2 gives up that case, and session 4 keeps
  seeded-01 as the discovery it was built to be. Option (c) was never available: cohorts are rolling
  *and prereq-chained*, so every session-4 room has already taken session 2.
- ✅ **DONE 2026-09-29:** hour 3 is rewritten around an external, published test that cannot reject,
  one whose mechanism is **not** seeded-01's, and around the *habit* rather than a key (Thomas,
  2026-09-24: soften the closing rule). **This page must never state seeded-01's specific mechanism
  or check**: session 4 depends on students working it out. The case itself is in the facilitator
  pack.
- ✅ **DONE 2026-09-30, pending review:** hour 2's earlier worked case came from the lab's own
  research, which the 2026-08-25 ruling excludes, and it sat too close to session 4's exercise. Hour 2
  is now built on an external, published case whose negative control was reported as passing. Its
  mechanism is unrelated to seeded-01's. The case, its sources and the reveal are in the facilitator
  pack. **Not piloted.**
- ✅ **DONE 2026-09-30, pending review:** hour 1's earlier worked case also came from the lab's own
  research, which the 2026-08-25 ruling excludes. Hour 1 is now built on an external, published case
  whose conditions were assigned by design, and students work on it with their own hands before the
  reveal. Its mechanism is unrelated to either seeded exercise's. The case, its sources, the key and the reveal are in the facilitator pack. **Not
  piloted.** Its blind-labelling handout was drawn at random with a recorded seed and has never been
  run with a room.
- **Open: hour 1 assumes the design draft is pre-work.** `docs/session-clocks.md` (H1 −15) moves it
  there: the target and a one-page template are posted about five days ahead, with *"arrive with a
  two-condition design."* That template and posting do not exist yet. Until they do, a student who
  arrives without a design does hour 1's last block on a partner's.
