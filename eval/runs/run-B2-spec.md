# Member Services Voice Agent — Agent Spec

**Version:** 0.1
**Date:** 2026-06-25
**Authors:** ax-agent-spec
**Team:** <TEAM_NAME>
**Product Owner (owner_contact):** <TBD — captured at intake>
**Primitives version:** 1.0 (last_verified 2026-06-24)

---

## Completion manifest

### Rubric coverage

| Rubric row                                                  | Scope    | Status   | Notes / Spike refs |
|-------------------------------------------------------------|----------|----------|---------------------|
| 1. Goal + non-goals                                         | Agent    | PARTIAL  | Non-goals not listed in PRD. |
| 2. Primary user & their goal                                | Agent    | PARTIAL  | Persona detail thin; "member" only. |
| 3. Trigger / entry point                                    | Agent    | ANSWERED | Inbound member call.       |
| 4. Channel                                                  | Agent    | ANSWERED | Voice.                     |
| 5. Subagent inventory                                       | Subagent | MISSING  | PRD lists capabilities, not subagents.       |
| 9. Guardrails / must-nevers, with placement                 | Agent    | MISSING  |                            |
| 10. Failure & recovery + global messages                    | Agent    | MISSING  |                            |
| 11. Human escalation / handoff                              | Agent    | PARTIAL  | Trigger named; copy + context not.           |
| 12. Success metrics                                         | Agent    | PARTIAL  | Directional only; no baselines or units.     |
| 13. v1 scope boundary + open spikes                         | Agent    | MISSING  | "this release if possible" not a boundary.   |

### Source documents ingested

| Document                                  | Type | Ingested on | Notes                                  |
|-------------------------------------------|------|-------------|-----------------------------------------|
| Member Services Voice Agent (sparse draft) | PRD  | 2026-06-25  | ~250 words; no mechanisms, no owners.   |

### P0 gaps (recorded at P0 gate)

| Rubric row                                          | Subagent ref | Downstream sections this degrades                                                                       |
|------------------------------------------------------|--------------|----------------------------------------------------------------------------------------------------------|
| 5. Subagent inventory                                 | —            | Every per-subagent row (6/7/8). Layer 2 cannot wire any routing.                                          |
| 6. Action inventory (per subagent)                    | —            | Engineering has no actions to build.                                                                       |
| 7. Execution mechanism (per subagent)                 | —            | No `apex`/`flow`/`prompt` selection possible; no feasibility spike scope.                                  |
| 8. Data read/written + Variables Block (per subagent) | —            | Reversibility and Trust Layer masking gates cannot be designed.                                            |
| 9. Guardrails / must-nevers, with placement            | —            | No `system: instructions` body; no Script-enforced rules.                                                  |
| 10. Failure & recovery + global messages               | —            | `welcome` and `error` hooks undefined.                                                                     |
| 12. Success metrics                                    | —            | Cannot ship/no-ship gate — directional only.                                                                |
| 13. v1 scope boundary + open spikes                    | —            | Engineering cannot scope.                                                                                  |

User chose: **proceed with gaps**.

### Open questions awaiting user

| ID    | Question                                                                                                                            | Blocking? |
|-------|--------------------------------------------------------------------------------------------------------------------------------------|------------|
| Q-01  | What sensitive-data classes does the agent touch (PHI, PII, financial)? PRD only says "member data, be careful."                       | yes        |
| Q-02  | What Trust Layer masking posture applies to any transcript fed to an LLM?                                                              | yes        |
| Q-03  | What is the subagent inventory? PRD lists capabilities (identify, answer, create case, summarize, hand off) — are these subagents?     | yes        |
| Q-04  | What is the v1 success metric, baseline, and reporting surface? "Reps spend less time on wrap-up" needs a number.                       | yes        |
| Q-05  | What is in-scope and out-of-scope for v1? PRD says "this release if possible" — that's not a boundary.                                 | yes        |
| Q-06  | What does "the easy calls" mean? Which intents are in v1 (eligibility, benefits, claim status named — anything else)?                  | yes        |
| Q-07  | Who owns this agent (team + product owner)? Required for the title block and pattern provenance.                                       | yes        |
| Q-08  | What is the escalation policy — copy, threshold, retry count? PRD says "pass to a human when needed."                                 | no         |
| Q-09  | What does "the same whether a human or the agent handled" mean operationally — same Case fields, same summary format, both?           | no         |

### Pattern candidates

| Situation | Mechanism | Subagent ref | Candidate-type | Note |
|-----------|-----------|--------------|----------------|------|

> No rows: PRD names no subagents (row 5 MISSING) so candidates cannot be
> anchored to an `SA-N` reference. Tagging deferred until the subagent
> inventory exists. Two recurring situations are visible in the PRD —
> escalation-to-human and sensitive-data-disclosure — but they will be
> tagged at the next generation once subagents are named.

### Changelog

| Version | Date         | Author          | Summary                                                                       |
|---------|--------------|-----------------|-------------------------------------------------------------------------------|
| 0.1     | 2026-06-25   | ax-agent-spec   | First generation from sparse PRD. P0 gate fired; user chose proceed with gaps. Iteration 02 rules applied: mechanism-on-SPIKE not exercised (no actions inventoried); taxonomy sweep ran but candidates table stays empty per evidence-only + SA-N-anchor rule. |

---

## Seeding context

> "Roughly, what does this agent do, for whom, in what channel?"

Per PRD: an AI voice agent for payer member calls that handles routine
questions (eligibility / benefits / claim status), creates a Case at the
end, writes a summary, and hands off to a human when needed. The PRD is
a thin early draft; many fields are missing.

---

## 1. Goal + non-goals — [PARTIAL]

Stand up a voice agent that answers common member questions (eligibility,
benefits, claim status), creates a case for the issue, writes a wrap-up
summary, and hands off to a human when it cannot handle the request.

**Won't do (explicit non-goals):** MISSING.

> Challenge: "If it works perfectly, what changed for the user and the
> business? Name 3 things a user might expect that it won't do." The PRD
> names what the agent SHOULD do but not what it explicitly won't —
> without that, scope creep is guaranteed.

## 2. Primary user & their goal — [PARTIAL]

End-customer payer health-plan members making inbound calls. Their goal
per PRD: get a routine question answered (eligibility, benefits, claim
status) or initiate something simple. Beneficiary persona named in PRD
as the call-center rep, whose wrap-up burden the agent reduces.

> Challenge: "Is the agent acting FOR the user, or AS the user toward a
> third party?" Also unanswered: which member sub-personas (member vs
> caregiver / proxy) are in scope for v1.

## 3. Trigger / entry point — [ANSWERED]

Inbound member phone call to the payer call centre.

## 4. Channel — [ANSWERED]

Voice. Channel profile reference: `references/channels/text.md` for the
base modality; voice overlay not yet authored.

> **Staleness note:** primitives last_verified 2026-06-24 — within the
> 120-day window. Voice channel parity claim still
> `[steward-provided, link pending]` in primitives.

---

## 5. Subagent inventory + routing — [MISSING]

PRD enumerates capabilities ("take inbound calls / figure out who's
calling / answer common questions / create a case / write a summary /
hand off / maybe send email") but does NOT define subagents. Without an
inventory, archetype tagging cannot occur, and the conditional rows for
grounding (informational subagents) and confirmation (transactional
subagents) cannot be applied per subagent. Logged as Q-03.

> Challenge: "Could two subagents both claim the same request? How does
> the Reasoning Engine decide?" If a subagent is genuinely both
> transactional and informational, it is usually two subagents.
>
> A subagent inventory is required before generation can proceed to
> per-subagent rows 6/7/8. The skill does NOT invent subagents from the
> capability list — that is the user's call.

---

## 9. Guardrails / must-nevers, with placement — [MISSING]

PRD says only "member data … be careful." That is a hint, not a
guardrail. No specific rule, no placement (`system: instructions` vs
subagent-local vs Script-enforced) is declared.

> Challenge: "What's the worst thing it could do if it misunderstood?
> Which rules are deterministic enough for Script?" Health Cloud
> sensitive-data invariant requires masking posture BEFORE the first
> LLM call — this must be specified, not inferred.

## 10. Failure & recovery + global messages — [MISSING]

PRD does not define retry behaviour on action failure, unclear intent,
or low confidence. No `welcome` or `error` hook copy is provided.

> Challenge: "After how many failed attempts does it stop trying? What
> does the `error` hook say?" Without `welcome` defined, the first
> sentence the caller hears is undefined.

## 11. Human escalation / handoff — [PARTIAL]

PRD: "If it can't handle something, it should pass the caller to a
human." Trigger is named at the highest level. NOT named: the specific
triggers (caller explicitly asks vs sentiment vs intent failure vs
action failure), the copy used to transition, and what context transfers
to the human.

> Challenge: "When the human picks up, what do they already see without
> re-asking?"

## 12. Success metrics — [PARTIAL]

PRD lists directional outcomes: "Reps spend less time on wrap-up / Members
get answers faster / Fewer calls need a human." No baseline, no target
number, no reporting surface specified.

> Challenge: "What number moves if this agent works?"

## 13. v1 scope boundary + open spikes — [MISSING]

PRD: "Timeline is this release if possible. Will fill in more detail
after design review." That is not a v1 boundary. Spikes are not
enumerated in the PRD.

> Challenge: "What's the smallest version still worth shipping?"

---

# Conditional sections (rendered only when their trigger fires)

## Data sensitivity & masking posture — [MISSING]

Trigger fired by PRD §Notes: "This is a payer/health use case so there's
member data involved — we'll need to be careful about that." Per
`references/invariants.md`, the agent must define its masking posture
BEFORE the first LLM call. In Health Cloud, Einstein Trust Layer masking
is mandatory and PHI-adjacent generation requires CUSTOM prompt
templates (not generic summaries). The PRD specifies none of this.

> Challenge: "Which member-data fields are PHI, which are PII, and which
> are neither? What is the masking configuration? Does call summary
> generation require a custom prompt template?"

## Performance & latency tolerance — [MISSING]

Trigger fired: voice channel. PRD does not state acceptable latency,
concurrency, or availability targets.

> Challenge: "What is the maximum acceptable latency between caller
> utterance and agent response in voice mode?"

---

# Deferred placeholders

## Golden path & decision-point design — [DEFERRED-L2]
Golden path required — to be designed in Behavior Blueprint.

## Persona / voice & tone detail — [DEFERRED-L2]
Persona detail required — to be designed in Behavior Blueprint.

## Recovery flow CONVERSATION design — [DEFERRED-L2]
Recovery flow conversation required — to be designed in Behavior Blueprint.

## Rendering, trust-signal UI, surface patterns — [DEFERRED-L3]
Rendering, trust-signal UI, and surface patterns required — to be designed
in the Interface layer.

---

# Spike log

| Spike ID | Owner role        | Priority | Rubric ref     | Question                                                                                          | Status |
|----------|-------------------|----------|----------------|---------------------------------------------------------------------------------------------------|--------|
| S-01     | Product owner      | P0       | Row 5          | Define subagent inventory: are the capabilities listed in the PRD one subagent or several?         | open   |
| S-02     | Product owner      | P0       | Row 9 / Row 12 | Define sensitive-data class + Trust Layer masking posture for member data referenced in PRD Notes.  | open   |
| S-03     | Product owner      | P0       | Row 12         | Name v1 success metric, baseline, reporting surface. "Less / faster / fewer" is directional only.   | open   |
| S-04     | Product owner      | P0       | Row 13         | Define v1 scope boundary explicitly — in scope, out of scope, deferred-to-264+.                     | open   |
