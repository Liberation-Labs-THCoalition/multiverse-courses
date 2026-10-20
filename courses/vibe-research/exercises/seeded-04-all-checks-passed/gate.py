"""
The methods gate for the word-problem pilot.

    python gate.py               run every check; run the analysis only if they all pass
    python gate.py --self-test   plant one defect per check, and confirm each check fires on it

A check is a function. It takes the data, as analysis.load() returns it, and returns a
list of problems: an empty list is a pass. Its docstring is a kill in the course's
format: the NAME on the first line, what it catches, WHY IT PASSES REVIEW, and EARNED,
the case it came from. The function body is the TEST.

To add a check:
  1. write the function, with its docstring;
  2. add it to CHECKS;
  3. add a plant for it to PLANTS: a defect it should catch, so the self-test can make
     it fire once. A check that has never fired is not known to work.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))   # find analysis.py beside this file
import analysis  # noqa: E402

PLANNED_PROMPTS = {"direct", "step_by_step"}
PLANNED_ITEMS = 160
COLUMNS = ("item", "steps", "prompt", "sample", "tokens", "response_end", "answer", "gold", "correct")


# ------------------------------------------------------------------------------ checks

def columns_present(d):
    """COLUMNS_PRESENT
    Every column the plan names is in the data.
    WHY IT PASSES REVIEW: a missing column fails somewhere later, far from its cause, or not at all.
    EARNED: inherited from the team's template.
    """
    return [f"missing column: {c}" for c in COLUMNS if c not in d]


def planned_prompts(d):
    """PLANNED_PROMPTS
    The data holds exactly the two prompts the plan names, spelled as the plan spells them.
    WHY IT PASSES REVIEW: "step-by-step" and "step_by_step" look the same to a reader, and not to code.
    EARNED: inherited from the team's template.
    """
    found = set(d["prompt"].tolist())
    return [] if found == PLANNED_PROMPTS else [f"prompts found: {sorted(found)}"]


def correct_is_binary(d):
    """CORRECT_IS_BINARY
    Every response is scored 0 or 1, and nothing else.
    WHY IT PASSES REVIEW: a stray 2 or 0.5 still averages to a plausible accuracy.
    EARNED: inherited from the team's template.
    """
    bad = ~np.isin(d["correct"], [0.0, 1.0])
    return [f"{int(bad.sum())} scores are not 0 or 1"] if bad.any() else []


def answer_in_response(d):
    """ANSWER_IN_RESPONSE
    Every graded answer appears in the response it was extracted from.
    WHY IT PASSES REVIEW: an extractor that grabs the wrong number still returns a number.
    EARNED: inherited from the team's template.
    """
    bad = [i for i, (a, text) in enumerate(zip(d["answer"], d["response_end"])) if str(a) not in text]
    return [f"{len(bad)} answers not found in their responses"] if bad else []


def no_duplicate_responses(d):
    """NO_DUPLICATE_RESPONSES
    No (item, prompt, sample) appears twice.
    WHY IT PASSES REVIEW: a batch pasted in twice looks like more data, not like a copy.
    EARNED: inherited from the team's template.
    """
    keys = list(zip(d["item"].tolist(), d["prompt"].tolist(), d["sample"].tolist()))
    dupes = len(keys) - len(set(keys))
    return [f"{dupes} duplicate responses"] if dupes else []


def both_prompts_every_item(d):
    """BOTH_PROMPTS_EVERY_ITEM
    Every item has at least one graded response under each prompt, so the analysis can pair it.
    WHY IT PASSES REVIEW: an item with one side missing drops out of a paired mean without a word.
    EARNED: inherited from the team's template.
    """
    problems = []
    for it in np.unique(d["item"]):
        have = set(d["prompt"][d["item"] == it].tolist())
        if have != PLANNED_PROMPTS:
            problems.append(f"{it}: only {sorted(have)}")
    return problems


def items_match_plan(d):
    """ITEMS_MATCH_PLAN
    The data covers the 160 items the plan names.
    WHY IT PASSES REVIEW: 152 items and 160 items produce equally convincing tables.
    EARNED: inherited from the team's template.
    """
    n = len(np.unique(d["item"]))
    return [] if n == PLANNED_ITEMS else [f"{n} items, plan says {PLANNED_ITEMS}"]


CHECKS = [
    columns_present,
    planned_prompts,
    correct_is_binary,
    answer_in_response,
    no_duplicate_responses,
    both_prompts_every_item,
    items_match_plan,
]


# ------------------------------------------------------------------------------ self-test plants
# Each plant takes the data and returns a copy with one defect in it.

def _copy(d):
    return {k: v.copy() for k, v in d.items()}


def _drop_rows(d, mask):
    return {k: v[~mask] for k, v in d.items()}


def plant_missing_column(d):
    d = _copy(d)
    del d["gold"]
    return d


def plant_misspelt_prompt(d):
    d = _copy(d)
    d["prompt"] = d["prompt"].astype(object)
    d["prompt"][np.flatnonzero(d["prompt"] == "step_by_step")[0]] = "step-by-step"
    return d


def plant_score_of_two(d):
    d = _copy(d)
    d["correct"][0] = 2.0
    return d


def plant_wrong_extraction(d):
    d = _copy(d)
    d["answer"][0] = d["answer"][0] + 7777
    return d


def plant_duplicate_row(d):
    return {k: np.concatenate([v, v[:1]]) for k, v in d.items()}


def plant_item_missing_one_prompt(d):
    first = d["item"][0]
    return _drop_rows(d, (d["item"] == first) & (d["prompt"] == "step_by_step"))


def plant_item_missing(d):
    return _drop_rows(d, d["item"] == d["item"][0])


PLANTS = {
    columns_present: ("the gold column removed", plant_missing_column),
    planned_prompts: ('one prompt spelled "step-by-step"', plant_misspelt_prompt),
    correct_is_binary: ("one score set to 2", plant_score_of_two),
    answer_in_response: ("one answer replaced by a number not in its response", plant_wrong_extraction),
    no_duplicate_responses: ("one response copied", plant_duplicate_row),
    both_prompts_every_item: ("one item's step-by-step responses removed", plant_item_missing_one_prompt),
    items_match_plan: ("one item removed", plant_item_missing),
}


# ------------------------------------------------------------------------------ running

def name(check):
    return (check.__doc__ or check.__name__).strip().splitlines()[0]


def run_checks(d, checks=CHECKS):
    """Every check's problems, by check. Empty lists mean pass."""
    out = {}
    for check in checks:
        try:
            out[check] = check(d)
        except Exception as e:                      # a check that crashes has not passed
            out[check] = [f"the check crashed: {type(e).__name__}: {e}"]
    return out


def gate(d):
    results = run_checks(d)
    failed = [c for c, problems in results.items() if problems]
    print(f"Gate for the word-problem pilot: {len(CHECKS)} checks on {analysis.DATA.name}")
    for check, problems in results.items():
        print(f"  {'FAIL' if problems else 'PASS'}  {name(check)}")
        for p in problems[:5]:
            print(f"          {p}")
        if len(problems) > 5:
            print(f"          ... and {len(problems) - 5} more")
    print()
    if failed:
        print(f"GATE: BLOCKED ({len(failed)} of {len(CHECKS)} checks failed). The analysis was not run.")
        return False
    print(f"GATE: PASS ({len(CHECKS)} of {len(CHECKS)}). Running the analysis.\n")
    analysis.run(d)
    return True


def self_test(d):
    print("Self-test: every check must pass the data as it is, and fail on its planted defect.")
    ok = 0
    for check in CHECKS:
        clean = run_checks(d, [check])[check]
        if check not in PLANTS:
            print(f"  ??    {name(check)}: no plant, so it has never been seen to fire")
            continue
        label, plant = PLANTS[check]
        fired = bool(run_checks(plant(d), [check])[check])
        good = (not clean) and fired
        ok += good
        why = "" if good else ("  <- fails the data as shipped" if clean else "  <- did NOT fire")
        print(f"  {'ok  ' if good else 'BAD '}  {name(check):<26} fires on: {label}{why}")
    print()
    print(f"SELF-TEST: {ok} of {len(CHECKS)} checks pass the data and fire on their planted defect.")
    return ok == len(CHECKS)


if __name__ == "__main__":
    data = analysis.load()
    if "--self-test" in sys.argv[1:]:
        sys.exit(0 if self_test(data) else 1)
    sys.exit(0 if gate(data) else 1)
