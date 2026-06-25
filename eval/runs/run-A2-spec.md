# Call Wrap-Up Summary Agent — Agent Spec

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
| 1. Goal + non-goals                                         | Agent    | ANSWERED |                     |
| 2. Primary user & their goal                                | Agent    | ANSWERED |                     |
| 3. Trigger / entry point                                    | Agent    | ANSWERED |                     |
| 4. Channel                                                  | Agent    | ANSWERED |                     |
| 5. Subagent inventory                                       | Subagent | PARTIAL  | Archetype tags MISSING from PRD; routing descriptions MISSING |
| 6. Action inventory — SA-1                                  | Subagent | PARTIAL  |                     |
| 7. Execution mechanism & feasibility — SA-1                 | Subagent | SPIKE    | S-01                |
| 8. Data read/written + Variables Block — SA-1               | Subagent | PARTIAL  | Variables Block MISSING |
| 6. Action inventory — SA-2                                  | Subagent | SPIKE    | S-02                |
| 7. Execution mechanism & feasibility — SA-2                 | Subagent | SPIKE    | S-02                |
| 8. Data read/written + Variables Block — SA-2               | Subagent | PARTIAL  |                     |
| 6. Action inventory — SA-3                                  | Subagent | PARTIAL  |                     |
| 7. Execution mechanism & feasibility — SA-3                 | Subagent | PARTIAL  |                     |
| 8. Data read/written + Variables Block — SA-3               | Subagent | PARTIAL  | Variables Block MISSING |
| 6. Action inventory — SA-4                                  | Subagent | PARTIAL  |                     |
| 7. Execution mechanism & feasibility — SA-4                 | Subagent | PARTIAL  |                     |
| 8. Data read/written + Variables Block — SA-4               | Subagent | PARTIAL  | Variables Block MISSING |
| 6. Action inventory — SA-5                                  | Subagent | PARTIAL  |                     |
| 7. Execution mechanism & feasibility — SA-5                 | Subagent | SPIKE    | S-03                |
| 8. Data read/written + Variables Block — SA-5               | Subagent | PARTIAL  | Variables Block MISSING |
| 6. Action inventory — SA-6                                  | Subagent | PARTIAL  |                     |
| 7. Execution mechanism & feasibility — SA-6                 | Subagent | PARTIAL  |                     |
| 8. Data read/written + Variables Block — SA-6               | Subagent | MISSING  |                     |
| 6. Action inventory — SA-7                                  | Subagent | PARTIAL  | PRD references existing subagent |
| 7. Execution mechanism & feasibility — SA-7                 | Subagent | PARTIAL  |                     |
| 8. Data read/written + Variables Block — SA-7               | Subagent | MISSING  |                     |
| 6. Action inventory — SA-8                                  | Subagent | PARTIAL  | PRD references existing subagent |
| 7. Execution mechanism & feasibility — SA-8                 | Subagent | PARTIAL  |                     |
| 8. Data read/written + Variables Block — SA-8               | Subagent | MISSING  |                     |
| 6. Action inventory — SA-9                                  | Subagent | PARTIAL  | PRD references existing subagent |
| 7. Execution mechanism & feasibility — SA-9                 | Subagent | PARTIAL  |                     |
| 8. Data read/written + Variables Block — SA-9               | Subagent | MISSING  |                     |
| 9. Guardrails / must-nevers, with placement                 | Agent    | PARTIAL  |                     |
| 10. Failure & recovery + global messages                    | Agent    | PARTIAL  | system: messages MISSING |
| 11. Human escalation / handoff                              | Agent    | ANSWERED |                     |
| 12. Success metrics                                         | Agent    | MISSING  |                     |
| 13. v1 scope boundary + open spikes                         | Agent    | ANSWERED | S-01..S-07          |

### Source documents ingested

| Document                          | Type | Ingested on | Notes                                       |
|-----------------------------------|------|-------------|----------------------------------------------|
| 264 Call Wrap-up PRD (developed)  | PRD  | 2026-06-25  | Subagent terminology translated on intake.   |

### P0 gaps (recorded at P0 gate)

| Rubric row                                       | Subagent ref | Downstream sections this degrades |
|--------------------------------------------------|--------------|------------------------------------|
| 5. Subagent inventory (archetype tags + routing) | —            | Layer 2 Goal/Role-Boundaries; routing of Reasoning Engine cannot be wired. |
| 7. Execution mechanism — SA-1                    | SA-1         | Engineering cannot select Identity Verification mechanism without spike outcome. |
| 7. Execution mechanism — SA-2                    | SA-2         | P2-TBD per PRD; engagement records data-model decision blocked. |
| 7. Execution mechanism — SA-5                    | SA-5         | Case search mechanism — Omni Flow vs custom path — undecided. |
| 12. Success metrics                              | —            | No measurable v1 success criteria; ship/no-ship decision cannot be made. |

User chose: **proceed with gaps** (recorded in changelog v0.1 below).

### Open questions awaiting user

| ID    | Question                                                                                                    | Blocking? |
|-------|--------------------------------------------------------------------------------------------------------------|------------|
| Q-01  | Is "call wrap-up summary" its own subagent, or is it a post-call step of SA-5 Case Management?              | yes        |
| Q-02  | What is the engagement-records data model decision (P2-TBD per PRD)?                                          | yes        |
| Q-03  | Should the agent support caregiver / proxy callers in v1, and if so, how is POA verified?                    | yes        |
| Q-04  | Which Trust Layer masking posture applies to the sanitized transcript fed to the intent + summary prompts?   | yes        |
| Q-05  | What is the v1 success metric and the baseline it improves against?                                           | yes        |
| Q-06  | Does v1 support both AFV and SCV channels, or AFV only?                                                        | no         |

### Pattern candidates

| Situation                          | Mechanism | Subagent ref | Candidate-type                | Note                                                                                       |
|------------------------------------|-----------|--------------|--------------------------------|---------------------------------------------------------------------------------------------|
| identity-verification/payer        | flow      | SA-1         | would-match-seeded-standard    | PRD: "Leverage existing Identity Verification flows" for member calls.                      |
| identity-verification/provider     | flow      | SA-1         | would-match-seeded-standard    | PRD: provider verification via NPI; distinct from member verification.                       |
| sensitive-data-disclosure          | prompt    | SA-1         | would-match-seeded-standard    | PRD: "Verification: After identification, we need to verify the caller before giving out any PHI data." |
| disambiguation                     | prompt    | SA-3         | harvested                      | PRD: "If the user is talking about multiple things — claims, not happy, eligibility — what should be the intent?" |
| missing-fallback                   | flow      | SA-5         | harvested                      | PRD: "If multiple cases are found, VA says … 'this request needs a quick review by one of our agents.'" Multi-case branch has no automated alternative path. |
| irreversible-action-confirmation   | flow      | SA-5         | harvested                      | PRD: Case creation is irreversible in regulated books — Cases are auto-created from transcripts. |
| escalation-to-human                | action    | SA-4         | harvested                      | PRD: explicit + sentiment-driven + failure-driven escalation paths.                          |
| confirmation                       | prompt    | SA-5         | harvested                      | PRD: confirm case-number with caller before re-search; confirm updates.                       |

### Changelog

| Version | Date         | Author          | Summary                                                                 |
|---------|--------------|-----------------|--------------------------------------------------------------------------|
| 0.1     | 2026-06-25   | ax-agent-spec   | First generation from developed PRD. P0 gate fired; user chose proceed with gaps. Iteration 02: mechanism blanked on SPIKE rows; taxonomy sweep added 3 candidates. |

---

## Seeding context

> "Roughly, what does this agent do, for whom, in what channel?"

Per PRD problem + objective: a voice agent that handles low-risk member
calls for a payer call centre, automates case creation and call wrap-up
summary, and hands off to a human when complexity exceeds its scope.
Channel: voice (with chat parity per a Platform Advisor note in PRD).

---

## 1. Goal + non-goals — [ANSWERED]

Ship a voice agent template (Service Assistant Agent with Voice modality)
that allows payer customers to divert low-risk member queries (status,
eligibility, claim lookup) to a voice agent that performs end-to-end call
orchestration: identification, verification, intent routing, case
search/create, wrap-up summary, escalation, and optional email
(PRD §Requirements + §Objective).

**Won't do (explicit non-goals per PRD):**

- Initial CC setup, routing logic, escalation queue, and base flows
  (PRD §Requirements closing note: "out of scope as this is already
  available by platform").
- Update member contact details subagent (struck through in PRD §Happy
  Path).
- Activity / Task / Event creation; the PRD explicitly says "We don't
  create tasks or logActivity as that's not a std customers follow."
- Spanish language (deferred to 264+).
- Complex case creation (Referral, Schedule appt., Grievance, PriorAuth
  marked as 264+).

## 2. Primary user & their goal — [ANSWERED]

End-customer member callers (payer health-plan members) whose goal is to
get a routine question answered or a request logged. The PRD also names
"Call Center Representative" as a beneficiary because the agent reduces
their admin burden, but the agent's direct interlocutor is the member
(PRD §Problem Statement + §Requirements).

## 3. Trigger / entry point — [ANSWERED]

Inbound phone call to the payer call centre. A Voice Call record is
auto-created by Service Cloud Voice; the agent activates after SCV-side
greeting and routing (PRD §Happy Path: "Call lands … Voice call creation
happens automatically").

## 4. Channel — [ANSWERED]

Voice (Service Cloud Voice / Agentforce Voice). PRD also notes the
Platform Advisor view that the same implementation should work over
phone, SMS, and web chat with no voice-specific functionality. Channel
profile: read `references/channels/text.md` as the base; voice overlay
not yet authored.

> **Staleness note:** primitives last_verified 2026-06-24 — within the
> 120-day window. Voice-channel parity claim in primitives is still
> `[steward-provided, link pending]`; flag if engineering needs the live
> doc citation before sprint planning.

---

## 5. Subagent inventory + routing — [PARTIAL]

Per PRD, the following subagents (the PRD says "subagents" in legacy
terminology; translated on intake). Archetype tags are MISSING from the
PRD and not invented here. Routing descriptions and deterministic
routing conditions are MISSING from the PRD beyond high-level intent →
subagent mapping.

| ID    | Subagent name                | Archetype | Routing description (PRD)                                          | Deterministic routing conditions |
|-------|------------------------------|-----------|---------------------------------------------------------------------|-----------------------------------|
| SA-1  | Identity & Verification      | MISSING   | Identify caller via ANI; verify before any PHI is disclosed.        | MISSING                            |
| SA-2  | Engagement Records           | MISSING   | Create EngagementInteraction / EngagementAttendee / EngagementTopic records (P2-TBD). | MISSING |
| SA-3  | Intent Extraction            | MISSING   | Extract intent + sentiment from transcript; route to other subagents. | MISSING                          |
| SA-4  | Escalation                   | MISSING   | Hand off to human agent on explicit request, sentiment, or failure. | MISSING                            |
| SA-5  | Case Search / Create         | MISSING   | Search existing case if intent implies follow-up; else create case. | MISSING                            |
| SA-6  | Member Eligibility (Knowledge) | MISSING | Answer plan/benefit/coverage questions via OOTB Knowledge subagent. | MISSING                            |
| SA-7  | Claims Assistant             | MISSING   | Existing subagent referenced in PRD setup section.                  | MISSING                            |
| SA-8  | Prior Auth Assistant         | MISSING   | Existing subagent referenced in PRD setup section.                  | MISSING                            |
| SA-9  | Provider Network Search      | MISSING   | Existing subagent referenced for provider-matching intent.          | MISSING                            |

> Challenge if MISSING: "Could two subagents both claim the same request?
> How does the Reasoning Engine decide?" Archetype tagging is required
> before grounding (informational) and confirmation (transactional)
> conditional rows can be applied per-subagent — this is currently
> blocked.

---

# Subagent: SA-1 — Identity & Verification  [archetype: MISSING]

## 6. Action inventory — [PARTIAL]

| Action ID | Name                              | One-line purpose                                                                 |
|-----------|-----------------------------------|----------------------------------------------------------------------------------|
| 1.1       | Look up account by ANI            | Search Account/Contact records using inbound phone number stamped on VoiceCall.   |
| 1.2       | Collect identity fallback         | Prompt caller for member/provider/caregiver self-id when ANI fails.               |
| 1.3       | Verify identity                   | Confirm member full name + DOB (member) or full name + NPI (provider) before PHI. |
| 1.4       | Escalate on verification failure  | Hand off to human after one retry per PRD.                                        |

> Challenge: "For each action, who or what actually performs it?" — input
> / output schemas are MISSING from the PRD.

## 7. Execution mechanism & feasibility — [SPIKE]

| Action ID | Mechanism | Exists today? | Spike (if not) |
|-----------|-----------|---------------|-----------------|
| 1.1       |           | unknown       | S-01            |
| 1.2       |           | unknown       | S-01            |
| 1.3       |           | unknown       | S-01            |
| 1.4       |           | unknown       | S-01            |

PRD §Requirements explicitly logs a spike: "Conduct a technical spike to
evaluate and leverage existing Identity Verification flows." Logged as
S-01. Mechanism column blank per mechanism-on-SPIKE rule — guessing
`flow` here would be invention.

> Challenge: "Which actions assume a capability that doesn't exist yet?"

## 8. Data read/written + Variables Block — [PARTIAL]

**Records / objects read vs created/mutated** (per PRD §Happy Path):

| Object / record       | Direction      | Reversible? |
|-----------------------|----------------|-------------|
| VoiceCall             | read           | n/a         |
| Account               | read           | n/a         |
| Contact               | read           | n/a         |
| EngagementInteraction | create         | no          |
| EngagementAttendee    | create         | no          |

**Declared state (Variables Block):** MISSING — PRD does not enumerate
declared variables.

> Challenge: "What does it change, and is that reversible? What state
> must survive across turns that you're assuming the LLM will just
> remember?"

---

# Subagent: SA-2 — Engagement Records  [archetype: MISSING]

## 6. Action inventory — [SPIKE]

PRD §Requirements marks this entire subagent **[P2-TBD]**. Action
inventory not yet defined; engagement-record creation may instead
happen automatically as part of SA-1 per PRD §Happy Path. Logged as
S-02.

> Challenge: "For each action, who or what actually performs it?" — to
> be answered after the engagement-records data-model spike.

## 7. Execution mechanism & feasibility — [SPIKE]

Mechanism cannot be selected until S-02 resolves the engagement-records
data-model question. PRD: "Voice object records are automatically
created and have the same purpose. Creation of engagement interaction
records is not a std. our customers follow." No action inventory yet
means no mechanism table to populate.

> Challenge: "Which actions assume a capability that doesn't exist yet?"

## 8. Data read/written + Variables Block — [PARTIAL]

**Records / objects read vs created/mutated** (per PRD §Happy Path table
row for EngagementTopic creation):

| Object / record       | Direction      | Reversible? |
|-----------------------|----------------|-------------|
| EngagementInteraction | create / update | no         |
| EngagementAttendee    | create / update | no         |
| EngagementTopic       | create / update | no         |

**Declared state (Variables Block):** MISSING — PRD does not enumerate.

> Challenge: "What does it change, and is that reversible?"

---

# Subagent: SA-3 — Intent Extraction  [archetype: MISSING]

## 6. Action inventory — [PARTIAL]

| Action ID | Name                          | One-line purpose                                                                  |
|-----------|-------------------------------|------------------------------------------------------------------------------------|
| 3.1       | Extract intent from transcript | Per PRD: "Flow & prompt for intent extraction to connect to the right other subagents." |
| 3.2       | Extract sentiment              | Per PRD: post-processing flow + LLM prompt template stamping sentiment on Voice Call record. |

> Challenge: "For each action, who or what actually performs it?" — PRD
> conflicts on difficulty: one source says "pretty straightforward,"
> another says "must be built using a record-triggered flow with an
> embedded prompt template." Both noted; neither resolved.

## 7. Execution mechanism & feasibility — [PARTIAL]

| Action ID | Mechanism      | Exists today? | Spike (if not) |
|-----------|----------------|---------------|-----------------|
| 3.1       | flow + prompt  | no            | PRD: "not OOTB; must be built."  |
| 3.2       | flow + prompt  | no            | PRD: "is not OOTB feature; requires post-processing via a flow and an LLM prompt template." |

Mechanism here is NOT a guess — the PRD names "Flow & prompt" verbatim
for both actions.

> PRD does not give a confidence-score threshold for intent extraction —
> the PRD open question is logged as Q-01 in the rubric-coverage table
> via the matching open question, but the threshold itself is NOT
> invented here. PRD: "Will we need an intent extraction confidence
> score?"

## 8. Data read/written + Variables Block — [PARTIAL]

**Records / objects read vs created/mutated:**

| Object / record | Direction | Reversible? |
|-----------------|-----------|-------------|
| VoiceCall       | read      | n/a         |
| VoiceCall       | mutate (stamp intent + sentiment fields) | no |

**Declared state (Variables Block):** MISSING.

> Challenge: "What state must survive across turns?"

---

# Subagent: SA-4 — Escalation  [archetype: MISSING]

## 6. Action inventory — [PARTIAL]

| Action ID | Name                                 | One-line purpose                                                  |
|-----------|--------------------------------------|---------------------------------------------------------------------|
| 4.1       | Initiate human transfer              | PRD: "use existing OOTB Escalation Action."                          |
| 4.2       | Provide conversation catch-up         | PRD: "Std feature to provide the human agent with a summary of everything that has happened." |

> Challenge: "For each action, who or what actually performs it?"

## 7. Execution mechanism & feasibility — [PARTIAL]

| Action ID | Mechanism | Exists today? | Spike (if not) |
|-----------|-----------|---------------|-----------------|
| 4.1       | action    | yes (OOTB)    |                 |
| 4.2       | action    | yes (OOTB)    |                 |

PRD names both as OOTB platform features — mechanism is sourced, not
guessed.

## 8. Data read/written + Variables Block — [PARTIAL]

| Object / record | Direction | Reversible? |
|-----------------|-----------|-------------|
| VoiceCall       | read      | n/a         |

**Declared state (Variables Block):** MISSING.

> Challenge: "What state must survive across turns?"

---

# Subagent: SA-5 — Case Search / Create  [archetype: MISSING]

## 6. Action inventory — [PARTIAL]

| Action ID | Name                              | One-line purpose                                                |
|-----------|-----------------------------------|------------------------------------------------------------------|
| 5.1       | Search case by case number        | PRD: "P0: Search on Case no."                                    |
| 5.2       | Search case by intent + recency    | PRD: "P1: Search on Case description using caller intent + sort on most recent cases" |
| 5.3       | Create case                        | PRD: "Else, create a new case for all inquiries."                |
| 5.4       | Pre-fill case from transcript      | PRD: "pre-fill Case record details from the call transcription." |
| 5.5       | Auto-close case if no follow up    | PRD: "Auto-close case if no follow up work needed."              |
| 5.6       | Send email on open case            | PRD: "Send emails as applicable."                                |

> Challenge: "For each action, who or what actually performs it?" —
> input / output schemas MISSING from PRD.

## 7. Execution mechanism & feasibility — [SPIKE]

| Action ID | Mechanism | Exists today? | Spike (if not) |
|-----------|-----------|---------------|-----------------|
| 5.1       |           | unknown       | S-03            |
| 5.2       |           | unknown       | S-03            |
| 5.3       |           | unknown       | S-03            |
| 5.4       |           | unknown       | S-03            |
| 5.5       |           | unknown       | S-03            |
| 5.6       |           | unknown       | S-03            |

PRD logs spike: "Search if an open case exists … check SCV framework"
and "We may not need to create a case always, sometimes we should just
create an activity log — should be decided based on call transcription
inputs." Logged as S-03. Mechanism column blank per mechanism-on-SPIKE
rule.

> Challenge: "Which actions assume a capability that doesn't exist yet?"

## 8. Data read/written + Variables Block — [PARTIAL]

| Object / record | Direction         | Reversible? |
|-----------------|-------------------|-------------|
| Case            | read / create / mutate / close | no |
| VoiceCall       | read / link       | n/a         |
| EngagementTopic | create / link     | no          |

**Declared state (Variables Block):** MISSING.

> Challenge: "What state must survive across turns?"

---

# Subagent: SA-6 — Member Eligibility (Knowledge)  [archetype: MISSING]

## 6. Action inventory — [PARTIAL]

| Action ID | Name                                  | One-line purpose                                            |
|-----------|---------------------------------------|--------------------------------------------------------------|
| 6.1       | Answer questions with knowledge        | PRD: "use existing knowledge action Answer questions with knowledge Agentforce action." |

> Challenge: "For each action, who or what actually performs it?"

## 7. Execution mechanism & feasibility — [PARTIAL]

| Action ID | Mechanism | Exists today? | Spike (if not) |
|-----------|-----------|---------------|-----------------|
| 6.1       | action    | yes (OOTB)    |                 |

PRD names it as OOTB; grounding source for the Knowledge content is
MISSING (PRD does not specify whether Salesforce Knowledge, Uploaded
Files, Web Search, or Custom Retriever holds the member-plan content).

## 8. Data read/written + Variables Block — [MISSING]

PRD does not enumerate objects read for this subagent beyond the general
Knowledge action.

> Challenge: "What does it change, and is that reversible? What state
> must survive across turns?"

---

# Subagent: SA-7 — Claims Assistant  [archetype: MISSING]

## 6. Action inventory — [PARTIAL]

PRD references "Claims Assistant Subagent" as an existing subagent.
Action inventory MISSING in this PRD; presumably covered in the existing
subagent's own spec.

> Challenge: "For each action, who or what actually performs it?"

## 7. Execution mechanism & feasibility — [PARTIAL]

Existing subagent per PRD; mechanism inherited from the existing
subagent's own spec.

> Challenge: "Which actions assume a capability that doesn't exist yet?"

## 8. Data read/written + Variables Block — [MISSING]

PRD does not enumerate.

> Challenge: "What does it change, and is that reversible?"

---

# Subagent: SA-8 — Prior Auth Assistant  [archetype: MISSING]

## 6. Action inventory — [PARTIAL]

PRD references "Prior Auth Assistant Subagent" as an existing subagent.
Action inventory MISSING in this PRD.

> Challenge: "For each action, who or what actually performs it?"

## 7. Execution mechanism & feasibility — [PARTIAL]

Existing subagent per PRD; mechanism inherited from the existing
subagent's own spec.

> Challenge: "Which actions assume a capability that doesn't exist yet?"

## 8. Data read/written + Variables Block — [MISSING]

PRD does not enumerate.

> Challenge: "What does it change, and is that reversible?"

---

# Subagent: SA-9 — Provider Network Search  [archetype: MISSING]

## 6. Action inventory — [PARTIAL]

PRD references "provider matching subagent" for `search_provider /
check_provider_ntw_status` intent. Action inventory MISSING in this PRD.

> Challenge: "For each action, who or what actually performs it?"

## 7. Execution mechanism & feasibility — [PARTIAL]

Existing subagent per PRD; mechanism inherited from the existing
subagent's own spec.

> Challenge: "Which actions assume a capability that doesn't exist yet?"

## 8. Data read/written + Variables Block — [MISSING]

PRD does not enumerate.

> Challenge: "What does it change, and is that reversible?"

---

## 9. Guardrails / must-nevers, with placement — [PARTIAL]

| Constraint                                                  | Placement              | Rationale                              |
|-------------------------------------------------------------|------------------------|----------------------------------------|
| Do NOT share member PHI before identity is confirmed.       | system: instructions   | PRD §Happy Path: "Before I proceed, can you confirm your details for me?" |
| Do NOT keep asking after one retry on ID failure; escalate. | Script-enforced        | PRD: "Hand off to a human agent if identification fails."                  |
| Member-data handling must respect HIPAA posture.            | system: instructions   | PRD §Notes: payer/health use case, member data involved.                    |

Placements above are best-fit inferences from PRD intent; PRD does NOT
explicitly classify each constraint by placement.

> Challenge: "What's the worst thing it could do if it misunderstood?
> Which rules are deterministic enough for Script?"

## 10. Failure & recovery + global messages — [PARTIAL]

**Retry / fallback policy** (per PRD scattered notes):

| Failure case        | Retry policy                    | Fallback behaviour                                                       |
|---------------------|---------------------------------|---------------------------------------------------------------------------|
| ID failure          | 1 retry, then escalate          | PRD: "I am having difficulty at the moment to retrieve your account details, let me connect you to a representative." |
| Verification failure| 1 retry, then escalate          | PRD: same escalation copy.                                                |
| Intent unclear      | 1 retry, then escalate          | PRD: "I am having difficulty at the moment to assist you on your requirement, let me connect you to a representative." |
| Case search fails   | 1 retry, then escalate          | PRD: "I'm having trouble retrieving your case details, let me connect you to a representative." |

**`system: messages` hooks:**

| Hook      | Defined? | Content                                                                |
|-----------|----------|-------------------------------------------------------------------------|
| `welcome` | yes      | PRD: "Hi, thanks for calling! How may I help you today?"                |
| `error`   | MISSING  | PRD does not define a global `error` hook copy.                          |

> Challenge: "After how many failed attempts does it stop trying? What
> does the `error` hook say?"

## 11. Human escalation / handoff — [ANSWERED]

PRD §Happy Path "Human agent hand-off" enumerates escalation triggers:

- Fails to identify / verify caller
- Caller explicitly asks for a human
- Caller sounds angry / frustrated / urgent
- Intent is unclear or does not match existing subagents
- Existing case search fails after one retry
- Any place VA fails

Context that transfers: PRD names the OOTB "Conversation catch up"
feature, which surfaces a real-time AI-generated summary of the
conversation when the human joins.

## 12. Success metrics — [MISSING]

PRD §Objective talks qualitatively about reducing admin burden and
automating case creation but does NOT name a measurable metric, a
baseline, or a reporting surface. Logged as a P0 gap.

> Challenge: "What number moves if this agent works?"

## 13. v1 scope boundary + open spikes — [ANSWERED]

**In v1** (per PRD):

- Identification + verification (with spike on existing IDV flows)
- Intent extraction + sentiment
- Subagent routing to Claims / PriorAuth / Knowledge / Provider Network
- Case search + create + auto-close
- Wrap-up summary attached to Voice Call record
- Escalation to human
- Email send (marked Maybe / P1 in PRD)

**Out of v1** (per PRD §Happy Path strikethroughs + 264+ notes):

- Update member contact details subagent
- Caregiver / proxy caller HIPAA verification (264+)
- Complex case creation (Referral, Schedule appt., Grievance, PriorAuth)
- Spanish language
- Activity / Task creation
- Summary prompt template customisation (264+)

Open spikes: see Spike log below (S-01 through S-07).

---

# Conditional sections (rendered only when their trigger fires)

## Data sensitivity & masking posture — [PARTIAL]

Trigger fired: PRD describes PHI handling explicitly. Per
`references/invariants.md`, the agent must define masking posture before
the first LLM call. PRD says: "Verification: After identification, we
need to verify the caller before giving out any PHI data." PRD does NOT
specify the Einstein Trust Layer masking configuration, nor whether
PHI-adjacent generation requires custom prompt templates vs generic
summary. Logged as Q-04.

> Challenge: "What is the Trust Layer masking posture for the sanitized
> transcript fed to the intent and summary prompts? What custom prompt
> templates are required for PHI-adjacent generation?"

## Performance & latency tolerance — [MISSING]

Trigger fired: voice channel. PRD does not state acceptable latency,
concurrency, or availability targets.

> Challenge: "What is the maximum acceptable latency between caller
> utterance and agent response in voice mode?"

## Architecture: subagent design + GA status — [PARTIAL]

Trigger fired: 9 subagents + orchestration. PRD names individual
subagents and a high-level routing intent but does NOT identify the
routing approach (default subagent-description routing vs reasoning
instructions vs Script `if`/`else`), nor verify GA status of all named
subagents. Logged as S-04.

> Challenge: "Routing approach — descriptions, reasoning instructions,
> or Script? GA status of Claims, Prior Auth, Provider Network
> subagents?"

## Grounding — SA-6 — [PARTIAL]

Trigger fired: SA-6 archetype is MISSING but the PRD describes it as a
read-only Knowledge answerer (informational shape). Per PRD: "use
existing knowledge action Answer questions with knowledge." Which of the
four Data Library types (Knowledge / Uploaded Files / Web Search /
Custom Retriever) backs the subagent in v1 is MISSING.

> Challenge: "Is this grounded via Data Library, or actually executing a
> retrieval ACTION via Flow/Apex? Only the first is formal grounding."

## Confirmation / verification — SA-5 — [PARTIAL]

Trigger fired: SA-5 (case create) is irreversible (Case is created in
prod data). PRD describes confirmation gates loosely ("confirm the case
# with the user", "Confirm with caller before updating") but does not
enumerate per-action confirmation requirements.

> Challenge: "Which actions require user confirmation or identity
> verification first?"

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

| Spike ID | Owner role           | Priority | Rubric ref            | Question                                                                                  | Status |
|----------|----------------------|----------|------------------------|--------------------------------------------------------------------------------------------|--------|
| S-01     | Platform architect    | P0       | Row 7 / SA-1           | Evaluate existing Identity Verification flows for reuse vs custom action (PRD inline).      | open   |
| S-02     | Platform architect    | P1       | Row 6 / SA-2           | Engagement records (P2-TBD): data-model decision per PRD requirements section.              | open   |
| S-03     | Engineering lead      | P0       | Row 7 / SA-5           | Case search/create framework: SCV framework reuse vs custom (PRD Possible Spikes).          | open   |
| S-04     | Platform architect    | P0       | Row 5                  | Routing approach + GA status of existing subagents (Claims, Prior Auth, Provider Network).  | open   |
| S-05     | Engineering lead      | P1       | Conditional / SA-3     | Sentiment analysis OOTB feasibility: Voice + chat (PRD Possible Spikes).                    | open   |
| S-06     | Engineering lead      | P1       | Row 6 / SA-5           | Case wrap-up summary: SCV summary object vs custom prompt template (PRD Possible Spikes).    | open   |
| S-07     | Product owner         | P1       | Row 13                 | Send-email exploration: how to recommend extending the use case to also send email (PRD).    | open   |
