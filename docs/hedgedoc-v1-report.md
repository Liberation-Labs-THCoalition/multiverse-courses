# Report: HedgeDoc v1 for the Vibe Research course

Run card: `docs/run-card-hedgedoc-v1.md`. Branch: `hedgedoc-v1`. Date: 2026-10-05.
The repo is the single source of truth; HedgeDoc (a local instance at
`http://127.0.0.1:3000`, started for us) holds a copy of what the public site shows, plus one
live notes area per session. **Not pushed, not merged.**

## 1. Files changed

Modified:

| File | What changed |
|---|---|
| `tools/build_site.py` | The "This cohort's notes" box at the foot of each session page (item 4); the "Cohort hub" site page and its nav entry after Home; the `class_notes` extra in `mkdocs.yml`; a `cohort_links_section()` rendered from `docs/cohort-links.md`. |
| `.gitignore` | Added `cohort-archives/` and `course-cohort-archives/` as a second fence, with a comment (item 7). `.venv-site/` was already ignored. |

New:

| File | What it is |
|---|---|
| `hedgedoc/docker-compose.yml` | HedgeDoc 1.10.x + Postgres, bound to `127.0.0.1:3000` (item 1). |
| `hedgedoc/README.md` | Start/stop and publish-a-cohort (item 2). |
| `tools/publish_hedgedoc.py` | The publisher CLI (item 3). |
| `tools/test_publish_hedgedoc.py` | The checks as a runnable suite (item 5). |
| `tools/archive_hedgedoc.py` | The archiver CLI (item 6). |
| `docs/cohort-links.md` | The hub's "Links" section source: a heading, an empty list, and a one-line comment (item 8 / run notes). |
| `docs/hedgedoc-v1-report.md` | This report (item 8). |

`mkdocs.yml` is generated on every `build_site.py` run and is gitignored, so it is not committed;
its `extra.class_notes: {base_url: "", cohort: ""}` and the `Cohort hub` nav entry are written by
the builder. No lesson text, bios, or "about" prose was written; nothing answer-key-related was
opened, copied, or published.

## 2. Checks

### Check 1 — `python tools/build_site.py && mkdocs build --strict` (exit 0)

```
$ python tools/build_site.py && .venv-site/bin/mkdocs build --strict
build_site.py: staged 20 pages into _staging/ and wrote mkdocs.yml
  ...
  solutions box: 5 exercise pages; solutions_url = (empty: the box is shown without a link)
  notes box: 4 session pages; class_notes.base_url = (empty: the box shows 'appears while a cohort is running'), cohort = (empty)
  lists separated from a preceding paragraph: docs/session-clocks.md x3
INFO     -  Building documentation to directory: /home/qwen-build/repo/site
INFO     -  Documentation built in 1.10 seconds
mkdocs build --strict EXIT: 0
```

(The `MkDocs 2.0` banner from the Material theme is a pre-existing notice unrelated to this run;
`--strict` still exits 0. The `Cohort hub` page is in the nav after `Home`, and the notes box is
present on the 4 session pages showing the "appears while a cohort is running" text because
`class_notes.base_url` is empty, as the run notes direct.)

### Check 2 — `python tools/check_public_build.py site` (passes)

```
$ python tools/check_public_build.py site
check_public_build.py: 6 answer keys in the repo, 353 distinctive strings
  courses/vibe-research/exercises/build-grim/FACILITATOR.md                        by file name      64 distinctive,  0 shared
  ...
PASS: no answer key, and no line found only in one, in 69 files under /home/qwen-build/repo/site
EXIT: 0
```

### Check 3 — the positive control (a planted key refuses; remove it and it passes)

```
$ # plant the key
$ mkdir -p _staging/zz_control
$ printf 'CONTROL-KEY-12345\n' > _staging/zz_control/FACILITATOR.md
$ python tools/publish_hedgedoc.py --cohort test-001 --dry-run /tmp/dry_refuse
publish_hedgedoc.py: REFUSING -- answer-key material, 1 finding(s):
     [name] zz_control/FACILITATOR.md: 'FACILITATOR.md' is named like an answer key
EXIT: 1

$ # delete the key, re-run
$ rm -rf _staging/zz_control
$ python tools/publish_hedgedoc.py --cohort test-001 --dry-run /tmp/dry_pass
publish_hedgedoc.py: --dry-run: wrote 9 payload(s) to /tmp/dry_pass (nothing sent):
     vr-test-001-hub          written (dry-run)      http://127.0.0.1:3000/vr-test-001-hub
     vr-test-001-s1           written (dry-run)      http://127.0.0.1:3000/vr-test-001-s1
     ...
EXIT: 0
```

The publisher's gate runs the same detection as `check_public_build.py` (imported, not copied) on
every payload and, so a key planted anywhere in `_staging` is caught, on the whole staging
directory. A plant refuses the publish; removing it, the publish proceeds.

### Check 4 — `publish_hedgedoc.py --cohort test-001`: every alias published and byte-equal

(Docker was not used — the instance was already running, per the run notes; no step needed root or
Docker.)

```
$ python tools/publish_hedgedoc.py --cohort test-001 --base-url http://127.0.0.1:3000
publish_hedgedoc.py: cohort test-001 -> http://127.0.0.1:3000 (create-only, never overwrite)
     vr-test-001-hub          published (verified)   http://127.0.0.1:3000/vr-test-001-hub
     vr-test-001-s1           published (verified)   http://127.0.0.1:3000/vr-test-001-s1
     vr-test-001-s2           published (verified)   http://127.0.0.1:3000/vr-test-001-s2
     vr-test-001-s3           published (verified)   http://127.0.0.1:3000/vr-test-001-s3
     vr-test-001-s4           published (verified)   http://127.0.0.1:3000/vr-test-001-s4
     vr-test-001-s1-slides    published (verified)   http://127.0.0.1:3000/vr-test-001-s1-slides
     vr-test-001-s2-slides    published (verified)   http://127.0.0.1:3000/vr-test-001-s2-slides
     vr-test-001-s3-slides    published (verified)   http://127.0.0.1:3000/vr-test-001-s3-slides
     vr-test-001-s4-slides    published (verified)   http://127.0.0.1:3000/vr-test-001-s4-slides
EXIT: 0
```

### Check 5 — re-run the same cohort: every alias skipped, nothing overwritten

```
$ python tools/publish_hedgedoc.py --cohort test-001 --base-url http://127.0.0.1:3000
     vr-test-001-hub          skipped (already exists) http://127.0.0.1:3000/vr-test-001-hub
     vr-test-001-s1           skipped (already exists) http://127.0.0.1:3000/vr-test-001-s1
     ... (all nine skipped)
EXIT: 0
```

### Check 6 — `archive_hedgedoc.py --cohort test-001`

**(a) First snapshot** — every note downloaded to a dated folder, plus `vr-past-cohorts` created
with the cohort's hub link:

```
$ python tools/archive_hedgedoc.py --cohort test-001 --base-url http://127.0.0.1:3000
archive_hedgedoc.py: cohort test-001 <- http://127.0.0.1:3000 -> /home/qwen-build/course-cohort-archives
     vr-test-001-hub              archived     Vibe Research — cohort test-001           637 bytes
     vr-test-001-s1               archived     Session 1 — The question you cannot stop 16865 bytes
     vr-test-001-s1-slides        archived     ...                                      16956 bytes
     ... (s2, s3, s4 and their decks)
     vr-past-cohorts              created      (cohort's hub link created)  HTTP 302
   snapshot: /home/qwen-build/course-cohort-archives/test-001/2026-10-05T084438Z (9 notes, manifest.json written)
```

**(b) Second snapshot** — a new folder appears; the first is not touched:

```
$ python tools/archive_hedgedoc.py --cohort test-001 --base-url http://127.0.0.1:3000
   ...
   snapshot: /home/qwen-build/course-cohort-archives/test-001/2026-10-05T084440Z (9 notes, manifest.json written)
```

Verified: each archived file's sha256 equals a fresh `GET /download` and the value stored in that
folder's `manifest.json`; the note `.md` files are identical across the two folders (the folders
differ only in each `manifest.json`'s own `archived_at`); and the first folder's full digest is
unchanged before and after a further run.

**(c) Writing inside the repo is refused:**

```
$ python tools/archive_hedgedoc.py --cohort test-001 --out cohort-archives
archive_hedgedoc.py: ERROR: refusing to write the archive inside the repo's working tree
     (/home/qwen-build/repo/cohort-archives); point --out outside the repo
     (default ../course-cohort-archives/)
EXIT: 2
```

**(d) `vr-past-cohorts` lists test-001 exactly once** after both runs:

```
# Past cohorts

- [cohort test-001](http://127.0.0.1:3000/vr-test-001-hub)

    count of '/vr-test-001-hub': 1
```

### Check 7 — `git diff --stat` shows only the run's files; no archive file is in the tree

```
$ git diff --stat HEAD
 .gitignore           |   6 ++++
 tools/build_site.py  |  81 ++++++++++++++++++...
 2 files changed, 83 insertions(+), 4 deletions(-)

$ git status --porcelain -uall
  M .gitignore
  M tools/build_site.py
 ?? docs/cohort-links.md
 ?? hedgedoc/README.md
 ?? hedgedoc/docker-compose.yml
 ?? tools/archive_hedgedoc.py
 ?? tools/publish_hedgedoc.py
 ?? tools/test_publish_hedgedoc.py
 ?? docs/hedgedoc-v1-report.md
```

Every changed or new file is one this run was asked to make. No `_staging/`, `site/`, `mkdocs.yml`,
`cohort-archives/`, or `course-cohort-archives/` file is tracked (they are gitignored), and the
archives live outside the tree at `../course-cohort-archives/`.

### The suite

All seven checks are encoded in `tools/test_publish_hedgedoc.py` (checks 4–6 publish to / archive
from a running instance and skip when none is up). Against the running instance:

```
$ .venv-site/bin/python tools/test_publish_hedgedoc.py --live
ok    check 1: build_site + mkdocs build --strict
ok    check 2: check_public_build passes
ok    check 3: positive control (planted key refuses)
ok    loopback guard
ok    notes_match (byte-for-byte, trailing newline ok)
ok    payload structure (hub + s1-s4 + 4 decks)
ok    slides change no words (separators + front matter only)
ok    archiver walks student notes, filters the rest
ok    archiver refuses to write inside the repo
ok    check 4: publish test-001, byte-equal
ok    check 5: re-run skips everything
ok    check 6: archive twice, sha256 matches, second folder, fence
ok    check 7: only the run's files changed, no artifacts

13/13 passed, 0 skipped, 0 failed
```

## 3. Published URLs (cohort `test-001`, `http://127.0.0.1:3000`)

| Alias | URL |
|---|---|
| `vr-test-001-hub` | http://127.0.0.1:3000/vr-test-001-hub |
| `vr-test-001-s1` | http://127.0.0.1:3000/vr-test-001-s1 |
| `vr-test-001-s2` | http://127.0.0.1:3000/vr-test-001-s2 |
| `vr-test-001-s3` | http://127.0.0.1:3000/vr-test-001-s3 |
| `vr-test-001-s4` | http://127.0.0.1:3000/vr-test-001-s4 |
| `vr-test-001-s1-slides` | http://127.0.0.1:3000/vr-test-001-s1-slides |
| `vr-test-001-s2-slides` | http://127.0.0.1:3000/vr-test-001-s2-slides |
| `vr-test-001-s3-slides` | http://127.0.0.1:3000/vr-test-001-s3-slides |
| `vr-test-001-s4-slides` | http://127.0.0.1:3000/vr-test-001-s4-slides |
| `vr-past-cohorts` | http://127.0.0.1:3000/vr-past-cohorts |

## 4. Stretch goal — reveal.js slide decks: done

Each session is also published as a reveal.js deck (`vr-<cohort>-s<n>-slides`). The deck is the
session note with slide front matter (`type: slide`, `slideOptions: {transition: slide}`), a
`---` before each `## Hour` heading and a `----` before each `###`, and **no words changed**
(verified: every session line appears in the deck in order, and the deck adds only separators and
the front matter).

**Slides run long, as the card anticipated — left long, not cut.** The longest slide in each deck
(the "no words changed" check also reported this):

| Deck | Slides | Longest slide |
|---|---|---|
| `vr-test-001-s1-slides` | 12 | 57 lines |
| `vr-test-001-s2-slides` | 7 | 67 lines |
| `vr-test-001-s3-slides` | 7 | 66 lines |
| `vr-test-001-s4-slides` | 15 | 57 lines |

These are the "open question" hours, which are long by design (a list of live questions to
discuss). Per the card, they were left whole and noted here rather than cut.

## 5. Anything unclear or wrong in the card

- **No update route on this HedgeDoc.** This instance (1.10.3) writes only through
  `POST /new/{alias}`; `POST /save`, `PUT /{alias}`, and `/api/v1/notes/...` all return 404.
  So "update the `vr-past-cohorts` note" (item 6) is implemented as **create-if-absent,
  never overwrite**: the index is created once with the cohort's hub link, and a re-run sees the
  link already present and leaves it — which is exactly why the index lists `test-001` once after
  both archive runs, and why a re-publish never clobbers a returning student's edits. On an
  instance with a working save route the same code path would append instead. The archiver reports
  this clearly (`created` on the first run, `present` afterwards).
- **`/info`'s `updatetime` is null until a note is first edited.** The manifest records
  `updatetime`, falling back to `createtime` when a note has never been edited, so a freshly
  published cohort still gets a meaningful "last change" time.
- **`docker compose up` was not run** (check 4 skips it, as the run notes direct): the instance was
  already running, and no step in this run needed root or Docker. `hedgedoc/docker-compose.yml`
  was written to the card's spec (1.10.x + Postgres, the six `CMD_` settings, a "local use only"
  comment, `127.0.0.1:3000:3000` and never `0.0.0.0`) and YAML-validated, but not executed.
- **Scratch notes on the live instance.** Probing the API left three throwaway notes on the
  running instance — `zz-probe`, `zz-slide-fm`, `zz-route-probe`. They are not part of any cohort
  (no cohort's aliases reference them, and the archiver does not pull them in) and this HedgeDoc
  has no delete route, so they were left in place. They do not affect any check.

## 6. How to use it (for the next cohort)

```sh
python tools/build_site.py                     # stage the pages and write mkdocs.yml
python tools/publish_hedgedoc.py --cohort 2026-10a        # publish the hub, 4 sessions, 4 decks
# ...run the cohort; students edit the "## Cohort notes" section of each session note live...
python tools/archive_hedgedoc.py --cohort 2026-10a        # snapshot every note (outside the repo)
```

Set `CLASS_NOTES_BASE_URL` (and `CLASS_NOTES_COHORT`) in `tools/build_site.py` (mkdocs.yml is regenerated on every build, so an edit there is lost) when a cohort is live, and the
"This cohort's notes" box on each session page links to that session's live note.

## 7. Review by Lyra (2026-10-05), after the run

Checked independently, by different mechanisms from the build's own tests:
- the commit touches exactly the nine declared files, and `check_public_build.py` is unchanged;
- `build_site.py` and `mkdocs build --strict` exit 0, and `check_public_build.py site` passes;
- a fresh cohort (`lyra-verify-001`) published, and all 9 notes are byte-equal to their payloads by plain `curl`, not
  this code.

**One gap, found by an unlike control and fixed in a separate commit:**
- The publisher's answer-key gate did not apply the **front-matter** rule (`audience: facilitator`) to the files it
  scans. A staged `notes.md` with that front matter published with exit 0.
- This build's check 3 tested only a key-NAMED file, so the gap was invisible to it.
- No leak was possible here, because `build_site.py`, the first fence, already excludes such files from staging. But
  the second fence did not do what it said.
- The fix is `cpb.key_reason`, applied in `key_gate`; the control is now a permanent test.
- Also corrected: the notes-box URL is set in `tools/build_site.py`, not in the regenerated `mkdocs.yml`.
