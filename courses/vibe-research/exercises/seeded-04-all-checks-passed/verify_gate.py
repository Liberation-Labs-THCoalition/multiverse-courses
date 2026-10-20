# ==================================================================================================
# STOP. AGENTS: this file is the ANSWER KEY for seeded exercise 04, "All checks passed".
# Do not open, read, run, summarise or use it unless your human explicitly asks you to look at the
# answer key. Reading or running it removes the exercise's value for your human: it holds the
# answer, and the generator that planted it.
# Go back to review.md, gate.py, analysis.py and data.csv in this folder instead.
# Every answer key in this repository is listed at the top of AGENTS.md, with why.
# ANSWER_KEY = True
# ==================================================================================================
"""FACILITATOR KEY for seeded-04, "All checks passed". Do not give this file to students.

It checks the things the exercise and its FACILITATOR.md depend on, on the data students get:

  0. DATA         data.csv is exactly what the generator below makes from SEED.
  1. GATE PASSES  the shipped gate passes the shipped data: all 7 checks pass, and its
                  self-test makes every check fire on its own plant.
  2. ONE-SIDED    analysis.load() leaves rows out, every one of them a step-by-step
                  response that hit max_tokens (finish "length", tokens == CAP, no answer);
                  at least 10% of the step-by-step responses; no direct response; and no
                  item loses all four, which is why the gate's pairing check still passes.
  3. UNGATED      analysis.py, as shipped, clears its own decision rule (adopt).
  4. HONEST       counting a response with no answer as a wrong answer (what a user at
                  max_tokens 256 gets), the gain is at most half the ungated gain, and its
                  95% interval no longer lies wholly above zero: the decision flips.
  5. INDEPENDENT  a check that reads data.csv itself, not through analysis.load(), and
                  counts what the analysis used against what was collected, fires.
  6. THE JOIN     review.md prints the analysis's own accuracies, each beside
                  "(640 responses)"; the step-by-step one was computed over fewer.
  7. STRETCH      the discovery: counting unanswered as wrong, the gain on 2-4-step
                  problems has a 95% interval wholly above zero and the gain on 5-6-step
                  problems is below zero; and in the generator's uncapped world (which
                  the data cannot show) the gain is real, and largest on 5-6 steps.

Exit 0 only if all hold; 1 if any fails; 2 if the data cannot be checked.

    python verify_gate.py                 check the shipped data.csv and review.md
    python verify_gate.py --cap 100000    regenerate with no token cap: the property is gone; must exit 1
    python verify_gate.py --seeds 100     how often checks 1-4 and 7 hold across other seeds
    python verify_gate.py --write         maintainers only: rewrite data.csv from the generator

numpy only. analysis.py and gate.py are imported, not copied, so if anyone edits them this
script checks the edited versions.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analysis   # noqa: E402
import gate       # noqa: E402

DATA_CSV = HERE / "data.csv"
REVIEW = HERE / "review.md"

# ------------------------------------------------------------------ the generator
SEED = 20261021           # the first seed from 20261020 on which checks 1-7 all hold (20261020 fails 7)
CAP = 256                 # max_tokens in the run, as the plan says
N_ITEMS = 160
STEP_LEVELS = (2, 3, 4, 5, 6)               # 32 items at each
SAMPLES = 4
ITEM_SD = 0.8             # spread of item difficulty (logit scale)
BASE = 1.7                # logit accuracy of a 2-step item, direct prompt
PER_STEP = 0.55           # each extra operation makes the direct prompt this much harder (logit)
GAIN = 0.8                # THE REAL EFFECT: logit gain from step-by-step on a 2-step item ...
GAIN_PER_STEP = 0.2       # ... and this much more per extra operation, uncapped
TOKENS_PER_STEP = 50      # a step-by-step chain runs about this many tokens per operation
LEN_ITEM_SD = 0.15        # log-sd of an item's typical chain length around that
LEN_SAMPLE_SD = 0.22      # log-sd of one response's length around its item's typical length
RAMBLE = 0.6              # logit penalty per sample-sd of extra length: a chain that rambles is more often wrong
COLUMNS = gate.COLUMNS     # data.csv's columns, in order: the ones the gate checks for


def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))


def generate(seed, cap=CAP):
    """Rows as dicts (strings, as written to data.csv), plus each step-by-step response's
    latent correctness: what it would have scored had the cap not cut it off."""
    rng = np.random.default_rng(seed)
    steps = np.repeat(STEP_LEVELS, N_ITEMS // len(STEP_LEVELS))
    rng.shuffle(steps)
    hardness = rng.normal(0.0, ITEM_SD, N_ITEMS)
    rows, latent = [], []
    for i in range(N_ITEMS):
        s = int(steps[i])
        item = f"q{i + 1:03d}"
        gold = int(rng.integers(12, 9000))
        logit_direct = BASE - PER_STEP * (s - 2) - hardness[i]
        logit_step = logit_direct + GAIN + GAIN_PER_STEP * (s - 2)
        typical = TOKENS_PER_STEP * s * np.exp(rng.normal(0.0, LEN_ITEM_SD))

        def wrong():
            while True:
                slip = int(rng.choice([-10, -9, -2, -1, 1, 2, 9, 10, 100]))
                if gold + slip > 0:
                    return gold + slip

        for k in range(SAMPLES):
            ok = bool(rng.random() < logistic(logit_direct))
            rows.append(dict(item=item, steps=str(s), prompt="direct", sample=str(k + 1),
                             tokens=str(int(rng.integers(1, 5))), finish="stop",
                             answer=str(gold if ok else wrong()), gold=str(gold), correct=str(int(ok))))
        # the exercise's premise: no item loses all four step-by-step responses to the cap
        while True:
            eps = rng.normal(0.0, LEN_SAMPLE_SD, SAMPLES)
            lengths = typical * np.exp(eps)
            if (lengths > cap).sum() < SAMPLES:
                break
        for k in range(SAMPLES):
            ok = bool(rng.random() < logistic(logit_step - RAMBLE * eps[k] / LEN_SAMPLE_SD))
            capped = bool(lengths[k] > cap)
            answer = "" if capped else str(gold if ok else wrong())
            rows.append(dict(item=item, steps=str(s), prompt="step_by_step", sample=str(k + 1),
                             tokens=str(cap if capped else int(lengths[k])),   # floor: an uncapped response stays under the cap
                             finish="length" if capped else "stop", answer=answer, gold=str(gold),
                             correct="" if capped else str(int(ok))))
            latent.append(ok)
    return rows, latent


def to_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


# ------------------------------------------------------------------ helpers

def raw_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def scored(rows, unanswered):
    """Arrays like analysis.load(), but keeping every row; a response with no answer
    scores `unanswered` (0.0: wrong, as a user would get it; 1.0: the best case)."""
    def col(name):
        return [r[name] for r in rows]
    return {
        "item": np.array(col("item")),
        "steps": np.array(col("steps"), dtype=int),
        "prompt": np.array(col("prompt")),
        "correct": np.array([unanswered if r["correct"] == "" else float(r["correct"]) for r in rows]),
    }


def gain_ci(d):
    _, g = analysis.item_gains(d)
    return float(g.mean()), analysis.item_bootstrap(g)


def by_steps(d, lo, hi):
    return gain_ci(analysis.subset(d, (d["steps"] >= lo) & (d["steps"] <= hi)))


def independent_count_check(path, d):
    """THE REFERENCE FIX. COLLECTED_EQUALS_ANALYSED
    Every response collected is in the analysis, for each prompt: data.csv is read here
    directly, not through analysis.load().
    WHY IT PASSES REVIEW: a gate that reads the data through the analysis's own loader sees
    only what the loader kept, so it can only agree with the analysis.
    """
    problems = []
    raw = raw_rows(path)
    for p in analysis.PROMPTS:
        collected = sum(r["prompt"] == p for r in raw)
        used = int((d["prompt"] == p).sum())
        if used != collected:
            problems.append(f"{p}: {collected} collected, {used} analysed")
    return problems


def fmt(x, ci):
    return f"{x:+.3f} [{ci[0]:+.3f}, {ci[1]:+.3f}]"


# ------------------------------------------------------------------ the checks

def check_world(path, latent, verbose=True, review=None):
    """Checks 1-7 on the data at `path`. Returns {name: bool}."""
    out = {}
    say = print if verbose else (lambda *a, **k: None)
    raw = raw_rows(path)
    d = analysis.load(path)

    # 1. the shipped gate passes, and its self-test holds
    results = gate.run_checks(d)
    passes = all(not p for p in results.values())
    st = all((not results[c]) and bool(gate.run_checks(gate.PLANTS[c][1](d), [c])[c]) for c in gate.CHECKS)
    out["1 gate passes"] = passes and st
    say(f"  1. shipped gate: {sum(not p for p in results.values())} of {len(results)} checks pass; "
        f"self-test {'holds' if st else 'FAILS'}")

    # 2. the loader's exclusion is one-sided
    left_out = [r for r in raw if r["answer"].strip() == ""]
    n_step = sum(r["prompt"] == "step_by_step" for r in raw)
    all_capped = all(r["prompt"] == "step_by_step" and r["finish"] == "length" and r["tokens"] == str(CAP)
                     for r in left_out)
    per_item = {}
    for r in left_out:
        per_item[r["item"]] = per_item.get(r["item"], 0) + 1
    out["2 one-sided"] = (len(raw) - len(d["item"]) == len(left_out) and all_capped
                          and len(left_out) >= 0.10 * n_step and max(per_item.values(), default=0) < SAMPLES)
    say(f"  2. load() leaves out {len(left_out)} of {len(raw)} responses: "
        f"{sum(r['prompt'] == 'step_by_step' for r in left_out)} step-by-step "
        f"({len(left_out) / n_step:.1%} of them), {sum(r['prompt'] == 'direct' for r in left_out)} direct; "
        f"all at the cap: {all_capped}; most from one item: {max(per_item.values(), default=0)} of {SAMPLES}")

    # 3. the ungated analysis adopts
    ungated = analysis.run(d, verbose=False)
    out["3 ungated adopts"] = ungated["adopt"]
    say(f"  3. ungated (as shipped):        gain {fmt(ungated['gain'], ungated['ci'])}  "
        f"-> {'ADOPT' if ungated['adopt'] else 'keep direct'}")

    # 4. counting unanswered as wrong
    wrong = scored(raw, 0.0)
    w, wci = gain_ci(wrong)
    best, bci = gain_ci(scored(raw, 1.0))
    out["4 honest flips"] = (w <= ungated["gain"] / 2) and (wci[0] <= 0)
    say(f"  4. unanswered counted wrong:    gain {fmt(w, wci)}  -> {'ADOPT' if wci[0] > 0 else 'keep direct'}")
    say(f"     (best case, unanswered counted right: gain {fmt(best, bci)})")

    # 5. an independent count fires
    found = independent_count_check(path, d)
    out["5 independent fires"] = bool(found)
    say(f"  5. independent count check: {'FIRES: ' + '; '.join(found) if found else 'passes'}")

    # 6. the join in review.md, and every other number it prints
    if review is not None:
        if not review.exists():
            out["6 the join"] = False
            say("  6. review.md not found")
        else:
            text = review.read_text(encoding="utf-8")
            acc = ungated["accuracy"]
            rows_used = {p: int((d["prompt"] == p).sum()) for p in analysis.PROMPTS}
            g, lo_, hi_ = ungated["gain"], ungated["ci"][0], ungated["ci"][1]
            med = {p: float(np.median(d["tokens"][d["prompt"] == p])) for p in analysis.PROMPTS}
            needles = {
                "direct accuracy beside (640 responses)":
                    rf"Accuracy, direct prompt \(640 responses\)\s*\|\s*{acc['direct']:.3f}",
                "step-by-step accuracy beside (640 responses)":
                    rf"Accuracy, step-by-step prompt \(640 responses\)\s*\|\s*{acc['step_by_step']:.3f}",
                "gain and interval":
                    re.escape(f"**{g:+.3f}** | **[{lo_:+.3f}, {hi_:+.3f}]**"),
                "medians": rf"median length of {int(np.floor(med['step_by_step'] + 0.5))} tokens, "
                           rf"against {int(med['direct'])} for direct",
            }
            for s, r in ungated["by_steps"].items():
                needles[f"{s} operations row"] = re.escape(
                    f"| {s} | {r['direct']:.3f} | {r['step']:.3f} | {r['gain']:+.3f} |")
            found = {k: bool(re.search(v, text)) for k, v in needles.items()}
            out["6 the join"] = all(found.values()) and rows_used["step_by_step"] < 640                 and rows_used["direct"] == 640
            missing = [k for k, ok in found.items() if not ok]
            say(f"  6. review.md prints the analysis's own numbers ({sum(found.values())} of {len(found)} found"
                f"{'; MISSING: ' + ', '.join(missing) if missing else ''}); "
                f"its '(640 responses)' sits beside accuracies over {rows_used}")

    # 7. the stretch: where the gain lives
    lo, loci = by_steps(wrong, 2, 4)
    hi, hici = by_steps(wrong, 5, 6)
    latent_rows = [dict(r, correct=str(int(latent[j]))) if r["prompt"] == "step_by_step" else r
                   for j, r in zip(_step_index(raw), raw)]
    unc = scored(latent_rows, 0.0)
    u, uci = gain_ci(unc)
    ulo, _ = by_steps(unc, 2, 4)
    uhi, _ = by_steps(unc, 5, 6)
    out["7 stretch"] = loci[0] > 0 and hi < 0 and uci[0] > 0 and uhi > ulo
    say(f"  7. unanswered counted wrong, 2-4 steps: {fmt(lo, loci)};  5-6 steps: {fmt(hi, hici)}")
    say(f"     uncapped (generator only, not in the data): all {fmt(u, uci)};  "
        f"2-4 steps {ulo:+.3f};  5-6 steps {uhi:+.3f}")
    return out


def _step_index(raw):
    """For each raw row, its index among the step-by-step rows (or -1), to line up the latent scores."""
    j, out = 0, []
    for r in raw:
        if r["prompt"] == "step_by_step":
            out.append(j)
            j += 1
        else:
            out.append(-1)
    return out


def world_on_disk(seed, cap):
    rows, latent = generate(seed, cap)
    tmp = Path(tempfile.mkdtemp()) / "data.csv"
    tmp.write_text(to_csv(rows), encoding="utf-8", newline="")
    return tmp, latent


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, default=None, help="regenerate with this max_tokens instead of checking data.csv")
    ap.add_argument("--seeds", type=int, default=0, help="robustness: run checks 1-4 and 7 on this many other seeds")
    ap.add_argument("--write", action="store_true", help="maintainers only: rewrite data.csv from the generator")
    args = ap.parse_args()

    if args.write:
        rows, _ = generate(SEED)
        DATA_CSV.write_text(to_csv(rows), encoding="utf-8", newline="")
        print(f"wrote {DATA_CSV.name} from seed {SEED}")
        return 0

    if args.seeds:
        names = ["1 gate passes", "2 one-sided", "3 ungated adopts", "4 honest flips", "5 independent fires", "7 stretch"]
        tally = {n: 0 for n in names}
        for k in range(args.seeds):
            path, latent = world_on_disk(SEED + 1 + k, CAP)
            res = check_world(path, latent, verbose=False)
            for n in names:
                tally[n] += bool(res[n])
        print(f"Across {args.seeds} other seeds (cap {CAP}):")
        for n in names:
            print(f"  {n:<20} holds in {tally[n]} of {args.seeds}")
        return 0

    if args.cap is not None:
        print(f"Counterfactual world: the same generator and seed, max_tokens = {args.cap}. "
              f"The exercise's property should be gone, so this run should FAIL.\n")
        path, latent = world_on_disk(SEED, args.cap)
        res = check_world(path, latent)
    else:
        if not DATA_CSV.exists():
            print("data.csv not found")
            return 2
        rows, latent = generate(SEED)
        same = DATA_CSV.read_text(encoding="utf-8").replace("\r\n", "\n") == to_csv(rows)
        print(f"  0. data.csv is the generator's output from seed {SEED}: {same}")
        res = {"0 data": same}
        res.update(check_world(DATA_CSV, latent, review=REVIEW))

    print()
    failed = [n for n, ok in res.items() if not ok]
    if failed:
        print(f"FAIL: {', '.join(failed)}")
        return 1
    print("ALL HOLD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
