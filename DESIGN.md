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
264 golden eval. Phase 2: ax-behavior-blueprint with four-way traceability
(system: instructions / system: messages / subagent instructions / Agent
Script). Phase 3: ax-agent-interface v1 + patterns.json + Storybook
convention. Phase 4: primitives-refresh steward skill + publish pipeline.
Phase 5: pilot, description optimization, voice channel overlay.
