# Text channel profile

Text is the AX framework's DEFAULT and FOUNDATIONAL channel profile. Voice,
Slack, and embedded surfaces are future additive overlays that follow this
same file pattern (`references/channels/<channel>.md`) and only document
their deltas from this baseline.

## Entry surfaces (current sanctioned)

- **CRM-embedded chat** — Agentforce surface inside Service Cloud /
  Health Cloud / Sales Cloud console.
- **Enhanced Web Chat (Messaging for Web)** — branded, customer-facing web
  surface deployed on company sites.
- **Embedded Service / Messaging Embedded** — chat widget embedded inside
  customer-owned web experiences and apps.

All three terminate in the same Agent Script runtime; subagent and
variable semantics are identical. Differences live in styling, anonymous-vs-
authenticated session context, and which linked-variable namespaces are
populated (see below).

## Turn-taking assumptions

- **Strict half-duplex turns.** User submits a message; agent responds;
  user replies. No interruption, no overlap.
- **No time pressure on the user side.** A user may pause arbitrarily
  between turns without invalidating the session, unlike voice. Skills
  that generate text-channel artifacts can assume the user has time to
  read, scroll, and reread; they should NOT pre-emptively compress
  responses the way voice scripts must.
- **Agent latency budget is loose** by voice standards. Multi-second
  pauses for retrieval or action chaining are tolerable; longer pauses
  benefit from a "thinking" affordance but are not session-fatal.
- **Persistent transcript.** The whole conversation is on-screen; the
  user can scroll back. Earlier turns do NOT need to be re-summarized in
  later agent replies (a voice-channel necessity).

## Linked-variable namespaces that typically apply

- `@MessagingSession` — the messaging session record (Id, status,
  routing metadata).
- `@MessagingEndUser` — the end-user record on the messaging session
  (Id, contact linkage if authenticated).
- `@system_variables.user_input` — the most recent user utterance,
  available to every subagent.

`@VoiceCall` does NOT apply on text channels.

Authoritative names + syntax: see Variables section of
`references/agentforce-primitives.md`.

## Note

This is the foundational modality. Voice/Slack/embedded profiles, when
authored, follow this same structure (entry surfaces, turn-taking,
linked-variable namespaces, channel-specific deltas) so that downstream
skills can swap channel context by file path rather than by branching
logic.
