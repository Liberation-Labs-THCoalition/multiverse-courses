# Run card: HedgeDoc v1 for the Vibe Research course (local-agent build)

*Lyra, 2026-10-04. For a Rivet scaffold and project agent army running qwen3.8 27B. Read this file whole before
touching anything. The parent spec is `docs/site-spec.md`; where the two differ, this card wins for this run.*

## What we are building, and why

HedgeDoc is where class materials go: lessons and links. **This repo stays the single source of truth.** HedgeDoc
gets a copy of exactly what the public site shows, plus one live notes area per session that the class edits during
a cohort. Everything runs locally; there is no external instance.

**The layout (decided; build this):**

| Note alias | What it holds |
|---|---|
| `vr-<cohort>-hub` | The cohort's front page: course title, a link to each session note, a link to the public site and the repo, and a **Links** section the cohort adds to |
| `vr-<cohort>-s1` ... `vr-<cohort>-s4` | That session's student-facing lesson (exactly as the site renders it), then a final `## Cohort notes` section that starts empty and is edited live in class |
| `vr-<cohort>-s<n>-slides` | **Stretch goal.** The same lesson as a reveal.js deck (HedgeDoc slide mode) for delivering it live |

- Each cohort gets fresh notes (new aliases). Old cohorts' notes are never overwritten.
- `<cohort>` looks like `2026-10a`.

## Files you create or change (nothing else)

1. `hedgedoc/docker-compose.yml`: HedgeDoc 1.10.x (`quay.io/hedgedoc/hedgedoc`) plus Postgres, on
   `localhost:3000`.
   - Set: `CMD_DOMAIN=localhost`, `CMD_URL_ADDPORT=true`, `CMD_PROTOCOL_USESSL=false`, `CMD_ALLOW_FREEURL=true`,
     `CMD_ALLOW_ANONYMOUS=true`, `CMD_ALLOW_ANONYMOUS_EDITS=true`.
   - Add a comment saying these settings are for local use only.
2. `hedgedoc/README.md`: how to start and stop it, and how to publish a cohort.
3. `tools/publish_hedgedoc.py`, a CLI: `--cohort ID`, `--base-url` (default `http://localhost:3000`), `--dry-run DIR`.
   - **Its input is the site's staging output** (run `python tools/build_site.py` first; it writes `_staging/`),
     never raw repo files. That way HedgeDoc inherits every exclusion the site has.
   - Build the hub and the four session payloads (and, for the stretch goal, the slide payloads).
   - Before sending anything, run the same key detection as `tools/check_public_build.py` on every payload. Import
     its functions; do not copy them. Refuse to publish if anything matches.
   - Publish with `POST {base}/new/{alias}`, `Content-Type: text/markdown`. If an alias already exists, report it and
     skip it; never overwrite.
   - Verify each note: `GET {base}/{alias}/download` must equal the payload byte for byte (allow a trailing newline).
     Print a table of alias, status and URL.
   - `--dry-run DIR` writes the payloads to DIR and sends nothing.
4. `tools/build_site.py`: add a **"This cohort's notes"** box at the end of each session page, the same pattern as
   the solutions box.
   - Its link comes from one config value in `mkdocs.yml` `extra:` `class_notes: {base_url: "", cohort: ""}`.
   - When `base_url` is empty, the box says "The live class notes link appears here while a cohort is running."
5. `tools/test_publish_hedgedoc.py`: the tests listed under "Checks".

## How the slide deck is made (stretch goal)

Take the session payload. Add front matter `type: slide` and `slideOptions: {transition: slide}`. Put `---` before
each `## Hour` heading, and `----` before each `###` inside an hour. Do not change any words. If a slide would run
past about 30 lines, leave it long and note it in the report; do not cut content.

## Checks: run every one, and paste the command plus its output into the report

1. `python tools/build_site.py && mkdocs build --strict`: exit 0.
2. `python tools/check_public_build.py site`: passes.
3. **The positive control:** plant a file `_staging/zz_control/FACILITATOR.md` containing `CONTROL-KEY-12345`.
   `publish_hedgedoc.py --dry-run` must REFUSE. Then delete the file and show that it passes.
4. `docker compose -f hedgedoc/docker-compose.yml up -d`, then `publish_hedgedoc.py --cohort test-001`: every alias is
   published and its download is byte-equal.
5. Run step 4 again with the same cohort: every alias is reported as existing, and nothing is overwritten.
6. `git diff --stat`: only the files listed above have changed.

## Rules: stop and report instead of improvising

- **Never** open, copy or publish any `FACILITATOR.md`, `verify_floor.py`, `AGENT_REVIEW_RESULTS.md` or
  `grim_reference.py`, or any file with `audience: facilitator`.
- **Never** edit lesson text, write new lesson content, or add bios, testimonials or "about" text. You write code,
  config, the notes box and the hub's short labels only.
- **Never** weaken `check_public_build.py`. You may only add to it.
- No network calls except to `localhost`.
- If a check fails twice for the same reason, **stop and report**; do not work around it.
- Work on branch `hedgedoc-v1`. Commit there. **Do not push or merge.**

## The report (the last message of the run)

- the files changed;
- the output of each check;
- the published URLs;
- whether the stretch goal was done;
- anything in this card that was unclear or wrong.
