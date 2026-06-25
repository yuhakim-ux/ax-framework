# Appointment Reminder — Agent Spec

**Version:** 0.1
**Date:** 2026-06-25
**Authors:** Yuha Kim
**Team:** HC Patient Experience
**Product Owner (owner_contact):** Jordan Park
**Primitives version:** 1.0 (last_verified 2026-06-24)

---

## Completion manifest

### Rubric coverage

| Rubric row                                                  | Scope    | Status   | Notes / Spike refs |
|-------------------------------------------------------------|----------|----------|---------------------|
| 1. Goal + non-goals                                         | Agent    | ANSWERED |                     |
| 2. Primary user & their goal                                | Agent    | ANSWERED |                     |
| 3. Trigger / entry point                                    | Agent    | ANSWERED |                     |
| 4. Channel                                                  | Agent    | ANSWERED |                     |
| 5. Subagent inventory                                       | Subagent | ANSWERED |                     |
| 6. Action inventory — SA-1                                  | Subagent | ANSWERED |                     |
| 7. Execution mechanism & feasibility — SA-1                 | Subagent | ANSWERED |                     |
| 8. Data read/written + Variables Block — SA-1               | Subagent | ANSWERED |                     |
| 9. Guardrails / must-nevers, with placement                 | Agent    | ANSWERED |                     |
| 10. Failure & recovery + global messages                    | Agent    | ANSWERED |                     |
| 11. Human escalation / handoff                              | Agent    | ANSWERED |                     |
| 12. Success metrics                                         | Agent    | ANSWERED |                     |
| 13. v1 scope boundary + open spikes                         | Agent    | ANSWERED | S-01                |

### Source documents ingested

| Document            | Type | Ingested on  | Notes |
|---------------------|------|--------------|-------|
| Reminder PRD draft  | PRD  | 2026-06-20   | v3    |

### Pattern candidates

| Situation                    | Mechanism | Subagent ref | Candidate-type | Note                            |
|------------------------------|-----------|--------------|----------------|---------------------------------|
| confirmation                 | prompt    | SA-1         | harvested      | Confirm intent before send.     |
| identity-verification/patient| flow      | SA-1         | would-match-seeded-standard | Verify before any PHI mention. |

### Changelog

| Version | Date         | Author    | Summary                  |
|---------|--------------|-----------|---------------------------|
| 0.1     | 2026-06-25   | Yuha Kim  | First generation.         |

---

## 1. Goal + non-goals — [ANSWERED]

Send confirmed-appointment reminders to patients on their preferred channel.

**Won't do (explicit non-goals):**

- Reschedule appointments.
- Cancel appointments.
- Send unsolicited marketing.

## 2. Primary user & their goal — [ANSWERED]

End-customer patients who want a reliable reminder before their visit.

## 3. Trigger / entry point — [ANSWERED]

Fires 24 hours before a scheduled appointment, on a queued reminder job.

## 4. Channel — [ANSWERED]

Text only (Messaging for Web; SMS deferred to v2).

---

## 5. Subagent inventory — [ANSWERED]

| ID   | Subagent name      | Archetype     | Routing description              | Deterministic routing conditions |
|------|--------------------|---------------|----------------------------------|-----------------------------------|
| SA-1 | Reminder Composer  | TRANSACTIONAL | Drafts and sends the reminder.   | Always invoked at job time.       |

---

# Subagent: SA-1 — Reminder Composer  [archetype: TRANSACTIONAL]

## 6. Action inventory — [ANSWERED]

| Action ID | Name           | One-line purpose         |
|-----------|----------------|--------------------------|
| 1.1       | compose_text   | Draft the reminder body. |
| 1.2       | send_message   | Send the drafted text.   |

## 7. Execution mechanism & feasibility — [ANSWERED]

| Action ID | Mechanism | Exists today? | Spike (if not) |
|-----------|-----------|---------------|-----------------|
| 1.1       | prompt    | yes           |                 |
| 1.2       | apex      | yes           |                 |

## 8. Data read/written + Variables Block — [ANSWERED]

**Records / objects read vs created/mutated:**

| Object / record | Direction | Reversible? |
|-----------------|-----------|-------------|
| Appointment     | read      | n/a         |
| MessagingSession| create    | no          |

**Declared state (Variables Block):**

| Variable kind | Reference                       | Source / Notes              |
|---------------|---------------------------------|------------------------------|
| Regular       | `@variables.draft_body`         | Composed text awaiting send. |
| Linked        | `@MessagingSession.Id`          | Session context.             |
| System        | `@system_variables.user_input`  | Most recent user reply.      |

---

## 9. Guardrails / must-nevers, with placement — [ANSWERED]

| Constraint                              | Placement              | Rationale         |
|-----------------------------------------|------------------------|--------------------|
| Never disclose diagnosis in reminder.   | system: instructions   | HIPAA posture.     |
| Never send before identity-verify.      | Script-enforced        | Compliance gate.   |

## 10. Failure & recovery + global messages — [ANSWERED]

**Retry / fallback policy:**

| Failure case   | Retry policy | Fallback behaviour       |
|----------------|--------------|---------------------------|
| Action failure | 2 retries    | Escalate to staff queue.  |
| Unclear intent | 1 reprompt   | Hand off to human.        |
| Low confidence | none         | Hand off to human.        |

**`system: messages` hooks:**

| Hook      | Defined? | Content                                             |
|-----------|----------|------------------------------------------------------|
| `welcome` | yes      | "Hi — quick reminder about your upcoming visit."     |
| `error`   | yes      | "Something went wrong — connecting you to a person." |

## 11. Human escalation / handoff — [ANSWERED]

Hands off to the scheduling team queue with the session transcript and the
appointment record link attached.

## 12. Success metrics — [ANSWERED]

| Metric              | How measured                  | Where reported |
|---------------------|-------------------------------|-----------------|
| Reminder open rate  | Messaging session open event. | Weekly review.  |

## 13. v1 scope boundary + open spikes — [ANSWERED]

**In v1:**

- Text channel only.

**Out of v1:**

- Voice reminders.

See S-01 below.

---

# Deferred placeholders

## Golden path & decision-point design — [DEFERRED-L2]
Golden path required — to be designed in Behavior Blueprint.

## Persona / voice & tone detail — [DEFERRED-L2]
Persona detail required — to be designed in Behavior Blueprint.

## Recovery flow CONVERSATION design — [DEFERRED-L2]
Recovery flow conversation required — to be designed in Behavior Blueprint.

## Rendering, trust-signal UI, surface patterns — [DEFERRED-L3]
Rendering, trust-signal UI, and surface patterns required — to be designed
in the Interface layer.

---

# Spike log

| Spike ID | Owner role        | Priority | Rubric ref | Question                              | Status |
|----------|-------------------|----------|------------|---------------------------------------|--------|
| S-01     | Scheduling owner  | P1       | Row 13     | Confirm v2 voice channel requirement. | open   |
