# AX Framework Invariants

Hard rules every skill in the AX suite enforces. These define the WHAT;
some will be SATISFIED by Layer 3 seeded-standard patterns (the HOW)
later. This file stays a list of hard rules, not patterns.

1. **No model-memory platform claims.** Skills NEVER rely on the model's
   background knowledge of Agentforce. Every platform claim cites
   `references/agentforce-primitives.md` (and through it, a live Salesforce
   doc URL where one exists). If primitives.md does not cover a fact, the
   skill records a spike; it does not invent the answer.

2. **Terminology translation: subagent, never topic.** The current
   platform term is SUBAGENT (renamed from "topic," April 2026, no
   functionality change). Source documents may say "topic" — translate on
   intake. NEVER emit "topic" in generated artifacts.

3. **Spike discipline.** When an answer requires someone else, the skill
   logs a numbered spike (S-01, S-02, …) with a proposed owner ROLE and
   P0/P1 priority. The skill NEVER invents an answer to fill a section.
   Skipping a question yields MISSING/PARTIAL status, not a fabricated
   value.

4. **Version-stamp every artifact.** Every generated artifact stamps the
   `version` and `last_verified` of the primitives file it was built
   against. Downstream readers can tell at a glance whether an artifact
   was built against a stale snapshot.

5. **Sensitive-data rule.** Any agent touching regulated/sensitive data
   (PHI, PII, financial) MUST define its masking/handling posture before
   any LLM call. In Health Cloud specifically: Einstein Trust Layer
   masking is mandatory, and PHI-adjacent generation requires CUSTOM
   prompt templates, not generic summaries. Note: this invariant defines
   the WHAT; the HOW (identity-before-PHI verification flow, PHI-masking
   prompt-template patterns) is satisfied later by Layer 3
   seeded-standard patterns. This file stays a list of hard rules.

6. **Staleness warning.** Skills consuming `agentforce-primitives.md`
   MUST warn in their output if its `last_verified` is older than 120
   days OR if the user indicates a newer platform release than the
   primitives' `platform_release`. The warning names the stale date and
   points the user at the steward.
