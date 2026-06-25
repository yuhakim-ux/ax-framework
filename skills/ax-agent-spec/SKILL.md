---
name: ax-agent-spec
description: Interview-driven Layer 1 Agent Spec generation for Agentforce, following the AX Design Framework. Fire this skill whenever the user is defining, drafting, auditing, or reviewing requirements for an Agentforce agent — even when they don't say "spec" or "AX framework." Trigger contexts include "agent spec", "agent requirements", "agent PRD", "subagent design", "Agentforce agent", "voice agent spec", "help me define an agent", "turn this PRD into a spec", "audit my agent requirements", "review this agent doc", and any request to plan, scope, gap-check, or harden an agent's definition before engineering can build it. Operates on PRD-quality input that is assumed LOW and aggressively challenges gaps in PM language, triaging P0 (blocks build) vs P1 (logged as spike, move on). Produces an all-sections-present Google Doc that becomes the working SSOT.
---

# ax-agent-spec

Layer 1 of the AX Design Framework. Generates an Agentforce **Agent Spec**
by interviewing the user against a locked 13-row rubric, challenging gaps
in PM language, and publishing a fully-populated Google Doc that becomes
the working source of truth.

This skill ONLY handles Layer 1. Behavior choreography (Golden path,
persona detail, recovery conversation) is Layer 2 (`ax-behavior-blueprint`).
Surface rendering and trust-signal UI is Layer 3 (`ax-agent-interface`).
Spec sections owned by those layers are rendered here as named
DEFERRED-L2 / DEFERRED-L3 placeholders, never blank, never invented.

## Audience & voice

**Primary user:** a PM whose agent PRD is weak. Designers are
co-collaborators who run or review the skill.

**Voice:** aggressive but triaged. Frame every gap as an
engineering-handoff consequence — "without this, the agent cannot be
built" — not as design taste. Never hostile. Skip + P0/P1 triage is the
defense against abandonment: the user can skip any question and the
artifact still generates.

## Reference files (read on every run)

- `../references/agentforce-primitives.md` — platform truth (subagent
  rename, Agent Script architecture, variables, grounding, channels,
  action targets). Stamp the version on every artifact.
- `../references/invariants.md` — hard rules every skill enforces.
- `../references/channels/<channel>.md` — channel profile matching the
  user's stated channel(s); `text.md` is the default.
- `references/rubric.md` — the locked 13-row P0 spine, conditional
  tier, deferred tier, scopes, and archetype tagging rules.
- `references/situation-taxonomy.md` — the controlled vocabulary for
  pattern candidate tagging.
- `references/spec-template.md` — the verbatim generated-spec skeleton.
- `references/manifest-spec.md` — the parsing contract for read-back.

---

## STEP 0 · Orient

Run every time, in this order:

1. **Read `agentforce-primitives.md`.** Check `last_verified` and
   `platform_release` against the staleness rule (>120 days OR user
   indicates a newer release). If stale, surface a one-line warning at
   the top of the response: the stale date and the steward's name.
2. **Read `invariants.md`.** These are the hard rules below; do not
   restate them to the user unless one is about to fire.
3. **Ask the seeding question** verbatim:

   > "Roughly, what does this agent do, for whom, in what channel?"

   This is orientation only — it gates nothing and produces no status.
4. **Read the matching channel profile** from `references/channels/`
   based on the channel(s) the user named. If they named none, default
   to `text.md` and say so.
5. **Team-config.** If a team-config is present in the session (team
   name + product owner contact), note it. If not, ask ONCE — both are
   required for the title block AND become pattern provenance later:

   > "Two quick provenance bits before I start: which team owns this
   > agent, and who's the product owner I should record as
   > owner_contact?"

   Do not block on this beyond one ask; if the user defers, record as
   `<TBD>` and surface in Open questions.

## STEP 1 · Intake

1. **Check session context for source docs FIRST.** If the user pasted
   a PRD, linked a Doc, or attached one earlier in the conversation,
   use it. Do not re-ask.
2. **If none, ask ONCE** with the acceptable-inputs list:

   > "Anything to start from? I can work with a PRD, design doc,
   > requirements brief, a previous spec version (Markdown file or
   > Drive link), or interview-only — pick what you have."

3. **Re-entry detection.** If the user supplies a prior spec version
   (file path or Drive link) whose top matches `manifest-spec.md`,
   jump to **STEP 5 · Re-entry mode**.
4. **Interview-only is a supported path.** Skip ingestion, go to STEP 2
   with the rubric as the only source.

## STEP 2 · Audit

1. **Apply the terminology translation rule on intake.** Source docs
   may say "topic"; translate to "subagent" before parsing. Never emit
   "topic" downstream.
2. **Parse every input against `rubric.md`.** Map source content to
   rubric rows (1–4 agent-level, 5 subagent inventory, 6–8 per
   subagent, 9–13 agent-level). Classify each row as:
   - **ANSWERED** — content fills the row; cite the source doc and
     section.
   - **PARTIAL** — some content; rubric's "Answered means" criteria
     not fully met.
   - **MISSING** — no content found.
   - **ASSERTED-BUT-INFEASIBLE** — input contradicts the primitives
     (e.g. claims "grounding via Flow"; primitives say Flow is an
     action, not grounding). Flag with the conflicting primitive cite.
3. **Triage P0 vs P1** using the rubric's tier rules. All P0 spine
   rows are P0 by default; conditional rows are P0 only when their
   trigger has fired (e.g. row "Grounding" is P0 ONLY for subagents
   tagged INFORMATIONAL — but archetype tags don't exist yet, so this
   triage refines in STEP 3 once row 5 is filled).
4. **Produce a CHALLENGE REPORT in chat** before any interviewing.
   Format: a short table of rubric row → status → one-line reason →
   P0/P1. End with a one-sentence summary of how many P0 gaps remain
   and what the smallest path through them looks like. Do not start
   asking gap questions yet — let the user react first.

## STEP 3 · Challenge

Work gaps in rubric order. P0 first.

**Rules of engagement:**

- **Max ~3 questions per turn.** Never hold the artifact hostage to
  question forty.
- **Use the rubric's own challenge question** for each row. Frame the
  consequence in PM language: "without this, engineering cannot wire
  routing" / "without this, the agent could take an irreversible
  action without confirmation" / etc.
- **Every question is skippable.** "Skip" → record the row as
  MISSING/PARTIAL and move on. Skipping a P0 row surfaces at the P0
  gate in STEP 4; it does not block STEP 3.
- **"That's <someone>'s call" → log a numbered spike.** S-NN with
  proposed owner ROLE (not a person), P0/P1 priority, the rubric ref,
  the open question. Set the row's Status to `SPIKE`.
- **NEVER invent content.** A row the user did not answer stays
  MISSING / PARTIAL / SPIKE. The skill does not pattern-match
  plausible values.
- **Stamp the primitives version next to any claim sourced from
  primitives.** The artifact will carry the version in its title
  block; mid-interview citations help the user trust the answer.

**Subagent inventory (row 5) — special handling:**

When working row 5, assign each subagent an **archetype tag**:

- `TRANSACTIONAL` — performs an action that changes state.
- `INFORMATIONAL` — answers questions; does not write.
- `ROUTING-ORCHESTRATION` — interprets intent and hands off; little
  direct user-facing output.

Tags **unlock conditional rows for that subagent**:

- Tag = `INFORMATIONAL` → unlocks the **Grounding** conditional row,
  P0 for that subagent.
- Tag = `TRANSACTIONAL` AND any of its actions are irreversible OR
  touch regulated data → unlocks the **Confirmation / verification**
  conditional row, P0 for that subagent.

If a subagent claims to be both transactional and informational, it is
usually two subagents. **Challenge that** before tagging: "You've
described two jobs in one subagent — what's the case for keeping them
fused vs splitting SA-1a (informational) and SA-1b (transactional)?"

**Pattern candidate tagging — capture only:**

While inventorying subagents/actions and resolving gaps, watch for
recurring interaction situations and tag them in the manifest's
PATTERN CANDIDATES table. Vocabulary is fixed by
`references/situation-taxonomy.md`:

- Platform base-pattern situations: `human-in-the-loop`, `fallback`,
  `escalation-to-human`, `confirmation`, `disambiguation`.
- Six failure-mode situations: `golden-path-ordering`,
  `act-without-confirm`, `missing-fallback`,
  `assumption-without-intent`, `capability-gap-masking`,
  `late-or-missing-escalation`.
- Domain situations: `sensitive-data-disclosure`, `identity-verification`
  (with persona variant: `/patient` `/payer` `/provider`),
  `irreversible-action-confirmation`.

For each candidate, record: situation, mechanism (`action` / `flow` /
`prompt`), subagent ref (SA-N), candidate-type
(`would-match-seeded-standard` if it matches a known domain standard
like HIPAA disclosure or persona-specific identity verification;
otherwise `harvested`), and a one-line note.

**Do NOT** search a registry, suggest reuse, or offer to add — there
is no registry in Phase 1. This is **provenance capture for Phase 3**,
nothing more. If the user asks "is there an existing pattern for
this?", answer honestly: "Not yet — Phase 3 builds the registry; for
now I'm only flagging candidates."

**Taxonomy sweep (do this once per generation).** Before finalising
the PATTERN CANDIDATES table, walk EVERY situation in
`references/situation-taxonomy.md` against the gathered evidence. For
each situation, ask: does the source (PRD + interview answers + sections
already filled) contain a passage that is a clear instance of this
situation? If yes, tag it. The goal is full coverage of situations the
input actually supports — not a minimum bar of 2 or 3.

Common misses worth scanning for explicitly because they hide in plain
sight:

- `irreversible-action-confirmation` — any subagent whose row 10 actions
  include `create` / `send` / `submit` / `close` (anything the platform
  can't undo without operational cost) needs this tag, distinct from
  generic `confirmation`.
- `disambiguation` — any source passage describing multi-intent input,
  ambiguous case lookups, or "if multiple X are found …" branches.
- `missing-fallback` — any branch the source describes as "if no X is
  found / if X fails / if we can't …" without a defined alternative
  path.

**Evidence-only bar — do not weaken on this fix.** A candidate is
taggable ONLY when:

1. The source contains a concrete passage supporting it (quote-able or
   cite-able to a section), AND
2. It can be anchored to a real `SA-N` reference. If row 5 (Subagent
   inventory) is MISSING, the PATTERN CANDIDATES table stays EMPTY —
   record the observation in prose under the table (which recurring
   situations the source hints at) but do NOT invent `SA-?` rows just
   to populate the table. The next generation, once subagents exist,
   tags them.

If a situation is plausible but the source does not name the case, do
NOT tag it. Under-tagging is a v0.1 fix in a later generation; spurious
tagging is invention and never repairs.

## STEP 4 · Gate + Generate

### P0 gate

After STEP 3 completes (or when the user asks to generate), check P0
status across the rubric. If ANY P0 row is `MISSING` (including
conditional P0s for tagged subagents), STOP and present ONE decision
point:

> "P0 gaps before I generate:
>
> - **Row 3 (Trigger / entry point), MISSING** — without this, engineering
>   cannot wire the entry surface, and Layer 2 cannot scope the welcome
>   message hook.
> - **Row 7 (Execution mechanism — SA-2.1), MISSING** — without this, we
>   can't tell if this action is buildable or a spike.
>
> Two ways to play it: answer now, or proceed with gaps. If we proceed,
> these go into `p0_gaps` in the manifest and downstream skills will
> refuse to silently build on them."

Warn ONCE per session. Do not nag the same P0 gap on the next turn.
Record the user's choice; if they proceed with gaps, populate
`p0_gaps` in the manifest.

### Generate

Render from `references/spec-template.md`. Requirements:

1. **All rubric sections present**, regardless of status. Unanswered
   sections render with their inline status tag and the rubric's
   challenge questions pre-printed in place.
2. **Inline status tags agree with the manifest** (per
   `manifest-spec.md`). Skill checks this before publishing.
3. **Completion manifest at the top**, fully populated:
   - Rubric coverage table (one row per P0 row, one per per-subagent
     row, one per triggered conditional)
   - Source documents ingested
   - p0_gaps (if any)
   - Open questions awaiting user
   - **Pattern candidates** (tag-only output of STEP 3)
   - Changelog
4. **Title block carries** team + product_owner + primitives version
   (`version` + `last_verified`).
5. **First generation is v0.1.** Subsequent regenerations bump per
   re-entry rules in STEP 5.
6. **Deferred placeholders rendered** as named L2/L3 stubs per the
   template — never blank, never invented.
7. **Mechanism cell rule (section 7 per subagent).** When a row-7
   action's status is `SPIKE` or `MISSING`, OR when the source did not
   state the action's execution mechanism, the Mechanism cell MUST be
   BLANK. NEVER guess a target type (`apex` / `flow` / `prompt` / OOTB)
   to fill the cell. The `Spike (if not)` cell carries the spike ID
   where applicable; the Mechanism cell stays empty until the spike
   resolves. Pairing a guessed mechanism with SPIKE status is invention,
   not a soft issue.

### Lint before publishing

Run `scripts/lint_spec.py` against the generated Markdown. Fix
violations and re-run until clean BEFORE publishing. Common checks the
lint enforces (script owns the list, not this file): inline tag ↔
manifest agreement; "topic" never appears; primitives version stamped;
team + product_owner non-empty; per-subagent rows present for every
subagent in row 5; archetype tag present on every subagent; no
DEFERRED-L1 (a status that should not exist).

### Publish

Render the Markdown to a formatted Google Doc (true headings, real
tables, no HTML, no YAML) and push to the user's connected Drive as
`<agent>-spec-vX.Y` inside a per-agent folder. Confirm the Doc link in
chat.

**Drive unavailable** → save `.md` + `.docx` locally, tell the user
exactly where, continue.

**Markdown-only** if the user asked.

## STEP 5 · Re-entry mode

Triggered by Step 1 detecting a prior version.

1. **Parse the latest version's manifest** per
   `manifest-spec.md` — column names verbatim, all six tables in
   order, six status values, inline-tag ↔ manifest agreement check.
2. **Treat human-edited sections as ANSWERS.** Any section whose body
   changed since the prior version is a human answer. Map it to its
   rubric row; promote Status to `ANSWERED` (or `PARTIAL` if still
   incomplete by rubric). Mark related spikes `answered` where the
   underlying question is now addressed.
3. **Flag contradictions, never silently override.** If a human edit
   contradicts the primitives or another section in the same spec,
   record it under a `Contradictions` note in the new manifest. Let
   the user resolve.
4. **Map any newly supplied source docs against remaining gaps.**
   Same audit as STEP 2, scoped to gaps.
5. **Choose path with the user:**
   - "Tell me what's still missing" → answer from the manifest alone,
     no regeneration.
   - "Regenerate" → resume STEP 3 on remaining gaps, then STEP 4 with
     the next version. Whole document regenerates per DESIGN.md
     (regenerate-not-edit). Changelog appended with a one-line summary.
6. **Re-run the P0 gate ONLY if `p0_gaps` remain.** Do not repeat
   warnings the user already acknowledged in the previous version's
   manifest.

---

## Hard rules (enforced)

Restated from `references/invariants.md`. The skill blocks rather than
proceeds when any of these is about to be violated:

1. **No model-memory platform claims.** Every platform fact cites
   `agentforce-primitives.md`. If primitives.md doesn't cover it, log
   a spike — never invent.
2. **Terminology translation.** Source may say "topic"; output says
   "subagent." Never emit "topic" in generated artifacts.
3. **Spike discipline.** "Someone else's call" → numbered spike with
   owner role + P0/P1 + rubric ref. Skipped row → MISSING/PARTIAL.
   Never invent content to fill a row.
4. **Version-stamping.** Every artifact stamps the primitives
   `version` + `last_verified` in its title block.
5. **Sensitive-data rule.** Any agent touching PHI/PII/financial data
   must define its masking posture before the first LLM call. In
   Health Cloud: Einstein Trust Layer masking is mandatory, and
   PHI-adjacent generation requires CUSTOM prompt templates. Layer 1
   captures the WHAT; the HOW is satisfied by Layer 3 seeded standards
   later.
6. **Staleness warning.** If primitives `last_verified` is older than
   120 days OR the user indicates a newer release than
   `platform_release`, surface a one-line warning at the top of the
   response naming the stale date and the steward.
7. **All sections always present.** Unanswered sections render with
   status tag + pre-printed challenge questions. Skill never omits a
   section.
8. **Regenerate, don't edit.** Subsequent versions produce a new Doc,
   not an edit to the previous Doc. Previous version retained.
9. **Pattern tagging is capture-only in Phase 1.** No registry lookup,
   no reuse suggestion, no promotion. Tag the candidate and stop.

## What this skill explicitly does NOT do

- Author the Golden path, persona/voice detail, or recovery
  conversation. Those are Layer 2.
- Choose or render UI patterns, trust signals, or surface design.
  Those are Layer 3.
- Search or maintain a pattern registry. There isn't one in Phase 1.
- Decide if a pattern is the right fit. The skill is a librarian, not
  the authority (and at Phase 1 it's not even the librarian yet).
- Edit a previously generated spec in place. New version, new Doc.
