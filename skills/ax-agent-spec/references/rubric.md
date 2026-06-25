# ax-agent-spec — Rubric (v1.0, locked)

Two scopes: **agent-level** (once per agent) / **subagent-level** (per
subagent).

Three tiers: **P0 spine** (every agent, gate-blocking) / **conditional**
(trigger-unlocked) / **deferred** (recorded, designed in L2/L3).

**Seeding question** opens the interview ("Roughly, what does this agent
do, for whom, in what channel?") — orients only, gates nothing.

**Archetype tagging at row 5:** each subagent tagged
**transactional / informational / routing-orchestration**; the tag
unlocks that subagent's conditional rows only. A subagent that's
genuinely both is usually two subagents — challenge it.

---

## P0 spine (13 rows)

| # | Scope    | Requirement                                                    | "Answered" means                                                                                                                                                                              | Challenge question                                                                                                            |
|---|----------|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| 1 | Agent    | Goal + non-goals                                                | One sentence on the outcome produced and for whom, plus explicit list of what it won't do                                                                                                      | If it works perfectly, what changed for the user and the business? Name 3 things a user might expect that it won't do.        |
| 2 | Agent    | Primary user & their goal                                       | Who interacts (end customer / internal employee / both) and what they're trying to accomplish                                                                                                  | Is the agent acting FOR the user, or AS the user toward a third party?                                                         |
| 3 | Agent    | Trigger / entry point                                           | What initiates the agent (inbound call, chat, button, another agent)                                                                                                                            | What is true about the world the instant before the agent activates?                                                           |
| 4 | Agent    | Channel                                                         | Modality and surface; text is default unless stated. Read the matching `references/channels/` profile.                                                                                          | Does anything about this agent only make sense in one channel?                                                                 |
| 5 | Subagent | Subagent inventory + routing descriptions + archetype tags      | Each subagent named, with scope, a routing DESCRIPTION (this IS the routing config), archetype tag, and any deterministic routing conditions (reasoning instructions / Script `if`/`else`)     | Could two subagents both claim the same request? How does the Reasoning Engine decide?                                          |
| 6 | Subagent | Action inventory per subagent                                   | Every discrete action named and grouped under its subagent                                                                                                                                      | For each action, who or what actually performs it?                                                                              |
| 7 | Subagent | Execution mechanism & feasibility per action                    | How each action is implemented (`apex` / `flow` / `prompt` per primitives; or OOTB) and whether that mechanism EXISTS TODAY or is a spike                                                       | Which actions assume a capability that doesn't exist yet?                                                                       |
| 8 | Subagent | Data read/written + Variables Block                             | Objects/records read vs created/mutated, with direction; PLUS declared state in the three variable categories (`@variables.*`, linked `@Namespace.Property`, `@system_variables.*`)             | What does it change, and is that reversible? What state must survive across turns that you're assuming the LLM will just remember? |
| 9 | Agent    | Guardrails / must-nevers, with placement                        | Each constraint classified: `system: instructions` (global persona/compliance) / subagent-local / Script-enforced (deterministic). Per the "deterministic sandwich."                            | What's the worst thing it could do if it misunderstood? Which rules are deterministic enough for Script?                        |
| 10| Agent    | Failure & recovery + global messages                            | Behavior on action failure, unclear intent, low confidence (retry policy + fallback), AND the `system: messages` hooks defined (`welcome`, `error`)                                              | After how many failed attempts does it stop trying? What does the `error` hook say?                                             |
| 11| Agent    | Human escalation / handoff                                      | When and how it hands to a human, and what context transfers                                                                                                                                    | When the human picks up, what do they already see without re-asking?                                                            |
| 12| Agent    | Success metrics                                                 | How success is measured, at the level it will be reported                                                                                                                                       | What number moves if this agent works?                                                                                          |
| 13| Agent    | v1 scope boundary + open spikes                                 | Explicit in/out for first release; every unresolved item logged as numbered spike with proposed owner ROLE and P0/P1                                                                            | What's the smallest version still worth shipping?                                                                                |

---

## Conditional tier (trigger-unlocked)

| Trigger                                                          | Scope    | Requirement unlocked                                  | "Answered" means                                                                                                                                                                                                                                            |
|------------------------------------------------------------------|----------|--------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Touches regulated/sensitive data (PHI, PII, financial)            | Agent    | Data sensitivity & masking posture                     | Classification of sensitive data + masking/handling rule before any LLM call (HC: Trust Layer + custom prompt templates — see invariants)                                                                                                                    |
| Real-time / voice / high concurrency                              | Agent    | Performance & latency tolerance                        | Acceptable latency, concurrency, availability                                                                                                                                                                                                                |
| Multiple subagents or orchestration                               | Agent    | Architecture: subagent design + GA status              | Chosen routing approach (descriptions / reasoning instructions / Script) and GA-stability check against primitives                                                                                                                                            |
| Subagent tagged INFORMATIONAL                                     | Subagent | Grounding (P0 for that subagent)                        | Which of the four Data Library types grounds it (Knowledge / Uploaded Files / Web Search / Custom Retriever), and what it does when the source has no answer. **Challenge:** is this grounded via Data Library, or actually executing a retrieval ACTION via Flow/Apex? Only the first is formal grounding. |
| Subagent tagged TRANSACTIONAL with irreversible/regulated actions | Subagent | Confirmation / verification (P0 for that subagent)      | Which actions require user confirmation or identity verification first                                                                                                                                                                                       |

---

## Deferred tier

Recorded as named placeholders, never blank, never invented.

- **Golden path & decision-point design** → Layer 2 (Behavior Blueprint)
- **Persona / voice & tone detail** → Layer 2
- **Recovery flow CONVERSATION design** → Layer 2
- **Rendering, trust-signal UI, surface patterns** → Layer 3 (Interface)

Rendered e.g. "Golden path required — to be designed in Behavior Blueprint."
