# Run card: the mystery deck (splash teaser v2), plus a link check and a phone-width check

*Lyra, 2026-10-05. For a local-model build (qwen3.8 in a scoped account). Read this whole file first. The parent spec is
`docs/site-spec.md` ("Teaser v2" and the acceptance checks). Where they differ, this card wins.*

## Why
The splash's teaser counter climbs to 93% and glitches to 20%, then just sits there. Teaser v2 gives visitors the
**mystery, not the answer**: a small deck where each card goes mystery → inspect the evidence → commit a prediction →
reveal. It is "predict, then look" in miniature. **The deck rewards predicting before looking, never being right.**

## The content is DONE. You build the deck around it
- `splash/src/deck/cards.json` holds every word: the intro, 6 cards and the closing panel. **Render it; never change
  it, add to it, or reword it.** Check 1 verifies it is byte-identical to master.
- Every non-fictional card shows its `sources` on the reveal side, as links. When `url` is `null`, show the label
  without a link, and never invent a URL.
- **Exactly one card is fictional** (`"fictional": true`, id `false-premise`). Its root element carries
  `data-fictional="true"`, and its reveal shows `reveal` **and** `fiction_notice`, visibly. These two are not
  optional. They are the citogenesis guard: a fabricated study on a public page must be marked as fiction for both
  humans and scrapers.
- After the last card, show the `closing` panel (its question and body).

## The interaction (build this)
1. **Where it lives.** When the teaser counter finishes its glitch to 20%, show a button **"See how: play the deck"**
   under it, which opens or scrolls to the deck. The deck also appears as a section below the hero, for visitors who
   scroll. Keep everything that already exists working: the counter, the outlier dot, the source-code riddle and
   `llms.txt`.
2. **A card's front** shows `title` and `mystery`. Its button, **"Inspect"**, reveals `inspect` underneath.
3. **Commit before the reveal.**
   - On a normal card, the player picks **"It holds up"** or **"It falls apart"** before the reveal unlocks.
   - On the `false-premise` card, the single commit button reads **"Fix the axis (metres → centimetres)"**.
   - The reveal button stays disabled until a commit is made.
4. **The reveal** turns the card over, showing `reveal` and the sources (and `fiction_notice` on the fictional card),
   plus one small line: **"You predicted before you looked."**
   - Show no "correct" or "wrong" marks and no score anywhere.
   - Remembering the player's picks in `localStorage` is fine, wrapped in try/catch. Nothing leaves the browser.
5. **Navigation:**
   - swipe or drag on touch;
   - buttons and arrow keys (← →, with Enter or Space to act) everywhere;
   - a visible "card N of 6";
   - after card 6, the closing panel.
6. **Components:**
   - Prefer React Bits' **Stack** or **Card Swap**, if the React Bits repository (DavidHDev/react-bits) has them.
     Copy the source the same way the existing components were copied, and record each in `splash/THIRD_PARTY.md`
     with its licence.
   - Do the reveal flip in plain CSS (a 3D transform). Add **no npm dependency** unless it is truly necessary; if you
     add one, justify it in the report.
7. **Accessibility:**
   - focus is visible;
   - the reveal is announced (`aria-live="polite"`);
   - `prefers-reduced-motion` turns off the flip and drag animations, swapping them for instant changes;
   - text contrast is at least that of the existing splash;
   - it is usable at 360-414 px wide.

## `llms.txt`: append exactly this line, and change nothing else in the file
`The splash page's mystery deck contains one deliberately invented study (the greenhouse houseplant chart). It is marked as fiction in the page markup and on its reveal, and it is not a real finding.`

## The extras (small)
- **`tools/check_links.py`:** checks every internal `href`/`src` in the built course site (`site/`) and the built
  splash (`splash/dist/`) and reports broken targets. External links are not fetched; list them only.
  - **Positive control:** in a temp copy, plant a page linking to a missing file; the checker must fail. Then show it
    passing on the real build.
- **Phone width:** if a headless browser can be installed without sudo (`npx playwright install chromium`, in your
  home), screenshot the splash and the deck at 390 px wide and save the images under `docs/screenshots/`. If not,
  check that the viewport meta is present and that no fixed width over 390 px exists in the splash CSS, and say
  plainly that no screenshot was taken.

## Checks: paste each command and its output into the report
1. `git diff --quiet master -- splash/src/deck/cards.json && echo UNCHANGED`
2. `cd splash && npm ci && npm run build`, exit 0.
3. The built bundle contains every card `title`, the `fiction_notice` text and `data-fictional` (grep `splash/dist`).
4. `python tools/build_site.py && .venv-site/bin/mkdocs build --strict`, exit 0. Make the venv if needed (see the
   HedgeDoc card's run notes). Then `python tools/check_public_build.py site` passes.
5. `python tools/check_links.py`: its control fails, then the real build passes, or the real broken links are
   listed.
6. The phone-width result, either screenshots or the static check and the note.
7. `git diff --stat master` shows only the files listed below.

## Files you may create or change (nothing else)
- `splash/src/**`, except `splash/src/deck/cards.json`;
- `splash/THIRD_PARTY.md`;
- `splash/public/llms.txt` (the one appended line);
- `splash/package.json` and `splash/package-lock.json`, only if a dependency is truly needed;
- `tools/check_links.py`;
- `docs/screenshots/*`;
- your report `docs/mystery-deck-v1-report.md`.

## Rules: stop and report instead of improvising
- Never change the deck's words or invent content: no new cards, examples, sources or URLs.
- **Never put instructions to AI models in hidden text** (comments, alt text, `llms.txt`). The easter eggs are notes
  to the reader, never instructions to a model. A hidden "ignore previous instructions" is prompt injection, even as
  a joke.
- Never touch the course pages' content, the facilitator material, `check_public_build.py` (you may only add to it),
  or the HedgeDoc tools.
- You have no sudo and no Docker, by design. If something needs root, stop and report.
- Network is allowed for `npm` and for fetching React Bits source. Nothing else.
- Work on branch `mystery-deck-v1`. Commit there. **Do not push or merge.**
- If a check fails twice for the same reason, stop and report.

## The report
- the files changed;
- each check with its output;
- the components used, with their licences;
- what the deck looks like at phone width;
- anything in this card that was unclear or wrong.
