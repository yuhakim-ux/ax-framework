# Definition of Done — Layer 1 Agent Spec

A reviewer should be able to walk this list end-to-end in five minutes.
A spec is **Done** when every item below is true. Stop and fix the spec
at the first item that isn't.

## 1. Lint passes clean

```
python3 skills/ax-agent-spec/scripts/lint_spec.py path/to/spec.md
```

Expected: `OK: <path> lints clean` and exit code 0. If anything prints,
the spec is not Done — fix and re-run.

## 2. Zero MISSING P0 rows (or every remaining one is acknowledged)

Read the manifest's **Rubric coverage** table. Confirm:

- Every P0 row is `ANSWERED`, `PARTIAL`, `SPIKE`, `DEFERRED-L2`, or
  `DEFERRED-L3`. Any P0 row still `MISSING` blocks Done **unless** it
  is listed in the manifest's **P0 gaps** table.
- For each row in **P0 gaps**, the manifest records the user's explicit
  "proceed with gaps" decision (typically in the changelog summary for
  the version where the gate fired). No silent proceed.

Subagent-scoped P0s count too: Grounding (P0 for `INFORMATIONAL`
subagents) and Confirmation / verification (P0 for `TRANSACTIONAL`
subagents with irreversible or regulated actions) only apply when their
trigger fires — verify the archetype tags in section 5 first.

## 3. Every spike has owner role + priority

Scan the **Spike log** table at the end of the spec. For each `S-NN`:

- Owner role filled in (a role, not a person name; never a `<placeholder>`).
- Priority `P0` or `P1` (never `P0 / P1`, never blank).
- Status set to `open`, `answered`, or `superseded`.

Cross-check: every spike referenced in section bodies or the manifest
exists in the log. The lint already enforces this (Check 6); use this
DoD line as a fast eyeball.

## 4. Every platform mechanism named in section 7 exists in primitives

For each subagent's section 7 (`Execution mechanism & feasibility`),
verify the Mechanism column values against
`references/agentforce-primitives.md`:

- `apex`, `flow`, `prompt` are the documented Agent Script action
  targets — these are always valid.
- `OOTB` is a steward-asserted bucket; flag if used without a citation.
- Anything else (custom mechanism names, made-up types) is a fail.

If an action's mechanism is genuinely TBD, it should be a `SPIKE` row,
not an invented mechanism name.

## 5. Primitives version stamp present and current

Read the title block. Confirm:

- `Primitives version: X.Y (last_verified YYYY-MM-DD)` is present and
  non-empty.
- The `last_verified` date is within 120 days of today AND the
  `platform_release` in `references/agentforce-primitives.md` matches
  the release this agent is targeting.
- If stale, the skill should already have surfaced a warning at
  generation time — confirm the warning is acknowledged in the
  changelog or the user's chat decision.

## 6. Title block has Team + Product Owner (pattern provenance)

Both fields must be non-empty in the title block:

- `Team:` — the team that owns the agent.
- `Product Owner (owner_contact):` — the named owner contact who will
  become the pattern provenance handle in Phase 3.

These are not stylistic — Phase 3 partitions the pattern registry by
team and uses `owner_contact` on every pattern card. A spec missing
either cannot become provenance for harvested patterns.

## 7. Published (or local fallback noted)

Confirm one of:

- The spec is published to Google Drive at the per-agent folder as
  `<agent>-spec-vX.Y`, and the Drive link is recorded in the most
  recent changelog row, OR
- Drive was unavailable; `.md` and `.docx` saved locally; the local
  paths AND the Drive-unavailable note are recorded in the most recent
  changelog row.

Either path counts as Done. A spec that exists only as chat output is
not Done.

---

## Reviewer's five-minute pass

1. Run the lint command. (≈30 sec)
2. Open the spec; eyeball the title block (items 5, 6). (≈30 sec)
3. Skim the manifest's Rubric coverage + P0 gaps (item 2). (≈90 sec)
4. Scroll to Spike log; check rows (item 3). (≈30 sec)
5. Spot-check section 7 mechanisms against primitives (item 4). (≈60 sec)
6. Confirm the changelog row carries the Drive link or local-fallback
   note (item 7). (≈30 sec)

Total: ~5 minutes. If steps 1–6 all clear, the spec is Done.
