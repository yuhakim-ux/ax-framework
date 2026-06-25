# Phase 5 — pilot notes & validation to-dos

Items captured during Phase 1 build that need pilot-time validation.

## `ax-agent-spec` description: validate trigger rate in real use

Description trigger-rate was tuned via deterministic match analysis
(6/6 positives, 3/3 negatives against the HC PM/designer eval set in
v0.0.11), **not rep-based subagent testing**. Validate against real
PM/designer phrasing during the pilot; re-tune if real usage
under- or over-triggers.

**Watch the "pattern" keyword overlap** once the Layer 3 sibling skill
ships. The current Phase 1 description carves out
`pattern-library work` as a negative — when `ax-agent-interface`
arrives in Phase 3, re-check both descriptions together so they
disambiguate cleanly rather than competing for the same triggers.
