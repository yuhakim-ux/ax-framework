# ax-agent-spec — Manifest Parsing Contract (v1.0)

The completion manifest is the machine-readable surface of a generated
spec. On re-entry, the skill reads the latest Doc back from Drive, parses
the manifest, and reconciles human edits against the previous version.

This file is the parsing contract. Any change to a column name, status
value, or table shape MUST land here first; downstream skills depend on
it.

---

## Manifest tables and column contract

The manifest lives at the TOP of every spec, immediately after the title
block, under the heading `## Completion manifest`. It contains the
following tables, in this order, with these column names verbatim.

### 1. Rubric coverage

| Column           | Type        | Notes                                                                  |
|------------------|-------------|------------------------------------------------------------------------|
| Rubric row       | string      | "1. Agent purpose & success criteria" … "13. Exit conditions & handoff/escalation — SA-<N>". Subagent rows include the SA-N suffix. |
| Scope            | enum        | `Agent` or `Subagent`.                                                  |
| Status           | enum        | One of the six status values below.                                     |
| Notes / Spike refs | string    | Free text; may reference spike IDs (e.g. `S-03`).                       |

One row per rubric P0 row. Subagent rows 8–13 repeat once per subagent.
Conditional-tier rows appear here ONLY when triggered.

### 2. Source documents ingested

| Column        | Type   | Notes                              |
|---------------|--------|-------------------------------------|
| Document      | string | Title.                              |
| Type          | enum   | e.g. `PRD`, `design doc`, `email`.  |
| Ingested on   | date   | `YYYY-MM-DD`.                       |
| Notes         | string |                                     |

### 3. P0 gaps

Populated only if the user chose "proceed with gaps" at the P0 gate.

| Column                              | Type   | Notes                          |
|-------------------------------------|--------|--------------------------------|
| Rubric row                          | string | Matches "Rubric coverage".     |
| Subagent ref                        | string | SA-N or blank if agent-level.  |
| Downstream sections this degrades   | string | List of L2/L3 section names.   |

### 4. Open questions awaiting user

| Column     | Type     | Notes                          |
|------------|----------|--------------------------------|
| ID         | string   | `Q-01`, `Q-02`, …              |
| Question   | string   |                                |
| Blocking?  | enum     | `yes` / `no`.                  |

### 5. Pattern candidates

Phase 1 flag list. Filled by the skill; consumed by Phase 3 later.

| Column         | Type   | Notes                                                                     |
|----------------|--------|---------------------------------------------------------------------------|
| Situation      | enum   | One value from `references/situation-taxonomy.md`.                        |
| Mechanism      | enum   | `action` / `flow` / `prompt`.                                              |
| Subagent ref   | string | SA-N.                                                                      |
| Candidate-type | enum   | `would-match-seeded-standard` or `harvested`.                              |
| Note           | string | One-line reason for tagging.                                               |

### 6. Changelog

| Column   | Type   | Notes                          |
|----------|--------|--------------------------------|
| Version  | string | `X.Y`.                         |
| Date     | date   | `YYYY-MM-DD`.                  |
| Author   | string |                                |
| Summary  | string |                                |

---

## Status values — the six

Per DESIGN.md "Spec completeness model". Exactly these six values appear
in the `Status` column AND in the inline section header tag.

| Value         | Meaning                                                                                                             |
|---------------|---------------------------------------------------------------------------------------------------------------------|
| `ANSWERED`    | Section is filled and consistent with the primitives + other sections.                                              |
| `PARTIAL`     | Section is filled but the rubric's required questions are not all addressed.                                        |
| `MISSING`     | Section is empty. At the P0 gate, MISSING on a P0 row triggers the gate.                                            |
| `SPIKE`       | An answer requires someone else. A spike ID is recorded (S-NN) with proposed owner ROLE and P0/P1 priority.         |
| `DEFERRED-L2` | The section is owned by Layer 2 (ax-behavior-blueprint). Rendered as a named placeholder.                            |
| `DEFERRED-L3` | The section is owned by Layer 3 (ax-agent-interface). Rendered as a named placeholder.                               |

**Inline tag rule.** Every section header carries an inline status tag in
square brackets after an em dash (e.g. `## 5. Data sensitivity — [SPIKE S-03]`).
The inline tag MUST agree with the manifest's `Status` for that row. The
skill checks this on every generation and on every read-back. A mismatch
is a contradiction the skill flags during reconciliation.

---

## Reconciliation rules (read-back → next version)

Per DESIGN.md "Layer 1 output architecture":

1. **The Doc is the working SSOT.** On re-entry, the skill reads the
   latest Doc back from Drive (or `.md` if Drive is unavailable).
2. **Human-filled sections are answers.** Any section whose content has
   changed since the previous version is treated as a human answer.
   Reconcile, never overwrite.
3. **Status promotion.** If a section was `MISSING` / `PARTIAL` / `SPIKE`
   and the human filled it, the skill promotes the status to `ANSWERED`
   (or `PARTIAL` if still incomplete by rubric) in the new manifest.
   Spike entries are marked `answered` in the spike log if their question
   is now addressed in the section.
4. **Contradiction flagging.** If a human-filled section contradicts
   either the primitives file or another section in the same spec, the
   skill flags it in the new version's manifest under a `Contradictions`
   note — it does NOT silently rewrite. The user resolves.
5. **Regenerate, don't edit.** The next version is a new Doc, named
   `<agent>-spec-vX.Y`, in the same per-agent Drive folder. The whole
   document regenerates; the previous version is retained.
6. **Inline-tag / manifest agreement.** Re-check rule applies to the
   read-back: any mismatch between an inline section tag and the
   manifest status is recorded as a contradiction.
7. **p0_gaps carry forward** unless the human filled the underlying row,
   in which case the gap is closed and removed from `p0_gaps` in the new
   manifest.
8. **Pattern candidates carry forward** until Phase 3 owns harvesting.
   The skill may append new candidates surfaced this round but does not
   remove or modify existing ones at Phase 1.

---

## What the parser MUST do (Phase 1 contract)

- Find `## Completion manifest`, then locate each of the six tables by
  heading name, in the order listed.
- Validate column names verbatim against this file. Reject (and ask the
  user) on schema drift.
- Read every `Status` value and check against the inline tag for the
  matching section.
- Build a per-subagent index from rubric rows 8–13 by SA-N suffix.
- Surface contradictions (inline-tag vs manifest, section vs primitives,
  section vs section) before generating the next version.

## What the parser MUST NOT do at Phase 1

- No registry lookup or pattern matching against the Pattern candidates
  table. It is read, carried forward, and otherwise inert until Phase 3.
- No silent rewriting of human-filled content.
- No invention of answers to fill `MISSING` / `SPIKE` rows.
