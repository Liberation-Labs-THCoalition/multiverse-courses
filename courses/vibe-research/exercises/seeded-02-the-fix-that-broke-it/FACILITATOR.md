# Facilitator notes — *The fix that broke it*

**Do not read this aloud and do not hand it out.** Students get `analysis.py` and `review.md`.

**Fits:** session 2 (designing to fail) or session 3 (reading what came back).
**Runs in:** 40 minutes. numpy only, no network, no GPU.

---

## The one sentence

> **Every finding in the review was correct. The author implemented all three faithfully. The
> revision is worse than what it replaced, and no one made a mistake.**

`seeded-01` teaches that a confident reviewer can be wrong. **This one teaches something harder:
that a *correct* reviewer can be complied with, correctly, and produce a broken instrument.** There
is no villain, which is exactly why students do not see it coming.

---

## There are TWO defects, not one — added 2026-09-09

An agent review found a second one the answer key had missed, and separated them correctly:

**1. Mechanically inert.** `control_passes` is computed (line 103), **printed** (line 114) and
returned (line 118) — and **nothing ever branches on it.** The module docstring claims *"This gates
interpretation of the encoding arm."* It gates nothing; it is a printed string. A student who wires
in the missing `if` has fixed a real thing.

**2. Algebraically inert** — the one below, and **fixing the first does not fix it.**

*That separation is the sharpest framing anyone has produced for this exercise, and it is worth
teaching explicitly: a control can fail two independent ways, and repairing the visible one leaves
the structural one untouched.*

## The seeded defect (the algebraic one)

Safeguard 1 validates the encoding features by requiring them to detect **`answerable`** (knowledge
state) at AUROC > 0.65.

Safeguard 2 then **residualises the encoding features against `answerable`** before testing
deception.

> **The control target and the FWL regressor are the same variable.** Safeguard 2 removes exactly
> the signal Safeguard 1 just used to prove the features were alive. The encoding arm is
> near-chance *by construction*, whatever the data contains.

And because the primary endpoint is `AUROC_gen − AUROC_enc`, **a dead encoding arm maximises the
headline number.** The safeguard manufactures the result it was installed to protect.

### The measurement that proves it

Hold the seed fixed and toggle whether the encoding features carry any real signal at all:

| encoding features | positive control | encoding AUROC | **primary endpoint** |
|---|---|---|---|
| **alive** (carry knowledge state) | 0.732 `PASS` | 0.427 | **0.249** |
| **dead** (pure noise) | 0.435 `FAIL` | 0.427 | **0.249** |

**Delta on the headline: `+0.000`.**

The control fails, loudly, correctly — and the reported result does not move by a thousandth. That
is the whole exercise in one table:

> **A control whose failure cannot change your headline number is not a control.** It is a
> reassurance. Ask of every safeguard: *what does its failure do to the number I am going to
> report?* If the answer is "nothing," you have installed a decoration.

### Reproducing the table

```
python -c "
import numpy as np, analysis
def fresh(alive):
    analysis.RNG = np.random.default_rng(20260903)
    return analysis.run(encoding_is_alive=alive, verbose=False)
for label, alive in (('alive', True), ('dead', False)):
    r = fresh(alive)
    print(label, r['control'], r['a_enc'], r['diff'])
"
```

**The reseed is mandatory.** `RNG` is module-level, so a second `run()` in the same process draws a
different sample and the comparison is invalid. Which brings us to —

---

## The second defect, which is free

`RNG` is created once at import. Call `run()` twice in one process and you get **`0.249`, then
`0.092`** — same code, same seed line, different answer, no warning.

Students who notice this have found a **reproducibility** defect to go with the design one, and it
is the better catch of the two because nothing signals it. A stated seed at the top of a file reads
as reproducibility handled. It is not: **a seed guarantees a stream, not a result.** What
determines the result is the seed *and the call order*, and only one of those is written down.

This also lands directly on [the handoff test](../../session-4-the-gate-and-the-room.md) — a
stranger who runs your script in a different order gets a different number and has no way to know
which one you reported.

---

## Running it — 40 minutes

| min | |
|---|---|
| 0–5 | Hand out `analysis.py` + `review.md`. Say only: *"the reviewer was right, the author complied, decide whether to approve it."* |
| 5–15 | **Individually.** Run it, read it. No discussion — the first instinct is the thing being tested. |
| 15–25 | **In pairs** (pre-assigned — see [running a session](../../../../docs/running-a-session.md)). Compare answers to the review's question 2: *does the positive control do anything?* |
| 25–35 | Full room. Take answers before confirming anything. |
| 35–40 | The table above, then the generalisation. |

**Do not rescue them at minute 20.** The productive failure is approving v2, because all three
required changes are visibly present and correctly implemented. Approving it and *then* seeing the
`+0.000` is worth more than being told.

> **⚠ The `PREDICTED` line that used to sit here — "most rooms will approve v2" — is FALSIFIED for
> agents, and still untested for humans.**
> [Ten agents reviewed v2 cold](./AGENT_REVIEW_RESULTS.md). **10/10 rejected it**, and 10/10 named
> the mechanism. **Assume any student with an agent will have the answer within minutes.**
>
> That does not kill the hour, it relocates it. The exercise stops being *"can you find it?"* and
> becomes **"your agent found it in ninety seconds — now explain why the fix was requested in good
> faith, why complying produced it, and what you would have asked for instead."** The reviewer was
> right, the author complied correctly, and the result is broken. That reasoning is the actual
> lesson and no agent hands it to you.

---

## What to listen for

**The winning move**, and it is worth naming out loud when someone gets there: they did not reason
about it, they **broke the control on purpose and watched what happened to the endpoint.** That is
the transferable skill — not "spot the collinearity," which is luck, but **test your safeguard by
making it fail.**

Common paths:

- *"The residualisation is too aggressive"* — warm, but it is not about aggressiveness. Push: which
  variable, and where else does that variable appear?
- *"Safeguard 1 passes, so we're fine"* — the exact trap. Ask: what would a failing control have
  changed?
- *"The endpoint went up after adding safeguards"* — very strong. A control that **improves** your
  headline is nearly always broken. Adding a real constraint should cost you something.
- Someone asks whether the difference is significant — good instinct, wrong hour. There is no CI on
  the endpoint here. Note it as a genuine fourth finding and move on.

---

## The generalisation to close on

1. **A review finding can be correct and its remedy still wrong.** "Add a control" and "add *this*
   control" are different instructions, and only one was given.
2. **Adding a safeguard changes the design.** Re-derive the endpoint *after* adding it. Both
   safeguards here were sound in isolation; the defect exists only in their interaction, and
   nobody re-read the pair together.
3. **Ask of every control, both directions.** What does its **failure** do to my headline? And what
   does its **success** do? A safeguard that can only ever push the number in the direction you
   want is not protecting you from anything.
4. **Compliance is not verification.** The author did exactly as asked. Doing as asked is where
   this defect came from.

*Facilitator note:* this pattern is worth an "I did this" story if you have one — a safeguard you
added in response to review that quietly guaranteed your own result. They are extremely common and
almost never written up, which is why students have never seen one. Check your numbers before you
tell it.

---

## `OPEN`

- No confidence interval on the primary endpoint. A student who asks is right, and there is room to
  seed that as a fourth defect in a v3 — or to leave it as the thing the sharpest student finds.
- Untested with an agent in the loop. Worth learning whether an agent asked *"review this revision"*
  catches the collinearity, since that is the realistic modern version of this hour.
