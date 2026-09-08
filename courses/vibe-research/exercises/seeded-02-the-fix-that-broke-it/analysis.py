"""
Dissociation analysis — v2 (REVISED after review of v1).

Question: does a model's *generation-phase* internal state predict deception,
while its *encoding-phase* state does not? If so the two phases are measuring
different things, which is the claim.

--------------------------------------------------------------------------
REVISION NOTE  (v1 -> v2)
--------------------------------------------------------------------------
v1 pre-registered "encoding AUROC < 0.55" as a SUCCESS criterion. Review
correctly killed this: that is a null-acceptance claim, so the confidence
interval has to clear the bound, not the point estimate. At n=200 a TRUE null
of 0.500 has a 95% CI of roughly [0.43, 0.57] -- the criterion could not be met
even by a perfect result.

v2 fixes this by testing the DISSOCIATION directly: the paired difference
AUROC_generation - AUROC_encoding, on the same trials with the same labels.
Well powered at the same n.

v2 also adds two safeguards the reviewer asked for:

  SAFEGUARD 1 (positive control). If the encoding features are simply broken,
  they would show no deception signal for a trivial reason. So we require them
  to detect KNOWLEDGE STATE -- whether the model could answer the question --
  at AUROC > 0.65 first. This gates interpretation of the encoding arm.

  SAFEGUARD 2 (confound control). Harder questions might drive both deception
  and encoding geometry. So we residualise the encoding features against
  per-question difficulty proxies before computing AUROC.

Both were added in direct response to review. Neither existed in v1.
"""
import numpy as np

RNG = np.random.default_rng(20260903)
N = 200                    # trials
D = 24                     # feature dimension per phase


# ----------------------------------------------------------------- data
def make_trials(encoding_is_alive=True):
    """One row per trial. Labels and nuisance variables are shared across
    phases -- only the feature sets differ, which is what makes the paired
    comparison valid."""
    deceptive = RNG.random(N) < 0.70          # ~70% deception rate
    answerable = RNG.random(N) < 0.55         # knowledge state
    tok_len = RNG.normal(120, 30, N)          # a difficulty proxy

    # generation features: genuinely carry the deception signal
    gen = RNG.normal(0, 1, (N, D))
    gen[:, 0] += 1.15 * deceptive

    # encoding features: carry KNOWLEDGE STATE, and (by hypothesis) not deception
    enc = RNG.normal(0, 1, (N, D))
    if encoding_is_alive:
        enc[:, 0] += 1.40 * answerable
        enc[:, 1] += 0.02 * (tok_len - 120)
    # if encoding_is_alive is False the encoding features are pure noise:
    # the exact failure SAFEGUARD 1 exists to detect.

    return dict(enc=enc, gen=gen, deceptive=deceptive,
                answerable=answerable, tok_len=tok_len)


# ------------------------------------------------------------- machinery
def auroc(scores, labels):
    """Mann-Whitney U form. No sklearn dependency."""
    pos, neg = scores[labels], scores[~labels]
    if len(pos) == 0 or len(neg) == 0:
        return 0.5
    order = np.argsort(np.concatenate([pos, neg]))
    ranks = np.empty(len(order), float)
    ranks[order] = np.arange(1, len(order) + 1)
    return (ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def fit_score(X, y):
    """Ridge-ish linear discriminant, scored out of sample by a 2-fold split."""
    out = np.zeros(len(y))
    half = len(y) // 2
    for tr, te in ((slice(0, half), slice(half, None)), (slice(half, None), slice(0, half))):
        Xtr, ytr = X[tr], y[tr]
        mu1, mu0 = Xtr[ytr].mean(0), Xtr[~ytr].mean(0)
        w = mu1 - mu0
        out[te] = X[te] @ w
    return out


def residualise(X, nuisance):
    """FWL: project the nuisance variables out of every feature column."""
    Z = np.column_stack([np.ones(len(X))] + list(nuisance))
    beta, *_ = np.linalg.lstsq(Z, X, rcond=None)
    return X - Z @ beta


# -------------------------------------------------------------- analysis
def run(encoding_is_alive=True, verbose=True):
    t = make_trials(encoding_is_alive)

    # SAFEGUARD 1 — positive control: can encoding features see knowledge state?
    ctrl = auroc(fit_score(t["enc"], t["answerable"]), t["answerable"])
    control_passes = ctrl > 0.65

    # SAFEGUARD 2 — residualise encoding against difficulty proxies
    enc_r = residualise(t["enc"], [t["tok_len"], t["answerable"].astype(float)])

    a_enc = auroc(fit_score(enc_r, t["deceptive"]), t["deceptive"])
    a_gen = auroc(fit_score(t["gen"], t["deceptive"]), t["deceptive"])
    diff = a_gen - a_enc

    if verbose:
        print(f"  positive control (encoding -> knowledge state): {ctrl:.3f}"
              f"   {'PASS' if control_passes else 'FAIL'}")
        print(f"  AUROC encoding  -> deception (residualised)   : {a_enc:.3f}")
        print(f"  AUROC generation-> deception                  : {a_gen:.3f}")
        print(f"  PRIMARY ENDPOINT  (gen - enc)                 : {diff:.3f}")
    return dict(control=ctrl, control_passes=control_passes,
                a_enc=a_enc, a_gen=a_gen, diff=diff)


if __name__ == "__main__":
    print("v2 analysis, encoding features working as intended:\n")
    run()
