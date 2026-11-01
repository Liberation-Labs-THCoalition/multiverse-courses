# Glossary — the course's words, and where each one first appears

> **Each term links to the place in the course where it first appears,** so you can read it where it is used.
> The definitions are short on purpose: the page each term links to is where it is taught.

**Status: `DRAFT`, 2026-11-01.** 37 terms, from the session pages, the spine and the course README.
Every definition was checked against the passage it links to. A word you think belongs here and is missing is
a gap in this page, not a word the course does not use.

---

**[ablation](README.md)** — A comparison of two runs that differ in one thing, with that one thing removed in one run. The session pages call it a *comparison*; the word is defined here because papers use it.
*First appears in:* the course README.

**[adjustment set](tools-by-stage.md#tools-and-there-are-good-ones)** — The variables you statistically control for so your comparison is not confounded; a tool like dagitty finds the minimal such set and shows when adjusting for one would break the design.
*First appears in:* Tools by stage, “Tools, and there are good ones”.

**[agent](README.md)** — A program that pursues a goal using tools such as web search, keeps notes between runs, and can act without a person at every step; every student arrives with one.
*First appears in:* the course README.

**[bootstrap](toolset.md#must-haves--no-alternatives-offered)** — A resampling method that estimates a statistic's uncertainty by repeatedly re-sampling your data, with replacement, and recomputing the statistic; the course uses it with BCa to build confidence intervals.
*First appears in:* Toolset, “Must-haves — no alternatives offered”.

**[Cohen's d](tools-by-stage.md#6--analyse--where-the-tool-choice-does-the-work-for-you)** — A common measure of effect size; at small sample sizes it is biased upward, which is why the course prefers Hedges' g, a corrected version.
*First appears in:* Tools by stage, “6 · Analyse — where the tool choice does the work for you”.

**[collider bias](tools-by-stage.md#tools-and-there-are-good-ones)** — A bias that appears when you adjust for a variable that both your exposure and your outcome affect; tools like dagitty make it mechanical to spot.
*First appears in:* Tools by stage, “Tools, and there are good ones”.

**[confidence interval](toolset.md#categories--pick-one-know-why)** — The range the true value plausibly sits in, given how much data you have; a bare point estimate with no interval hides both its width and any bias.
*First appears in:* Toolset, “Categories — pick one, know why”.

**[confound](session-2-designing-to-fail.md)** — Something other than your variable that differs between your two conditions and could, by itself, produce your result; the output it makes looks just like a finding.
*First appears in:* Session 2.

**[DAG](tools-by-stage.md#tools-and-there-are-good-ones)** — A diagram of the causal structure between variables; a tool like dagitty draws it and uses it to find valid adjustment sets, but it is only as good as the diagram you supply.
*First appears in:* Tools by stage, “Tools, and there are good ones”.

**[decision rule](session-2-designing-to-fail.md#hour-4--pre-register-then-have-your-agent-attack-it)** — In a pre-registration, the branches that say which result leads to which conclusion, including the result that would make you believe your own claim.
*First appears in:* Session 2, “Hour 4 — Pre-register, then have your agent attack it”.

**[effect size](toolset.md#categories--pick-one-know-why)** — A number for how large a difference or relationship is; at small sample sizes it can be inflated, which is why the course prefers libraries that report it with a confidence interval.
*First appears in:* Toolset, “Categories — pick one, know why”.

**[estimator](session-2-designing-to-fail.md#hour-4--pre-register-then-have-your-agent-attack-it)** — The specific formula or function that produces a number; when two results share a name but not an estimator, comparing them really compares the formulas, not the concept.
*First appears in:* Session 2, “Hour 4 — Pre-register, then have your agent attack it”.

**[Evil Genie Test](README.md)** — A check, from the Agentic SDLC course, that grants the result you are hoping for and asks whether your claim could still be false; session 2 points it at a student's own pre-registration.
*First appears in:* the course README.

**[falsify](session-1-the-question.md#hour-1--from-curiosity-to-a-claim-that-can-be-wrong)** — To show a claim is false by producing the observation it predicted would not happen; a claim that can be falsified can, in principle, come out the other way.
*First appears in:* Session 1, “Hour 1 — From curiosity to a claim that can be wrong”.

**[gate](README.md#what-the-series-is-for)** — The set of checks, built from your own past errors, that a result must survive before you are willing to commit to it; a prosthesis, not a virtue.
*First appears in:* the course README, “What the series is for”.

**[GRIM](tools-by-stage.md#mechanical-detectors)** — A check that tests whether a reported mean and standard deviation are arithmetically possible for the stated sample size.
*First appears in:* Tools by stage, “Mechanical detectors”.

**[Hedges' g](toolset.md#categories--pick-one-know-why)** — A corrected effect-size measure that, unlike Cohen's d, is not biased upward at small sample sizes; pingouin reports it by default.
*First appears in:* Toolset, “Categories — pick one, know why”.

**[kill list](README.md#the-spine)** — The running list of your own verified errors, each written as a check someone else could run; a memory you earned, not a checklist handed to you.
*First appears in:* the course README, “The spine”.

**[lit review](README.md#what-the-series-is-for)** — A structured search of the published work on a question; the course builds it as a loop with a rule for what counts as relevant and a condition under which it stops (saturation).
*First appears in:* the course README, “What the series is for”.

**[negative control](session-2-designing-to-fail.md#hour-2--a-control-that-is-capable-of-failing)** — A run that contains everything in your pipeline except the thing you think you are measuring; its whole value is that it can come back positive.
*First appears in:* Session 2, “Hour 2 — A control that is capable of failing”.

**[null](README.md#two-cautions)** — A result that does not show the effect you expected; whether it means "nothing happened" or "your test could not see it" depends on the test's power.
*First appears in:* the course README, “Two cautions”.

**[per-sample statistic](session-3-reading-what-came-back.md)** — A number computed as an average over items, each of which has its own value; adding more items only makes it steadier, not larger.
*First appears in:* Session 3.

**[pilot](session-2-designing-to-fail.md#hour-4--pre-register-then-have-your-agent-attack-it)** — The smallest version of your design that could still produce a signal; the course has students run one before the full study, bringing both synthetic runs alongside it.
*First appears in:* Session 2, “Hour 4 — Pre-register, then have your agent attack it”.

**[positive control](session-2-designing-to-fail.md#hour-2--a-control-that-is-capable-of-failing)** — A run that should pass, used to show the instrument works; it proves the instrument, not the scope of your claim.
*First appears in:* Session 2, “Hour 2 — A control that is capable of failing”.

**[power](session-2-designing-to-fail.md#hour-4--pre-register-then-have-your-agent-attack-it)** — The chance that a test with your sample size detects an effect of a given size, if the effect is real; with low power, a null does not mean "nothing."
*First appears in:* Session 2, “Hour 4 — Pre-register, then have your agent attack it”.

**[pre-commit hook](README.md)** — A check that runs automatically every time you commit to git, before your change is recorded; the course uses it to run a gate or catch a stale artifact.
*First appears in:* the course README.

**[pre-registration](README.md#outcomes-in-the-multiverses-own-competency-verb-style)** — A record, written and timestamped before the data arrives, of your prediction, decision rule and hopes, so you cannot quietly change the plan after seeing results.
*First appears in:* the course README, “Outcomes, in the Multiverse's own competency-verb style”.

**[problematization](session-1-the-question.md#job-one--the-review-tells-you-where-the-edge-is)** — Generating a question by finding an assumption the whole literature shares and challenging it, rather than spotting a gap the literature has not yet covered.
*First appears in:* Session 1, “Job one — the review tells you where the edge is”.

**[rank-bounded](session-3-reading-what-came-back.md)** — A statistic whose largest possible value is capped by how many items you have (for example, an effective dimensionality can't exceed the sample count), so it can grow just because you added items.
*First appears in:* Session 3.

**[residualise](session-2-designing-to-fail.md#hour-1--the-confound-that-got-there-first)** — To subtract, from your measurement, the part that some other variable predicts, usually by fitting a straight line; it removes what the adjustment can see, but does not make your conditions the same.
*First appears in:* Session 2, “Hour 1 — The confound that got there first”.

**[saturation](session-1-the-question.md#job-one--the-review-tells-you-where-the-edge-is)** — The point in a literature search where new sources stop changing the picture; the first real stopping condition most people ever write.
*First appears in:* Session 1, “Job one — the review tells you where the edge is”.

**[sensitivity analysis](session-2-designing-to-fail.md#hour-4--pre-register-then-have-your-agent-attack-it)** — Rerunning your main analysis with one choice changed, to see whether the answer depends on that choice; the course commits to these in advance and reports all of them.
*First appears in:* Session 2, “Hour 4 — Pre-register, then have your agent attack it”.

**[severe testing](tools-by-stage.md#methods)** — The standard that a claim passes a test only if it would probably have failed that test had the claim been false.
*First appears in:* Tools by stage, “Methods”.

**[stake](session-1-the-question.md#hour-1--from-curiosity-to-a-claim-that-can-be-wrong)** — What you are hoping to find, written down as an interest rather than a prediction, so it can be audited rather than quietly tilting the result.
*First appears in:* Session 1, “Hour 1 — From curiosity to a claim that can be wrong”.

**[stopping condition](session-1-the-question.md#falsifiable-is-not-the-same-as-finishable)** — A rule, written before the work starts, saying what result will let you stop; without it a question has no end and an agent will keep proposing next steps.
*First appears in:* Session 1, “Falsifiable is not the same as finishable”.

**[stranger](session-4-the-gate-and-the-room.md)** — A person with none of your context — in session 4, another student or a fresh agent — who tries to reproduce your number; only a stranger can show whether your work is reproducible.
*First appears in:* Session 4.

**[Type S / Type M error](tools-by-stage.md#tools-and-there-are-good-ones)** — A way of assessing a test beyond plain power: Type S is the chance a significant result has the wrong sign; Type M is how much it overstates the true effect. Both get worse at small n.
*First appears in:* Tools by stage, “Tools, and there are good ones”.
