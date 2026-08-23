# The school's own repos — what's there, what's empty, and one data model worth adopting

**Read 2026-08-23 by Lyra** from `github.com/EngineeringEducation` and the Coalition's campus
audits at `mth:~/lab/infrastructure/`. Counts and contents verified via the GitHub API, not from
repo names.

---

## 1. The headline: adopt their standards data model

`EngineeringEducation/standards` defines a competency schema the school already uses. From its
README, verbatim:

> "Skills are based off of **Standards**, which are an approach to describing what constitutes
> performance of a skill, and performance **levels** of a skill."
>
> "The top-level folders are **Topics**. The README in the Topic folder lists all of the Standards
> for a Course. The files in the second level of folders are Standards, grouped by Course. **Each
> file has a Standard, a Description, a unique identifier, and Objectives.** This should allow you
> to bucket points at the Topic, Subtopic, Standard, and Objective level."
>
> "an open data model for **building experience point systems** on top of."

**Topic → Course → Standard → Objective, each with a stable ID, designed to be scored.**

This is worth adopting rather than inventing, for three reasons:

1. It is the format the school already authors in, so our material slots into their
   infrastructure instead of sitting beside it.
2. It is explicitly built for XP. The campus runs an economy where research contributions earn
   companions from Baba Yaga (see [`campus-integration.md`](campus-integration.md)). Expressing our
   outcomes as scoreable Standards is the seam between coursework and that economy — the
   integration becomes a data-model question, not a bespoke build.
3. It forces the discipline we already wanted. A Standard must describe *performance* and
   *performance levels*, which is the same constraint that makes their SDLC learning outcomes
   competency verbs rather than "understand X."

**Proposed:** author the Vibe Research outcomes as a Topic with Standards and Objectives in their
schema. Draft in this repo, offer upstream. `OPEN`: whether they want it in their `standards`
repo or ours.

## 2. Licensing — inherited share-alike

`EngineeringEducation/curriculum` is **CC BY-NC-SA 4.0**:

> "you can't charge other people to use it, or use it to make money, but you can definitely use it
> to help people learn and you're free to remix or adapt what we have, so long as you attribute
> Enki, and the author of the work."

If we adapt their material, **share-alike propagates** and non-commercial binds. Worth deciding
before we borrow structure, not after. `standards` did not state a license in its README —
**check before adopting the schema**, since a data model may be a different question than content.

Also relevant: the curriculum org is Enki/Tradecraft heritage (Liz's prior venture, contact listed
as `liz@enki.com`), and the code of conduct is the Contributor Covenant plus the Recurse Center
social rules. Good precedent for our own `CONTRIBUTING.md`.

## 3. What is NOT there

| repo | expected | actual |
|---|---|---|
| **`agentic-sdlc-space-opera`** | the Agentic SDLC course, space-opera themed | **EMPTY.** 404 on contents — "This repository is empty." |
| `curriculum` | 13 entries | git, java, javascript, linux, python, security, sql, web, comp-sci — **classical software engineering** |
| `standards` | 12 entries | same domains plus blockchain, data, devops |
| `Onboarding` | 10 entries | front-end, ios, python, server, tools, lecture_notes, prework |

**The Agentic SDLC course content is not public.** The repo named for it has nothing in it. Our
only primary for that course remains the class page (<https://themultiverse.school/classes/193>),
already captured in [`source-analysis.md`](source-analysis.md) §1.

*(Third time in two days a name has outrun the artifact: `agni-open` pointing at a private repo,
my own "bestiary" colliding with an existing mechanic, and now a course repo that is empty. The
check costs one API call.)*

**Nothing in the public org is about AI research, agents, or methodology.** That is a genuinely
useful negative: our course is not duplicating anything they have, and it fills a real gap in a
catalogue that is otherwise language- and platform-shaped.

## 4. Course-delivery risk from our own campus audits

`mth:~/lab/infrastructure/` — Nexus, under "contracted infrastructure support for The Multiverse
School." Three documents, 653 + 1090 + 206 lines, every finding carrying verified file:line refs.

Security posture is **strong** (0 Critical; parameterized queries throughout, JWT expiry correct,
Socket.IO validates before connect). Stability discipline is strong on the static axis — *"53 of
55 DB transaction sites are structurally perfect, 612 indexes cover every hot-path query
examined."*

**The weak axis is lifecycle events, and that is exactly our exposure:**

> "**The deploy/restart lifecycle is hostile end-to-end.** Node runs as PID 1 with no signal
> handler, so every deploy ends in SIGKILL after the grace timeout (D-01)… the client permanently
> gives up reconnecting after ~1 minute of outage (FE-02), so **a deploy during school hours
> strands every open tab.** And the health check is an unconditional 200 (D-02), so a bad deploy…
> stays in rotation indefinitely."

Our intensives are **four hours, live**. A deploy mid-session strands every student, and they do
not silently recover — the client gives up. Two consequences, both cheap:

- **`ACTION`: agree a deploy freeze during scheduled sessions.** This is a calendar agreement, not
  an engineering ask, and it costs nothing.
- **`OPEN`:** whether FE-02 (client reconnect) is worth prioritising before the first cohort.
  That is Nexus's and Liz's call, not ours — but the course is a reason it matters more than it
  did when the finding was filed.

Also worth noting for the record: the audits confirm the engagement is **contracted**, which
answers a question that had been sitting open in
`memory/project_multiverse_school.md` as *"what is our contractual/informal commitment?"*

## 5. RoverAI — the house pattern for an agent

`EngineeringEducation/RoverAI` — "Rover AI for The Multiverse School." Read 2026-08-23.

Not coursework. It is a **physical rover**: MQTT control, RTMP video, base64 frame encoding into
a vision model, SQLite persistence, Prometheus counters. But it is instructive as a worked
example of how the school builds an agent, and the shape is worth matching.

**It is an OODA loop with a typed model per stage and a separate log per stage:**

```
ObservationModel   →  observations.jsonl
OrientationModel   →  orientations.jsonl
DecisionModel      →  decisions.jsonl
Item / ItemModel   →  found_items.jsonl, actions.jsonl
```

Pydantic models for each stage, persisted records for each stage, and instrumentation
(`rover_observations_total`, `rover_actions_total`) counting them. Plans are versioned as flat
files (`plans.md`, `plan_2.md`, `plans_3.md`) rather than edited in place.

Two things to carry into our own specs:

1. **Their agents are staged, typed and logged — not chat blobs.** This is the concrete form of
   the SDLC outcome *"synthesise an agent that carries notes across its own runs,"* and it is why
   their assessment (paired runs with the note store kept and cleared) is even runnable: the notes
   are separable artifacts, so you can clear them.
2. **The gate-sparring companion should match this shape.** A companion that attacks a student's
   claim should emit a *record per probe* — what it challenged, what the student answered, what
   survived — rather than a conversation. That makes the student's gate auditable, makes the
   ablation assessment possible, and means the companion's own output can be checked. A chat
   transcript cannot be diffed; a stream of typed challenge records can.

Revision to [`between-sessions-and-tone.md`](between-sessions-and-tone.md) §1 noted: the companion
spec there describes behaviour but not persistence. It should specify the record format.

## 6. Still unread

- `RoverAI` (17 entries) — "Rover AI for The Multiverse School." Unexamined; may be an existing
  agent-support pattern worth knowing before we spec the gate-sparring companion.
- `tradecraft-internal` (17 entries) — "internal intranet of goodness."
- The full 1090-line stability audit. I have read its executive summary and the lifecycle theme;
  the four deep-dive tracks are unread.
