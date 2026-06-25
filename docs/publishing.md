# Publishing — promotion from personal repo to the shared HC Design repo

This is the promotion checklist for moving an AX Framework Skills release
from this personal repo (`~/projects/personal/ax-framework/`) to the
shared Health Cloud Design repo at
https://ubiquitous-adventure-43w5j5o.pages.github.io/.

Don't publish until every box is ticked. The Phase 1 ship-to-shared cut
is `v0.1.0` (Layer 1 only).

## Checklist

- [ ] **(a) Definition of Done is green** against the **latest** eval
      iteration. Run `python3 skills/ax-agent-spec/scripts/lint_spec.py
      --self-test`; both fixtures must pass. Walk `docs/definition-of-done.md`
      against the most recent run-A* and run-B* specs in `eval/runs/`. If
      either fails, do not publish — fix and re-tag.
- [ ] **(b) Pilot feedback** from at least **one designer other than the
      author**. Verbal "looks good" is not feedback — capture a written
      note (Slack message, doc comment, GUS work item, anything dateable)
      that names what they tried, what worked, and what they'd want
      changed. If the only feedback is the author's own, this is not
      ready to ship to a shared repo.
- [ ] **(c) Primitives `last_verified` within 120 days.** Open
      `references/agentforce-primitives.md`, confirm the header
      `last_verified` date is no older than 120 days. If stale, refresh
      the steward review BEFORE publishing — downstream skills will
      emit a staleness warning at the top of every generated spec
      otherwise, and shipping that to other teams is a bad first
      impression.
- [ ] **(d) Tag pushed.** `git tag vX.Y.Z` on the commit that snapshots
      the publish, then `git push --tags`. The shared repo consumes
      tagged releases, not `main` snapshots.
- [ ] **(e) Announce note drafted.** A one-paragraph announce that
      names: the version, what's new since the previous publish (read
      the relevant `CHANGELOG.md` entries), known caveats (e.g. items
      still flagged `[steward-provided, link pending]` in primitives),
      and the contact (you, as steward) for issues. This goes wherever
      the HC Design repo announces releases.

## Org-wide note (read before changing the publish target)

The AX Framework Skills suite is **intended to be shared org-wide
eventually**, not just inside Health Cloud. Phase 1 publishes to the
HC Design repo because that is the testing/adoption ground for HC
teams; broader distribution is Phase 4 (Marketplace packaging).

Two architectural commitments to keep in mind whenever the publish
target or team-config conventions change:

- **The skill suite itself is org-shared by design.** All Salesforce
  teams should be able to install and run it as-is. Skill content must
  remain general; only `references/` and team-configs carry per-team
  variation.
- **The pattern registry is team-scoped by design.** Per DESIGN.md, the
  Layer 3 registry has `seeded-standards` (authority-owned, org/domain
  visible) plus per-team partitions, with `team` as a first-class
  attribute on every pattern. `visibility = team` is the default;
  promotion to `org` is a deliberate, curator-gated step.

Implication for publishing: the publish target (and any team-config
conventions baked into the release) should anticipate **multiple teams
adopting independently**. Do not bake "Health Cloud" into the skill's
default team-config; HC is the first adopter, not the only one. When
Phase 4 ships Marketplace packaging, the conventions established here
need to round-trip with the rest of the suite without HC-specific
assumptions.

## Phase reminder

- Phase 1 (this publish) — Layer 1, references layer, lint, DoD,
  264 golden eval. HC Design repo.
- Phase 4 — Marketplace packaging. Broader org-wide distribution.
  At that point this checklist gets revisited; treat it as living
  guidance, not a contract.
