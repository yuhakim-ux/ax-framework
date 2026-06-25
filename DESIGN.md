# AX Framework Skills — Design Decisions (locked, June 2026)

## What this is
A suite of Claude Skills encoding the AX Design Framework for Salesforce
Health Cloud agent work. Three layers, three skills: ax-agent-spec (Layer 1,
this phase), ax-behavior-blueprint (Layer 2), ax-agent-interface (Layer 3).
Skills share a common references/ layer. One version number across the suite.

## Distribution
Develop and test in this personal repo. After testing clears, publish tagged
releases to the shared HC Design repo:
https://ubiquitous-adventure-43w5j5o.pages.github.io/
(Marketplace packaging is Phase 4.)

## Platform grounding rules (non-negotiable)
1. NEVER rely on the model's background knowledge of Agentforce. All platform
   claims trace to references/agentforce-primitives.md, which is curated,
   versioned, steward-reviewed truth.
2. Terminology translation rule: the current platform term is SUBAGENT
   (renamed from "topic," April 2026, no functionality change). Source
   documents may say "topic" — translate on intake. NEVER emit "topic" in
   generated artifacts.
3. Every generated artifact stamps the primitives version it was built
   against. Skills warn when the primitives file looks stale (see staleness
   rules in the primitives file header).

## Layer 1 output architecture
- Canonical generation format: Markdown, rendered into a formatted document
  (heading hierarchy + tables, matching the team's existing agent-spec docx
  style) and published to the user's connected Google Drive as a Google Doc.
- The GOOGLE DOC IS THE WORKING SSOT. The team fills gaps manually in the
  Doc. On re-entry, the skill reads the latest Doc back from Drive, parses
  the manifest and section statuses, treats human-filled sections as answers
  (reconcile, never overwrite), flags contradictions with the primitives or
  other sections, and generates the NEXT version.
- Versioning: regenerate-not-edit. One new Doc per version, named
  <agent>-spec-vX.Y, in a per-agent Drive folder. Changelog inside the doc.
- Graceful degradation: if Drive is not connected, save .md and .docx
  locally and tell the user.
- Markdown-only output when the user explicitly asks for it.

## Spec completeness model
- Status vocabulary per rubric row: ANSWERED / PARTIAL / MISSING / SPIKE /
  DEFERRED-L2 / DEFERRED-L3.
- Every generated spec contains ALL rubric sections regardless of status.
  Unanswered sections render with their status tag and the rubric's
  challenge questions pre-printed in place, so the team can fill them
  manually in the Doc.
- Completion manifest: a human-readable table at the TOP of every spec
  (not YAML front matter — it must survive Google Doc format and be
  parseable by the skill on read-back). Records: rubric coverage per row,
  per-subagent archetype tags + conditional status, source documents
  ingested, primitives version, open questions awaiting the user, p0_gaps,
  changelog.
- Spike discipline: when an answer requires someone else, the skill logs a
  numbered spike (S-01, S-02, …) with a proposed owner ROLE and P0/P1
  priority. The skill NEVER invents an answer to fill a section.
- P0 gate: at generation time, if any P0 row is MISSING, stop and present
  ONE decision point: list the missing P0s, state which downstream Layer
  2/3 sections each degrades, offer "answer now" or "proceed with gaps."
  If proceeding, record p0_gaps in the manifest. Downstream skills read
  the manifest and refuse to silently build on gapped foundations. Warn
  once; never nag twice in a session.

## Interview posture
PRD quality is assumed LOW. The skill aggressively challenges gaps but
triages: distinguish "spec cannot proceed without this" (P0) from "log a
spike and move on" (P1). Never hold the artifact hostage to question forty.
Users may skip any question; skipping produces a MISSING/PARTIAL status,
not a block (except at the P0 gate, which is a single explicit choice).

## Build phases
Phase 1 (this repo, now): references layer + ax-agent-spec + lint + DoD +
264 golden eval. Phase 2: ax-behavior-blueprint built on the SIX AX dimensions (Goal /
Role-Boundaries / Golden path / Recovery / Handoff / Trust signals), with
the four-way platform map (system: instructions / system: messages /
subagent instructions / Agent Script) applied as a TRACEABILITY layer
AFTER the six dimensions. The six failure modes are the blueprint's
quality lint. Phase 3: ax-agent-interface v1 — team-scoped pattern
registry (patterns.json) + pattern cards + in-workflow lookup; Storybook
is the rendering view for the UI-bearing subset. Standalone browse may be
built here too (schema is shared) — see addendum. Phase 4:
primitives-refresh steward skill + publish pipeline.
Phase 5: pilot, description optimization, voice channel overlay.

## Audience (Layer 1)
Primary audience is PMs: defining the PRD/spec is their job, and current
agent PRDs are weak. The skill's default voice aggressively challenges the
PM to define critical agent requirements. Designers are co-collaborators who
run or review it. Challenge reports and questions are framed in PM language
(engineering-handoff consequences: "without this, the agent cannot be
built"). Skip + P0/P1 triage is the defense against abandonment.

## Layer 2 (Phase 2) spine
ax-behavior-blueprint interviews across the SIX AX dimensions (AX Framework
Lite): Goal / Role-Boundaries / Golden path / Recovery / Handoff / Trust
signals. The four-way platform map (system: instructions / system: messages /
subagent / Agent Script) is a TRACEABILITY layer applied AFTER the six
dimensions, not a substitute. The SIX failure modes (wrong golden-path order;
acting without confirming; no fallback; assumption without intent-gathering;
personality masking capability gaps; late/missing escalation) are the
blueprint's quality lint. [OPEN: confirm whether Role and Boundaries are one
dimension or two before building Phase 2.]

## Layer 3 (Phase 3) reframed: team agent pattern ecosystem
- Scope = interaction/behavioral patterns, NOT UI only. Platform base
  patterns (HITL, Fallback, Escalation, Confirmation, Disambiguation) are
  referenced, never re-documented; the captured value is team/domain
  SPECIALIZATIONS on top of them.
- Two population mechanisms:
  (1) Top-down SEEDED STANDARDS — domain-mandatory patterns (e.g. HIPAA
      disclosure; persona-specific identity verification for Patient/Payer/
      Provider). Authority-owned, authoritative; skills proactively
      enforce/suggest them when the situation arises.
  (2) Bottom-up HARVEST — ambient capture during design work. Offer to add
      ONLY when a pattern recurs across 2+ agents OR a human validates it as
      standard. Seen-once = flagged candidate only, no offer. (Mirrors the
      "flag, don't extract prematurely" principle.)
- Capture hooks live in Layer 1 & 2, but they ONLY TAG candidates in the
  manifest (situation + mechanism + team provenance). Registration/promotion
  is owned by Layer 3.
- SSOT = patterns.json (behavioral + UI patterns). Storybook is the rendering
  VIEW for the UI-bearing subset only.
- Matching taxonomy (controlled vocabulary for "situation") = the six failure
  modes + platform base patterns + domain situations (sensitive-data
  disclosure, identity verification, etc.).
- Every pattern entry carries: team, release, agent, situation, mechanism
  (action/flow/prompt), owner_contact (product owner), last_validated_release,
  visibility. We store INTERACTION METADATA, not code; implementation stays a
  pointer to the owning team.
- Invariant<->pattern link: a Layer 1 invariant (the WHAT, e.g. "verify
  identity before PHI") is satisfied BY a library standard pattern (the HOW).

## Layer 3 — pattern lookup (READ) is cross-cutting
- Registry query is available from ALL three skills, not gated to Layer 3.
  Flow (query -> relevancy -> pattern card -> handoff) lives in a shared
  reference: references/pattern-registry.md. Each skill's SKILL.md points to
  it in one line. No 4th skill.
- Pattern card = registry entry's human view + short "what/when" summary +
  a type tag: seeded-standard | harvested.
  * seeded-standard owner_contact = domain/compliance authority
  * harvested owner_contact = the team (product owner) that built it
- HARD RULE (lookup): every pattern shown carries provenance + owner_contact
  + an explicit "confirm with the owning team before adopting" recommendation.
  The agent is a librarian/matchmaker, NEVER the authority on fit. We provide
  a reference, not a verdict.
- Relevancy analysis rules: (1) surface DIFFERENCES, not just similarity;
  (2) state explicitly what cannot be verified. Relevancy is a starting
  hypothesis, not a judgment — this is what makes the handoff mandatory.

## Team-scoping & visibility (org-wide repo, per-team libraries)
- The SKILL SUITE is shared org-wide (all Salesforce teams). The LIBRARY
  (registry) is partitioned per team. `team` is a first-class attribute on
  every pattern and every candidate tag.
- The skill operates "as" a team via a team-config (team name + library
  location + the team's domain authority contact), set once at adoption.
- Registry partitions: (a) seeded-standards (authority-owned, domain/org
  visible), (b) <team> partitions (team-owned harvested patterns).
- Visibility gates CROSS-TEAM exposure:
  * team (DEFAULT) — visible within the owning team. The core
    cross-pollination vision (one HC designer finding another HC team's
    pattern) is satisfied at this level.
  * org (opt-in) — discoverable by other teams via cross-team lookup;
    promotion is a deliberate curator-gated step.
  Conservative default (team, not org) because auto-exposing healthcare
  patterns org-wide without review is a compliance risk. seeded-standards
  are domain/org-visible by nature.
- Standalone browse (outside a build session) and in-workflow lookup share
  the SAME team-scoped registry + visibility model. Browse build may happen
  in Phase 3; expect a near-empty catalog until capture fills it (cold-start).

## Governance — OPEN, for VP discussion (do not resolve in build)
The primitives-refresh skill, the pattern registry, AND the seeded-standards
all PROPOSE or require human acceptance; none auto-commits. This converges on
a single unresolved role: an AX steward/curator spanning (a) primitives
review, (b) harvested-pattern promotion to org visibility, (c) authority over
seeded domain standards (HIPAA, verification matrices) — possibly split with
HC compliance/domain owners. Yuha to raise with the VP. Until owned, design
for graceful staleness: last_verified / last_validated stamps + runtime
warnings.
