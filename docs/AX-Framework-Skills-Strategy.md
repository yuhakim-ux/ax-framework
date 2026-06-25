# AX Framework Skills — Strategy & PRD

**Owner:** Yuha Kim (UX, Health Cloud Design, Salesforce)
**Sponsor:** Design VP, Health Cloud
**Status:** Strategy locked; Phase 1 in build
**Last updated:** June 24, 2026

> **Source of truth.** `DESIGN.md` (at the repo root) is the
> authoritative in-repo decision record. This strategy doc is the
> narrative companion — broader context, audience, and rationale for
> leadership / external-agent reading. **If the two diverge, DESIGN.md
> wins.** Update DESIGN.md first; sync this doc to match.

---

## 1. Purpose

The Design VP of Health Cloud has asked Yuha to turn her AX (Agentic Experience) Design Framework — already used across multiple Health Cloud agent projects — into a suite of **Claude Skills** so that PMs and designers across Health Cloud can adopt it as a standardized practice.

The goal is not a document generator. The goal is to **standardize how Health Cloud teams define, design, and evaluate agent experiences**, and to do it in a way that stays correct against a fast-moving platform (Agentforce) and accumulates reusable knowledge over time. Success is measured by **adoption** (teams actually use it) and **consistency** (the artifacts it produces meet a shared definition of done).

This document is the canonical strategy record. It is written to be ingested by another agent (e.g. in Claude Code) and to be read by leadership.

---

## 2. Background: the AX Framework

The AX Framework is a three-phase system — **Define → Design → Develop** — that carries design intent continuously from a PM's requirements through behavior design into build and simulation, so intent survives the handoff to engineering. It has three layers, each producing one artifact:

1. **Layer 1 — Agent Spec** (the agent's PRD): the agent template, subagents, actions, variables, data, and feasibility constraints.
2. **Layer 2 — Agent Behavior Blueprint**: the agent's goal, role/boundaries, golden path, recovery, handoff, and trust signals — the foundation for agent instructions.
3. **Layer 3 — Agent Interface / Pattern Library**: consistent rendering and interaction patterns, evolving into Health Cloud Design's core agentic pattern library.

**AX Framework Lite** is the compact teaching/enforcement core:

- **Six dimensions** (the Behavior Blueprint spine): Goal · Role/Boundaries · Golden path · Recovery · Handoff · Trust signals. *(Open: confirm whether Role and Boundaries are one dimension or two.)*
- **Six failure modes** (the quality lint): wrong golden-path order · acting without confirming · no fallback · assumption without intent-gathering · personality masking capability gaps · late/missing escalation.

All of this targets **Salesforce Agentforce agents**. Every output must be aligned with current Agentforce reality, never the model's stale background knowledge.

---

## 3. Architecture overview

### 3.1 A suite of three skills sharing one foundation

```
ax-framework/                      (one repo, ONE version across the suite)
├── DESIGN.md                      (the decision record; every session reads this first)
├── references/                    (SHARED foundation — the anti-duplication layer)
│   ├── agentforce-primitives.md   (curated, versioned platform truth)
│   ├── invariants.md              (hard rules every skill enforces)
│   ├── pattern-registry.md        (the cross-cutting lookup contract)
│   ├── channels/                  (text.md = default; voice/slack/embedded added later)
│   └── templates/
├── skills/
│   ├── ax-agent-spec/             (Layer 1)
│   ├── ax-behavior-blueprint/     (Layer 2)
│   └── ax-agent-interface/        (Layer 3)
├── eval/golden/                   (264 ground truth)
└── docs/                          (definition-of-done, publishing, phase notes)
```

The three skills are separated because they have different triggers, audiences, and artifacts. They share a `references/` layer so the platform grounding is written once, not three times. **One version number** spans the suite, because the skills share references and independent versioning would create incompatibility for no benefit.

### 3.2 Platform grounding philosophy (the make-or-break constraint)

Agentforce moves fast enough that the model's background knowledge is a liability. (Proof: "Topics" were renamed "subagents" in April 2026; a designer prompting Claude cold would emit invalidated artifacts.) Therefore:

1. **No skill relies on model memory for platform facts.** Every platform claim traces to `agentforce-primitives.md` — curated, versioned, steward-reviewed truth.
2. **Terminology translation rule:** the current term is **subagent**. Source documents may say "topic"; translate on intake; never emit "topic" in generated artifacts.
3. **Every generated artifact stamps the primitives version** it was built against, and skills warn when the primitives file looks stale.

### 3.3 Current Agentforce platform facts (primitives v1 content)

- **New Agentforce Builder** is GA (Feb 2026), replacing the legacy Setup → Agents builder. All anatomy below refers to the new Builder.
- **Agent Script** is the control plane and has absorbed legacy agent-level configuration:
  - `system: instructions:` — the agent-level surface: foundational guardrails, compliance, core persona, brand tone.
  - `system: messages:` — mandatory global hooks including `welcome:` and `error:`.
  - `subagent` blocks (formerly topic blocks) — localized, task-specific instructions and scope.
  - Best practice "deterministic sandwich": universal tone/boundaries in `system`, workflow-specific guardrails per subagent, Agent Script expressions for hard routing. Use **Script for control**, **instructions for behavior**.
- **Routing** (subagent orchestration): default routing by subagent **descriptions**; **reasoning instructions** for deterministic invocation on runtime conditions; **Script if/else** to change reasoning behavior.
- **Variables**, declared globally in a `variables:` block, three categories: regular `@variables.name` (developer-defined state across turns), linked `@Namespace.Property` (channel context, e.g. `@VoiceCall.Id`), system `@system_variables.*` (read-only, platform-populated). Referenced via `@variables` pointers or `{!@variables.name}` merge fields.
- **Grounding** = the four **Agentforce Data Library** types: Salesforce Knowledge, Uploaded Files, Web Search, Custom Retriever (Data Cloud via Einstein Studio: Search Indexes + DMOs with field filtering). **Critical:** dynamic record queries via Flow/Apex are *actions*, not grounding; formal non-hallucinatory grounding is exclusively the four Data Library types.
- **Channels:** Agent Script is fully GA across channels with native parity, **including Agentforce Voice** (`@VoiceCall` namespace; deterministic control over routing, verification, action chaining before vocal synthesis). No text-first fallback caveat needed.

### 3.4 Invariants (hard rules every skill enforces)

1. Never rely on model memory for platform claims; cite primitives.
2. Terminology translation (subagent, never topic).
3. Spike discipline: never invent answers; log unknowns as numbered spikes with owner role + priority.
4. Version-stamp every artifact with the primitives version.
5. Sensitive-data rule: any agent touching regulated/sensitive data (PHI, PII, financial) must define its masking/handling posture before any LLM call. In Health Cloud: Einstein Trust Layer masking is mandatory, and PHI-adjacent generation requires custom prompt templates, not generic summaries. *(These invariants define the WHAT; Layer 3 seeded-standard patterns provide the reusable HOW.)*
6. Staleness warning per the primitives header (warn if `last_verified` > 120 days or the user signals a newer release).

---

## 4. Layer 1 — `ax-agent-spec`

### 4.1 Purpose and audience

Layer 1 turns requirements into a buildable Agent Spec. The **primary audience is PMs** — defining the PRD/spec is their job, and current agent PRDs are weak. Designers are co-collaborators who run or review it. The skill's value is not formatting; it is **encoding what an agent PRD must answer before a spec is buildable, and refusing to paper over gaps**. Its voice aggressively challenges in PM language (framing every gap as an engineering-handoff consequence: "without this, the agent cannot be built"), but it triages so it never holds the artifact hostage.

### 4.2 The rubric (the skill's brain)

Two scopes — **agent-level** rows (once per agent) and **subagent-level** rows (per subagent) — across three tiers: **P0 spine** (every agent, gate-blocking), **conditional** (unlocked by a trigger attribute), and **deferred** (recorded here, designed in Layer 2/3).

**P0 spine (13 rows):**

| # | Scope | Requirement | "Answered" means |
|---|-------|-------------|------------------|
| 1 | Agent | Goal + non-goals | Outcome produced and for whom; explicit list of what it won't do |
| 2 | Agent | Primary user & their goal | Who interacts (customer/employee/both) and what they want |
| 3 | Agent | Trigger / entry point | What initiates the agent |
| 4 | Agent | Channel | Modality + surface; text default; read the matching channel profile |
| 5 | Subagent | Subagent inventory + routing descriptions + archetype tags | Each subagent: scope, routing description (= the routing config), archetype tag, deterministic routing conditions |
| 6 | Subagent | Action inventory per subagent | Every discrete action, named, grouped under its subagent |
| 7 | Subagent | Execution mechanism & feasibility per action | How each action is implemented (Flow/Apex/Prompt Template/API/OOTB) and whether it exists today or is a spike |
| 8 | Subagent | Data read/written + Variables Block | Objects read vs created/mutated, with direction; declared state in the three variable categories |
| 9 | Agent | Guardrails / must-nevers, with placement | Each constraint classified: system instructions / subagent-local / Script-enforced |
| 10 | Agent | Failure & recovery + global messages | Retry/fallback behavior; `system: messages` hooks (welcome/error) |
| 11 | Agent | Human escalation / handoff | When/how it hands to a human; what context transfers |
| 12 | Agent | Success metrics | How success is measured, at the level it's reported |
| 13 | Agent | v1 scope boundary + open spikes | Explicit in/out; every unresolved item a numbered spike with owner role + priority |

**Archetype tagging:** during subagent inventory (row 5), each subagent is tagged **transactional / informational / routing-orchestration**. Tags unlock conditional rows for that subagent only — this dissolves the "an agent is often both transactional and informational" problem by locating archetype at the subagent level, where it actually lives. A subagent that is genuinely both is usually two subagents, and the skill challenges that.

**Conditional tier (unlocked by a trigger):**

| Trigger | Scope | Requirement |
|---------|-------|-------------|
| Touches regulated/sensitive data | Agent | Data sensitivity & masking posture (Trust Layer + custom prompt templates in HC) |
| Real-time / voice / high concurrency | Agent | Performance & latency tolerance |
| Multiple subagents / orchestration | Agent | Architecture: routing approach + GA-stability check |
| Subagent tagged informational | Subagent | **Grounding (P0 for that subagent):** which Data Library type, and what it does when the source has no answer |
| Subagent tagged transactional w/ irreversible actions | Subagent | **Confirmation/verification (P0 for that subagent):** which actions require confirm or identity verification first |

**Deferred tier:** golden path & decision-point design and persona/voice → Layer 2; recovery flow conversation design → Layer 2; rendering, trust-signal UI, surface patterns → Layer 3. Rendered as named placeholders ("Golden path required — to be designed in Behavior Blueprint"), never blank, never invented.

### 4.3 Output architecture

- The skill generates **canonical Markdown** internally, renders it into a **formatted document** matching the team's existing agent-spec style, and pushes it to the user's connected **Google Drive as a Google Doc**.
- **The Google Doc is the working SSOT.** Teams fill gaps manually in the Doc. On re-entry, the skill reads the latest Doc back, parses the manifest + section statuses, treats human-filled sections as answers (reconcile, never overwrite), flags contradictions, and generates the next version.
- **Versioning is regenerate-not-edit:** one new Doc per version, `<agent>-spec-vX.Y`, in a per-agent Drive folder; changelog inside the doc.
- **Graceful degradation:** if Drive is unavailable, save `.md` + `.docx` locally and say so. Markdown-only when explicitly requested.

### 4.4 Completeness model

- **Status vocabulary per rubric row:** ANSWERED / PARTIAL / MISSING / SPIKE / DEFERRED-L2 / DEFERRED-L3.
- **Every generated spec contains all 13 sections** regardless of status. Unanswered sections render with their status tag and the rubric's challenge questions pre-printed, so teams can fill them manually.
- **Completion manifest:** a human-readable table at the top of every spec (not YAML — must survive Google Doc format and be parseable on read-back). Records: coverage per row; per-subagent archetype tags + conditional status; source documents ingested; primitives version; open questions awaiting the user; `p0_gaps`; changelog; and a **Pattern candidates** table (see 6.3).
- **Spike discipline:** when an answer requires someone else, log a numbered spike (S-01…) with proposed owner role and P0/P1. Never invent.
- **P0 gate:** at generation, if any P0 row is MISSING, stop and present **one** decision point — list the missing P0s, state which downstream Layer 2/3 sections each degrades, offer *answer now* or *proceed with gaps*. If proceeding, record `p0_gaps`. Downstream skills read the manifest and refuse to silently build on a gapped foundation. Warn once; never nag twice in a session.

### 4.5 Title block

Carries agent name, version, date, authors, **team, product owner (owner_contact)**, and primitives version. Team and product owner are required because they become pattern provenance downstream (Layer 3).

---

## 5. Layer 2 — `ax-behavior-blueprint`

### 5.1 Purpose

Translates a Layer 1 spec into clear agent behavior, and is the foundation for agent instructions. It is separated from Layer 1 because behavior design (golden path, trust signals) is reasoning PMs won't write and shouldn't be buried in a technical spec — but the two are kept **traceable** to prevent drift.

### 5.2 The six-dimension spine

The blueprint interviews across the six AX dimensions: **Goal · Role/Boundaries · Golden path · Recovery · Handoff · Trust signals.** These are the *what* the blueprint captures.

### 5.3 Four-way platform traceability (the *where*)

After the six dimensions are designed, every behavior decision is classified onto its Agentforce platform surface:

| Surface | Holds |
|---------|-------|
| `system: instructions` | Global persona, compliance, brand tone, universal guardrails |
| `system: messages` | Global hooks: welcome, error |
| subagent instructions | Localized, task-specific behavior |
| Agent Script | Deterministic control: mandatory sequences, routing if/else, sensitive business rules |

This is a traceability layer applied **after** the six dimensions, not a substitute for them. It is the platform's own structure (Script for control, instructions for behavior), so the blueprint output is directly implementable.

### 5.4 Quality lint and round-trip

- The **six failure modes** are the blueprint's quality lint.
- **Round-trip:** Spec v0 (structure) → Blueprint (behavior) → Spec v1 (instruction-related sections populated from the blueprint). The blueprint reads the spec manifest on intake and blocks on unresolved P0 gaps rather than inventing content.

---

## 6. Layer 3 — `ax-agent-interface` (team agent pattern ecosystem)

### 6.1 What it is

Layer 3 is **not** UI-only. It is a system for **interaction/behavioral patterns** — capturing the invisible agent behavior system as a reusable, shareable, evolving library. Platform-native base patterns (human-in-the-loop, fallback, escalation, confirmation, disambiguation) are *referenced*, never re-documented; the captured value is **team/domain specializations on top of them** (e.g. "confirmation before creating a Case in a payer contact center, showing fields X").

The agent is a **librarian/matchmaker, never the authority on fit.** It provides a reference, not a verdict. Adoption decisions always route back to the owning team. The purpose is to stop PMs and designers from hunting for prior art and reinventing patterns each release.

### 6.2 Two population mechanisms

1. **Top-down seeded standards** — domain-mandatory patterns that must be right from the start (HIPAA disclosure; persona-specific identity verification for Patient / Payer / Provider). Authority-owned, authoritative; skills proactively enforce/suggest them when the situation arises.
2. **Bottom-up harvest** — ambient capture during design work. The agent offers to add a pattern **only when it recurs across 2+ agents OR a human validates it as standard.** Seen-once = flagged candidate only, no offer. This mirrors the principle: *flag extractable patterns, don't extract prematurely; revisit when a second data point exists.* It also solves cold-start and over-offering.

### 6.3 Capture is cross-layer; registration is Layer 3

Capture hooks live in Layers 1 and 2 too, but there they **only tag candidates** in the manifest (situation + mechanism + team provenance) against the shared situation taxonomy. Registration, promotion, and curation are owned by Layer 3. In Phase 1, candidate tagging is **capture-only** — no registry, no matching, no lookup, no reuse suggestions.

### 6.4 Situation taxonomy (the matching key)

A controlled vocabulary so "similar pattern" matching works: the six failure modes + the platform base patterns + domain situations (sensitive-data-disclosure, identity-verification with persona variants, irreversible-action-confirmation). This is the shared key the registry matches against.

### 6.5 Pattern card and registry entry

Each registry entry / pattern card carries: **team, release, agent, situation, mechanism (action/flow/prompt), owner_contact (product owner), last_validated_release, visibility**, plus a short "what/when" summary and a **type tag**:

- `seeded-standard` — owner_contact is the domain/compliance authority; the agent says "this is the HC standard; apply the variant matching your case."
- `harvested` — owner_contact is the team that built it; the agent says "Team X did this in release Y; here's the relevancy; confirm details with that team."

We store **interaction metadata, not code.** Implementation stays a pointer to the owning team.

### 6.6 Lookup is cross-cutting (available from all three skills)

A PM working in Layer 1 can ask "has anyone in Health Cloud done something like this?" and the agent searches the registry and returns pattern cards. The lookup flow (query → relevancy → pattern card → handoff) lives in a shared reference `references/pattern-registry.md`; each skill's SKILL.md points to it in one line. **No fourth skill.**

- **Hard rule:** every pattern shown carries provenance + owner_contact + an explicit "confirm with the owning team before adopting" recommendation.
- **Relevancy rules:** (1) surface **differences**, not just similarity ("they were Payer, you're Provider, so verification fields differ"); (2) state explicitly what cannot be verified. Relevancy is a starting hypothesis, not a judgment — which is exactly what makes the handoff mandatory. A confidently-wrong relevancy claim is the worst failure, and these two rules are the defense.

### 6.7 Team-scoping and visibility

The skill suite is shared **org-wide** (all Salesforce teams), but the **library is partitioned per team.** `team` is a first-class attribute on every pattern and candidate tag. The skill operates "as" a team via a one-time `team-config` (team name + library location + the team's domain authority contact).

Registry partitions: **seeded-standards** (authority-owned, domain/org visible) and **`<team>`** partitions (team-owned harvested patterns).

**Visibility gates cross-team exposure:**

- `team` (**default**) — visible within the owning team. The core cross-pollination vision (one HC designer finding another HC team's pattern) is satisfied here, because that vision is intra-Health-Cloud.
- `org` (**opt-in**) — discoverable by other Salesforce teams via cross-team lookup; promotion is a deliberate, curator-gated step.

Conservative default (`team`, not `org`) because auto-exposing healthcare patterns org-wide without review is a compliance risk. Seeded-standards are domain/org-visible by nature.

### 6.8 Registry vs Storybook

`patterns.json` is the canonical SSOT covering **all** patterns (behavioral + UI). **Storybook is the rendering view for the UI-bearing subset only.** Purely behavioral patterns live in the registry with no Storybook entry. A standalone browse view (outside a build session) shares the same team-scoped registry + visibility model.

---

## 7. User flows (step by step)

### 7.1 Layer 1 — first run (PM with a weak PRD)

1. PM says "turn this PRD into an agent spec" (or similar); the skill triggers.
2. Skill reads primitives, checks staleness, asks the seeding question (what / for whom / what channel), reads the channel profile, and notes the team (or asks team + product owner once).
3. **Intake:** checks context for the PRD; if absent, asks once with the acceptable-inputs list.
4. **Audit:** parses the PRD against the rubric; posts a challenge report in chat (per row: answered / partial / missing / asserted-but-infeasible); triages P0 vs P1.
5. **Challenge:** works gaps P0-first, ≤3 questions per turn; every question skippable (→ MISSING/PARTIAL); "that's someone's call" → logged spike; assigns subagent archetype tags and unlocks conditionals; tags reusable pattern candidates in the manifest (capture-only).
6. **P0 gate:** if any P0 missing, one decision point with downstream impact; PM chooses answer-now or proceed-with-gaps.
7. **Generate:** full spec, all 13 sections, manifest populated, primitives stamped, lint clean → rendered to a Google Doc in Drive; link confirmed.

### 7.2 Layer 1 — re-entry (later, after manual edits)

1. PM drops the latest spec Doc (plus any new inputs) into a fresh session.
2. Skill parses the manifest + inline statuses; treats human-filled sections as answers; flags contradictions; maps new inputs against remaining gaps.
3. Either answers "what's still missing" from the manifest, or resumes the challenge and regenerates the whole next version (changelog appended). Re-runs the P0 gate only if gaps remain; doesn't repeat acknowledged warnings.

### 7.3 Layer 2 — behavior design

1. Skill intakes a Layer 1 spec from Drive, reads the manifest, blocks on unresolved P0 gaps.
2. Interviews across the six dimensions per subagent; runs the six-failure-mode lint.
3. Classifies each decision onto its platform surface (four-way map); outputs a versioned Blueprint Doc plus the Spec v1 round-trip update.

### 7.4 Layer 3 — ambient capture

1. While a PM/designer works (any layer), the agent notices a recurring/validated pattern.
2. It offers — only past the 2+/validated threshold — "this looks reusable; refine and add to the library?"
3. On accept, it writes a registry entry (team partition, default `team` visibility) with full provenance.

### 7.5 Layer 3 — lookup and adoption

1. PM asks "has anyone in HC built something like this?"
2. Agent searches the registry, returns pattern cards (provenance + type tag).
3. PM asks "can we use it?"; agent gives an initial relevancy analysis emphasizing differences and what it can't verify, and **recommends confirming with the owning team.**

---

## 8. Execution plan

### Phase 1 — references layer + Layer 1 skill (in build)
**Deliverables:** repo scaffold + DESIGN.md; `agentforce-primitives.md` v1 (built from steward facts + live-doc verification) + invariants + text channel profile; `ax-agent-spec` (rubric, situation taxonomy, spec template, manifest contract, SKILL.md with interview → manifest → P0 gate → Drive publish → re-entry → pattern-candidate tagging); lint script; definition-of-done; 264 golden-example eval; tag v0.1.0.
**Exit:** the skill turns the 264 PM CSV into a usable starting-draft spec with no invention violations; lint and DoD green.

### Phase 2 — Layer 2 skill
**Deliverables:** `ax-behavior-blueprint` built on the six dimensions, with the four-way traceability map and the six-failure-mode lint; the Spec v0 → Blueprint → Spec v1 round-trip.
**Exit:** blueprint generated from the 264 spec matches the real behavior decisions; traceability table complete enough to draft an Agent Script skeleton.

### Phase 3 — Layer 3 skill + registry + Storybook
**Deliverables:** team-scoped pattern registry (`patterns.json`) with partitions + visibility; pattern cards; in-workflow lookup; the lookup one-liner retrofit into Layers 1 & 2; situation taxonomy as the matching key; empty Storybook stood up with the documentation convention; 2–3 seed patterns migrated; standalone browse (optional, shares the schema; expect cold-start).
**Exit:** one pattern goes from "doesn't exist" to "documented, in manifest, rendered" entirely through the skill; one cross-layer capture and one lookup demonstrated.

### Phase 4 — maintenance + publish
**Deliverables:** `primitives-refresh` steward skill (ingests release notes/internal docs, produces a **cited diff**, classifies impact per skill section, drafts changelog — **proposes, never auto-merges**); promotion pipeline personal repo → shared HC repo → marketplace; version-stamp convention verified end-to-end.
**Exit:** a simulated refresh (fed the April terminology change as news) correctly flags every place "topic" appears.

### Phase 5 — adoption & hardening
**Deliverables:** pilot with 2–3 designers on live projects; trigger-description optimization on real phrasing; formalized DoD checklists for design review; first channel overlay (voice, given full Script parity); the VP case study (the suite, the 264 golden examples, the terminology-change save, adoption numbers from version stamps).
**Exit:** adoption + consistency evidence; this artifact doubles as G7 evidence (composable systems, delivery, influence).

---

## 9. Distribution

Develop and test in a **personal repo**. After testing clears, publish tagged releases to the **shared HC Design repo** (`https://ubiquitous-adventure-43w5j5o.pages.github.io/`). The suite is intended to be shared **org-wide** eventually; the pattern registry is **team-scoped by design** so it generalizes to multiple teams. Marketplace packaging is Phase 4. The repo is the source of truth; the marketplace is a release channel.

---

## 10. Governance (OPEN — for VP discussion)

Three mechanisms all **propose or require human acceptance; none auto-commits**: the primitives-refresh skill, harvested-pattern promotion to `org` visibility, and authority over seeded domain standards (HIPAA, verification matrices). These converge on a single unresolved role — an **AX steward / curator** — possibly split with HC compliance/domain owners. Even if a refresh skill drafts updates automatically, a human must review and accept them; an LLM cannot be the author of record for platform truth or compliance standards.

This is the single most important decision for the suite's longevity: without a named owner, the primitives file and pattern library rot within two releases and take the whole suite with them. Until owned, the system is designed for **graceful staleness** (last-verified / last-validated stamps + runtime warnings). **Yuha to raise role ownership with the VP.**

---

## 11. Key design decisions (locked)

1. Suite of three skills + shared references; one version across the suite.
2. Platform truth lives only in versioned, steward-reviewed primitives; never model memory.
3. Terminology: subagent, never topic; translate on intake.
4. Layer 1 audience is PM-primary; aggressive challenge, P0/P1 triage, everything skippable.
5. The Google Doc is the working SSOT; regenerate-not-edit; read-back reconciliation.
6. All sections always present; spike discipline; one-warning P0 gate that propagates downstream.
7. Archetype is tagged per subagent, not per agent.
8. Layer 2 is the six dimensions first, four-way platform map as traceability second.
9. Layer 3 is a behavioral pattern ecosystem: seeded standards + harvested (2+/validated threshold), interaction-metadata-not-code, librarian-not-authority, mandatory team handoff.
10. Library is team-scoped; default visibility `team`, opt-in promotion to `org` (Salesforce-wide), curator-gated.
11. Lookup is cross-cutting via a shared reference; no fourth skill.
12. Evals and definition-of-done are Phase 1 deliverables, because success = adoption + consistency.

---

## 12. Open questions

1. **Role/Boundaries:** one dimension or two in the six-dimension spine? (Confirm before Phase 2.)
2. **Standalone browse:** ship in Phase 3 alongside in-workflow lookup, or later? (Schema is shared; cold-start is the only real cost.)
3. **Governance owner:** who is the AX steward/curator, and is the seeded-standards authority the same person or HC compliance? (VP discussion.)

---

## 13. Success metrics

Primary: **adoption** (teams use it — measurable via version-stamped specs committed to shared locations) and **consistency** (artifacts pass the shared definition of done). Velocity is a secondary benefit, not the current bar.
