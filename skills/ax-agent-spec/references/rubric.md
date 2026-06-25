# ax-agent-spec — Rubric (v1.0)

The Layer 1 spec rubric. Three tiers: **P0 spine** (13 rows, must be
addressed before downstream layers can build), **Conditional tier** (only
when its trigger fires), **Deferred tier** (placeholders rendered in every
spec, owned by Layer 2 or Layer 3).

Two scopes:

- **Agent-level** (rubric rows 1–7) — one set of answers per agent.
- **Subagent-level** (rubric rows 8–13) — one set of answers PER SUBAGENT.
  Each subagent is also tagged with an ARCHETYPE that gates which P0 rows
  apply to it.

Subagent archetypes (controlled vocabulary):

- **TRANSACTIONAL** — performs an action that changes state, books, writes,
  pays, schedules, dispatches.
- **INFORMATIONAL** — answers questions, surfaces records, summarizes,
  retrieves; does not write.
- **ROUTING-ORCHESTRATION** — interprets intent and hands off to other
  subagents; little to no direct user-facing output beyond confirmation.

Conditional P0 application:

- **Grounding (row 11) is P0 for INFORMATIONAL subagents.** Without it,
  the agent cannot answer truthfully; downstream cannot wire grounding
  sources.
- **Confirmation/verification (row 12) is P0 for TRANSACTIONAL subagents
  whose actions are IRREVERSIBLE or touch REGULATED data.** Without it,
  the agent can take unsafe action.
- Both rows still appear (and are filled) for all archetypes, but their
  **P0 vs P1 status** is set by archetype as above.

---

## P0 spine — 13 rows

### Agent-level (rows 1–7)

| # | Row                                            | Scope        | What it must answer                                                                                                                                                |
|---|------------------------------------------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Agent purpose & success criteria               | Agent        | What is this agent FOR? What outcome counts as success? What is the engineering-handoff consequence if absent? (PM-language framing.)                              |
| 2 | Users & personas in scope                      | Agent        | Who interacts with this agent? For Health Cloud: which of patient / payer / provider, and any sub-personas. Persona drives identity-verification posture.            |
| 3 | Channels in scope                              | Agent        | Text (CRM chat, enhanced web chat, embedded) / Voice / other. Default profile is text; additional channels are overlays.                                            |
| 4 | Scope boundaries                               | Agent        | What is explicitly IN scope. What is explicitly OUT of scope (referred elsewhere, deferred, blocked).                                                                |
| 5 | Data sensitivity & compliance posture          | Agent        | What regulated/sensitive data does the agent touch (PHI, PII, financial)? Einstein Trust Layer masking posture; custom-prompt-template requirement for PHI-adjacent generation. |
| 6 | Subagent inventory + archetype tag             | Agent        | Enumerate every subagent (SA-1, SA-2…). Tag each as TRANSACTIONAL / INFORMATIONAL / ROUTING-ORCHESTRATION. This drives row 11 / row 12 P0 conditionality.            |
| 7 | Agent-level instructions: tone, persona, guardrails, default escalation | Agent | Brand tone, persona constraints, hard refusal/escalation defaults that live in `system: instructions:` and `system: messages:`.                                     |

### Subagent-level (rows 8–13) — repeats once per subagent

| #  | Row                                             | Scope     | What it must answer (per subagent)                                                                                                                                                |
|----|-------------------------------------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 8  | Subagent scope & trigger                        | Subagent  | When is this subagent invoked? By LLM reasoning against its description, or by deterministic script condition (Agent Script `if`/`else`)? Boundaries vs sibling subagents.         |
| 9  | Inputs & required context                       | Subagent  | Regular variables required (`@variables.*`); linked-variable namespaces consumed (`@MessagingSession`, `@MessagingEndUser`, `@VoiceCall`, etc.); system variables relied on.        |
| 10 | Actions & mechanism                             | Subagent  | List of actions (SA-N.1, SA-N.2…) with `target` type: `apex` / `flow` / `prompt`. State irreversibility per action.                                                                |
| 11 | Grounding sources (P0 for INFORMATIONAL)        | Subagent  | Which Data Library type(s) ground this subagent's answers: Salesforce Knowledge / Uploaded Files / Web Search / Custom Retriever. Dynamic record queries are NOT grounding.        |
| 12 | Confirmation / verification gates (P0 for TRANSACTIONAL with irreversible OR regulated actions) | Subagent | Pre-action gates: identity verification, explicit user confirmation, double-check loop, dry-run summary. Names the gate even when the mechanism is deferred to Layer 2/3.         |
| 13 | Exit conditions & handoff/escalation            | Subagent  | When does this subagent end? Where does control go? Success exit, failure exit, escalation-to-human exit. Names the receiving subagent or human queue.                              |

---

## Conditional tier (only when triggered)

Each row below is dormant until its trigger fires. When triggered it
becomes a section in the generated spec and renders with the rubric's
challenge questions pre-printed.

| Row                                     | Trigger                                                                                       |
|-----------------------------------------|------------------------------------------------------------------------------------------------|
| Multi-channel parity                    | Row 3 lists more than one channel.                                                              |
| Voice-channel specifics                 | Row 3 includes Voice. Covers `@VoiceCall` linked-vars, turn pacing, verification loop pacing.   |
| Identity-verification flow              | Row 2 persona is patient / payer / provider AND any subagent in row 12 requires it before PHI. |
| Knowledge curation plan                 | Row 11 names Salesforce Knowledge for any subagent.                                             |
| Custom prompt-template plan             | Row 5 indicates PHI-adjacent generation (forces custom prompt templates, not generic).         |
| External Service / API action auth      | Row 10 references API / External Service actions for any subagent.                              |
| Routing-orchestration map               | Row 6 inventory has ≥2 subagents AND row 8 references deterministic routing for any of them.    |
| Multi-language support                  | Row 2 indicates non-English personas in scope.                                                  |

---

## Deferred tier (Layer 2 / Layer 3)

Always rendered as named placeholders in every spec; never blank, never
invented at Layer 1. Downstream skills own filling them in.

| Placeholder                                                 | Owner                            | Status tag      |
|-------------------------------------------------------------|----------------------------------|------------------|
| Six AX dimensions (Goal / Role-Boundaries / Golden path / Recovery / Handoff / Trust signals) | ax-behavior-blueprint (Layer 2) | DEFERRED-L2      |
| Four-way platform map (system: instructions / system: messages / subagent instructions / Agent Script) — traceability layer | ax-behavior-blueprint (Layer 2) | DEFERRED-L2      |
| Six failure-mode quality lint                               | ax-behavior-blueprint (Layer 2) | DEFERRED-L2      |
| Pattern selection + provenance for UI-bearing surfaces      | ax-agent-interface (Layer 3)     | DEFERRED-L3      |
| Pattern card adoption notes (which library standards adopted, by whom) | ax-agent-interface (Layer 3) | DEFERRED-L3      |

---

## Status vocabulary (per rubric row)

Per DESIGN.md and `references/invariants.md`. The skill emits ONE of:
**ANSWERED / PARTIAL / MISSING / SPIKE / DEFERRED-L2 / DEFERRED-L3**.
A row that depends on someone else becomes a numbered spike (S-01,
S-02…) with proposed owner ROLE and P0/P1 priority; the skill never
invents an answer.

## P0 gate behaviour

If any P0 row is MISSING at generation time (including row 11 for any
INFORMATIONAL subagent or row 12 for any TRANSACTIONAL subagent with
irreversible/regulated actions), the skill stops once, lists the missing
P0s and the downstream Layer 2/3 sections each degrades, and offers
"answer now" or "proceed with gaps." Proceeding records the row(s) in
the manifest's `p0_gaps` list. Warn once; never nag twice in a session.
