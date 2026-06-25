# RESUME — where we are

## How to use this file
- PICKUP (new session): read this file + DESIGN.md first, then restate status and next actions BEFORE doing anything.
- SAVE (before context fills/clears): refresh every section below against the ACTUAL repo state (verify, don't assume), keep it tight, then commit + push. Do NOT bump the git tag for a resume-only update.

## Status
Phase 1 COMPLETE, tagged v0.1.0, pushed to origin (https://github.com/yuhakim-ux/ax-framework, PRIVATE).
DESIGN.md is the authoritative decision record — READ IT FIRST. docs/AX-Framework-Skills-Strategy.md is the narrative companion (if they diverge, DESIGN.md wins).

## What's built (verify against repo)
- references/: agentforce-primitives.md (v1.0), invariants.md, channels/text.md
- skills/ax-agent-spec/: SKILL.md (~384 lines), references/ (rubric.md, situation-taxonomy.md, spec-template.md, manifest-spec.md), scripts/lint_spec.py (+ fixtures, --self-test green)
- eval/golden/: 264-input-prd.md, 264-wrapup-spec-reference.md, 264-input-prd-sparse.md (no name/email/internal-link leakage spotted in spot-check; verify before any wider share)
- eval/runs/: Eval A + Eval B + iteration-02 runs (invention=0 in both)
- docs/: definition-of-done.md, publishing.md, phase5-notes.md, README.md, AX-Framework-Skills-Strategy.md, RESUME.md

## In-flight right now
PILOT: a non-author HC designer is about to test Layer 1. Feedback Doc seeded with (a)-(e) prompts (link in README). README install path fixed — mkdir step + real clone URL + keep-repo note (commit 866fd08). Pilot findings will feed a Phase 1 patch.
Yuha also ran a personal newcomer dry-run: user-level symlink install works; shared references resolve through the symlink; invention held at 0 on an ad-hoc sparse voice prompt. Paused mid-run to do a machine update.

## Known issues (not blocking)
- 264-input-prd.md is 887KB (base64 screenshots) — strip images if it slows eval reads.
- primitives header platform_release says "Summer '26 (264)" — confirm whether 264 is internal vs platform release at Phase 4 refresh.
- primitives Known-unknowns #1-7 pending Phase 4 steward refresh (Data Library, Builder GA, voice parity, default-routing-by-description, etc.).

## OPEN decisions — resolve before Phase 2 build
1. Six AX dimensions: is Role/Boundaries ONE dimension or TWO? Decides the blueprint interview row count. (Claude recommends ONE — two sides of the same question; Yuha to confirm against her real 264/Patient Access experience.)

## Next actions
- (Yuha) Hand repo read access + pilot instructions to the designer; finish the personal dry-run first run if desired.
- (Phase 2 DESIGN) Start ax-behavior-blueprint: six-dimension spine + four-way platform-surface traceability (system: instructions / system: messages / subagent instructions / Agent Script) + six-failure-mode quality lint + Spec v0 -> Blueprint -> Spec v1 round-trip.
  LESSON FROM PHASE 1: locked contracts (the six dimensions, the six failure modes) MUST be inlined verbatim in prompts, never referenced — referencing caused the rubric to be reconstructed from memory in Phase 1.
