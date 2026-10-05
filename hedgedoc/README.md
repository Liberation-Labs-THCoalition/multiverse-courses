# HedgeDoc for Vibe Research

Local HedgeDoc instance where class materials go: the cohort's hub, one live notes note per
session, and the slide decks. **The repo stays the single source of truth**; HedgeDoc holds a
copy of exactly what the public site shows, plus a live notes area per session.

The instance is `http://localhost:3000` (the port is bound to `127.0.0.1`, so only this machine
can reach it). See `docs/run-card-hedgedoc-v1.md` for the run card.

## Start and stop

```sh
docker compose -f hedgedoc/docker-compose.yml up -d
# ...use it at http://localhost:3000 ...
docker compose -f hedgedoc/docker-compose.yml down
```

The compose file pins `quay.io/hedgedoc/hedgedoc` to the 1.10.x line with Postgres, and switches
on anonymous creation and edits **for local use only** — the port is bound to the loopback so
nothing outside this machine can reach an anonymous-editable instance. Do not change that bind.

> For the first local run the instance was already started for us, so these commands are not run
> here; the tools publish straight to the running instance.

## Publish a cohort

HedgeDoc notes are published from the **site's staging output**, never from raw repo files, so
HedgeDoc inherits every exclusion the site has. Run the site builder first, then publish:

```sh
# 1. stage the pages and write mkdocs.yml
python tools/build_site.py

# 2. (optional) publish for real, or dry-run into a directory first
python tools/publish_hedgedoc.py --cohort 2026-10a
python tools/publish_hedgedoc.py --cohort 2026-10a --dry-run ./preview   # write payloads, send nothing

# 3. at the end of the cohort (or whenever wanted), snapshot every note
python tools/archive_hedgedoc.py --cohort 2026-10a
```

A cohort looks like `2026-10a`. Each cohort gets fresh note aliases:

| Alias | Holds |
|---|---|
| `vr-<cohort>-hub` | the cohort's front page: title, links to the four session notes, the public site and the repo, a `vr-past-cohorts` link, and a **Links** section |
| `vr-<cohort>-s1` … `vr-<cohort>-s4` | the session's lesson, then a `## Cohort notes` section edited live in class |
| `vr-<cohort>-s<n>-slides` | the same lesson as a reveal.js deck (slide mode) |
| `vr-past-cohorts` | a running index of every past cohort's hub |

Publishing is **create-only and never overwrites**: an alias that already exists is reported and
skipped, so a returning student's edits in a live note are not clobbered by a re-publish. Before
anything is sent, the same answer-key detection as `tools/check_public_build.py` runs on every
payload, and publication is refused if a key or a line unique to one is found.

Archives are written **outside** the repo (default `../course-cohort-archives/`) and are never
committed; a later snapshot never overwrites an earlier one.
