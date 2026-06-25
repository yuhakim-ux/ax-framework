# ax-agent-spec — Generated Spec Skeleton (v1.0)

This is the verbatim skeleton the skill renders. Placeholders are in
ALL-CAPS angle brackets (`<LIKE_THIS>`). The rendered output is plain
Markdown so it converts cleanly to a Google Doc: real headings, real
tables, no HTML, no YAML.

Inline status tags appear in section headers and MUST agree with the
manifest. The skill never leaves a heading without a status tag.

The skill OPENS the interview with the seeding question — "Roughly, what
does this agent do, for whom, in what channel?" — which orients and gates
nothing.

---

# <AGENT_NAME> — Agent Spec

**Version:** <SPEC_VERSION>
**Date:** <YYYY-MM-DD>
**Authors:** <AUTHORS>
**Team:** <TEAM>
**Product Owner (owner_contact):** <PRODUCT_OWNER>
**Primitives version:** <PRIMITIVES_VERSION> (last_verified <YYYY-MM-DD>)

> Team and Product Owner are REQUIRED. They become the pattern provenance
> downstream (Layer 3 harvest, registry `team` partition, `owner_contact`
> on pattern cards). The skill refuses to generate a spec missing either.

---

## Completion manifest

### Rubric coverage

| Rubric row                                                                          | Scope     | Status | Notes / Spike refs |
|-------------------------------------------------------------------------------------|-----------|--------|---------------------|
| 1. Goal + non-goals                                                                 | Agent     |        |                     |
| 2. Primary user & their goal                                                        | Agent     |        |                     |
| 3. Trigger / entry point                                                            | Agent     |        |                     |
| 4. Channel                                                                          | Agent     |        |                     |
| 5. Subagent inventory + routing descriptions + archetype tags                       | Subagent  |        |                     |
| 6. Action inventory — SA-<N>                                                        | Subagent  |        |                     |
| 7. Execution mechanism & feasibility — SA-<N>                                       | Subagent  |        |                     |
| 8. Data read/written + Variables Block — SA-<N>                                     | Subagent  |        |                     |
| 9. Guardrails / must-nevers, with placement                                         | Agent     |        |                     |
| 10. Failure & recovery + global messages                                            | Agent     |        |                     |
| 11. Human escalation / handoff                                                      | Agent     |        |                     |
| 12. Success metrics                                                                 | Agent     |        |                     |
| 13. v1 scope boundary + open spikes                                                 | Agent     |        |                     |

> Subagent rows 6–8 repeat once per subagent (row 5 is the inventory
> table that names them). SA-N IDs follow the 264 pattern
> (SA-1, SA-2, …). Actions within a subagent are numbered N.1, N.2, …

### Source documents ingested

| Document                | Type        | Ingested on  | Notes               |
|-------------------------|-------------|--------------|----------------------|
| <DOC_TITLE>             | <PRD/DOC>   | <YYYY-MM-DD> | <NOTES>             |

### P0 gaps (recorded at P0 gate)

| Rubric row | Subagent ref | Downstream sections this degrades |
|------------|--------------|------------------------------------|
| <ROW>      | <SA-N>       | <L2/L3 sections>                   |

### Open questions awaiting user

| ID    | Question                          | Blocking? |
|-------|-----------------------------------|------------|
| Q-01  | <QUESTION>                        | <yes/no>   |

### Pattern candidates

> Flag list for Phase 3 harvest. Phase 1 fills this and stops — no
> registry lookup, no matching, no promotion. Vocabulary is fixed by
> `references/situation-taxonomy.md`.

| Situation                          | Mechanism          | Subagent ref | Candidate-type                   | Note |
|------------------------------------|--------------------|--------------|-----------------------------------|------|
| <from situation-taxonomy.md>       | action/flow/prompt | <SA-N>       | would-match-seeded-standard / harvested | <NOTE> |

### Changelog

| Version | Date         | Author       | Summary |
|---------|--------------|--------------|---------|
| <X.Y>   | <YYYY-MM-DD> | <AUTHOR>     | <SUMMARY> |

---

## Seeding context

> The seeding question is asked first and gates nothing. Its answer is
> recorded here in one or two sentences to orient every later section.

**"Roughly, what does this agent do, for whom, in what channel?"** —
<SEEDING_ANSWER>

---

## 1. Goal + non-goals — [STATUS]

<one-sentence outcome + for whom>

**Won't do (explicit non-goals):**

- <NON_GOAL_1>
- <NON_GOAL_2>
- <NON_GOAL_3>

> Challenge if MISSING: "If it works perfectly, what changed for the user
> and the business? Name 3 things a user might expect that it won't do."

## 2. Primary user & their goal — [STATUS]

<who interacts (end customer / internal employee / both) and what
they're trying to accomplish>

> Challenge if MISSING: "Is the agent acting FOR the user, or AS the
> user toward a third party?"

## 3. Trigger / entry point — [STATUS]

<what initiates the agent (inbound call, chat, button, another agent)>

> Challenge if MISSING: "What is true about the world the instant before
> the agent activates?"

## 4. Channel — [STATUS]

<modality and surface; text is default unless stated. Read the matching
references/channels/ profile.>

> Challenge if MISSING: "Does anything about this agent only make sense
> in one channel?"

---

## 5. Subagent inventory + routing — [STATUS]

| ID    | Subagent name | Archetype                                                    | Routing description (this IS the routing config) | Deterministic routing conditions (reasoning instructions / Script `if`/`else`) |
|-------|----------------|---------------------------------------------------------------|---------------------------------------------------|-------------------------------------------------------------------------------|
| SA-1  | <name>         | TRANSACTIONAL / INFORMATIONAL / ROUTING-ORCHESTRATION         |                                                   |                                                                                |
| SA-2  | <name>         |                                                               |                                                   |                                                                                |

> Archetype tag at this row unlocks that subagent's conditional rows.
> Challenge if MISSING: "Could two subagents both claim the same request?
> How does the Reasoning Engine decide?" If a subagent is genuinely both
> transactional and informational, it is usually two subagents — challenge.

---

# Subagent: SA-1 — <NAME>  [archetype: <ARCHETYPE>]

## 6. Action inventory — [STATUS]

| Action ID | Name      | One-line purpose |
|-----------|-----------|------------------|
| 1.1       | <name>    |                  |
| 1.2       | <name>    |                  |

> Challenge if MISSING: "For each action, who or what actually performs it?"

## 7. Execution mechanism & feasibility — [STATUS]

| Action ID | Mechanism (`apex` / `flow` / `prompt` / OOTB) | Exists today? | Spike (if not) |
|-----------|------------------------------------------------|---------------|-----------------|
| 1.1       |                                                | yes / no      | S-<NN>          |
| 1.2       |                                                |               |                 |

> **Mechanism cell rule:** if the source did not state a target type for
> an action, leave the Mechanism cell BLANK and mark the row's status
> SPIKE (with a spike ID). NEVER guess `apex` / `flow` / `prompt` /
> OOTB to fill the column.
>
> Challenge if MISSING: "Which actions assume a capability that doesn't
> exist yet?"

## 8. Data read/written + Variables Block — [STATUS]

**Records / objects read vs created/mutated:**

| Object / record    | Direction (read / create / mutate) | Reversible? |
|--------------------|-------------------------------------|-------------|
| <name>             |                                     |             |

**Declared state (Variables Block):**

| Variable kind          | Reference                  | Source / Notes |
|------------------------|----------------------------|----------------|
| Regular                | `@variables.<name>`        |                |
| Linked                 | `@<Namespace>.<Prop>`      |                |
| System                 | `@system_variables.<name>` |                |

> Challenge if MISSING: "What does it change, and is that reversible?
> What state must survive across turns that you're assuming the LLM
> will just remember?"

---

# Subagent: SA-2 — <NAME>  [archetype: <ARCHETYPE>]

<repeat sections 6–8 per subagent, with action IDs prefixed by SA index
(2.1, 2.2, …)>

---

## 9. Guardrails / must-nevers, with placement — [STATUS]

| Constraint | Placement (`system: instructions` / subagent-local / Script-enforced) | Rationale |
|------------|----------------------------------------------------------------------|-----------|
|            |                                                                      |           |

> Per the deterministic sandwich: global persona/compliance in
> `system: instructions`; workflow-specific in the subagent block;
> hard rules deterministic enough for Script live in Script.
> Challenge if MISSING: "What's the worst thing it could do if it
> misunderstood? Which rules are deterministic enough for Script?"

## 10. Failure & recovery + global messages — [STATUS]

**Retry / fallback policy:**

| Failure case        | Retry policy              | Fallback behaviour |
|---------------------|---------------------------|---------------------|
| Action failure      |                           |                     |
| Unclear intent      |                           |                     |
| Low confidence      |                           |                     |

**`system: messages` hooks:**

| Hook      | Defined? | Content |
|-----------|----------|---------|
| `welcome` |          |         |
| `error`   |          |         |

> Challenge if MISSING: "After how many failed attempts does it stop
> trying? What does the `error` hook say?"

## 11. Human escalation / handoff — [STATUS]

<when and how the agent hands to a human; what context transfers>

> Challenge if MISSING: "When the human picks up, what do they already
> see without re-asking?"

## 12. Success metrics — [STATUS]

| Metric | How measured | Where reported |
|--------|--------------|-----------------|
|        |              |                 |

> Challenge if MISSING: "What number moves if this agent works?"

## 13. v1 scope boundary + open spikes — [STATUS]

**In v1:**

- <ITEM>

**Out of v1:**

- <ITEM>

> Challenge if MISSING: "What's the smallest version still worth shipping?"

Open spikes are logged in the Spike log below.

---

# Conditional sections (rendered only when their trigger fires)

## Data sensitivity & masking posture — [STATUS or absent]
> Trigger: agent touches regulated/sensitive data (PHI, PII, financial).
> Classification of sensitive data + masking/handling rule before any
> LLM call (HC: Trust Layer + custom prompt templates — see
> `references/invariants.md`).

## Performance & latency tolerance — [STATUS or absent]
> Trigger: real-time / voice / high concurrency. Acceptable latency,
> concurrency, availability.

## Architecture: subagent design + GA status — [STATUS or absent]
> Trigger: multiple subagents or orchestration. Chosen routing approach
> (descriptions / reasoning instructions / Script) and GA-stability check
> against `references/agentforce-primitives.md`.

## Grounding — SA-<N> — [STATUS or absent]
> Trigger: subagent tagged INFORMATIONAL (P0 for that subagent).
> Which of the four Data Library types grounds it (Knowledge / Uploaded
> Files / Web Search / Custom Retriever), and what it does when the
> source has no answer.
> **Challenge:** is this grounded via Data Library, or actually executing
> a retrieval ACTION via Flow/Apex? Only the first is formal grounding.

## Confirmation / verification — SA-<N> — [STATUS or absent]
> Trigger: subagent tagged TRANSACTIONAL with irreversible/regulated
> actions (P0 for that subagent). Which actions require user
> confirmation or identity verification first.

---

# Deferred placeholders

> Always rendered. Never blank. Never invented at Layer 1.

## Golden path & decision-point design — [DEFERRED-L2]
Golden path required — to be designed in Behavior Blueprint.

## Persona / voice & tone detail — [DEFERRED-L2]
Persona detail required — to be designed in Behavior Blueprint.

## Recovery flow CONVERSATION design — [DEFERRED-L2]
Recovery flow conversation required — to be designed in Behavior Blueprint.

## Rendering, trust-signal UI, surface patterns — [DEFERRED-L3]
Rendering, trust-signal UI, and surface patterns required — to be
designed in the Interface layer.

---

# Spike log

| Spike ID | Owner role        | Priority (P0/P1) | Rubric ref           | Question                  | Status                        |
|----------|-------------------|------------------|----------------------|---------------------------|-------------------------------|
| S-01     | <role>            | P0 / P1          | Row <N> / SA-<N>     | <question>                | open / answered / superseded  |
| S-02     | <role>            |                  |                      |                           |                               |
