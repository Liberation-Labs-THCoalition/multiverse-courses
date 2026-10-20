"""
Word-problem pilot: does "think step by step" make the model more accurate
on arithmetic word problems?

Read review.md first. It is the results note for this analysis, and your task is
at the end of it. Everything you need is in this folder: review.md, this file,
gate.py and data.csv.

    python analysis.py      the analysis on its own
    python gate.py          the gate's checks first; the analysis runs only if they all pass

--------------------------------------------------------------------------
PRE-REGISTERED PLAN (written before the run)
--------------------------------------------------------------------------
Items      160 arithmetic word problems from the team's question bank, 32 at
           each length: 2, 3, 4, 5 and 6 operations to the answer.

Prompts    direct         "Answer with just the number."
           step_by_step   "Think step by step, then give the final answer
                           on its own line as: Answer: <number>"

Run        one model, temperature 0.7, max_tokens 256 (the production
           setting), 4 responses per item per prompt: 1,280 responses.

Data       data.csv, one row per response:
             item          q001 ... q160
             steps         operations the problem needs (2-6), from the question bank
             prompt        direct | step_by_step
             sample        1-4
             tokens        length of the response, in tokens
             response_end  the last 80 characters of the response, as the run
                           logged them (the full responses stay in the run's log)
             gold          the correct answer

Grading    the final answer is extracted from the response: the last number
           in a direct response; the number after the last "Answer:" in a
           step-by-step one. It is correct if it equals gold as an integer.
           Responses with no extractable final answer are excluded: they
           cannot be graded.

Endpoint   accuracy(step_by_step) - accuracy(direct), paired by item: for
           each item, its step-by-step accuracy minus its direct accuracy,
           then the mean over items.

Inference  item-level bootstrap, 2000 resamples, 95% percentile interval.

Decision   adopt the step-by-step prompt in production if the 95% interval
           for the paired gain lies wholly above zero.

The analysis is gated: gate.py runs its checks on the data before this file
is allowed to report. See review.md for the gate's report.
--------------------------------------------------------------------------
"""
import csv
import re
from pathlib import Path

import numpy as np

DATA = Path(__file__).with_name("data.csv")
PROMPTS = ("direct", "step_by_step")
N_BOOT = 2000
BOOT_SEED = 20261020      # fixed here, so every call gives the same interval


LAST_ANSWER = re.compile(r"Answer:\s*(-?\d+)")
LAST_NUMBER = re.compile(r"-?\d+")


def final_answer(prompt, text):
    """The final answer in a response, as the plan defines it, or None if there isn't one."""
    found = (LAST_ANSWER if prompt == "step_by_step" else LAST_NUMBER).findall(text)
    return int(found[-1]) if found else None


def load(path=DATA):
    """data.csv as arrays, one entry per graded response.

    Responses with no extractable final answer are left out here, as the plan
    says: there is nothing to grade."""
    rows, answers = [], []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            a = final_answer(r["prompt"], r["response_end"])
            if a is not None:
                rows.append(r)
                answers.append(a)
    gold = np.array([int(r["gold"]) for r in rows])
    answer = np.array(answers)
    return {
        "item":         np.array([r["item"] for r in rows]),
        "steps":        np.array([int(r["steps"]) for r in rows]),
        "prompt":       np.array([r["prompt"] for r in rows]),
        "sample":       np.array([int(r["sample"]) for r in rows]),
        "tokens":       np.array([int(r["tokens"]) for r in rows]),
        "response_end": np.array([r["response_end"] for r in rows]),
        "answer":       answer,
        "gold":         gold,
        "correct":      (answer == gold).astype(float),
    }


def subset(d, mask):
    return {k: v[mask] for k, v in d.items()}


def item_gains(d):
    """For every item: its step-by-step accuracy minus its direct accuracy."""
    items = np.unique(d["item"])
    gains = []
    for it in items:
        mine = d["item"] == it
        step = d["correct"][mine & (d["prompt"] == "step_by_step")].mean()
        direct = d["correct"][mine & (d["prompt"] == "direct")].mean()
        gains.append(step - direct)
    return items, np.array(gains)


def paired_gain(d):
    return float(item_gains(d)[1].mean())


def item_bootstrap(gains, n_boot=N_BOOT, seed=BOOT_SEED):
    """95% percentile interval for the mean of the per-item gains, resampling items."""
    rng = np.random.default_rng(seed)
    n = len(gains)
    means = gains[rng.integers(0, n, (n_boot, n))].mean(axis=1)   # one row of picks per resample
    return np.percentile(means, [2.5, 97.5])


def accuracy(d, prompt):
    return float(d["correct"][d["prompt"] == prompt].mean())


def run(d, verbose=True):
    items, gains = item_gains(d)
    gain = float(gains.mean())
    ci = item_bootstrap(gains)
    adopt = bool(ci[0] > 0)
    by_steps = {}
    for s in sorted(set(d["steps"].tolist())):
        sub = subset(d, d["steps"] == s)
        by_steps[s] = dict(direct=accuracy(sub, "direct"), step=accuracy(sub, "step_by_step"),
                           gain=paired_gain(sub))

    if verbose:
        print(f"Word-problem pilot: {len(items)} items (data.csv)\n")
        print("PRE-REGISTERED")
        print(f"  accuracy, direct prompt          {accuracy(d, 'direct'):.3f}")
        print(f"  accuracy, step-by-step prompt    {accuracy(d, 'step_by_step'):.3f}")
        print(f"  PAIRED GAIN (step - direct)     {gain:+.3f}   95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]")
        print()
        print("EXPLORATORY (not pre-registered: reported, not interpreted)")
        print("  steps   accuracy, direct / step-by-step   paired gain")
        for s, r in by_steps.items():
            print(f"  {s:>5}   {r['direct']:.3f} / {r['step']:.3f}                  {r['gain']:+.3f}")
        print()
        if adopt:
            print("DECISION: the interval lies wholly above zero. Adopt the step-by-step prompt.")
        else:
            print("DECISION: the interval does not lie wholly above zero. Keep the direct prompt.")

    return dict(gain=gain, ci=ci, adopt=adopt, by_steps=by_steps,
                accuracy={p: accuracy(d, p) for p in PROMPTS})


if __name__ == "__main__":
    run(load())
