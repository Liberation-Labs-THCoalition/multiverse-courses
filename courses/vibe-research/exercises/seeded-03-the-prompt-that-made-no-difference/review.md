# Results note — `step-by-step-pilot`

**Question:** does asking the model to reason step by step make it more accurate?
**Result:** `NULL` — no effect once response length is controlled
**Recommendation:** keep the direct prompt
**Analysis:** pre-registered; `analysis.py` reproduces every number below
**Date:** 2026-05-19

---

## Summary

Asking for step-by-step reasoning raised raw accuracy from 0.503 to 0.623. But step-by-step answers
are about 13 times longer, and response length is a well-documented confound in LLM evaluation. **With
length controlled, the gain is +0.015, 95% CI [−0.055, +0.092]: no evidence of an effect.** The direct
prompt is as accurate, at a thirteenth of the output.

## What was run

| | |
|---|---|
| Items | 160 questions: 112 lookups (single-fact recall), 48 multi-step arithmetic word problems |
| Prompts | `direct` — *"Answer with just the answer."* · `step_by_step` — *"Think step by step, then give the answer."* |
| Responses | 4 per item per prompt, temperature 0.7: 1,280 rows in `data.csv` |
| Grading | final answer against the gold answer: right or wrong |
| Primary endpoint | paired accuracy difference, step-by-step minus direct, **adjusted for response length** |
| Adjustment | Frisch–Waugh–Lovell: residualise correctness and the prompt indicator on response length, regress residual on residual |
| Inference | item-level bootstrap, 2,000 resamples; an item's eight responses are always drawn together |

Endpoint, confound, adjustment, inference and decision rule were all written down before the run.
Item type was recorded to keep the question bank balanced. It was not part of the plan.

## Why we adjusted for length

Step-by-step answers have a median length of 106 tokens; direct answers, 8. Longer answers tend to be
scored higher whether or not they are better, which is why evaluation suites now publish
length-controlled scores. If length moves the score here, a raw comparison between a long-answer
prompt and a short-answer prompt is confounded by construction.

Matching on length was not possible: the longest direct answer is 23 tokens, and the median
step-by-step answer is 106. So we pre-registered a regression adjustment instead.

## Result

| | estimate | 95% CI |
|---|---|---|
| Accuracy, direct prompt | 0.503 | |
| Accuracy, step-by-step prompt | 0.623 | |
| Raw gain | +0.120 | [+0.067, +0.177] |
| **Length-adjusted gain (primary)** | **+0.015** | **[−0.055, +0.092]** |

Most of the raw gain is what response length predicts. With length removed, what remains cannot be
told apart from zero.

## Limits

- **One model, one temperature, one wording per prompt.** Another model or phrasing could behave
  differently.
- **Multi-step items.** Before adjustment, the gain sits almost entirely in the 48 multi-step items
  (+0.406), with none among the 112 lookups (−0.002). We read this as the length confound rather than
  a separate effect: the multi-step items are where step-by-step answers run longest (median 204
  tokens, against 27 for lookups), which is exactly the variation the adjustment exists to remove. The
  split was not pre-registered, and a 48-item subgroup is where chance differences look largest, so we
  do not interpret it.
- **Right-or-wrong grading.** A response with sound reasoning and a slipped final digit scores zero.
- **The question bank.** 160 items written for this pilot, not a public benchmark.

## Recommendation

Keep the direct prompt. With length controlled, step-by-step buys no accuracy, and it costs about 13
times the output tokens.

---

## Your task

This analysis is careful. It named its confound before the run, adjusted for it in the standard way,
reported intervals, and was honest about its limits. **Decide whether you would sign its conclusion
and its recommendation.**

Everything you need is in this folder: this file, `analysis.py` and `data.csv`. Work in your pair,
with your agents, and keep your written answers where both of you can see them.

1. **Before you run anything.** For each limit above, write one sentence: *if this limit is wrong,
   what changes?* Mark the ones this data could actually check, and pick one.
2. **Predict, then look.** For the limit you picked, write down what the data would show if the
   write-up's reading is right, and what it would show if it is not. Both, before you check.
3. **Check.** Run it. Which of your two predictions did the data match?
4. **Sign, or rewrite.** If you would not sign, write the sentence you would put in place of the
   conclusion and the recommendation, and the one check a reader would need in order to believe it.
