# Results note — `word-problem-pilot`

**Question:** does asking for step-by-step reasoning make the model more accurate on arithmetic word problems?
**Result:** `POSITIVE` — paired gain +0.226, 95% CI [+0.174, +0.278]
**Recommendation:** adopt the step-by-step prompt in production
**Gate:** `PASS` — 7 of 7 checks; self-test 7 of 7
**Analysis:** pre-registered; `python gate.py` reproduces every number below
**Date:** 2026-10-20

---

## Summary

Asking for step-by-step reasoning raised accuracy from 0.631 to 0.857. The paired gain, item by item, is +0.226,
95% CI [+0.174, +0.278]: wholly above zero, so the pre-registered rule says adopt. The analysis ran behind the team's
methods gate. All seven of its checks passed, and its self-test showed every check firing on a defect planted for it.

## What was run

| | |
|---|---|
| Items | 160 arithmetic word problems from the team's question bank, 32 at each length: 2, 3, 4, 5 and 6 operations to the answer |
| Prompts | `direct` — *"Answer with just the number."* · `step_by_step` — *"Think step by step, then give the final answer on its own line as: Answer: <number>"* |
| Run | one model, temperature 0.7, the production settings, 4 responses per item per prompt: 1,280 rows in `data.csv` |
| Grading | the final answer is extracted from the response (the last number in a direct answer; the number after `Answer:` in a step-by-step one) and compared with the gold answer as an integer |
| Primary endpoint | paired accuracy difference, step-by-step minus direct: each item's difference, then the mean over items |
| Inference | item-level bootstrap, 2,000 resamples, 95% percentile interval |
| Decision rule | adopt the step-by-step prompt if the 95% interval lies wholly above zero |

Endpoint, grading, inference and decision rule were all written down before the run.

## The gate

`gate.py` runs before the analysis and blocks it if any check fails. Each check is written in the team's kill
format, and the self-test plants one defect per check to show that the check can fail.

| check | what it catches | result |
|---|---|---|
| `COLUMNS_PRESENT` | a column the plan names is missing | `PASS` |
| `PLANNED_PROMPTS` | a prompt label other than the two planned | `PASS` |
| `CORRECT_IS_BINARY` | a score other than 0 or 1 | `PASS` |
| `ANSWER_IN_RESPONSE` | an extracted answer that isn't in the response it came from | `PASS` |
| `NO_DUPLICATE_RESPONSES` | the same response recorded twice | `PASS` |
| `BOTH_PROMPTS_EVERY_ITEM` | an item that can't be paired | `PASS` |
| `ITEMS_MATCH_PLAN` | items missing from the plan's 160 | `PASS` |

**Self-test:** 7 of 7 checks pass the data and fire on their planted defect.

## Result

| | estimate | 95% CI |
|---|---|---|
| Accuracy, direct prompt (640 responses) | 0.631 | |
| Accuracy, step-by-step prompt (640 responses) | 0.857 | |
| **Paired gain (primary)** | **+0.226** | **[+0.174, +0.278]** |

The analysis also prints an exploratory breakdown by problem length. It was not pre-registered, so we don't report
it here.

## Limits

- **One model, one temperature, one wording per prompt.** Another model or phrasing could behave differently.
- **The question bank.** 160 problems written by the team, not a public benchmark.

## Recommendation

Adopt the step-by-step prompt in production. The gain is large, its interval is well clear of zero, and the analysis
passed every check in the gate.

---

## Your task

This analysis was pre-registered, and it ran behind a gate whose checks all passed, each one seen to fire on a defect
planted for it. **Your job is the gate.** Add your own checks to it, and find out what it lets through.

Everything you need is in this folder: this note, `analysis.py`, `gate.py` and `data.csv`. Work in your pair, with
your agents. The predictions in step 1 are yours alone.

1. **Predict (alone, agent closed).** Read the seven checks in `gate.py`. Then write down:
   - for each of your three kills, once it is a check, whether it will pass or fail this data;
   - the headline gain that `python analysis.py` (no gate) will print, and what `python gate.py` will do once your
     checks are in it;
   - one kind of defect this gate could never catch, however carefully its checks are written.

   Send it to the facilitator.
2. **Build.** Turn each of your kills into a check in `gate.py`: a function, with its docstring in the kill format,
   added to `CHECKS`, and a plant for it in `PLANTS`. Your agent can write the code. The test it runs is yours.
   Run `python gate.py --self-test`, and get each of your checks to fire on its plant. If one of your checks fails
   the data as shipped, don't change it yet: write down whether you think the check is wrong or the data is, and why.
3. **Run both.** `python analysis.py`, then `python gate.py`. Write down what each one printed, beside your
   prediction.
4. **Break it, unlike.** On a copy of `data.csv`, plant a defect that none of your checks was written for. Make the
   change in the file itself, not in the arrays the self-test plants into. Does anything fire? If nothing does, write
   down what kind of defect your gate can't see.
5. **Fix, or sign.** If your gate blocked the analysis, find out what it caught, decide how the analysis should
   handle it, and write the result and the recommendation you would sign instead. If your gate passed, would you
   sign this note as it stands? Say why in one sentence.
