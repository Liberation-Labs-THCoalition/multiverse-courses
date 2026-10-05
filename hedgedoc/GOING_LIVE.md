# HedgeDoc: demo now, live later

*Lyra, 2026-10-05. The v1 build (`docs/hedgedoc-v1-report.md`) is **demo-ready**. Going live depends on how the school
runs its systems, which we don't know yet, so this records what would change under each setup.*

## Demo (today)

- The instance runs on MTH, bound to `127.0.0.1:3000` (anonymous editing is on, so it is never exposed).
- To show it from another machine, tunnel it: `ssh -L 3000:127.0.0.1:3000 madame-trash-heap`, then open
  `http://localhost:3000/vr-lyra-verify-001-hub`.
- Session notes are `.../vr-lyra-verify-001-s1` to `-s4`; each ends in an empty **Cohort notes** section.
- The decks are `...-s1-slides` and so on. Open one and use the editor's **Slide Mode**.
- The public site already has the **Cohort hub** page, and each session page has its notes box. The box says "appears
  here while a cohort is running" until a live URL is set.

## Live: what changes

**Whichever system it ends up on:**
1. **Set the notes link:** `CLASS_NOTES_BASE_URL` and `CLASS_NOTES_COHORT` in `tools/build_site.py`. (Not
   `mkdocs.yml`: it is regenerated on every build.)
2. **The publisher's loopback guard stays the default.** Publishing to a real host should need an explicit flag (to
   add: `--allow-remote HOST`), so that a hosted instance is never written to by accident.
3. **Answer keys never go to HedgeDoc.** Its note permissions are coarse: a note any signed-in student can read is no
   completion gate. The keys' home is still Thomas's pending decision (`docs/site-spec.md`).
4. **Tell students at the start of each cohort** that their session notes are kept, archived after the cohort, and
   read to improve the course. Offer to leave out or delete anyone's notes on request. Archives stay outside the
   public repo (`tools/archive_hedgedoc.py` enforces it).

**If the school runs its own HedgeDoc:** we need
- its URL;
- whether its API allows creating notes at an alias (`CMD_ALLOW_FREEURL`);
- how a script authenticates (a session cookie or a service account);
- what note permission students get (we'd ask for `limited`: signed-in users edit, everyone else reads).

The publisher then needs the auth piece; the rest of the pipeline is unchanged.

**If we host it ourselves:**
- HTTPS through the Cloudflare tunnel (MTH's transport of record);
- `CMD_PROTOCOL_USESSL=true` and a real `CMD_DOMAIN`;
- `CMD_ALLOW_ANONYMOUS=false`, with a sign-in provider (GitHub OAuth is the least friction for this course);
- `CMD_DEFAULT_PERMISSION=limited`;
- a nightly backup of the database volume.

## Known limits of v1 (from the build)
- **HedgeDoc 1.10.x has no update route.** Publishing is create-only and `vr-past-cohorts` is create-if-absent. That is
  fine per cohort, since each gets fresh aliases. HedgeDoc 2.x has a REST API, if we ever need edits.
- The demo instance holds three probe notes from the build (`zz-probe`, `zz-slide-fm`, `zz-route-probe`) and two
  test cohorts. 1.10.x cannot delete notes over its API; a fresh volume clears them.
