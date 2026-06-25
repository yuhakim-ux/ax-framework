# ax-agent-spec — Generated Spec Skeleton (v1.0)

This is the verbatim skeleton the skill renders. Placeholders are in
ALL-CAPS angle brackets (`<LIKE_THIS>`). The rendered output is plain
Markdown so it converts cleanly to a Google Doc: real headings, real
tables, no HTML, no YAML.

Inline status tags appear in section headers and MUST agree with the
manifest. The skill never leaves a heading without a status tag.

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

| Rubric row                                       | Scope     | Status | Notes / Spike refs |
|--------------------------------------------------|-----------|--------|---------------------|
| 1. Agent purpose & success criteria              | Agent     |        |                     |
| 2. Users & personas in scope                     | Agent     |        |                     |
| 3. Channels in scope                             | Agent     |        |                     |
| 4. Scope boundaries                              | Agent     |        |                     |
| 5. Data sensitivity & compliance posture         | Agent     |        |                     |
| 6. Subagent inventory + archetype tag            | Agent     |        |                     |
| 7. Agent-level instructions                      | Agent     |        |                     |
| 8. Subagent scope & trigger — SA-<N>             | Subagent  |        |                     |
| 9. Inputs & required context — SA-<N>            | Subagent  |        |                     |
| 10. Actions & mechanism — SA-<N>                 | Subagent  |        |                     |
| 11. Grounding sources — SA-<N> (P0 if INFORMATIONAL) | Subagent |    |                     |
| 12. Confirmation / verification — SA-<N> (P0 if TRANSACTIONAL + irreversible/regulated) | Subagent |  |  |
| 13. Exit conditions & handoff/escalation — SA-<N>| Subagent  |        |                     |

> Subagent rows 8–13 repeat once per subagent. SA-N IDs follow the 264
> pattern (SA-1, SA-2, …). Actions within a subagent are numbered N.1,
> N.2, …

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
> registry lookup, no matching, no promotion.

| Situation                          | Mechanism          | Subagent ref | Candidate-type                   | Note |
|------------------------------------|--------------------|--------------|-----------------------------------|------|
| <from situation-taxonomy.md>       | action/flow/prompt | <SA-N>       | would-match-seeded-standard / harvested | <NOTE> |

### Changelog

| Version | Date         | Author       | Summary |
|---------|--------------|--------------|---------|
| <X.Y>   | <YYYY-MM-DD> | <AUTHOR>     | <SUMMARY> |

---

## 1. Agent purpose & success criteria — [STATUS]

<content or — if MISSING — the rubric's challenge questions, pre-printed>

## 2. Users & personas in scope — [STATUS]

<content / challenges>

## 3. Channels in scope — [STATUS]

<content / challenges>

## 4. Scope boundaries — [STATUS]

In scope:

- <ITEM>

Out of scope:

- <ITEM>

## 5. Data sensitivity & compliance posture — [STATUS]

| Data category | Present? | Handling posture | Trust Layer masking | Custom prompt template required? |
|---------------|----------|------------------|---------------------|-----------------------------------|
| PHI           |          |                  |                     |                                   |
| PII           |          |                  |                     |                                   |
| Financial     |          |                  |                     |                                   |

## 6. Subagent inventory — [STATUS]

| ID    | Subagent name | Archetype                          | One-line purpose |
|-------|----------------|-------------------------------------|-------------------|
| SA-1  | <name>         | TRANSACTIONAL / INFORMATIONAL / ROUTING-ORCHESTRATION | <purpose> |
| SA-2  | <name>         |                                     |                   |

## 7. Agent-level instructions — [STATUS]

- **Tone & persona:** <content>
- **Hard guardrails (`system: instructions:`):** <content>
- **Global hooks (`system: messages:` — welcome / error):** <content>
- **Default escalation behaviour:** <content>

---

# Subagent: SA-1 — <NAME>  [archetype: <ARCHETYPE>]

## 8. Scope & trigger — [STATUS]

<content / challenges>

## 9. Inputs & required context — [STATUS]

| Variable kind          | Reference              | Source / Notes |
|------------------------|------------------------|----------------|
| Regular                | `@variables.<name>`    |                |
| Linked                 | `@<Namespace>.<Prop>`  |                |
| System                 | `@system_variables.<name>` |            |

## 10. Actions & mechanism — [STATUS]

| Action ID | Name      | Target type (`apex`/`flow`/`prompt`) | Irreversible? | Touches regulated data? | Notes |
|-----------|-----------|---------------------------------------|---------------|-------------------------|-------|
| 1.1       | <name>    |                                       |               |                         |       |
| 1.2       | <name>    |                                       |               |                         |       |

## 11. Grounding sources — [STATUS]
[P0 if SA-1 archetype = INFORMATIONAL]

| Data Library type      | Used? | Source ref | Notes |
|------------------------|-------|------------|-------|
| Salesforce Knowledge   |       |            |       |
| Uploaded Files         |       |            |       |
| Web Search             |       |            |       |
| Custom Retriever       |       |            |       |

> Dynamic record queries via Flow/Apex are ACTIONS (row 10), not grounding.

## 12. Confirmation / verification gates — [STATUS]
[P0 if SA-1 archetype = TRANSACTIONAL AND any row-10 action is irreversible OR touches regulated data]

| Gate                       | When it fires                                | Mechanism (Layer 2 may resolve) |
|----------------------------|----------------------------------------------|---------------------------------|
| Identity verification      |                                              |                                 |
| Explicit user confirmation |                                              |                                 |
| Dry-run / summary          |                                              |                                 |

## 13. Exit conditions & handoff/escalation — [STATUS]

| Exit kind  | Trigger                          | Goes to (subagent / human queue) |
|------------|----------------------------------|----------------------------------|
| Success    |                                  |                                  |
| Failure    |                                  |                                  |
| Escalation |                                  |                                  |

---

# Subagent: SA-2 — <NAME>  [archetype: <ARCHETYPE>]

<repeat sections 8–13 per subagent>

---

# Conditional sections (rendered only when triggered)

## Multi-channel parity — [STATUS or absent]
## Voice-channel specifics — [STATUS or absent]
## Identity-verification flow — [STATUS or absent]
## Knowledge curation plan — [STATUS or absent]
## Custom prompt-template plan — [STATUS or absent]
## External Service / API action auth — [STATUS or absent]
## Routing-orchestration map — [STATUS or absent]
## Multi-language support — [STATUS or absent]

> Each conditional section, when rendered, opens with the rubric's
> challenge questions pre-printed so the team can fill them manually in
> the Doc.

---

# Deferred placeholders (Layer 2 / Layer 3)

> Always rendered. Never blank. Never invented at Layer 1.

## Six AX dimensions — [DEFERRED-L2]
Goal / Role-Boundaries / Golden path / Recovery / Handoff / Trust signals
will be authored by ax-behavior-blueprint.

## Four-way platform map — [DEFERRED-L2]
Traceability layer mapping Layer 2 dimensions onto: `system: instructions:` /
`system: messages:` / subagent instructions / Agent Script. Authored by
ax-behavior-blueprint.

## Six failure-mode quality lint — [DEFERRED-L2]
Authored by ax-behavior-blueprint.

## Pattern selection + provenance (UI-bearing) — [DEFERRED-L3]
Authored by ax-agent-interface.

## Pattern card adoption notes — [DEFERRED-L3]
Authored by ax-agent-interface.

---

# Spike log

| Spike ID | Owner role        | Priority (P0/P1) | Rubric ref           | Question                  | Status                        |
|----------|-------------------|------------------|----------------------|---------------------------|-------------------------------|
| S-01     | <role>            | P0 / P1          | Row <N> / SA-<N>     | <question>                | open / answered / superseded  |
| S-02     | <role>            |                  |                      |                           |                               |
