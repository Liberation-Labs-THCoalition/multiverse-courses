"""
Step-by-step pilot: does "think step by step" make the model more accurate?

Read review.md first. It is the write-up of this analysis, and your task is at
the end of it. Everything you need is in this folder: review.md, this file,
and data.csv.

--------------------------------------------------------------------------
PRE-REGISTERED PLAN (written before the run)
--------------------------------------------------------------------------
Data       data.csv: 160 questions, each asked 4 times (temperature 0.7) with
           each of two prompts. 1,280 rows, one per response:
             item     q001 ... q160
             type     lookup        single-fact recall                (112 items)
                      multi_step    multi-step arithmetic word problem  (48 items)
             prompt   direct        "Answer with just the answer."
                      step_by_step  "Think step by step, then give the answer."
             sample   1-4
             correct  1 if the final answer matches the gold answer, else 0
             tokens   length of the response, in tokens

Endpoint   accuracy(step_by_step) - accuracy(direct), paired by item.

Confound   response length. Step-by-step answers are several times longer,
           and length is a well-documented confound in LLM evaluation: longer
           answers tend to be scored higher whether or not they are better.
           So the primary estimate is LENGTH-ADJUSTED, by Frisch-Waugh-Lovell:
           residualise correctness and the prompt indicator on response
           length, then regress residual on residual.

Inference  item-level bootstrap, 2000 resamples. An item's eight responses
           are always drawn together. 95% percentile intervals.

Decision   step-by-step improves accuracy if the length-adjusted 95% CI lies
           wholly above zero.

Item type was recorded to keep the question bank balanced. It is not part of
the plan.
--------------------------------------------------------------------------
"""
import csv
from pathlib import Path

import numpy as np

DATA = Path(__file__).with_name("data.csv")
N_BOOT = 2000
BOOT_SEED = 20260519      # fixed here, so every call gives the same interval


def load(path=DATA):
    """data.csv as arrays, one entry per response."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    prompts = {r["prompt"] for r in rows}
    assert prompts == {"direct", "step_by_step"}, f"unexpected prompts: {prompts}"
    return {
        "item":    np.array([r["item"] for r in rows]),
        "type":    np.array([r["type"] for r in rows]),
        "step":    np.array([r["prompt"] == "step_by_step" for r in rows], dtype=float),
        "correct": np.array([int(r["correct"]) for r in rows], dtype=float),
        "tokens":  np.array([int(r["tokens"]) for r in rows], dtype=float),
    }


def subset(d, mask):
    return {k: v[mask] for k, v in d.items()}


def residualise(v, Z):
    """Frisch-Waugh-Lovell: the part of v that the columns of Z do not explain."""
    beta, *_ = np.linalg.lstsq(Z, v, rcond=None)
    return v - Z @ beta


def raw_gain(d):
    """Accuracy with the step-by-step prompt minus accuracy with the direct one.
    Every item has the same number of responses per prompt, so this is the mean
    paired difference."""
    return d["correct"][d["step"] == 1].mean() - d["correct"][d["step"] == 0].mean()


def length_adjusted_gain(d):
    """The pre-registered estimate: the effect of the step-by-step prompt on
    correctness, with response length partialled out of both."""
    Z = np.column_stack([np.ones(len(d["tokens"])), d["tokens"]])
    y = residualise(d["correct"], Z)
    t = residualise(d["step"], Z)
    return float(t @ y / (t @ t))


def item_bootstrap(d, stat, n_boot=N_BOOT, seed=BOOT_SEED):
    """95% percentile interval for stat(d), resampling items with replacement
    and keeping all of an item's responses together."""
    rng = np.random.default_rng(seed)
    items, inverse = np.unique(d["item"], return_inverse=True)
    rows_of = [np.flatnonzero(inverse == i) for i in range(len(items))]
    draws = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(items), len(items))
        draws.append(stat(subset(d, np.concatenate([rows_of[i] for i in pick]))))
    return np.percentile(draws, [2.5, 97.5])


def median_tokens(d, step):
    return float(np.median(d["tokens"][d["step"] == step]))


def run(d, verbose=True):
    raw, raw_ci = raw_gain(d), item_bootstrap(d, raw_gain)
    adj, adj_ci = length_adjusted_gain(d), item_bootstrap(d, length_adjusted_gain)
    improves = bool(adj_ci[0] > 0)
    by_type = {}
    for t in ("lookup", "multi_step"):
        s = subset(d, d["type"] == t)
        by_type[t] = dict(n=len(np.unique(s["item"])), gain=raw_gain(s),
                          tokens_direct=median_tokens(s, 0), tokens_step=median_tokens(s, 1))

    if verbose:
        n_items = len(np.unique(d["item"]))
        print(f"Step-by-step pilot: {n_items} items x 2 prompts = {len(d['item'])} responses (data.csv)\n")
        print("PRE-REGISTERED")
        print(f"  accuracy, direct prompt          {d['correct'][d['step'] == 0].mean():.3f}")
        print(f"  accuracy, step-by-step prompt    {d['correct'][d['step'] == 1].mean():.3f}")
        print(f"  raw gain (step - direct)        {raw:+.3f}   95% CI [{raw_ci[0]:+.3f}, {raw_ci[1]:+.3f}]")
        print(f"  median length, direct / step     {median_tokens(d, 0):.0f} / {median_tokens(d, 1):.0f} tokens")
        print(f"  LENGTH-ADJUSTED GAIN (primary)  {adj:+.3f}   95% CI [{adj_ci[0]:+.3f}, {adj_ci[1]:+.3f}]")
        print()
        print("EXPLORATORY (not pre-registered: reported, not interpreted)")
        print("  item type      n   raw gain   median tokens, direct / step")
        for t, r in by_type.items():
            print(f"  {t:<11} {r['n']:>4}   {r['gain']:+.3f}     {r['tokens_direct']:.0f} / {r['tokens_step']:.0f}")
        print()
        if improves:
            print("CONCLUSION: step-by-step prompting improves accuracy, with length controlled.")
        elif adj_ci[1] < 0:
            print("CONCLUSION: step-by-step prompting lowers accuracy, with length controlled.")
        else:
            print("CONCLUSION: the raw gain does not survive adjustment for response length.")
            print("            No evidence that step-by-step prompting improves accuracy.")

    return dict(raw=raw, raw_ci=raw_ci, adjusted=adj, adjusted_ci=adj_ci, improves=improves,
                by_type=by_type)


if __name__ == "__main__":
    run(load())
