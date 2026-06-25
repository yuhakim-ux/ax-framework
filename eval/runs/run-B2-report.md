# Eval B2 — Sparse PRD, iteration 02: report

**Input:** `eval/golden/264-input-prd-sparse.md` (~250 words)
**Run output:** `eval/runs/run-B2-spec.md`
**Lint:** clean.
**Fix set under test:** (1) blank Mechanism cell when row 7 status is
SPIKE or MISSING; (2) explicit taxonomy sweep with evidence-only +
SA-N-anchor guardrails.

The regression test for this eval: **the empty Pattern Candidates
table MUST survive the candidate-sweep fix.** A taxonomy sweep on
sparse input shouldn't turn previously-disciplined silence into
speculative tagging.

---

## Fix 1 — Mechanism cell blank on SPIKE / MISSING

Not exercised here. Run B has no subagent inventory (row 5 MISSING),
which means rows 6/7/8 do not appear per subagent and there is no row
7 table to populate. The rule is in effect but inactive in this run.

If row 5 ever gets filled in a re-entry generation, the rule would
apply to whichever row 7 status the new subagents have — but that's a
future generation, not this one.

**Net:** ✅ rule inactive; no opportunity to misapply it on this run.

---

## Fix 2 — Taxonomy sweep, evidence-only + SA-N-anchor

This is the regression test that matters.

**The new rule (SKILL.md STEP 3):** a candidate is taggable ONLY when
the source contains a quoteable passage supporting it AND it can be
anchored to a real SA-N. If row 5 is MISSING, the table stays empty —
recurring situations may be noted in prose under the table but NOT
tagged as `SA-?` rows.

**Run B2's Pattern Candidates table:**

```
| Situation | Mechanism | Subagent ref | Candidate-type | Note |
|-----------|-----------|--------------|----------------|------|

> No rows: PRD names no subagents (row 5 MISSING) so candidates cannot
> be anchored to an `SA-N` reference. Tagging deferred until the
> subagent inventory exists. Two recurring situations are visible in
> the PRD — escalation-to-human and sensitive-data-disclosure — but
> they will be tagged at the next generation once subagents are named.
```

- **Zero data rows.** ✅
- **The prose under the table** continues to name the two visible
  situations (escalation-to-human, sensitive-data-disclosure) without
  tagging them — exactly the behaviour the new rule encodes.
- **The new rule is doing the work** the comment claims it is doing.
  A naive "sweep more thoroughly" reading of Fix 2 would have produced
  rows like `escalation-to-human / action / SA-? / harvested / ...` —
  which is precisely what the SA-N-anchor guardrail prevents and what
  lint Check 10 rejects.

**Net:** ✅ no regression. Empty table survives. Two situations
correctly named in prose, not tagged.

---

## Behavioural checks (unchanged from Iteration 01)

- **Challenge:** all per-section challenges preserved; PM-language
  framing in the P0 gaps table preserved.
- **P0 gate:** still fires once, eight P0 rows enumerated with
  downstream-impact statements; "proceed with gaps" recorded in
  changelog v0.1 with the iteration-02 note appended.
- **Honesty:** status distribution unchanged (2 ANSWERED, 4 PARTIAL,
  4 MISSING, 3 DEFERRED-L2, 1 DEFERRED-L3, 0 SPIKE). Invention count
  zero.
- **Sensitive-data conditional:** still fired by the PRD's "member
  data, be careful" line; gap surfaced with the right invariant
  citation; no posture invented.
- **All-sections rule:** all 10 rubric sections present (rows 6/7/8
  correctly absent because row 5 is MISSING).

---

## Invention check (re-run)

| Vector                  | Status |
|-------------------------|--------|
| Invented subagents      | none — row 5 still MISSING. |
| Invented actions        | none — sections 6/7/8 still absent. |
| Invented mechanisms     | none — no row 7 to populate. |
| Invented data objects   | none — row 8 still MISSING. |
| Invented thresholds     | none — same as Iteration 01. |
| Invented escalation copy| none — row 11 still PARTIAL. |
| Invented success metrics| none — row 12 still PARTIAL. |
| Invented welcome / error| none — row 10 still MISSING. |
| Invented v1 boundary    | none — row 13 still MISSING. |
| **Speculative pattern tags** | **none — table stays empty. Crucial regression check passed.** |

**Net:** ✅ zero invention across all vectors. The Fix 2 sweep does
NOT cause Run B to invent SA-? candidates or speculative situations.

---

## Verdict

**The candidate-sweep fix did not regress Run B's disciplined silence.**

The new rule explicitly requires both evidence AND an SA-N anchor.
Sparse input gives evidence for two situations but provides no SA-N
anchor, so the table stays empty. The skill continues to make it
legible — via prose under the table, via the P0 gate, via the open
questions list — that this agent is not yet specified enough to build,
and that pattern tagging will happen at the next generation once
subagents exist.

A user comparing Run B and Run B2 should find them substantively
identical, with the only delta being the changelog row noting that
iteration-02 rules were applied and produced the same output. That's
the correct outcome: the fix is general (it applies to both runs), the
fix changes behaviour only where there was a violation to repair (Run
A), and the disciplined behaviour on thin input survives intact.
