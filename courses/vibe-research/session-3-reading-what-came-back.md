# Session 3 — Running it, and reading what came back

> **Clock:** this session's clock is on this page, [below](#the-clock): 201 minutes of content in a
> 240-minute session, rebuilt 2026-10-14 and not yet piloted. [The four clocks](../../docs/session-clocks.md)
> still shows this session's old plan (252 minutes against 201) and the cuts it needed. For session 3,
> this page replaces it.

**Status: `DRAFT`, 2026-08-25; rebuilt 2026-10-14 around published cases and a new discovery
exercise.** Four hours. Third of four.
**Standards covered:** *distinguish a per-sample statistic from a rank-bounded one*, *reconcile a
result with the estimator that produced it*, `vr.verify-number` objective 2, and *verify that a search
which returned nothing actually ran*, from [Course: Execution and Analysis](../../standards/vibe-research/README.md).
Two objectives this session teaches are not written as standards yet; they are marked `PROPOSED` in
hours 3 and 4.

**Walks in with:** a pre-registration their agent has attacked, the break log, two kills, and the
pilot from session 2's homework, with both synthetic runs from session 2 hour 3.
**Walks out with:** a result, an honest account of what it does not support, **a verdict on whether
they have something** (what they now believe, and its limits), the check for the one thing they nearly
explained away, and a third kill.

---

## The one idea

Sessions 1 and 2 taught you to doubt a *number* and a *design*. Session 3 is where your own data
comes back, and the job changes from doubting to **reading**.

Your design can be fine and your run clean, and the number in front of you can still be something
other than what you think it is:

1. **It can be measuring your sample size.** Some statistics move when you collect more, even when
   nothing else changes.
2. **It can be a different statistic from the one its name promises.** You computed A and reported
   it as B.
3. **What you set aside can matter as much as what you kept.** Every analysis explains some things
   away. Each of those is a decision, and it can be wrong in either direction.

The first two make you careful. The third is the reason to be careful at all: **care is how you find
things, not only how you avoid being wrong.** Hour 4 puts the day together: what your result does not
support, and what you now believe.

## The clock

*`DRAFT`, 2026-10-14. Not piloted: every timing here is a prediction.*

| clock | block | min |
|---|---|---|
| 0:00 | Opening. Orientation and hour 1's pairs are posted the night before; confirm them, don't brief | 5 |
| 0:05 | **Hour 1** — the number that was measuring your sample size | 48 |
| 0:53 | **break**, "back at 0:58". Post any change to hour 3's pairs | 5 |
| 0:58 | **Hour 2** — the statistic that is not what its name says | 45 |
| 1:43 | transition | 3 |
| 1:46 | **Hour 3** — would you sign it? *(the discovery hour)* | 50 |
| 2:36 | **break**, "back at 2:41". Post hour 4's new pairs and the template | 5 |
| 2:41 | transition | 3 |
| 2:44 | **Hour 4** — the limits section first, then the verdict | 48 |
| 3:32 | **Hour 4½** — the third kill (straight on, no transition) | 10 |
| 3:42 | overrun buffer, **unspent** | 13 |
| 3:55 | close | 5 |

**201 minutes of content** (48 + 45 + 50 + 48 + 10). The buffer is not a block: nothing is scheduled
into it.

**Pairs.** Hours 1 to 3 run in the same pre-assigned pairs, posted before the session (hour 1's pair
work comes before any break). Hour 4's exchange needs a reader who hasn't seen your work all day, so
hour 4 gets new pairs, posted at the second break. One named room per pair; the facilitator takes any
odd one out. See [running a session](../../docs/running-a-session.md).

**Commit, then reveal.** Every hour has a step where you write your answer down before anything is
revealed. Online, that means sending it to the facilitator (a direct message is fine) before the next
handout is posted. During those steps your agent and search stay closed. That's an honour rule, and
it's part of the exercise.

---

## Hour 1 — The number that was measuring your sample size

Covers *distinguish a per-sample statistic from a rank-bounded one* (taught here more widely: from any
statistic that moves with a count) and *reconcile a result with the estimator that produced it*.
**48 minutes.**

Some numbers measure the world. Some also measure how much of it you looked at, and the second kind
looks exactly like the first.

**The case (4 min).** A published finding, read aloud: places that stand out on a map of one health
measure, and what they have in common. Poll the room: *what explains it?* Take the vote and don't
discuss it yet.

**Sort the eight (8 min), on your own, agent and search closed.** The first handout is a results
summary from one simulated step-by-step pilot: eight statistics, each with its number. For each one,
write:

1. **safe to report as-is**, or **needs care**;
2. if it needs care, **which count moves it**: questions, runs, samples per question, or prompts tried;
3. how sure you are, from 50% to 100%.

Send it to the facilitator. That's your prediction.

**Make them move (12 min), in pairs, with your agents.** The second handout is a prompt. Your agent
builds a pilot in which nothing about the model changes, with true values you can see, and computes
all eight statistics at 10, 30, 100 and 300 questions, many times over, plus several values of any
other count a statistic depends on. Read its code before you believe its table: does it run, and are
the true values the ones you asked for? Then put the table next to your sort.

**The reveal (6 min), third handout.** The key, a published source for every statistic, and the rest
of the case.

**The rule, and the fix (4 min).**

> **An average, over items, of something each item has on its own is safe: more items only make it
> steadier. A number that describes the set as a whole, or that leans on a second count (runs,
> samples, tries), can move when that count grows, even when nothing about the world has changed.**

A statistic that needs care isn't banned. It's unsafe when the counts behind it differ. Three fixes,
best first:

- **compare at the same counts:** cut the bigger group down to the smaller one's size, or fix every
  count in advance and keep it the same for everything you compare;
- **switch to an average:** each group's own number with its interval, rather than one number picked
  or built from the whole set;
- **report the counts with the number**, so a reader can see what it was measuring.

And the other way round: a small group's big number isn't noise just because the group is small. Its
interval tells you how much of it the size can explain.

**Your own pilot (11 min).** List every statistic in your pilot, starting with your
pre-registration's primary statistic. Sort each one the same way. For each that needs care: are the
groups you compare the same size, in every count that matters? If not, write down which fix you'll
use. If everything in your pilot is an average, look at what you planned next: a breakdown by
subgroup, the best of several prompts, a spread across samples. That's where the care column fills
up.

**Close (3 min).** One line each in the chat: the statistic in your work most likely to be measuring a
count, and which count.

*Facilitator note —* **`PREDICTED`**, not piloted: most people will fill in a column for every
statistic and leave the count blank. Push for the count, not just the column.

*The case, the eight statistics and their key, the prompt, the sources, the clock and what **not** to
use in this hour are in the **facilitator pack**, not in this repository. Learners get full citations
for every source at the reveal, once their own answers are on paper.*

## Hour 2 — The statistic that is not what its name says

Covers `vr.verify-number` objective 2 (*identify the estimator the artifact used, and confirm the
citing text names the same one*) and *reconcile a result with the estimator that produced it*.
**45 minutes.**

People name a statistic after what they think it means. The name is what travels; the formula is what
was computed. When two results share a name and not a formula, comparing them compares the formulas.

**The case (4 min).** Two scores for the same task on the same test set, read aloud. Poll the room:
*which is better?* Take the vote and don't discuss it yet.

**What's inside the name (7 min), in pairs, agents and search closed.** The first handout defines the
statistic in one paragraph, the way it's usually written. Before that definition can run on real text,
someone has to make choices. List every choice that could change the number, rank them by how much you
think each could move it, and bet on the biggest. Send your list in.

**Name, then settings (12 min), in pairs, with your agents.** The second handout has four short
pieces of output and the reference texts they're scored against, written for this exercise. Ask your
agent for the score **by name only**. Then ask it to compute the score again, changing one setting at a time, and to
print every number beside its settings. Note whether your agent ran code or estimated. Both happen.

**The reveal (6 min), third handout.** What the two numbers in the poll were, and the published paper
that explains them.

**The rule (3 min).**

> **A statistic's name is a promise. Its formula is what you computed. Report the formula with the
> number.**

**Your own statistics (11 min).** Open the "exact formula" line of your pre-registration. For each
statistic in your pilot:

1. write the exact formula, **including the rule that decides an answer counts as correct**: how the
   final answer is pulled out of the response, and what is normalised first (case, spaces,
   punctuation, number formats);
2. **predict** whether your agent, given only the statistic's name, will compute the same number;
3. have it implement the statistic from the name alone, run both versions on your pilot, and compare.

Where the two disagree, the name was doing work your formula doesn't support. Then the harder
question: **what did your preprocessing remove before your statistic looked?**

This is the kind of comparison the course assesses (see [Assessment tie-in](#assessment-tie-in)):
two analysis choices on the same data, predicted first.

**Close (2 min).**

*Facilitator note —* **`PREDICTED`**, not piloted: pairs will list the obvious choices first and
rank them wrongly. The settings run is where the ranking gets tested, and only for pairs who committed
to one.

*The case, the handouts, the scores computed for the second handout, the sources, the clock and what
**not** to use in this hour are in the **facilitator pack**, not in this repository.*

## Hour 3 — Would you sign it?

`PROPOSED` objective (2026-10-14), not yet a written standard: *judge what an analysis set aside: say
what it would mean if it were real, then test the explanation with a check you predicted first,
whichever way it comes out*. **The discovery hour. 50 minutes.**

Everything so far today has been about not believing something false. This hour adds the other
direction: **not throwing away something true**. Scepticism protects you from the first mistake and
does nothing about the second. Only a check does, and a check can come out either way.

> **When an analysis explains something away, yours or anyone's, say what it would mean if it were
> real. Then write down what the explanation predicts, and check it.** If the explanation survives,
> you've learned it was right. If it doesn't, you may have a finding.

**The case (5 min).** A measurement from the history of science, read aloud up to the moment of
decision: an instrument that reads too high, everywhere, and the people who built it. Poll the room:
*what would you do with the excess?* Take the vote. The answer comes at the end of the hour.

**The exercise (2 + 25 min), in pairs, with your agents.** Go to your pair's room and open
[*The prompt that made no difference*](exercises/seeded-03-the-prompt-that-made-no-difference/review.md)
(in a clone: `exercises/seeded-03-the-prompt-that-made-no-difference/`). It is a careful analysis of a
step-by-step pilot, with its data and its write-up. Your task is at the end of the write-up: decide
whether you would sign its conclusion and its recommendation. It has four steps, of about 5, 3, 12
and 5 minutes. **Step 2 is the one that matters: both predictions written down before you check
anything.** One of you shares a screen and drives an agent; the other keeps the written predictions.

Your agents may give you a verdict quickly. That's fine. The hour isn't "what did the agent say?"
It's the prediction you wrote first, and whether you can explain what the check showed.

**Debrief: Look and Check (8 min), whole room.** Each pair gives one row: what they looked at, what
they ran, and what it showed. Then the table those rows fill in:

| | the move | the failure it prevents | the failure it invites |
|---|---|---|---|
| **Look** | say what the set-aside thing would mean if it were real | burying a finding as a nuisance | chasing noise you like |
| **Check** | run it as a claim that can fail | publishing what you hoped | burying it again |

Neither one is the safe one. **Scepticism has a cost, and it is paid in findings you never made.**

**The reveal (5 min).** What the people in the opening case actually did, and the answer to the poll.

**Your own (5 min).** In your own pilot, find one thing you were about to explain away: a subgroup
that behaves differently, a result you were going to call noise, a pattern you had already put in
your limits. Write three lines:

1. what it would mean if it were real;
2. the check that could kill it, and the result that would;
3. what you predict that check will show, and how sure you are.

That's your homework, and it may be your finding.

*Facilitator note —* **`PREDICTED`**, never observed: some pairs will stop as soon as their agent
gives a verdict. Ask for the prediction they wrote before it, and for the explanation after it. Name
it out loud when a pair turns an explanation into a claim that could fail.

*The opening case, its sources and its reveal, and what **not** to use in this hour are in the
**facilitator pack**. The exercise's own facilitator notes, with its answer, are kept privately and
shared after the session.*

## Hour 4 — Write the limits section first, then say what you believe

Covers *verify that a search which returned nothing actually ran*, applied to a null result, and a
`PROPOSED` objective (2026-10-14): *state what a result does not support, and what you now believe*.
**48 minutes.**

**The limits section isn't the apology at the end. It's the part that makes the rest citable**, and
it's the part least likely to travel with your result.

**The case (4 min).** A short published text, read aloud, and one sentence of the kind that later cited
it. Poll the room: *does the text support the sentence?* Take the vote and don't discuss it yet.

**Write its limits (5 min), in pairs, agents and search closed.** The first handout gives the text.
Write its limits section in three lines: what it does not support. Send it in.

**The reveal (5 min), second handout.** How the text was cited, counted by people who went and looked.

> **A finding travels. Its limits section doesn't.**

The same mechanism has been measured across a whole literature. Greenberg (2009) reconstructed the
citation network behind one biomedical claim: **242 papers, 675 citations, and 220,553 citation paths
supporting it.** He shows how the belief gained authority it hadn't earned: **bias** (citing the
supportive work and not the critical work), **amplification** (citing reviews and other papers that
had no data on the claim, as if they were evidence for it), and **invention** (a hypothesis turned
into a fact by citation alone).

> Greenberg, *BMJ* 2009;339:b2680 · free full text: <https://pmc.ncbi.nlm.nih.gov/articles/PMC2714656/>

So writing the limits section isn't defensive. It's the only part of your work that tells the next
person what they're *not* allowed to build on top of it. Write it as if it will be the only thing that
survives, knowing it probably won't be.

**Your limits section, first (10 min), on your own.** Use the template,
[`templates/limits-and-verdict.md`](./templates/limits-and-verdict.md), posted at the break. Write the
limits for your own result **before** you write the result: for each limit, the claim it rules out.
Put the one that matters most first.

**Hand it over (10 min), with your new partner.** Give your partner your limits section **and nothing
else**. They write one answer: *what would you now be entitled to claim?* Then compare it with what
you wanted to claim. **The gap is this hour's deliverable.** Either your limits rule out something you
were about to claim, or your partner found a claim your limits don't rule out. Then swap.

**Say what you believe (12 min), on your own.** The verdict, in the template:

1. **What I now believe**, in one sentence, with a direction, and a number with its interval. *"Nothing
   yet"* is allowed, if you say why.
2. **Which branch of my decision rule** (from session 2's pre-registration) the result landed in.
3. **Did the hypothesis fail, or the measurement?** *"The prediction failed"* is a finding. *"My
   statistic wasn't measuring what I named it"* is a repair. Report them differently: mixing them up
   lets a real null hide behind a fixable bug, and lets a bug get published as a null.
4. **If the result is null: could my test have seen the effect I predicted?** Session 2 had you build
   data that should make your test reject. Build it again at the effect you predicted and the size you
   ran. If the test can't see that, your null isn't a no. It's a silence.
5. **What it does not support:** the first line of your limits section.
6. **What would change my mind.**
7. **What I might be under-claiming.** After two sessions of killing things, it's easy to undersell
   the next one. Check that too.

**Close (2 min).** Your verdict sentence, one line, in the chat.

*Facilitator note —* **`PREDICTED`**, not piloted: the hand-over produces the biggest surprise of the
day for most people, because their partner claims something their limits never ruled out. Leave time
for the swap.

*The case, its handouts and sources, the clock and what **not** to use in this hour are in the
**facilitator pack**, not in this repository.*

## Hour 4½ — The third kill

**10 minutes, straight after hour 4.**

Pick the thing from today that would most have changed your verdict if you had missed it: a statistic
that was measuring a count, a name doing a formula's work, the discrepancy you nearly explained away,
or the limit your partner didn't read. **A kill can point either way.** A finding you nearly threw out
counts as much as a claim you nearly believed.

Write it in the template, in the three steps from session 1:

1. what happened, with the artifact that showed it;
2. the class it belongs to, named;
3. a check someone else could apply without your context.

That's your third kill. Session 4 builds your gate out of all three.

## Assessment tie-in

One comparison, predicted first. Before anything runs, write down what you expect to differ
between two **analysis choices on the same data**: two estimators, or the same data with and
without a preprocessing step. Then have your agent run both. Report both, say which you think is
right and why, and say whether your prediction held. You are graded on the prediction and the
explanation, not on the run.

## Between sessions

1. **Run the check you wrote at the end of hour 3**, on your own data. Write your prediction first,
   run it, and bring the result whichever way it went. If it holds, it may be the finding you defend
   in session 4.
2. **Finish the template:** the limits section, the verdict and the third kill.
3. **Your sparring partner** (session 1's prompt, in your own agent), now with three kills. Give it
   your verdict and ask it both ways: what would break this, and what would show I'm right?

## Open

- **`OPEN`: which data session 3 runs on.** Students bring the pilot from session 2's homework; the
  [target bank](./the-target-bank.md) gives session 3 its own question (step-by-step). Hour 3's
  exercise is a step-by-step pilot, so the bank's question is met there either way.
- **`OPEN`: a fallback dataset for anyone without a pilot.** None exists yet. Until it does: hours 1
  and 2 on a partner's pilot, and hour 4 on your own verdict about the hour 3 exercise's result.
- **`OPEN`: whether hour 2's "your own statistics" block is the first comparison done together in
  class**, which the [course README](./README.md) leaves open.
- **`DRAFT` (2026-10-14): session 3 does not return to session 1's sealed prediction.** Session 1 opens
  it in its own hour 4. Session 3's verdict works from session 2's pre-registration instead.
- **`OPEN`: whether Build GRIM is set between sessions 3 and 4.**
- **Not piloted.** No cohort has run this session. The hour 3 exercise has never been run with
  students or with agents, and every timing above is a prediction.
