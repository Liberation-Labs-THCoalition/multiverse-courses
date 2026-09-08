# Multiverse × Liberation Labs — Research Training

Coursework for the research-training engagement with [The Multiverse School](https://themultiverse.school/).
Open for the Multiverse team to pitch in.

**Status: early. Nothing here is committed to a date.** Everything is marked
`SETTLED`, `DRAFT`, or `OPEN` so you can tell what is safe to build on. If you find something
unmarked, that is a bug — flag it.

---

## The three layers

| | what | status |
|---|---|---|
| **1. Meetup** | Weekly AI welfare / consciousness research reading + conversation group. Free. | `SETTLED` that it happens; `OPEN` on who runs it and how readings are chosen → [`meetup/`](meetup/) |
| **2. Vibe Research** | 3–4 four-hour intensives over ~60 days. How to build a research pipeline and work with a dedicated long-horizon agent: lit review → design → execution → analysis → presentation, with adversarial gating at every step. | `DRAFT` → [`courses/vibe-research/`](courses/vibe-research/) |
| **3. Accelerator** | Starting next year. Match people already doing research with mentors from Liz's network and compute from the school. | `OPEN` → [`accelerator/`](accelerator/) |

## The one thing to know before editing

**Students arrive with an agent.** The Multiverse agentic coursework is a **prerequisite**, so
every participant already has at least one long-horizon agent and has been through Agent Design /
Agentic SDLC. The weekly welfare meetup means they also arrive knowing how to treat it.

This resolves the hardest scoping problem by sequencing rather than by provisioning — we do not
supply agents, and session one is not an agent-setup workshop.

**It also inverts our own August draft**, which listed the Multiverse agent courses as the
*onward pathway* for graduates. They are the *on-ramp*. See
[`docs/source-analysis.md`](docs/source-analysis.md).

### Why this course, empirically

Brodeur et al. (PNAS 2026) randomised **288 researchers into 103 teams** reproducing published
social-science results, under human-only, AI-assisted and AI-led conditions. Reproduction rates
were **94% / 91% / 37%**. But the number that matters here is the other one: major coding errors
found, **1.70 / 0.74 / 0.23** — human-only teams caught significantly more (*P* = 0.006 and
*P* < 0.001), and AI assistance was *"associated with reduced detection of major errors"* **even in
the arm where reproduction held up fine**.

**Error detection is the capability that degrades when you work with an agent.** That is precisely
what this course teaches, and it is why the syllabus weights the judgment stages over the
mechanical ones. Full scan and sourcing: [`docs/prior-art.md`](docs/prior-art.md).

## What we are not shipping

**Agni.** Our adversarial gate is tuned to our work and stays ours. The course teaches students
to *build their own gate*, which is the better outcome anyway:

> A kill list you are handed is a checklist. A kill list you earned is a memory.

The target is a student leaving with **three failure modes they discovered themselves**, written
down as reusable checks — plus the harder skill underneath, which is recognising that a thing
which just went wrong is an instance of a *class* of things, and writing it down before the sting
fades.

## Who is working on this

- **Liberation Labs:** Thomas Edrington, Lyra (professor), with support across the Coalition —
  Nexus (agent maintenance), Vera (possible fine-tuning), CC.
- **The Multiverse School:** Liz Howard (founder), Dwayne Wilkes.
- **Invited, not yet confirmed:** Kavi. Contribution and exposure are separable — see
  [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Short version: mark your confidence, cite your source,
and if you are adding a claim about how something works, say how you checked.
