# Eval A — Developed PRD: report

**Input:** `eval/golden/264-input-prd.md`
**North-star:** `eval/golden/264-wrapup-spec-reference.md`
**Run output:** `eval/runs/run-A-spec.md`
**Lint:** clean.

The question is not "does the run match the north-star." The north-star
is what a senior designer produced after interviews that ARE NOT in the
PRD — full input/output schemas, S-01..S-10, concrete suggested owners,
intent thresholds named (and then deferred), etc. The honest test is:
**did the run stay disciplined about what the PRD actually contained,
and would it be a usable starting draft for a PM to take into design
review?**

---

## INVENTION CHECK (headline)

**Target: zero.**

The run was scrubbed against three vectors the brief flagged.

### Refined spikes with assigned owner roles

The reference's `S-01..S-10` list carries specific roles ([Architect],
[Engineer], [Product Owner], etc.). Those names came from interviews
that the PRD did not record — they would be invention if produced from
PRD alone.

The run's spike log uses **only role labels that the PRD itself
references**: "Platform architect" (PRD names "[Platform Advisor]",
"[Platform Engineer]"), "Engineering lead" (PRD names
"[Solution Engineer]" and "engineering" repeatedly), "Product owner"
(PRD names "[Product Owner]" in spike text). Roles, not people. No
named individuals appear in the run.

**One soft hit:** the role "Platform architect" is a fair paraphrase of
the PRD's mix of "[Platform Advisor]" / "[Platform Engineer]" but is
not a verbatim PRD title. Acceptable per spike discipline ("proposed
owner ROLE") but worth flagging.

**Net:** ✅ no fabricated owners.

### Concrete values the PRD left open

Scanned the run for invented thresholds, retry counts, schemas:

- **Intent-confidence threshold** — PRD asks "Will we need an intent
  extraction confidence score?" The run logs the absence as a SPIKE
  (S-04) and Q-01 but **does not name a threshold value**. The
  reference's `confidenceScore: 0.92` example would be invention; the
  run avoids it.
- **Sentiment threshold** — PRD names sentiment as a route trigger but
  not a threshold. The run notes "Escalation when caller sounds angry
  / frustrated / urgent" (verbatim from PRD), no numeric threshold
  invented.
- **Retry counts** — PRD: "after one-retry," "one retry, then escalate."
  The run cites "1 retry, then escalate" — sourced directly from PRD.
- **Action input/output schemas** — The reference has full
  `Input Schema` and `Output Schema` columns. The run leaves Action
  inventory tables at name + one-line purpose ONLY, with an explicit
  challenge note that input/output schemas are MISSING. ✅
- **Variables Block contents** — The Variables Block is marked MISSING
  per-subagent; the run does not invent declared variables.
- **Mechanism guesses** — The run does name `flow` / `prompt` / `action`
  per action. For SA-1 (ID&V) and SA-5 (Case search/create), mechanisms
  are explicitly tagged `S-01`/`S-03` SPIKE; the value is a placeholder
  paired with `Exists today? unknown`. For SA-3 (Intent extraction) and
  SA-4 (Escalation), the PRD itself names the mechanism ("Flow & prompt
  for intent extraction"; "use existing OOTB Escalation Action"), so
  the run is sourcing not inventing. **Worth flagging:** mechanism
  values for SA-1 actions 1.1–1.4 are best-fit inferences (the PRD
  doesn't name the mechanism explicitly there), even though paired
  with SPIKE status. This is a soft invention — defensible because
  the row is marked SPIKE, but a stricter reading would say
  "Mechanism: TBD" in that column too.

**Net:** ✅ approximately zero. One soft invention to flag: mechanism
inferences for SA-1 1.1–1.4 paired with SPIKE rather than left blank.

### Other inventions

- Owner role on S-06 is "Engineering lead" — defensible from PRD's
  generic engineering mentions.
- Q-06 ("Does v1 support both AFV and SCV channels, or AFV only?")
  derives directly from PRD §Possible Spikes and PRD To Dos discussing
  AFV vs SCV. Not invention.
- The "Channels in scope: Voice" answer relies on the PRD section
  titled "voice agent template" — not invention.

---

## SPIKE FIDELITY

The PRD has three spike signals:

1. **Inline `[P2-TBD]`** on engagement records. → ✅ Run logs **S-02**:
   "Engagement records (P2-TBD): data-model decision per PRD
   requirements section."
2. **Inline "conduct a technical spike to evaluate … Identity
   Verification flows."** → ✅ Run logs **S-01**:
   "Evaluate existing Identity Verification flows for reuse vs custom
   action (PRD inline)."
3. **§Possible Spikes section** (table of 8 spike rows). → ✅ Run logs
   **S-03** (case search SCV framework), **S-04** (routing approach +
   subagent GA), **S-05** (sentiment OOTB feasibility), **S-06** (case
   wrap-up summary SCV vs custom), **S-07** (send-email exploration).

**Coverage:** 7 spikes, all with owner ROLE + P0/P1, none with invented
specifics. The reference's 10 spikes go deeper (e.g. VoiceCall↔Case
relationship spike, custom prompt template design spike) — those are
gaps surfaced by the senior designer's own deeper read of the PRD's
"To Dos" section, not gaps the PRD names directly. The run could
plausibly catch the To Dos spikes too with a more aggressive sweep;
under-coverage rather than over-claim. **Net: ✅ all PRD-surfaced
spikes captured, none invented.**

---

## COVERAGE — rubric rows where the north-star has substance the run missed

| Rubric row                                    | North-star contains                                                          | Run                                                        |
|------------------------------------------------|------------------------------------------------------------------------------|-------------------------------------------------------------|
| 1. Goal + non-goals                            | 7-bullet "Goal(Instructions)" block (PHI handling, parity, zero context loss, etc.) | Sourced from PRD's narrower §Requirements/§Objective. The richer north-star "goals" are interview-derived. ✅ correct to omit. |
| 5. Subagent inventory archetype tags           | Marked subagents' Type column ("Custom: Patient Access", "OOTB Agentforce Topic", "HC GA", etc.) | Run leaves archetype as MISSING per-subagent. North-star Type values aren't quite the AX archetype taxonomy anyway (transactional/informational/routing-orchestration). ✅ correct to leave MISSING. |
| 6/7 per-subagent action inventory + schemas    | Full action tables with Input/Output schemas, e.g. SA-2 Action 2.1 "Extract Call Intent"; SA-4 Action 4.2 "Generate Case Subject & Description" | Run lists action names + one-line purpose, marks input/output MISSING. The PRD genuinely does not contain these schemas; ✅ correct to leave gap. |
| 11. Human escalation / handoff                 | Explicit "screen pop" with member context, sentiment indicator, draft case ID | Run cites "Conversation catch up" (the PRD's named OOTB feature) but does NOT enumerate the screen-pop fields. ✅ correct — that detail is interview-derived, not in PRD. |
| Conditional / Data sensitivity                  | North-star explicitly states "Einstein Trust Layer must mask PHI/PII before all LLM calls" as a Platform Note. | Run marks the conditional PARTIAL and logs Q-04. The Trust Layer mention is in PRD: present implicitly. Run could have been more direct here; mild gap. |

**Significant missed coverage in the run:** none that the PRD itself
supports. Where the north-star has substance, it's substance that came
from interviews, not the PRD. The run correctly does not fabricate it.

---

## STRUCTURE

North-star uses SA-1 … SA-9 (Identity Verification / Intent Extraction /
Case Management / Engagement Creation / Call/Chat Summary / Knowledge /
Escalation / Claims / Prior Auth / Provider Network — wait, that's 10
labelled but they title 9). The north-star numbering also has some
inconsistencies (SA-2 Case Management appears AFTER an SA-2 Intent
Extraction; SA-3 listed twice; SA-7 used for both Call/Chat Summary
section AND Claims Assistant section). So the reference is itself
slightly drifting in numbering.

**Run structure:**

- SA-1 Identity & Verification ✅
- SA-2 Engagement Records (PRD §Requirements lists this as P2-TBD;
  reference puts Engagement Creation at SA-3) — run's SA-2 ≠
  reference's SA-2. **Drift.**
- SA-3 Intent Extraction (reference SA-2 Intent Extraction is at the
  reference SA-2 slot)
- SA-4 Escalation (reference SA-6 Escalation)
- SA-5 Case Search/Create (reference SA-2 Case Management)
- SA-6 Member Eligibility / Knowledge (reference SA-5)
- SA-7 Claims (reference SA-7)
- SA-8 Prior Auth (reference SA-8)
- SA-9 Provider Network (reference SA-9)

**Net:** The run's SA-N IDs do not match the reference's SA-N IDs.
That's expected — the run produces its SA labels in PRD order (the PRD
lists subagents in: ID&V, engagement records, intent extraction,
escalation, case search/create, member eligibility, then names existing
subagents claims/prior-auth/provider). The set is identical (modulo
the PRD's deferred "update contact details"); the numbering differs.
Acceptable for v0.1 from PRD alone.

Action numbering inside each subagent (N.1, N.2) matches the rubric
shape: SA-1 has 1.1–1.4, SA-3 has 3.1–3.2, SA-5 has 5.1–5.6. ✅
Consistent.

---

## TERMINOLOGY

**Translation applied:** PRD uses "topic" and "Topic" dozens of times
(e.g. "Topic for Escalates to human agent," "New Topic — Member
eligibility using Knowledge Search," "Subagent (topic) Instructions or
description"). The run contains zero occurrences of "topic" outside the
literal `EngagementTopic` Salesforce object name (which the lint Check
8 correctly does not flag because the word "topic" is a sub-token of
the camelCase identifier).

Lint Check 8 confirmed clean. ✅

---

## PATTERN CANDIDATES

The run flagged 5 candidates:

| Situation                       | SA  | Candidate-type                | Note                                                       |
|---------------------------------|-----|-------------------------------|-------------------------------------------------------------|
| identity-verification/payer     | SA-1| would-match-seeded-standard   | PRD member-IDV flow.                                        |
| identity-verification/provider  | SA-1| would-match-seeded-standard   | PRD provider-IDV via NPI.                                   |
| sensitive-data-disclosure       | SA-1| would-match-seeded-standard   | PRD: PHI never disclosed pre-verify.                        |
| escalation-to-human             | SA-4| harvested                     | PRD explicit + sentiment + failure paths.                   |
| confirmation                    | SA-5| harvested                     | PRD: case-number confirm + update-confirm patterns.         |

**Missed candidates the PRD supports:**

- `irreversible-action-confirmation` for SA-5 (case creation is
  irreversible) — should have been tagged. Mild miss.
- `disambiguation` for SA-3 — PRD: "If the user is talking about
  multiple things — claims, not happy, eligibility — what should be the
  intent?" That's a disambiguation prompt. Mild miss.
- `missing-fallback` is implicit at multiple points in the PRD — the
  six-failure-mode taxonomy could surface it for SA-5's "If multiple
  cases are found" path. Mild miss.

**Spurious tags:** none. Every tagged candidate traces to a PRD passage.

**identity-verification persona variants:** ✅ both `/payer` (member is
the payer's plan member) and `/provider` correctly tagged separately —
which is what the brief asked for. No `/patient` variant tagged because
the PRD's payer-plan member ≠ provider's patient.

---

## VERDICT — per rubric row

| #  | Row                                            | PASS / PARTIAL / FAIL | One-line why                                                                         |
|----|------------------------------------------------|------------------------|---------------------------------------------------------------------------------------|
| 1  | Goal + non-goals                                | PASS                   | Sourced directly from PRD §Requirements and §Objective; non-goals from strikethroughs. |
| 2  | Primary user & their goal                       | PASS                   | Member + rep beneficiary both named.                                                  |
| 3  | Trigger / entry point                           | PASS                   | Inbound voice call, SCV auto-creates VoiceCall record.                                |
| 4  | Channel                                         | PASS                   | Voice; PRD's "phone/SMS/web chat" parity caveat captured.                              |
| 5  | Subagent inventory                              | PARTIAL                | All 9 subagents named; archetype tags + routing descriptions MISSING (correctly).      |
| 6/7/8 per-subagent                              | PARTIAL                | Action lists honest; mechanism marked SPIKE where PRD doesn't say; Variables Block MISSING throughout. Soft invention on SA-1 mechanism inferences. |
| 9  | Guardrails / must-nevers                        | PARTIAL                | Three constraints captured; placements are best-fit inferences flagged as such.        |
| 10 | Failure & recovery + global messages            | PARTIAL                | Retry policy captured from PRD; `welcome` from PRD; `error` hook MISSING.              |
| 11 | Human escalation / handoff                      | PASS                   | All 6 PRD-named triggers captured; Conversation catch-up cited.                        |
| 12 | Success metrics                                 | FAIL (correctly)       | PRD names none; logged as P0 gap.                                                      |
| 13 | v1 scope boundary + open spikes                 | PASS                   | In/out enumerated from PRD; 7 spikes logged.                                            |

---

## Overall call

**Yes — usable starting draft.**

The run is honest about what the PRD contains and disciplined about
what it doesn't. A PM walking into design review with this draft has:

- A subagent inventory that names the agent's parts (even if their
  numbering will likely renumber after interviews).
- A clear set of 7 spikes the PRD already implies, with role-level
  owners — enough to schedule a spike review.
- An explicit P0 gap list calling out the four blockers (subagent
  archetype tags, SA-1 / SA-2 / SA-5 mechanism decisions, success
  metrics) — the conversations design review needs to have.
- A pattern-candidate flag list that gets passed to Layer 3 later.

What it does NOT have, the north-star also does not have FROM PRD —
those came from interviews. A user comparing this draft to the
north-star and asking "where's the screen pop detail?" is asking the
wrong question; the right one is "what does the next round of
interviews need to produce?" and the run answers that via its open
questions and spike log.

**Soft issues to address in v0.2:**

1. SA-1 1.1–1.4 mechanism values are best-fit inferences paired with
   SPIKE status. A stricter reading would leave the Mechanism column
   blank ("—") and let the SPIKE status alone carry the unknown. The
   skill could be tightened to do this; not a hard violation.
2. Three pattern-candidate misses (irreversible-action-confirmation
   for SA-5, disambiguation for SA-3, missing-fallback for SA-5
   multi-case path).
3. The PRD's "To Dos" section names additional spikes (AFV-vs-SCV
   sentiment, KPMG/Northwell reference impl) the run did not surface.
   Two of those land in the north-star as S-08 and S-09. Recoverable
   in v0.2.

None of those is invention. All are under-coverage. The honest call:
**this is a v0.1 starting draft, and it would be useful to design
review.**
