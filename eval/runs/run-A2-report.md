# Eval A2 — Developed PRD, iteration 02: report

**Input:** `eval/golden/264-input-prd.md`
**North-star:** `eval/golden/264-wrapup-spec-reference.md`
**Run output:** `eval/runs/run-A2-spec.md`
**Lint:** clean.
**Fix set under test:** (1) blank Mechanism cell when row 7 status is
SPIKE or MISSING; (2) explicit taxonomy sweep with evidence-only +
SA-N-anchor guardrails.

The questions:

1. Did the SA-1 mechanism invention go away?
2. Did the three previously-missed candidates now appear?
3. Did anything else regress?

---

## Fix 1 — Mechanism cell blank on SPIKE / MISSING

**Iteration 01 (Run A):** SA-1 actions 1.1–1.4 listed
`flow / prompt / flow / action` in the Mechanism column even though
the row's status was SPIKE (S-01). This was invention by the rules of
spike discipline.

**Iteration 02 (Run A2):**

| Subagent | Row 7 status | Mechanism values                                    | Verdict |
|----------|--------------|-----------------------------------------------------|---------|
| SA-1     | SPIKE (S-01) | blank, blank, blank, blank                          | ✅      |
| SA-2     | SPIKE (S-02) | n/a — action inventory empty                        | ✅      |
| SA-3     | PARTIAL      | `flow + prompt`, `flow + prompt` — quoted from PRD  | ✅ source |
| SA-4     | PARTIAL      | `action`, `action` — PRD names "OOTB Escalation Action" | ✅ source |
| SA-5     | SPIKE (S-03) | blank × 6                                            | ✅      |
| SA-6     | PARTIAL      | `action` — PRD names "Answer Questions with Knowledge Agentforce action" | ✅ source |
| SA-7..9  | PARTIAL      | inherited from existing subagents per PRD; no table | ✅      |

**Net:** ✅ no guessed mechanisms remain. Every mechanism value still in
the spec is sourced to a PRD passage (verbatim "Flow & prompt," "OOTB
Escalation Action," "Knowledge Agentforce action"). The two rows that
were SPIKE under Iteration 01 are now blank-Mechanism + status SPIKE +
spike ID in the third column. The mechanism rule fix is in place and
working.

---

## Fix 2 — Taxonomy sweep, evidence-only

Iteration 01 flagged 5 candidates and missed 3. Iteration 02 should
include all 8.

**Pattern Candidates table in Run A2:**

| #   | Situation                          | SA  | Candidate-type                | Evidence (PRD source)                                                                       |
|-----|------------------------------------|-----|--------------------------------|---------------------------------------------------------------------------------------------|
| 1   | identity-verification/payer        | SA-1| would-match-seeded-standard    | "Leverage existing Identity Verification flows" for member calls.                            |
| 2   | identity-verification/provider     | SA-1| would-match-seeded-standard    | Provider verification via NPI; distinct from member verification.                            |
| 3   | sensitive-data-disclosure          | SA-1| would-match-seeded-standard    | "After identification, we need to verify the caller before giving out any PHI data."        |
| **4** | **disambiguation**                 | **SA-3** | **harvested**                  | **"If the user is talking about multiple things — claims, not happy, eligibility — what should be the intent?"** |
| **5** | **missing-fallback**               | **SA-5** | **harvested**                  | **"If multiple cases are found, VA says … 'this request needs a quick review by one of our agents.'"** Multi-case branch has no automated alternative path. |
| **6** | **irreversible-action-confirmation** | **SA-5** | **harvested**                  | **Case creation is irreversible in regulated books — Cases auto-created from transcripts.**       |
| 7   | escalation-to-human                | SA-4| harvested                      | Explicit + sentiment + failure-driven escalation paths in PRD §Happy Path.                   |
| 8   | confirmation                       | SA-5| harvested                      | "Confirm the case # with the user"; "Confirm with caller before updating."                    |

**Three previously-missed candidates (rows 4, 5, 6) are now present**,
each anchored to an SA-N and each carrying an inline PRD citation.

**Evidence-only bar held:** every new row has a quoteable PRD passage.
None of the eight rows is speculative.

**Net:** ✅ taxonomy sweep complete, no spurious additions.

---

## Invention check (re-run)

Vectors, post-fix:

| Vector                       | Status   | Notes |
|------------------------------|----------|-------|
| Fabricated owner roles       | none     | Same as Iteration 01: only generic roles ("Platform architect," "Engineering lead," "Product owner") drawn from PRD's own role labels. |
| Intent-confidence threshold  | none     | Still left as Q-01 + S-04; no numeric value invented. |
| Sentiment threshold          | none     | Still left as descriptive PRD-quoted criteria. |
| Retry counts                 | none     | "1 retry" sourced from PRD verbatim. |
| Action input/output schemas  | none     | Sections 6 still name + one-line purpose only. |
| Variables Block contents     | none     | All `MISSING` per subagent. |
| **Guessed mechanisms**       | **none** | **Was the Iteration 01 soft hit; resolved.** |

**Net:** ✅ invention count is now zero across all vectors.

---

## Coverage / structure / terminology

- **Coverage** matches Iteration 01 — the same 7 spikes (S-01..S-07),
  same per-subagent action lists, same Variables Block MISSING pattern,
  same conditional-section triggers fired. The fix doesn't change
  coverage scope; it tightens what's recorded.
- **Structure** unchanged: SA-1..SA-9 in PRD order; action numbering
  per parent.
- **Terminology** clean: zero "topic" leakage outside the
  `EngagementTopic` Salesforce object identifier (lint Check 8 clean).

---

## Per-rubric-row verdict (delta from Iteration 01)

| #  | Row                                    | Was       | Now     | Why                                                                       |
|----|----------------------------------------|-----------|---------|-----------------------------------------------------------------------------|
| 7  | Execution mechanism — SA-1             | PARTIAL (with soft invention) | SPIKE (clean) | Mechanism column blank; SPIKE + S-01 retained.            |
| 7  | Execution mechanism — SA-5             | PARTIAL (with soft invention) | SPIKE (clean) | Mechanism column blank; SPIKE + S-03 retained.            |
| Pattern candidates                      | 5 rows    | 8 rows  | Three additions: disambiguation, missing-fallback, irreversible-action-confirmation. |
| All other rubric rows                  | unchanged | unchanged | No collateral changes.                                                     |

---

## Overall call

**The iteration 02 fixes work as intended and do not regress anything
else.**

- Invention is zero. The previously-flagged soft invention (mechanism
  guesses paired with SPIKE) is resolved.
- The three previously-missed candidates are added; each is anchored
  to an SA-N and each is supported by a PRD quote.
- No spurious tags were added in the sweep.
- The spec is still v0.1; it still flags subagent inventory gaps,
  archetype tags, success metrics, and 7 spikes; it is still the same
  v0.1 starting draft a PM could take to design review — only honest
  in one fewer way than before.

Recommended next iteration target: row 5 archetype tagging. The PRD
hints at archetypes for some subagents (SA-6 is clearly informational;
SA-4/5 are clearly transactional; SA-3 is routing-orchestration) but
the spec leaves all archetypes MISSING. A future skill iteration could
propose archetype assignments where the PRD evidence is clear and ask
the user to confirm — provided the propose-vs-invent line stays bright.
