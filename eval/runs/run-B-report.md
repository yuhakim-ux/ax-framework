# Eval B — Sparse PRD: report

**Input:** `eval/golden/264-input-prd-sparse.md` (~250 words)
**Run output:** `eval/runs/run-B-spec.md`
**Lint:** clean.
**Scoring:** behavioral, not similarity (there is no reference).

The question: **on weak input, did the skill challenge hard, fire the
P0 gate, stay honest, and invent nothing?**

---

## CHALLENGE

Did the skill produce a challenge report and aggressive PM-language
gap questions framed as engineering-handoff consequences?

- **Per-section challenge questions** are pre-printed under every
  MISSING / PARTIAL section, sourced from `rubric.md`. Examples:
  - Row 1: "If it works perfectly, what changed for the user and the
    business? Name 3 things a user might expect that it won't do."
  - Row 9: "What's the worst thing it could do if it misunderstood?
    Which rules are deterministic enough for Script?"
  - Row 12: "What number moves if this agent works?"
- **PM-language consequence framing** appears in the P0 gap table.
  The "Downstream sections this degrades" column is engineering-handoff
  language by construction: "Layer 2 cannot wire any routing,"
  "Engineering has no actions to build," "`welcome` and `error` hooks
  undefined," "Cannot ship/no-ship gate."
- **The Open Questions table** raises nine concrete unanswered items
  (Q-01..Q-09), most marked blocking. Q-01 surfaces the
  sensitive-data-classes question that the PRD's "be careful" line
  hand-waves. Q-04 demands a baseline-and-number replacement for
  "less / faster / fewer."

**Net:** ✅ challenges produced; PM-language framing present; gap
questions are pre-printed where required.

**Soft observation:** the challenge report referenced in SKILL.md
Step 2 ("before any interviewing, produce a CHALLENGE REPORT in chat")
is interactive output, not part of the spec file. The spec file
captures the *result* of that report. In a real session it would
appear in chat first; the run-B-spec.md captures the post-gate output.

---

## P0 GATE

Did it fire — listing missing P0s with downstream impact — exactly once?

The spec's P0 gaps table fires the gate and lists **eight** P0 rows as
MISSING:

| Row                                             | Downstream consequence                                                          |
|--------------------------------------------------|----------------------------------------------------------------------------------|
| 5. Subagent inventory                            | Every per-subagent row degrades. Layer 2 cannot wire any routing.               |
| 6. Action inventory                              | Engineering has no actions to build.                                             |
| 7. Execution mechanism                           | No mechanism selection possible; no feasibility spike scope.                     |
| 8. Data read/written + Variables Block           | Reversibility and Trust Layer masking gates cannot be designed.                  |
| 9. Guardrails / must-nevers, with placement      | No `system: instructions` body; no Script-enforced rules.                        |
| 10. Failure & recovery + global messages         | `welcome` and `error` hooks undefined.                                            |
| 12. Success metrics                              | Cannot ship/no-ship gate.                                                         |
| 13. v1 scope boundary + open spikes              | Engineering cannot scope.                                                          |

The user choice is recorded as **proceed with gaps**, then captured in
the changelog row v0.1 with "P0 gate fired; user chose proceed with
gaps." That's the once-and-only-once acknowledgement the SKILL.md
Step 4 specifies.

**Net:** ✅ gate fires once, with downstream-impact statements per
row, with the user's proceed decision recorded in the manifest and
changelog.

---

## HONESTY

Is the output mostly MISSING / PARTIAL / SPIKE (correct for thin input)?
Is invented content zero?

**Status distribution across rubric rows:**

| Status     | Count |
|------------|-------|
| ANSWERED   | 2     |
| PARTIAL    | 4     |
| MISSING    | 4     |
| SPIKE      | 0     |
| DEFERRED-L2| 3     |
| DEFERRED-L3| 1     |

10 rubric rows (because subagent inventory is MISSING, the 6/7/8
per-subagent rows don't repeat — they cannot exist without subagents).
Status is dominated by PARTIAL/MISSING, which is the correct response
to a 250-word PRD. The two ANSWERED rows (3 Trigger, 4 Channel) reflect
the two facts the PRD actually states clearly: it's inbound, it's voice.

**Invented content scan:**

| Vector                  | Result   | Evidence                                                                                                   |
|-------------------------|----------|-------------------------------------------------------------------------------------------------------------|
| Invented subagents      | none     | Row 5 is MISSING; the SA-1..SA-N inventory is genuinely empty.                                              |
| Invented actions        | none     | Sections 6/7/8 do not exist in this spec — they require an inventory first.                                 |
| Invented mechanisms     | none     | No `apex`/`flow`/`prompt` assertions appear outside the (now-empty) Pattern Candidates table caption.       |
| Invented data objects   | none     | Row 8 is MISSING; no `Case` / `VoiceCall` / `Account` named.                                                |
| Invented thresholds     | none     | No retry counts, sentiment thresholds, latency targets.                                                     |
| Invented escalation copy| none     | Row 11 is PARTIAL and explicitly says copy + context "NOT named."                                            |
| Invented success metrics| none     | Row 12 is PARTIAL with a quote of the PRD's directional bullets; no baseline / number invented.              |
| Invented `welcome`/`error` text | none | Row 10 is MISSING; neither hook is filled.                                                                   |
| Invented v1 boundary    | none     | Row 13 is MISSING; PRD's "this release if possible" is called out as non-boundary.                          |

**Net:** ✅ zero invented content.

---

## SENSITIVE-DATA

Did the lone "member data, be careful" hint trigger the sensitive-data
conditional per `references/invariants.md`?

Yes. The **Data sensitivity & masking posture** conditional section
appears in the spec marked `[MISSING]` (the trigger fired; the answer
is absent). The section explicitly:

- Quotes the PRD's "we'll need to be careful about that."
- Cites `references/invariants.md` for the Health-Cloud-specific
  invariant (Einstein Trust Layer masking mandatory; PHI-adjacent
  generation requires CUSTOM prompt templates).
- Asks the unanswered question: "Which member-data fields are PHI,
  which are PII, and which are neither? What is the masking
  configuration? Does call summary generation require a custom prompt
  template?"

The corresponding open question is Q-01 (sensitive-data classes) +
Q-02 (Trust Layer masking posture), both marked blocking. A spike on
this is S-02 in the spike log.

**Net:** ✅ trigger fired; gap surfaced; no posture invented.

---

## ALL-SECTIONS

Are all rubric sections present despite the thin input, each with a
status tag and pre-printed challenge question?

The lint's Check 1 expects:
- Rows 1, 2, 3, 4, 5 (agent + subagent inventory) — always.
- Rows 6, 7, 8 — once per subagent. **No subagents in this spec** →
  these rows correctly do NOT appear.
- Rows 9, 10, 11, 12, 13 (agent) — always.

That's 10 rubric sections in this spec. All ten appear in the manifest
AND have matching headings in the body. The lint passes Check 1.

Each section carries an inline status tag (`[ANSWERED]` / `[PARTIAL]` /
`[MISSING]`). Each non-ANSWERED section ends with a `> Challenge:`
block carrying a `?`-terminated pre-printed challenge question from
the rubric. Lint Check 9 confirms.

The two triggered conditional sections (Data sensitivity & masking
posture; Performance & latency tolerance) are present with status tags
and challenges. The five deferred-tier placeholders (Golden path,
Persona/voice, Recovery conversation, Rendering/trust-signal UI) are
present with their DEFERRED-L2/L3 tags.

**Net:** ✅ all required sections present; nothing omitted to mask
gaps.

---

## PATTERN CANDIDATES

Minimal is fine on thin input. What appears?

The Pattern Candidates table is **empty**, with an explanation:

> No rows: PRD names no subagents (row 5 MISSING) so candidates cannot
> be anchored to an `SA-N` reference. Tagging deferred until the
> subagent inventory exists. Two recurring situations are visible in
> the PRD — escalation-to-human and sensitive-data-disclosure — but
> they will be tagged at the next generation once subagents are named.

This is correct behaviour. A first pass through the script attempted
to tag those two situations with `SA-?` as the subagent reference;
lint Check 10 rejected that (subagent-ref format) and the run was
corrected to leave the table empty rather than fabricate SA labels.

**Spurious tags:** none (table empty).

**Net:** ✅ no premature flagging; the absence of subagents
correctly blocks pattern tagging until the next generation.

---

## VERDICT

**The skill behaved as designed on weak input.**

- It challenged hard with PM-language consequences via the
  per-section challenges + the P0 gaps table.
- The P0 gate fired exactly once with downstream-impact statements;
  the user's proceed decision is recorded once.
- Status distribution skews MISSING/PARTIAL (10/10 non-deferred rows
  are non-ANSWERED except for the two PRD-given facts: voice channel,
  inbound trigger). Honest response to a 250-word PRD.
- Invention count: **zero**. No subagents, actions, mechanisms,
  objects, thresholds, retry counts, masking postures, escalation
  copy, success metrics, or v1 boundaries were invented to fill gaps.
- Sensitive-data conditional fired on the one "member data, be
  careful" PRD line; gap is surfaced with the right invariant
  citation, not papered over with a posture inference.
- All required sections present; deferred placeholders correctly
  rendered.
- Pattern candidates correctly empty — no SA-N anchor, no tagging.

**One thing the skill does NOT do** that a stricter reading might
expect: it does not REFUSE generation on a sparse PRD. It generates
the spec at v0.1 with everything marked MISSING / SPIKE and the
proceed-with-gaps decision recorded. That matches DESIGN.md ("Skip +
P0/P1 triage is the defense against abandonment") and the SKILL.md
"warn once; never nag twice" rule. The user retains the choice.

A reviewer reading this output would conclude the agent is **not yet
specified enough to build** — which is the correct conclusion, and
which the spec makes legible rather than hiding behind plausible
filler.
