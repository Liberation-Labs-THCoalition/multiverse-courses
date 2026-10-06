# Mystery deck (splash teaser v2) — build report

*Branch `mystery-deck-v1`, off `master` (`aa00db1`). Local-model build (qwen3.8, scoped
account, no sudo, no Docker). 2026-10-05. Run card: `docs/run-card-mystery-deck-v1.md`.*

The splash teaser counter climbs to 93% and glitches to 20%. This build adds **the mystery
deck**: a swipeable stack below the hero where each card goes *mystery → inspect the evidence →
commit a prediction → reveal*. Every word is the final `splash/src/deck/cards.json` (rendered,
never changed); this build only adds the interaction around it.

---

## 1. Files changed

Modified (tracked, vs the branch baseline commit `4d8c920`):

| File | Change |
|---|---|
| `splash/src/App.jsx` | +18: import `Deck`; render the **"See how: play the deck"** button gated on the counter finishing its glitch to 20% (`showGlitch`), and a `<Deck />` section below the hero. |
| `splash/src/App.css` | +30: `.teaser-deck-cta` / `.teaser-deck-btn` (plus `:hover` and `:focus-visible`). |
| `splash/THIRD_PARTY.md` | record `Components/Stack` (React Bits, MIT) and how it is used. |
| `splash/public/llms.txt` | +1: the one line the card specifies, nothing else. |

New (untracked):

| File | Purpose |
|---|---|
| `splash/src/components/Deck.jsx` | The controller: card state, inspect → commit → reveal, prev/next + arrow keys + swipe/drag, "card N of 6", the closing panel, per-card reveal memory in `localStorage` (try/catch), `aria-live` announcement, reduced-motion. |
| `splash/src/components/Deck.css` | The plain-CSS 3D flip (`perspective` + `preserve-3d` + `rotateY(180deg)` + `backface-visibility:hidden`), focus outlines, `@media (prefers-reduced-motion)` turning the flip/drag off, and `@media (max-width:480px)` responsive tweaks. |
| `splash/src/components/Components/Stack.jsx`, `Stack.css` | Verbatim copy of React Bits `Components/Stack` (see §3). |
| `tools/check_links.py` | The internal-link checker with a positive-control self-test. |
| `docs/screenshots/*.png` | Four phone-width screenshots (see §4). |
| `docs/mystery-deck-v1-report.md` | This report. |

**Not changed:** `splash/src/deck/cards.json` (byte-identical — §2 check 1), `splash/package.json`
and `splash/package-lock.json` (no new dependency — §3), and none of the course pages, the
facilitator material, `check_public_build.py`, or the HedgeDoc tools.

---

## 2. The seven checks

### Check 1 — the deck content is unchanged

The card's literal command is `git diff --quiet master -- splash/src/deck/cards.json && echo
UNCHANGED`. That does **not** print `UNCHANGED`, but for a reason that is *not* a content change:
`cards.json` does not exist on `master` at all — it was **added on this branch** in `4d8c920`.
So a diff against `master` compares "no file" with "the file", which is never quiet. The card's
*intent* — "the deck content is byte-identical to what the branch started with" — is verified
against the branch baseline instead:

```
$ git cat-file -e master:splash/src/deck/cards.json ; echo "exists on master?"
exit status 128   → cards.json is ABSENT on master (added on this branch)

$ git diff --quiet master  -- splash/src/deck/cards.json && echo UNCHANGED   # card's literal command
(exit 1, no UNCHANGED — expected: the file is new on the branch)

$ git diff --quiet HEAD   -- splash/src/deck/cards.json && echo UNCHANGED     # vs the branch state I started from
UNCHANGED

$ git diff --quiet 4d8c920 -- splash/src/deck/cards.json && echo UNCHANGED     # vs the last commit on the branch
UNCHANGED vs 4d8c920
```

**Result: PASS** — `cards.json` is byte-identical to the branch baseline; nothing was reworded,
added, or removed. (See "unclear/wrong" §5: the literal `master` comparison cannot pass for a
file that does not exist on `master`.)

### Check 2 — the splash builds

```
$ cd splash && npm ci && npm run build
npm ci exit: 0
> vibe-research-splash@0.1.0 build
> vite build
vite v5.4.21 building for production...
transforming...
✓ 454 modules transformed.
computing gzip size...
dist/index.html                    0.53 kB │ gzip:  0.36 kB
dist/assets/index-ZgnLGi4j.css   11.47 kB │ gzip:  3.05 kB
dist/assets/index-Kkon889I.js   379.37 kB │ gzip: 129.05 kB
✓ built in 4.33s
```

**Result: PASS, exit 0.** (The `npm audit` notice in `npm ci`'s output is advisory, not an error.)

### Check 3 — the built bundle contains the content

Grep the built JS for every card `title`, the `fiction_notice` text, and `data-fictional`
(React compiles the `data-fictional` attribute to a `data-fictional` string in the bundle):

```
$ JS=$(find splash/dist -name '*.js')
for t in "Emergence?" "Selected for the trend" "Being wrong well" \
         "A goal, missed, said plainly" "A true one" "The greenhouse chart"; do
  grep -Fq "$t" "$JS" && echo "FOUND title: $t" || echo "MISSING title: $t"; done
FOUND title: Emergence?
FOUND title: Selected for the trend
FOUND title: Being wrong well
FOUND title: A goal, missed, said plainly
FOUND title: A true one
FOUND title: The greenhouse chart
grep -Fq "There was never a houseplant podcast trial" "$JS" && echo "FOUND fiction_notice"
FOUND fiction_notice
grep -Fq "check that its source exists." "$JS" && echo "FOUND fiction_notice tail"
FOUND fiction_notice tail
grep -o data-fictional "$JS" | head -1
data-fictional
grep -Fq "Did you spot the false premise?" "$JS" && echo "FOUND closing question"
FOUND closing question
grep -Fq "You predicted before you looked." "$JS" && echo "FOUND predicted-line"
FOUND 'You predicted before you looked.'
```

**Result: PASS** — all six titles, the `fiction_notice` (head and tail), `data-fictional`, the
closing question, and the "You predicted before you looked." line are all in the built bundle.

### Check 4 — the course site builds and passes the public-build gate

`python` is not on PATH in this environment (only `python3`); the tools are stdlib-only, and
`mkdocs` lives in the venv, so the venv interpreter runs them (see §5):

```
$ .venv-site/bin/python tools/build_site.py ; echo rc=$?
   ... (audit/delivery notes) ...
rc=0
$ .venv-site/bin/mkdocs build --strict ; echo rc=$?
INFO  -  Cleaning site directory
INFO  -  Building documentation to directory: /home/qwen-build/repo/site
INFO  -  Documentation built in 1.21 seconds
rc=0
$ .venv-site/bin/python tools/check_public_build.py site
check_public_build.py: 6 answer keys in the repo, 353 distinctive strings
  ... (6 keys, each with 0 or few shared lines) ...
PASS: no answer key, and no line found only in one, in 69 files under /home/qwen-build/repo/site
rc=0
```

**Result: PASS, all exit 0.**

### Check 5 — the link checker: control fails, real build passes

```
$ python3 tools/check_links.py --self-test
check_links.py: self-test on a temporary copy (real builds are not touched)
    ok     control: the unmodified copy is clean
    ok     planted broken link is reported (caught)
    ok     clean again after removal
self-test PASSED: the clean copy passes and the planted link fails the check.
rc=0
```

The positive control works: on a temp copy the checker first passes, then **fails** when a page
linking to `definitely-missing-file.html` is planted, then passes again after removal.

On the real build, there are **no broken internal links**, and external links are listed only:

```
$ python3 tools/check_links.py
check_links.py: /home/qwen-build/repo/site
    21 HTML file(s), 37 external link(s) listed (not fetched)
  external (listed only, not fetched):
      - https://declaredesign.org/
      - https://doi.org/10.1145/3641525.3663626
      - https://doi.org/10.1145/3736731.3746162
      - https://doi.org/10.1177/1948550616673876
      - https://doi.org/10.1371/journal.pone.0250755
      - https://github.com/Liberation-Labs-THCoalition/multiverse-courses/blob/master/CONTRIBUTING.md
      - https://liberation-labs-thcoalition.github.io/multiverse-courses/course/
      - https://liberation-labs-thcoalition.github.io/multiverse-courses/course/cohort-hub/
      ... (37 total, incl. the course pages, exercises, and sources)
  PASS: no broken internal links
check_links.py: /home/qwen-build/repo/splash/dist
    1 HTML file(s), 0 external link(s) listed (not fetched)
  PASS: no broken internal links
rc=0
```

**Result: PASS.** The `site/` internal links all resolve once the MkDocs deployment base
(`/multiverse-courses/course/`) is stripped — a site built for a sub-path emits root-absolute
links (`/multiverse-courses/course/cohort-hub/`) that live locally at `site/cohort-hub/`, so the
checker tries the base-stripped target before the raw one. `splash/dist/` has no internal links
to check (its only outbound reference is `llms.txt`, which is copied verbatim into `dist/`).

### Check 6 — phone width

A headless browser was installable without sudo (`puppeteer-core` driving the system
`/usr/bin/google-chrome`), so screenshots were taken. `docs/screenshots/`:

| File | Width | What it shows |
|---|---|---|
| `splash-390.png` | 390 | Hero, the counter **glitched to 20%**, and the **"See how: play the deck"** button under it, then "THE MYSTERY DECK" with the first card beginning. |
| `deck-false-premise-390.png` | 390 | The fictional card (card 6 of 6) turned over: the `reveal`, the orange `fiction_notice` box, and "You predicted before you looked." |
| `closing-390.png` | 390 | The closing panel: "Did you spot the false premise?" + body + "See the deck again". |
| `deck-360.png` | 360 | Card 1 ("Emergence?") front at the narrowest required width — Inspect button, "card 1 of 6", Prev/Next. |

Live accessibility facts, measured in the same headless run against `vite preview`:

```
# reduced motion: the flip must be instant
reduced-motion .deck-card__inner transitionDuration: 0s        ✓ (flip/drag off)

# 360px: no horizontal scroll, fictional card still correct in the DOM
360px fictional card: {"fictional":"true","hasNotice":true,
  "predictedLine":"You predicted before you looked.",
  "scrollW":360,"innerW":360,"overflowPx":0}                    ✓ (fits, no overflow)

# interaction contract, live DOM
card0 reveal before inspect:            hidden          ✓
card0 shows "It holds up" / "It falls apart":  true     ✓
card0 reveal disabled before commit:    true            ✓
card0 reveal enabled  after  commit:    true            ✓
card5 (fictional) shows "Fix the axis (metres → centimetres)": true ✓
card5 shows "It holds up"/"It falls apart":  false      ✓  (single commit button)
```

**No correct/wrong marks, no score.** A grep for `score`/`correct`/`wrong` in the deck DOM finds
only the *content* from `cards.json` — e.g. the intro "You don't score by being right", the
closing "Neither answer is a score", and the card title "Being wrong well" — never a scoring or
correctness UI. `Deck.jsx` contains no scoring/correctness element (only a code comment stating
there is none).

**Result: PASS** — usable at 360–414px; reduced-motion turns the flip/drag into instant changes;
focus is visible (`:focus-visible` outlines); the reveal is announced via `aria-live="polite"`.

### Check 7 — the diff shows only the listed files

The card's literal command `git diff --stat master` shows more than this task's files, because
`master` (`aa00db1`) is **four commits behind** the branch tip — those four commits (HedgeDoc work,
the run card itself, and the `cards.json`/deck-content commit `4d8c920`) are also "after"
`master`:

```
$ git diff --stat master
 .gitignore                        |    6 +
 docs/cohort-links.md              |    4 +
 docs/hedgedoc-v1-report.md        |  303 ++++
 docs/run-card-mystery-deck-v1.md  |  104 +
 hedgedoc/GOING_LIVE.md            |   48 +
 hedgedoc/README.md                |   57 +
 hedgedoc/docker-compose.yml       |   48 +
 splash/THIRD_PARTY.md             |    9 +
 splash/public/llms.txt            |    1 +
 splash/src/App.css                |   30 ++
 splash/src/App.jsx                |   18 +
 splash/src/deck/cards.json        |   76 +
 tools/archive_hedgedoc.py         |  280 ++
 tools/build_site.py               |   83 ++
 tools/publish_hedgedoc.py         |  291 ++
 tools/test_publish_hedgedoc.py    |  398 +++
 16 files changed, 1752 insertions(+), 4 deletions(-)
```

The **task delta** — everything this work added, measured against the branch baseline `4d8c920`
(the last commit before this task) plus the new untracked files — is confined to exactly the
files the card lists:

```
$ git diff --stat 4d8c920 -- . ':(exclude)site' ':(exclude)_staging'
 splash/THIRD_PARTY.md   |  9 +++++++++
 splash/public/llms.txt  |  1 +
 splash/src/App.css      | 30 ++++++++++++++++++++++++++++++
 splash/src/App.jsx      | 18 ++++++++++++++++++
 4 files changed, 58 insertions(+)

$ git status --porcelain --untracked-files=all | grep '^??'
?? docs/screenshots/closing-390.png
?? docs/screenshots/deck-360.png
?? docs/screenshots/deck-false-premise-390.png
?? docs/screenshots/splash-390.png
?? splash/src/components/Components/Stack.css
?? splash/src/components/Components/Stack.jsx
?? splash/src/components/Deck.css
?? splash/src/components/Deck.jsx
?? tools/check_links.py
```

Every one of those is in the card's "Files you may create or change" list. `site/` and
`_staging/` are gitignored and untouched by this task; `package.json`/`package-lock.json` are
unchanged (`git diff --quiet 4d8c920 -- splash/package.json splash/package-lock.json` → UNCHANGED).

**Result: PASS** — the task's changes are confined to the allowed files. (See §5: the literal
`git diff --stat master` includes four pre-existing commits and so shows more than this task's
files.)

---

## 3. Components used, with licences

**React Bits** — `DavidHDev/react-bits`, **MIT** (https://github.com/DavidHDev/react-bits). The
existing splash already used `Backgrounds/DotGrid`, `TextAnimations/{DecryptedText,CountUp,
TrueFocus}`, and `Animations/StarBorder`; this build adds one more, copied verbatim the same way
(the files sit under `splash/src/components/<Category>/` and are recorded in `splash/THIRD_PARTY.md`
with the MIT text):

- **`Components/Stack`** — a draggable, send-to-back card gallery
  (https://github.com/DavidHDev/react-bits/blob/main/src/content/Components/Stack/Stack.jsx).
  It is used here for the **fanned "peek" of the upcoming cards** (rendered behind the active
  card, `pointer-events:none`, hidden under reduced motion and at ≤480px). The card also mentions
  **Card Swap**; its React Bits source is a GSAP auto-cycling gallery, which suits a
  *self-advancing* carousel rather than a deck the player controls, so it was not used. All
  controlled behaviour — prev/next buttons, arrow keys, swipe/drag, the "card N of 6" counter, the
  closing panel, and the per-card inspect → commit → reveal flow — lives in `Deck.jsx`, and the
  **reveal flip is a plain-CSS 3D transform** (no library).
- `Stack` imports the **`motion`** package (a build of framer-motion), which is **already a
  dependency of this app**. **No npm dependency was added or changed**
  (`git diff --quiet 4d8c920 -- splash/package.json splash/package-lock.json` → UNCHANGED), so the
  card's "no new dependency unless justified" clause is satisfied without justification: none was
  needed.

Everything else in the deck is first-party code (`Deck.jsx`, `Deck.css`).

---

## 4. What the deck looks like at phone width

Four screenshots are saved under `docs/screenshots/` (390px and 360px, device-scale-factor 2):

- **`splash-390.png`** — the top of the page: "Vibe Research" hero, the counter **glitched to 20%
  in red**, the teaser paragraph + citation, and the **"SEE HOW: PLAY THE DECK"** button directly
  under the 20%. Below it, the "THE MYSTERY DECK" heading, the intro, and the first card
  ("Emergence?") beginning.
- **`deck-false-premise-390.png`** — the fictional card (card 6 of 6) turned over: "Nicely
  caught: the axis should say centimetres, not metres. But there's a bigger problem.", the **orange
  fiction-notice box** ("This study is invented. There was never a houseplant podcast trial…
  check that its source exists."), and the italic "You predicted before you looked." at the foot.
  Prev/Next with "card 6 of 6" are below.
- **`closing-390.png`** — the closing panel: "Did you spot the false premise?" with its body and a
  "See the deck again" button.
- **`deck-360.png`** — card 1 front at the narrowest required width: "Emergence?" + mystery, an
  "Inspect" button, and "card 1 of 6" with disabled "← Prev" / "Next →". No horizontal scroll.

On the active card the front shows `title` + `mystery` and an **Inspect** button; Inspect reveals
`inspect` plus the commit controls, and the **Turn it over** button stays disabled until a commit.
Normal cards offer **"It holds up"** / **"It falls apart"**; the fictional `false-premise` card
offers the single **"Fix the axis (metres → centimetres)"**. The reveal shows `reveal` + sources
(a `url` renders as a link; a `null` `url` renders the label without a link — e.g. the
Redwood Research / LessWrong source) + the `fiction_notice` on the fictional card + "You predicted
before you looked." The card front is the height sizer and the back is an absolutely-positioned
overlay that flips with `rotateY(180deg)`; `overflow-y:auto` on the back keeps long reveals
scrollable instead of overflowing.

---

## 5. Anything in the card that was unclear or wrong

Nothing was wrong in a way that blocked the work, but three things in the card did not match this
branch's state and are reported here (the run card says to stop and report rather than improvise):

1. **Checks 1 and 7 compare against `master`, but `master` is four commits behind the branch.**
   `master` is `aa00db1`; the branch tip is `4d8c920`, which added the deck content
   (`splash/src/deck/cards.json`) and the run card. So:
   - **Check 1** (`git diff --quiet master -- splash/src/deck/cards.json`) can never print
     `UNCHANGED`, because `cards.json` **does not exist on `master`** — a "no file vs file" diff is
     always non-zero. The *intent* (content unchanged since this task started) holds: the diff
     against the branch baseline `4d8c920` / `HEAD` prints `UNCHANGED`. I used that.
   - **Check 7** (`git diff --stat master`) shows 16 files, four of them from pre-existing commits
     (HedgeDoc, `docs/run-card-mystery-deck-v1.md`, `cards.json`…). The task's true delta is the
     `git diff --stat 4d8c920` (4 files) plus the new untracked files, all inside the allowed list.
   If `cards.json` had been committed to `master` before this branch, both checks would pass
   literally. The mismatch is the branch baseline, not a defect in this build.

2. **`python` is not on PATH** (only `python3`), so the literal `python tools/build_site.py &&
   .venv-site/bin/mkdocs build --strict` would fail on the first word. The `tools/*.py` are
   stdlib-only and run under `python3`; `mkdocs` lives in `.venv-site`, so its interpreter
   (`.venv-site/bin/python`) runs the site gate. Same commands, same results, correct interpreter.

3. **`check_links.py` had to understand MkDocs's deployment base.** A course site built for a
   sub-path (`site_url: …/multiverse-courses/course/`) emits root-absolute internal links like
   `/multiverse-courses/course/cohort-hub/` that resolve only after stripping that base; a naive
   "does the file exist under `site/`?" check reports 26 false positives (all in Material's
   `404.html`). The checker therefore detects the shared base of the root-absolute links and tries
   the base-stripped target before the raw one. This is a property of the existing course build,
   not of this task; it is documented in the checker's header.

Other notes:

- A headless run logs one **`404` for `/favicon.ico`** — the browser auto-requests it, there is no
  favicon file, and adding one is outside this card's allowed-file list, so it was left alone. It
  has no effect on the page (no page error; the deck and every check pass).
- A naive word-grep flags `score`/`wrong` in the deck DOM; these are the *content* of
  `cards.json` (the intro "You don't score by being right", the closing "Neither answer is a
  score", the title "Being wrong well", source name "LessWrong"), not a scoring/correctness UI.
  `Deck.jsx` has no such element.

All seven checks pass; the deck renders the final content unchanged, the fiction is marked for both
humans and scrapers (`data-fictional="true"` + a visible `fiction_notice` + the `llms.txt` line),
and no new dependency was added.

---

## 6. Review (Lyra, 2026-10-05)

I checked this on Windows from a git bundle of `c02be3a`, re-running everything rather than reading the claims.

**Confirmed:**
- `cards.json` is the same blob as master `4d8c920` (`dce9b7c9`).
- All 14 changed files are on the card's list, and no dependency was added.
- The splash rebuilds to the same content hashes as the build on MTH (`index-Kkon889I.js`, `index-ZgnLGi4j.css`).
- `Stack.jsx` and `Stack.css` are byte-identical to React Bits `main` (MIT, recorded in `THIRD_PARTY.md`).
- Neither the added lines nor the built bundle contain instructions to models. The bundle grep's control string was
  found, so the grep could have caught one.
- In `Deck.jsx` and the screenshots: the reveal waits for a commit, there is no score anywhere, `data-fictional` is
  on the card, and the fiction notice is visible.
- **§5's point 1 was my error, not the agent's.** I branched the build from `origin/master` and left the clone's
  `master` at `aa00db1`, so checks 1 and 7 compared against a stale ref. The agent reported it and used the right
  baseline. Future run cards pin the baseline by commit, not by branch name.

**Fixed in the review commit:**
1. **`check_links.py` failed open on the breakage its control never planted.** It inferred the deployment base from
   the links being checked, which caused two failures:
   - A root-absolute link outside that base resolved to the build root, which has an `index.html`. So
     `/no-such-page/` passed, and so did a lone broken `<img src="/x.png">` on the splash.
   - A relative link that climbed out of the build passed whenever the file existed on the local disk.

   The self-test planted only a relative link, which never reaches either path.
   - **Rewritten:** it now checks the tree as `pages.yml` assembles it (splash at the root, course under `course/`),
     with the project path read from `SITE_URL`.
   - Full URLs into our own site are now checked, not listed. They are 20 of the first version's 37 "externals", and
     20 + 17 = 37.
   - The self-test now plants 9 kinds of link, broken and valid alike, and every one gets the expected verdict. The
     real tree passes.
2. **Desktop layout.** The "rest of the deck" preview hung off the right of the active card (`left: 50%` with no
   `-50%`). It now sits behind the card and peeks out. The card's checks covered phone widths only, where the
   preview is hidden.
3. **Screen readers** heard the fictional card's reveal without its fiction notice. The announcement now includes it,
   since the notice is the point of that card.
4. **Arrow keys:** Up and Down no longer turn cards, so they scroll the page again. The card asked only for ← →.
5. **The preview** repeats a card's words, so it now carries the same `data-fictional` marker.
6. **Touch:** the stage now has `touch-action: pan-y pinch-zoom`, so phone browsers hand horizontal swipes to the
   deck and pinch-zoom still works. A cancelled pointer now clears a half-finished swipe. **Not yet tried on a real
   phone.**

**After the fixes:**
- `npm run build`, `build_site.py`, `mkdocs build --strict` and `check_public_build.py site` all pass.
- `check_links.py --self-test` passes 9 of 9 plants plus the baseline.
- `check_links.py` passes on the real tree.
