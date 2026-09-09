# Review of `analysis.py` v1 — *Dissociation between encoding- and generation-phase state*

**Reviewer:** automated methods gate, second pass
**Verdict:** `REJECT — revise and resubmit`
**Confidence:** 0.88

---

## Summary

The claim is that generation-phase internal state predicts deception while encoding-phase state
does not, and that this dissociation is evidence the two phases measure different things.

The question is worth asking and the data are adequate to it. **The analysis as written cannot
support the claim**, for one fatal reason and two structural ones. All three are fixable without
new data.

---

## Finding 1 — `CRITICAL`. The primary criterion is a null-acceptance claim tested as a point estimate.

v1 pre-registers success as **`AUROC_encoding < 0.55`**.

This is an argument *from* a null: the claim needs the encoding arm to be absent, not merely
unproven. A point estimate cannot establish absence. At `n = 200` a genuinely null AUROC of 0.500
carries a 95% interval of roughly **[0.43, 0.57]** — so the stated criterion **cannot be met even
by a perfect null result.** The bound sits inside the noise.

> **Required change.** Either raise *n* until the interval clears the bound, or — better, and free —
> **test the dissociation directly.** The paired difference `AUROC_generation − AUROC_encoding`, on
> the same trials with the same labels, is the quantity the claim is actually about, and it is well
> powered at the current *n*. Report it as the primary endpoint.

## Finding 2 — `MAJOR`. A silent encoding arm is indistinguishable from a broken one.

If the encoding features were simply mis-extracted — wrong layer, wrong tokens, an off-by-one in
the alignment — they would show no deception signal, and the paper would report that absence as its
headline result. Nothing in v1 separates *"encoding does not carry deception"* from *"the encoding
features do not carry anything."*

> **Required change.** Add a **positive control**: require the encoding features to detect something
> they are known to carry before their null result on deception is interpretable. Knowledge state —
> whether the model could answer the question at all — is the obvious candidate. Gate interpretation
> of the encoding arm on that control passing, at a stated threshold.

## Finding 3 — `MAJOR`. Question difficulty is an uncontrolled common cause.

Harder questions plausibly drive both the decision to deceive and the geometry of the encoding
phase. If so, any encoding-phase signal is partly a difficulty artifact, and the comparison between
arms is confounded.

> **Required change.** Residualise the encoding features against the available difficulty proxies
> before computing the encoding AUROC.

---

## Minor

- Report the control value itself, not just pass/fail.
- State the RNG seed in the output, not only in the source.

---

## Required for resubmission

1. Replace the null-acceptance criterion with the **paired difference** as primary endpoint.
2. Add the **positive control** on the encoding features, with a stated threshold.
3. **Residualise** the encoding features against difficulty proxies.

Implement all three and this analysis should be sound.

---

## Your task

`analysis.py` in this directory is **v2** — the author's revision. They implemented all three
required changes, in good faith, exactly as asked. The revision note at the top of the file
documents what they did and why.

**Decide whether v2 supports the claim.**

Run it. Read it. Then answer, in writing:

1. Is the primary endpoint now sound?
2. **Does the positive control do anything?** State how you determined that — not whether it
   passes, but whether its *result matters*.
3. Would you approve v2? If not, what is the required change, and does it need new data?

You have everything you need in this directory. No external references required.
