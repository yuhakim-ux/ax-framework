# ax-agent-spec — Situation Taxonomy (v1.0)

Controlled vocabulary for tagging reusable pattern CANDIDATES surfaced
during Layer 1 spec authoring.

**Scope this phase.** This vocabulary is the SHARED matching key the
Phase 3 pattern registry will use. **Phase 1 ONLY TAGS candidates against
it** — there is no registry, no relevancy matching, and no lookup yet.
Tagging populates the PATTERN CANDIDATES table in the spec manifest and
stops there.

**How to tag.** When the skill notices an interaction that matches a
situation below, it adds a row to the manifest's PATTERN CANDIDATES table
with: `situation` (one of the values below), `mechanism`
(`action` / `flow` / `prompt`), `subagent ref` (SA-N), `candidate-type`
(`would-match-seeded-standard` | `harvested`), and a one-line note.

---

## Platform base-pattern situations

Generic interaction shapes documented at the platform level. Tag a
candidate against one of these when the situation is the generic shape
itself.

- **human-in-the-loop** — the agent pauses for a human to approve,
  edit, or sign off on a draft / proposed action before proceeding.
- **fallback** — the agent's primary path failed (no answer, no match,
  no path) and a defined alternative path runs in its place.
- **escalation-to-human** — the agent hands the session off to a human
  agent / queue. Distinct from fallback: the agent itself stops.
- **confirmation** — the agent restates an intended action and gates
  execution on explicit user assent.
- **disambiguation** — the agent identifies that user intent could
  resolve more than one way and asks a targeted clarifying question
  before proceeding.

## Six failure-mode situations

The six failure modes that Layer 2 uses as quality lint. Tag here when
the candidate exists BECAUSE one of these failure modes is being
defended against.

- **golden-path-ordering** — the agent has more than one ordered step
  and the order itself is part of correctness (skipping or reordering
  breaks the outcome).
- **act-without-confirm** — the agent performs (or could perform) an
  action without an explicit user confirmation that the action is what
  the user wants.
- **missing-fallback** — a step has no defined behaviour for the
  not-found / no-answer / unreachable case.
- **assumption-without-intent** — the agent proceeds on an assumed
  user goal without having gathered the user's actual intent.
- **capability-gap-masking** — the agent's persona / phrasing hides
  that it cannot actually do something the user is asking for.
- **late-or-missing-escalation** — escalation to a human is not wired,
  is wired too late, or has no defined trigger.

## Domain situations

Health Cloud / regulated-data shapes. Tag here when the candidate is
specifically about the regulated-domain interaction, not a generic
platform pattern.

- **sensitive-data-disclosure** — the agent is about to surface
  regulated / sensitive data (e.g. HIPAA-covered PHI). Includes
  masking, disclosure language, and the gate that decides whether
  to disclose at all.
- **identity-verification** — the agent confirms the user is who
  they claim to be before any sensitive action or disclosure.
  Persona variants (call out which applies):
  - `identity-verification/patient`
  - `identity-verification/payer`
  - `identity-verification/provider`
- **irreversible-action-confirmation** — the agent is about to take
  an action that cannot be undone without operational cost (booked
  appointment, sent message, dispatched order, submitted claim).
  Distinct from generic `confirmation` because the failure-mode cost
  is asymmetric.

---

## Non-goals at Phase 1

- No relevancy matching against a registry. The registry does not exist
  yet.
- No "this candidate looks like seeded-standard X" lookup. Best the skill
  can do is tag `candidate-type: would-match-seeded-standard` as a
  Phase-3 hint.
- No harvest promotion. Candidates stay in the spec's manifest until
  Layer 3 owns harvesting / promotion (see DESIGN.md, Layer 3 reframed).
