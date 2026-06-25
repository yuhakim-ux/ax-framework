# AX Framework Skills

A suite of Claude Skills encoding the **AX Design Framework** for
Salesforce Agentforce agent work. **Phase 1 (this release, `v0.1.0`)**
ships Layer 1 only — `ax-agent-spec`, which turns an agent PRD into a
working specification. Behavior design (Layer 2) and pattern library
(Layer 3) come later.

For the full strategy and three-layer vision, see
[`docs/AX-Framework-Skills-Strategy.md`](docs/AX-Framework-Skills-Strategy.md).
**This README is the pilot starting point** — how to install, run, and
report back.

---

## What `ax-agent-spec` does (Layer 1)

It interviews you against a locked 13-row rubric (the AX agent-spec
spine), challenges weak requirements in PM language, **refuses to invent
answers** (logs them as numbered spikes), and produces an
**all-sections-present Agent Spec** as a Google Doc that becomes the
working source of truth. Re-entry is supported: drop the Doc back in
later, the skill reconciles your edits and regenerates the next version.

**Built for PMs** defining agent requirements. **Designers co-run or
review.**

What it does NOT do (yet):

- Design behavior (Goal · Role/Boundaries · Golden path · Recovery ·
  Handoff · Trust signals) — that's Layer 2.
- Choose or render UI patterns / trust-signal surfaces — that's Layer 3.

---

## Install & setup

### 1. Make the skill available to your Claude Code

Clone (or pull) this repo, then make `skills/ax-agent-spec/` discoverable
by your local Claude Code:

```bash
git clone <repo-url> ~/projects/ax-framework
ln -s ~/projects/ax-framework/skills/ax-agent-spec ~/.claude/skills/ax-agent-spec
```

Restart Claude Code (or reload skills) so it picks up the new entry. You
can verify by asking Claude: *"Do you have `ax-agent-spec` available?"* —
it should say yes.

> Phase 4 will ship a Marketplace install path. For Phase 1 pilot, this
> manual install is the supported flow.

### 2. Provenance config — asked once on first run

On first run the skill asks you for two things:

- **Team name** — the team that owns the agent being specced (e.g.
  `HC Patient Access`).
- **Product owner contact** — the person who'll be recorded as
  `owner_contact` on any patterns later harvested from your work.

Both are required for the spec's title block AND become the provenance
handle for the future pattern library. You can defer them once
(recorded as an Open Question) but the skill will nudge you to fill them
in before publishing.

### 3. Google Drive (recommended)

The skill publishes generated specs as Google Docs in your connected
Drive. You need a Google MCP tool enabled in Claude Code for this to
work.

**If Drive is unavailable**, the skill saves `.md` and `.docx` files
locally, tells you the paths, and continues. You can re-import later
when Drive is reconnected.

---

## How to use it — one walkthrough

### Trigger it

The skill activates when you describe agent-spec work to Claude Code in
your normal phrasing. Real triggering examples:

- *"Help me spec out a new service agent for member callbacks."*
- *"Turn this PRD into agent requirements."* (paste / link the PRD)
- *"Review this agent PRD — the PM's asks are vague, can you challenge
  them?"*

No CLI to run. The skill loads via its description and starts the
interview.

### The challenge report

Before any interviewing, the skill produces a **challenge report** in
chat: a table of which rubric rows your input answered, partially
answered, or missed, with P0/P1 priorities. It tells you how many P0
gaps remain and what the smallest path through them looks like, then
waits for you to react.

### The interview

Then it asks gap questions — **about 3 per turn**, in rubric order, P0
first. Every question is **skippable**: say "skip" and the row records
as MISSING / PARTIAL and the interview moves on. Say *"that's
engineering's call"* and the skill logs a numbered spike with a proposed
owner ROLE.

The skill will NOT invent an answer to fill a gap.

### The P0 gate

When you're ready to generate (or after the interview completes), the
skill checks if any **P0 row** is still MISSING. If yes, it surfaces a
single decision point listing:

- The MISSING P0 rows.
- Which downstream Layer 2/3 sections each one degrades.
- Two options: **answer now**, or **proceed with gaps**.

If you proceed, the gaps go into a `p0_gaps` list in the spec's
manifest, so future readers (and the future Layer 2/3 skills) know
what's not yet decided. The skill warns once and never nags twice in the
same session.

### What lands in Drive

A formatted Google Doc named `<agent>-spec-vX.Y` inside a per-agent
folder. It contains:

- A title block with version, primitives version, team, product owner.
- A completion manifest at the top — every rubric row, its status, any
  spike references, and a **pattern candidates** table for the future
  pattern library.
- Every rubric section, present, with its status tag inline.
- Unanswered sections render with the rubric's challenge questions
  **pre-printed in place** — you fill them in directly in the Doc.

### Coming back later (re-entry)

Once you've filled in some sections by hand in the Doc:

- Drop the Drive link back into Claude Code with the same trigger
  phrasing.
- The skill reads the latest version's manifest, treats your edits as
  ANSWERS, flags any contradictions (with the primitives or with other
  sections), and generates the **next version** as a new Doc in the
  same folder. The previous version is retained.

Versions are `regenerate-not-edit`. You never edit a prior Doc; each
generation is a fresh artifact with its own version stamp.

---

## What to expect — FAQ

**It will challenge aggressively.** By design. The skill assumes PRD
quality is LOW (most agent PRDs are) and frames every gap as an
engineering-handoff consequence — *"without this, the agent cannot be
built."* If it feels pointed, that's the design. **If it feels hostile
or makes you want to quit, that's pilot feedback we want.**

**It will NOT invent missing details.** Mechanisms it isn't sure of are
left blank. Owner names are never invented (only role labels).
Thresholds, retry counts, and schemas your input didn't state are not
made up. Invention is the specific failure mode the skill is designed
to prevent.

**Unanswered sections are preserved as MISSING / SPIKE.** You fill them
in the Doc and re-run the skill to reconcile. The skill never deletes a
section or silently hides a gap.

**It only does Layer 1.** It will explicitly defer behavior design
(Golden path, persona, recovery flow conversation) to Layer 2 and UI /
trust-signal patterns to Layer 3. You'll see `DEFERRED-L2` /
`DEFERRED-L3` placeholders in the generated Doc — those are intentional,
not gaps in your work.

---

## Pilot feedback — please report

You're the first non-author user. Your feedback is the point of the
pilot. Please report on the following specifically:

- **(a) Triggering.** Did the skill activate when you naturally
  described your task, or did you have to use a special phrase or force
  it? If you had to force it, what were your natural phrasings that
  didn't work?
- **(b) Challenge tone.** Did the challenge feel useful — or did it
  make you want to quit? **Where exactly?** (Section number, question,
  or turn count.)
- **(c) Invention.** Did the skill ever assume or fabricate something
  your input didn't say — any field, mechanism, threshold, schema,
  owner? A single instance is worth flagging.
- **(d) The P0 gate.** Was the gate decision clear? Did "answer now vs
  proceed with gaps" feel like a real choice, or did one path feel
  forced?
- **(e) The generated spec.** Did it read as a **usable starting
  draft** — something you could hand to design review, not just a
  form-filling artifact? Where did it succeed, where did it feel
  hollow?

**How to capture.** The simplest thing is a Google Doc or Slack thread
shared back to Yuha — date-stamped, with a short narrative for each of
(a)–(e). Screenshots of the challenge report or generated spec at the
moments something went well or badly are gold.

Pilot feedback from at least one non-author designer is on the
promotion checklist for the shared HC Design repo (see
[`docs/publishing.md`](docs/publishing.md)) — your write-up unblocks
that step.

---

## Roadmap

This release is **`v0.1.0` — Phase 1 only**. Coming, not yet available:

- **Phase 2 — `ax-behavior-blueprint`** (Layer 2): behavior design
  across the six AX dimensions, with the four-way Agent Script /
  subagent map as a traceability layer.
- **Phase 3 — `ax-agent-interface`** (Layer 3): team-scoped pattern
  registry + pattern cards + in-workflow lookup; Storybook as the
  rendering view for the UI-bearing subset.
- **Phase 4** — primitives-refresh steward skill, publish pipeline,
  Marketplace packaging.

See
[`docs/AX-Framework-Skills-Strategy.md`](docs/AX-Framework-Skills-Strategy.md)
for the full vision.

---

**Questions, friction, or things that broke?** Find Yuha. Phase 1 needs
you to be honest about what worked and what didn't — silence is the
worst feedback.
