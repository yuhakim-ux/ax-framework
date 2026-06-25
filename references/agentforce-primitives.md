# Agentforce Primitives

```
version:           1.0
last_verified:     2026-06-24
steward:           Yuha Kim
platform_release: Summer '26 (264)
```

**Staleness rule.** Skills consuming this file MUST warn in their output if
`last_verified` is older than 120 days OR if the user indicates a newer
platform release than `platform_release`. The warning names the stale date
and points the user at the steward.

**Verification status.** Facts below are recorded as supplied by the
steward (June 2026). Where a live Salesforce documentation page has been
fetched and quoted, the URL is cited inline. Where the live doc could not
be retrieved at verification time, the fact carries
`[steward-provided, link pending]`. NO claim in this file derives from
model background knowledge of Agentforce; everything is either steward-
authored or pulled from the cited URL.

If live docs CONTRADICT a steward fact, the fact is preserved with a
`[CONFLICT — steward review needed]` flag and both versions side by side
(none observed during the v1.0 pass).

---

## Terminology

- **"Topics" → SUBAGENTS, April 2026; no functionality change.** Docs are
  mid-transition and mix terms.
  > "Beginning in April 2026, agent **topics** are now called **subagents**.
  > There are no changes to functionality."
  > "During this transition, you may see a mix of the new and previous terms
  > in our documentation."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html
- **New Agentforce Builder, GA February 2026,** replacing the legacy
  Setup → Agents builder. All anatomy below refers to the new builder.
  [steward-provided, link pending]

---

## Agent Script architecture (the control plane)

Agent Script has absorbed legacy agent-level configuration. Hierarchy:

- **`system: instructions:`** — the agent-level surface. Foundational
  guardrails, compliance rules, core persona constraints, brand tone.
  > "The system block contains general instructions for the agent."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-blocks.html
- **`system: messages:`** — mandatory global conversational hooks.
  `welcome` and `error` are required.
  > "`welcome` and `error` are required messages"
  > "This information includes a list of message prompts that the agent
  > uses during specific scenarios."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-blocks.html
- **Subagent blocks** (formerly topic blocks) — localized, task-specific
  instructions and scope.
  > "Use the subagent block to specify the instructions, logic, and actions
  > for a subagent."
  > "A subagent block contains a description, a list of actions, and the
  > reasoning instructions."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-blocks.html

**Deterministic-sandwich best practice.** Universal tone and strict
boundaries live in the system block; workflow-specific guardrails live in
individual subagents; Agent Script expressions handle hard routing logic
between them. The phrase "deterministic sandwich" is steward shorthand;
the underlying mechanics are documented:
  > "Specific areas where the agent must execute deterministically."
  > "you can specify conditional logic (after the `->`) alongside LLM
  > prompts (after the `|`)"
  > "you can deterministically transition to a new subagent. Or you can
  > expose a subagent transition to the LLM as a tool"
  — https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html

**Guidance split.** Script for CONTROL (mandatory sequences, calculations,
sensitive business rules); instructions for BEHAVIOR (tone, persona,
conversational guidance). [steward-provided, link pending]

---

## Routing (multi-agent / subagent orchestration)

- **Default routing** relies on connected subagents' DESCRIPTIONS, editable
  in the Builder ("how and when to leverage this agent").
  [steward-provided, link pending]
- **Reasoning instructions** — deterministic invocation based on runtime
  conditions.
  > "reasoning.instructions: This property contains guidance for the
  > reasoning engine"
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-blocks.html
- **Script `if`/`else`** can change reasoning behavior (e.g., invoke a
  specific agent if a runtime condition is met).
  > "In reasoning actions, you can reference a subagent directly with
  > `@subagent.<topic_name>` or through a declarative transition"
  > "Use `available when` to define the conditions that must exist for the
  > LLM to use the tool."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-tools.html

---

## Variables

Consolidated. Replaces legacy `$Context.*` and split conversation
variables. Declared globally in a structured `variables:` block.
  > "The variables block contains the list of global variables that the
  > agent and script can use."
  > "You reference variables throughout the script by using the syntax
  > `@variables.<variable_name>`."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-blocks.html

Three categories:

- **Regular variables — `@variables.variable_name`.** Developer-defined
  primitives (string, boolean, object, list). Maintain state across turns
  without relying on LLM memory.
  > "regular variable: You can initialize a variable with a default value,
  > and the agent can change the variable's value."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-variables.html
- **Linked variables — `@Namespace.Property`.** Channel context mapped
  from the underlying channel (e.g., `@VoiceCall.Id`). Replaces legacy
  context variables. Documented source namespaces include
  `@MessagingSession`, `@MessagingEndUser`, and `@VoiceCall`.
  > "A linked variable's value is tied to a source, such as an action's
  > output."
  > "The `source` field references where the variable gets its value."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-variables.html
- **System variables — `@system_variables.user_input` etc.** Predefined,
  read-only, platform-populated.
  > "To access system variables, use `@system_variables.<variable_name>`."
  > "read-only, so you can't change its value"
  > "predefined, so you don't define it in the `variables` block"
  > "Currently, `@system_variables.user_input` is the only system variable."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-variables.html

**Reference forms.** `@variables` pointers in script logic; merge fields
`{!@variables.variable_name}` inside natural-language prompts.
  > "To reference a variable from within reasoning instructions, use
  > `{!@variables.<variable_name>}`."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-variables.html

---

## Grounding (Agentforce Data Library — the four sanctioned types)

[steward-provided, link pending — the live Data Library help page did not
load at verification time; revisit at next refresh.]

- **Salesforce Knowledge** — semantic indexing of native articles,
  auto-syncs on publish.
- **Uploaded Files** — `.pdf`, `.csv`, `.md`, `.txt` static resources.
- **Web Search** — designated external URLs.
- **Custom Retriever** — enterprise RAG: Data Cloud via Einstein Studio;
  Search Indexes and Data Model Objects with field-level filtering.

**CRITICAL DISTINCTION.** Dynamic record queries via Flow or Apex are
ACTIONS, not grounding. Formal non-hallucinatory LLM grounding is
EXCLUSIVELY the four Data Library types above.
[steward-provided, link pending]

---

## Action execution mechanisms

Verified action categories (Apex-family) from the live docs:

- **Apex REST Actions** — "Create actions from Apex REST classes."
- **AuraEnabled Actions** — "Create actions from Apex controller methods."
- **Named Query Actions** — "Create custom SOQL queries and expose them as
  actions."
- **Apex Invocable Method Actions** — "Create custom actions using Apex
  InvocableMethod."
  — https://developer.salesforce.com/docs/ai/agentforce/guide/get-started-actions.html

Additional steward-asserted categories not surfaced on the page above:

- **Flow actions** [steward-provided, link pending]
- **Prompt Template actions** [steward-provided, link pending]
- **API / External Service actions** (beyond Apex REST)
  [steward-provided, link pending]
- **OOTB standard actions** [steward-provided, link pending]

In Agent Script, actions are wired into subagents via the `reasoning.actions`
and `subagent.actions` blocks:
  > "Tools are executable functions that the LLM can choose to call, based
  > on the tool's description and the current context."
  > "You define tools in the subagent's `reasoning.actions` block. Tools can
  > be actions or other utilities."
  > "Subagent actions (`subagent.actions`) — Available to you from
  > logic-based reasoning instructions"
  > "Reasoning actions (`subagent.reasoning.actions`) — Available to the LLM
  > to call as needed, and can be referenced in your prompt-based
  > instructions"
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-tools.html

---

## Channels

Agent Script is fully GA across channels with native parity, INCLUDING
Agentforce Voice. Voice exposes the `@VoiceCall` namespace for linked
variables. Scripts have deterministic control over call routing,
verification loops, and action chaining before the LLM's vocal synthesis
turn. No text-first fallback caveats needed.

- `@VoiceCall` as a linked-variable namespace is documented in the
  Variables reference (see Variables section above).
  — https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-variables.html
- Channel parity / voice GA claim itself: [steward-provided, link pending]

---

## Known unknowns

The following could not be verified against live Salesforce docs during
the v1.0 pass and remain steward-asserted. Next refresh should chase these:

1. **New Agentforce Builder GA date (February 2026)** and the explicit
   claim that it replaces the legacy Setup → Agents builder. No GA notice
   was retrievable; the Help article URL returned a loading error.
2. **Agentforce Data Library — the four sanctioned grounding types** and
   the "dynamic record queries via Flow/Apex are ACTIONS, not grounding"
   distinction. The Data Library help page did not load.
3. **Default routing relies on connected subagents' DESCRIPTIONS** —
   editable copy in the Builder ("how and when to leverage this agent").
4. **Guidance split** (Script = CONTROL, instructions = BEHAVIOR) as
   stated. Implied by retrievable docs but not directly quoted.
5. **Action mechanisms beyond Apex-family** — Flow, Prompt Template,
   External Service, OOTB standard actions. The `get-started-actions.html`
   page surfaced only the four Apex-family categories above; the full list
   is likely on `ascript-ref-actions.html` (linked but not fetched in this
   pass).
6. **Channel parity claim and voice GA status.** The Voice channel page
   returned 404 on the guessed URL; canonical path is unknown.
7. **Exact term "deterministic sandwich."** Documented mechanics support
   the pattern; the phrase itself is steward shorthand.
