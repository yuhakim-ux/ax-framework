Release 264 · Health Cloud · PCC

**264 Call/Chat Wrap-Up Summary Agent**

Agentforce Implementation Requirements Spec — Agent Template, Subagents, Actions, Flows

*Version: 1.0 Draft  ·  Date: April 2026  ·  Designer: [UX Designer] Kim  ·  PO: [PM]  ·  Arch: [Architect] Mahajan  ·  EM: Shobha Setty  ·  Dev: Yazi/Surbhi*


**Legend**

| \[P0\] | Required for Release 264 | \[P1\] | Stretch goal for 264 |
| :---- | :---- | :---- | :---- |
| **\[264+\]** | Future release | **\[AFV\]** | Agentforce Voice (autonomous) |
| **\[SCV\]** | Salesforce Agenforce (Voice/Text) | **\[BOTH\]** | AFV \+ SCV applicable |
| **\[Flow\]** | Salesforce Flow (no/low code) | **\[Apex\]** | Apex (pro code) |
| **\[Prompt\]** | Prompt Template (LLM) | **\[MuleSoft\]** | MuleSoft External Action / API |
| **\[Spike Y/N\]** | Technical spike required before implementation | **\[★ Core\]** | Primary wrap-up automation scope for 264 |

**★ Wrap-Up Core:** Subagents 2–6 (Case Management, Engagement Creation, Call/Chat Summary) form the primary wrap-up automation scope for Release 264\. 

**Platform Note:** AFV is built on top of SCV. SCV handles telephony, routing, recording, and VoiceCall object creation. AFV adds speech-to-text and autonomous reasoning. Both expose transcript via SCV APIs using VoiceCallId. Einstein Trust Layer must mask PHI/PII before all LLM calls (HIPAA requirement). Should support different channels, like call, web chat, etc.

# 

| Status: | Draft |
| :---- | :---- |
| **PO Approval:** | Pending |
| **UX Approval:** | Pending |
| **CX Approval:** | Awaiting |

# 

# **Agent Template Definition**

| Agent Name | ~~264 Call Wrap-Up Summary Agent~~   Health Cloud Contact Center Call Wrap-Up Assistant |
| :---- | :---- |
| **Agent Template** | Agentforce Service Agent (A4S) |
| **Modalities** | Primary: Voice (via Service Cloud Voice/CTI) Secondary: Digital Chat (In-App/Web) |
| **Goal(Instructions)** | **Wrap-up automation:** Reduce average handle time (AHT) by automating post-call tasks — Case creation, AI summary, transcript attachment, timeline update — that contact-center staff previously performed manually. **HIPAA-compliant end-to-end flow:** PHI (member name, DOB, SSN, full MRN) is never passed raw to any LLM. PHI is never spoken by the agent before identity is confirmed. Einstein Trust Layer masking is mandatory on every prompt call. **Parity between AFV and SCV:** The quality and completeness of Case / Interaction / Summary records must be identical whether the call was handled autonomously (AFV) or by a human agent (SCV). Downstream systems must not be able to tell the difference. **Zero context loss on escalation:** When the call escalates to a human, all context up to that point — draft Case, Engagement Interaction, partial summary, sentiment, member ID — is preserved and surfaced on the human agent's screen pop. The human does NOT re-identify the caller or re-read the transcript. **Complete member timeline:** Every inbound call appears on the member's Engagement timeline — regardless of whether a Case was created. A care manager reviewing the member record three months later must see a complete interaction history. **Audit trail for regulated books:** Payer operations are regulated. Every member inquiry must have an auditable record. Per PM guidance this may mean auto-creating \+ auto-closing a Case even for pure knowledge queries. **Seamless human handoff:** Handoff between AI agent and human agent requires no re-work on the caller's side. The human must inherit full context and resume the conversation without asking the caller to repeat themselves. **Explicit unresolved decisions:** Every open question and every technical spike is named, owned, and tracked. The document surfaces what is NOT yet decided so sprint planning can prioritize resolution. |
| **Greeting (Welcome)** | Hi, thanks for calling\! How may I assist you today? If the caller was identified, personalize the greeting by including the caller's name in the greeting. If intent was available, confirm if the user is calling for intent\_primary (first intent), instead of asking what assistance can be provided. |
| **Variables** | \<To be added by engineering\> |
| **Topic selector (Seasoning)** |  |
| **License Required** | Service Cloud Voice in Unlimited editions Service Cloud Einstein Einstein GPT for Service add-on (for Einstein work summaries for voice & conversation catch up) Einstein for Service add-on Agentforce Voice Agent Force for Service (A4S)  Agentforce for Health Health Cloud  Data cloud / Mulesoft (for HC std topics & actions) |
| **Language (264)** | English. Spanish in 264+. (We will be supporting what platform supports currently. By default, English will be supported and customers will have to configure additional language support at the time of setup.) |
| **Objective** | Automate call wrap-up tasks: case/task/activity creation, AI summary, transcript & sentiment attachment, Engagement timeline update. Works for both autonomous AFV supported voice calls, as well as autonomous chats. |
| **PHI Handling** | Einstein Trust Layer must mask PHI/PII before every Prompt Template (LLM) call. No member SSN, DOB, or full MRN passed to LLM. Health Cloud Industries regulations. |
| **Total Subagents** | 10 Subagents / 22 Actions |
| **Scope** | Proactive Agentforce assistant that automates on-call & post-call activities using live transcription for voice calls & chats to reduce Average Handle Time (AHT) such as identity resolution, automated creation and population, interaction logging, knowledge retrieval  |

# 

# **Subagent Inventory**

| ID | Name | Type | Priority | Purpose | Notes |
| ----- | :---- | :---- | ----- | :---- | :---- |
| **SA-1** | **Identity Verification** | Custom: Patient Access | P0 | Authenticate the caller and establish member context | *SSOT: 264 Patient Access* |
| **SA-2** | **Case Management** | Custom | P0 | Create a new Case OR locate and update an existing follow-up Case | *Handles both new and follow-up scenarios* |
| **SA-3** | **Engagement Creation** | TBD | P0 | Create an Engagement Interaction and attendee records for the active call | *Foundation for timeline & wrap-up* |
| **SA-4** | **Call/Chat Wrap-Up Summary**  | Custom | P0 | Generate AI call summary, attach transcript, finalize records at end of call | *Primary focus of this document* |
| **SA-5** | **Knowledge — Member Plan** | OOTB Agentforce Topic | P0 | Answer plan, benefits, coverage, and ID-card questions from Knowledge articles | *Uses OOTB 'Answer Questions with Knowledge' topic* |
| **SA-6** | **Escalation** | OOTB Agentforce Topic \+ custom Omni Flow | P0 | Transfer the call to a human agent with context preservation | *Uses OOTB Escalation topic wired to a customer-configured Omni Flow* |
| **SA-7** | **Find Claims** | HC GA | P0 | Retrieve claim status, history, and summary information for the member | *Health Cloud GA; see HC release notes* |
| **SA-8** | **Find Prior Auth** | HC GA | P0 | Retrieve prior authorization status for the member | *Health Cloud GA; see HC release notes* |
| **SA-9** | **Provider Network Search** | HC GA | P0 | Search in-network providers by specialty and location scoped to member's plan | *Health Cloud GA; see HC release notes* |

## **\[Reuse\] SA-1: Identification & Verification &  \[P0\]  \[BOTH\]**

| Classification Description | Triggered automatically at call start via CTI/ANI event before any caller utterance. Applies to every inbound call. Handles ANI match, demographic lookup, and proxy caller detection.Request you to evaluate the existing [Identity Verification](https://help.salesforce.com/s/articleView?id=ind.admin_contact_center_identity_verification_and_engagement_details.htm&type=5) feature we have that works across *engagement channels,* and it can be configured to verify *any persona (member, provider, caregiver)* |
| :---- | :---- |
| **SF Objects Affected** | Contact / Account (Member), VoiceCall, Conversation / Messaging, EngagementInteraction, EngagementAttendee |
| **Scope (CAN do)** | Look up member by ANI (phone number from CTI stamped on Voice Call object). If no ANI matches, collect Name \+ DOB or MRN to identify member. Determine if the caller is the member or a proxy (caregiver, POA). Capture proxy name and relationship.  Identification will give the Account ID & Verification will verify the account’s details such as Name, DOB, etc. Do NOT proceed to intent matching without confirmed identity. Escalate to human agent when identity / verification fails after 1 retry. |
| **Guardrails (CANNOT do)** | Do NOT accept caller self-identification without cross-checking a registered field. Do NOT share member PHI verbally before identity is confirmed.  Do NOT keep asking the caller their details if Identity/Verification fails, instead escalate to human agent after 1 retry. |
| **Open Questions** | Should proxy (non-member) calls auto-escalate to human agent? Caller HIPAA verification is 264+, not in scope for this release. The [Identity Verification](https://help.salesforce.com/s/articleView?id=ind.admin_contact_center_identity_verification_and_engagement_details.htm&type=5) subagent should take care of above two points |

**Actions \- TBD \- Design in progress**

| \# | Action Name | Impl. Type | Description | Input Schema | Output Schema | Rules / Conditions | Spike |
| ----- | :---- | :---- | :---- | :---- | :---- | :---- | ----- |
| **1.1** |  |  |  |  |  |  | **N** |
| **1.2** |  |  |  |  |  |  | **N** |
| **1.3** |  |  |  |  |  |  | **N** |

## **\[It should be handled at the each SA’s level\] SA-2: Intent Extraction  \[P0\]  \[BOTH\]  \[Spike Required\]**

| Classification Description | Triggered after caller identity is confirmed. Analyzes caller's stated reason for calling, sentiments, classifies intent, and determines required record action. Supported intents \- claim, prior auth, provider search & network inquiry, knowledge (member benefits). The agent should confirm the intent. If we can correct the intent, let's give one retry before escalating to a human agent. |
| :---- | :---- |
| **SF Objects Affected** | VoiceCall (transcript read-only), ConversationEntry (off core) for chat transcripts.  |
| **Scope (CAN do)** | Extract all applicable intents from sanitized transcript. Map intent to record action. Detect follow-up signals (prior case or case number mentioned). Route to SA-3 for follow-up, or SA-4/5/6 for new record creation. Multiple intents can be detected over a call, and agent should extract all intents Per intent detected will tie to a separate case (either existing or new). Connect with SA-2 for case management. Escalate to human agent when intent classification fails after 1 retry. Escalate to human agent when caller sentiment is angry, frustrated, annoyed or request is urgent |
| **Guardrails (CANNOT do)** | Do NOT create any records.  No write operations in this subagent. Do NOT pass raw transcript with PHI to LLM — use sanitized version via Einstein Trust Layer.  Do NOT proceed without a classified intent.  Do NOT keep asking the caller their intent if intent extraction fails, intent is unclear, or intent does not match existing topics, instead escalate to human agent after 1 retry. |
| **Open Questions** | Multi-intent handling *(Yes):* what is the primary intent when caller raises claims \+ eligibility \+ complaint in one call *(we should not have primary/secondary; if we need to then the first intent is primary and rest all secondary)*? Confidence score thresholds TBD *(No, we will not do)* by PM/eng. Can multiple cases be created per call?*(Yes)* |
| **Intent definition** | Intent detection would be qualified as complete only when we know what is exactly needed related to a topic ❌I need to know claim status ✅I need to know claim status for claim \# 12345 ✅I need to know claim status for claim for MRI scan that happened last week |

**Actions**

| \# | Action Name | Impl. Type | Description | Input Schema | Output Schema | Rules / Conditions | Spike |
| ----- | :---- | :---- | :---- | :---- | :---- | :---- | ----- |
| **2.1** | **Extract Call Intent** *LLM-powered intent classification from sanitized transcript.* | **Prompt** | Analyzes sanitized caller utterances using LLM to extract primary intent category and a plain-language description. Outputs confidence score used for downstream BRE routing decisions. | **sanitizedTranscript** *String* e.g. "Caller says claim was denied and wants reprocessing" **memberContext** *String* e.g. "Member: Active, Plan: Medicaid" | **intentCategory** *String* e.g. "Claim Dispute" **intentDescription** *String* e.g. "Caller disputing denied claim, requesting reprocessing" **confidenceScore** *Decimal* e.g. 0.92 **isFollowUp** *Boolean* e.g. false **mentionedCaseNumber** *String (nullable)* e.g. "CASE-001234" | null | **•** PHI: Einstein Trust Layer must sanitize transcript before LLM call **•** If confidenceScore \< threshold → trigger SA-8 (Escalation) **•** Threshold value TBD — spike required *Spike: Confidence threshold value; multi-intent scoring approach* | **Y** |
| **2.2** |  |  |  |  |  |  | **Y** |
| **2.3** |  |  |  |  |  |  | **N** |

## **SA-2: Case Management  \[P0/P1\]  \[BOTH\]**

| Classification Description | Triggered only when SA-2 detects a matching intent corresponding to added subagents in the Agent. We are planning to use the existing get/create/update/close case actions, and add a send-email action when the call ends if a new case was created and remains open.  |
| :---- | :---- |
| **SF Objects Affected** | Case ~~(read-only SOQL search)~~ Engagement Topic (To link case with Engagement Topic created) |
| **Scope (CAN do)** | Search an existing case if  intent implies ongoing work Create a case if doesn’t exist already If no follow up is needed, close the case. Else keep the case open. Generate case summary and update same to Case Description field Send email for open cases for caller to reference the case number for future conversations |
| **Search Case** | When the intent implies ongoing work. If call transcription mentions below: following up for a case following up on an earlier request calling to check… I called last week… What’s the status of my complaint / dispute? I haven’t heard back yet I want to check status for an existing case Ask the caller: "Is this something you've already spoken to us about?" If yes, ask for case number  Search by case number using the existing OOTB ‘Get case xx’ action(s). There are 3 versions of ‘Get case’ action \- Engineering to decide which action makes more sense.  Read all case record fields once found. If an existing case is not found, escalate to a human agent \- “I’m having trouble retrieving your case details, let me connect you to a representative to help further.” |
| **Create Case** | A case is created for every intent corresponding to an issue / inquiry member makes. There can be multiple cases created for multiple unrelated inquiries on the same call Caller starts with benefit question → becomes grievance mid-call Provider calls for 3 different claims in one call If no follow-up work is required, we auto-close the case (STATUS \= CLOSED). Else, keep the case open (STATUS \= NEW) Each case should be attached to a corresponding Engagement Topic record (SA-3) Refer to case object on G-sheet for fields to be used for case creation |
| **Close Case** | When no follow up work is needed, auto-close the case Summarize case on Description field using existing feature (Einstein work summaries) |
| **Send Email** | Send email for open cases. Format below: Subject: Update on Your Recent Inquiry Dear \[Member Name\], Thank you for contacting us regarding your query. We have recorded the details and our team is currently reviewing it. Your reference number is **\[Case ID\]**. Please keep this handy for any follow-up. We will get back to you with an update as soon as possible.  Thank you for your patience.  |
| **Guardrails (CANNOT do)** | Do NOT create a new case before completing existing case search for follow-up calls. If no case found or multiple cases found → escalate to a human agent after informing the caller (do not attempt to pick one).  Do NOT update existing cases here — that is handled in SA-4 or SA-8. |
| **Open Questions** | If a member is following up: create a new child case linked to existing, OR update existing case with notes? TBD with [Product Owner] (Gap Item \#4 from Script Matrix gap analysis). |
| **Scenarios for case creation** | **When call gets dropped**: Before intent detected: ***No case created*** Intent\_1 detected, but during answering query for this intent: ***Case created*** Post intent\_1 detection, VA yet to answer query for this intent: ***Case created*** Post intent\_2 detected, answered query for intent\_1 but answering query associated with intent\_2 in progress / not started: ***Create case for both intents***  **When Call is Escalated** Before intent detected: No case created Intent\_1 detected, but during answering query for this intent: ***No Case created*** Post intent\_1 detection, VA yet to answer query for this intent: ***No Case created*** Post intent\_2 detected, answered query for intent\_1 but answering query associated with intent\_2 in progress / not started: ***Create case for completed intent only*** |

**Actions**

| \# | Action Name | Impl. Type | Description | Input Schema | Output Schema | Rules / Conditions | Spike |
| ----- | :---- | :---- | :---- | :---- | :---- | :---- | ----- |
| **3.1 \[P0\]** | **Search Case by Case Number** *Direct SOQL lookup using caller-provided case number.* | **Flow** | Performs a SOQL lookup on the Case object using the caller-provided case number, scoped to the identified member. Most reliable follow-up path. | **caseNumber** *String* e.g. "CASE-001234" **memberId** *String* e.g. "001..." | **caseId** *String* e.g. "500..." **caseStatus** *String* e.g. "Open" **caseSubject** *String* e.g. "Denied claim reprocessing" **caseFound** *Boolean* e.g. true | **•** If caseFound \= true → confirm with caller and proceed with existing case context **•** If caseFound \= false → VA says: "I'm having trouble retrieving your case details, let me connect you to a representative." → Trigger SA-8 | **N** |
| **3.2 \[P1\]** | **Search Case by Intent & Recency** *Fuzzy case search when caller has no case number.* | **Apex** **Flow** | Searches recent open cases (last 60 days) matching the caller's described intent when caller has no case number. SOQL with ORDER BY LastModifiedDate DESC LIMIT 10\. | **memberId** *String* e.g. "001..." **intentKeywords** *String* e.g. "claim denied reprocessing" **lookbackDays** *Integer* e.g. 60 | **matchedCases** *List\<{caseId, caseNumber, subject, lastModified}\>* e.g. max 10 results **matchCount** *Integer* e.g. 2 **searchStatus** *String (Enum)* e.g. "SINGLE\_MATCH" | "MULTIPLE\_MATCHES" | "NO\_MATCH" | **•** SINGLE\_MATCH → confirm with caller, proceed with that case **•** MULTIPLE\_MATCHES → VA: "I found multiple open cases... let me connect you to a representative." → SA-8 **•** NO\_MATCH → VA: "I'm having trouble retrieving your case details..." → SA-8 | **N** |
|  |  |  |  |  |  |  |  |

## 

| Classification Description | Triggered for fresh inquiry  ~~BRE returns~~ CREATE\_CASE. Intent involves investigation, dispute, complaint, or back-office work that cannot be resolved in real time. Creates Interaction \+ Case records pre-filled from transcript. Auto-closes if issue resolved during call. |
| :---- | :---- |
| **SF Objects Affected** | Case (write), Interaction / Engagement Interaction (write), VoiceCall (read, link) |
| **Scope (CAN do)** | Create one Interaction record per call. Create one Case per distinct inquiry (multiple cases allowed per Interaction per Accenture/Molina patterns). Pre-fill Case from transcript using AI-generated subject and description. Auto-close if resolved during call. Link Case to VoiceCall and Interaction. |
| **Guardrails (CANNOT do)** | Do NOT pass PHI (name, DOB, SSN) to LLM for case subject/description generation — Einstein Trust Layer required. Do NOT create a Case if BRE returned TASK or ACTIVITY. Do NOT skip Interaction creation — every call must have an Interaction record. |
| **Open Questions** | Interaction vs. Engagement Interaction object — which to use? (Spike S-02). Timing: Interaction before or after VoiceCall record creation? Multiple cases per call: confirm with [Product Owner]. Auto-close logic thresholds TBD. |

**Actions**

| \# | Action Name | Impl. Type | Description | Input Schema | Output Schema | Rules / Conditions | Spike |
| ----- | :---- | :---- | :---- | :---- | :---- | :---- | ----- |
| **4.1** | **Create Interaction Record** *Parent record for every call. Required before Case creation.* | **Flow** | Creates a parent Interaction (or Engagement Interaction) record for the voice call. Every call gets exactly one Interaction regardless of outcome. Must succeed before Case creation. | **voiceCallId** *String* e.g. "0MX..." **memberId** *String* e.g. "001..." **channel** *String* e.g. "Voice" **startTime** *DateTime* e.g. "2026-04-13T09:00:00Z" | **interactionId** *String* e.g. "0FT..." (or Engagement Interaction ID) **interactionCreated** *Boolean* e.g. true | **•** One Interaction per call — do not create duplicates **•** Must succeed before Case creation proceeds **•** Spike S-02: Interaction vs. Engagement Interaction object; timing vs. VoiceCall record *Spike: Confirm object: Interaction vs. Engagement Interaction; timing with [Engineer]* | **Y** |
| **4.2** | **Generate Case Subject & Description** *AI-generated case content — custom prompt, not generic SCV summary.* | **Prompt** | Uses a custom prompt template to generate concise, structured Case subject and description from sanitized transcript. NOT the generic SCV summary — this is a purpose-built case documentation prompt. | **sanitizedTranscript** *String* e.g. "Caller contacted to dispute denied claim..." **intentCategory** *String* e.g. "Claim Dispute" **intentDescription** *String* e.g. "Caller disputing denied claim, requesting reprocessing" | **caseSubject** *String (max 255 chars)* e.g. "Member dispute: denied claim reprocessing request" **caseDescription** *String* e.g. "Member called to dispute a denied claim and requested reprocessing." | **•** PHI: Einstein Trust Layer must strip member name, DOB, SSN before LLM call **•** Prompt template is custom — NOT the generic SCV call summary (per [Solution Engineer]) **•** Subject must be under 255 characters **•** Spike S-03: Custom prompt template design — discuss with [Engineer] *Spike: Custom prompt template design — [Engineer]* | **Y** |
| **4.3** | **Create Case Record** *Core wrap-up action — creates pre-filled Case from call data.* | **Flow** | Creates the Case record with all fields pre-populated from transcript data and member context. Links to Interaction and VoiceCall records. Supports multiple cases per call under one Interaction. | **memberId** *String* e.g. "001..." **accountId** *String* e.g. "001..." **recordType** *String* e.g. "Complaint" | "Inquiry" | "Grievance" **priority** *String* e.g. "High" | "Medium" | "Low" **subject** *String* e.g. "Member dispute: denied claim reprocessing" **description** *String* e.g. "Member called to dispute..." **interactionId** *String* e.g. "0FT..." **voiceCallId** *String* e.g. "0MX..." **origin** *String* e.g. "Phone" | **caseId** *String* e.g. "500..." **caseNumber** *String* e.g. "CASE-001234" **caseCreated** *Boolean* e.g. true | **•** One case per distinct inquiry; multiple cases allowed under one Interaction **•** Case must be linked to VoiceCall via ActivityId or custom lookup **•** For regulated books: case required for every inquiry for audit trail compliance | **N** |
| **4.4** | **Auto-Close Case** *Closes case immediately if resolved during the call.* | **Flow** | If the inquiry is fully resolved within the call, closes the Case and records resolution details. Wrap-up summary (SA-7) must still execute even after auto-close. | **caseId** *String* e.g. "500..." **resolutionSummary** *String* e.g. "Claim status confirmed during call. No further action required." **resolvedDuringCall** *Boolean* e.g. true | **caseStatus** *String* e.g. "Closed" **closureReason** *String* e.g. "Resolved during call" | **•** Only fires if resolvedDuringCall \= true **•** SA-7 (wrap-up summary) must still execute after auto-close **•** Both VoiceCall and Case statuses should show Completed/Closed (per Accenture pattern) | **N** |

## **SA-3: Engagement Creation  ★ Wrap-Up Core  \[P0\]  \[BOTH\]**

| Classification Description | Required to capture engagement. Usually created along with the Voice Call object. Create & update Engagement interaction record and link with VoiceCall or Conversation / Messaging record  Create & update Engagement attendee record linked with Engagement interaction and caller AccountId Create & update Engagement topic record(s) per each case created / searched. Link with case searched / created |
| :---- | :---- |
| **SF Objects Affected** | EngagementInteraction, EngagementAttendee, EngagementTopic |
| **Scope (CAN do)** | Create & update Engagement records & link with related Voice Call, Conversation / Messaging, Account & Case |
| **Guardrails (CANNOT do)** | DO not create EngagementInteraction, EngagementAttendee record if they already exist associated with  current Voice Call, Conversation / Messaging records |
| **Open Questions** | Create EngagementInteraction & EngagementAttendee records before IDV. Create EngagementTopic record(s) after case is created/searched |

**Actions**

| \# | Action Name | Impl. Type | Description | Input Schema | Output Schema | Rules / Conditions | Spike |
| ----- | :---- | :---- | :---- | :---- | :---- | :---- | ----- |
| **5.1** |  |  |  |   |  |  | **N** |
| **5.2** |  |  |  |  |  |  | **N** |
| **5.3** |  |  |  |  |  |  | **N** |

## **SA-4: Call/Chat Summary ★ Wrap-Up Core  \[P0\]  \[BOTH\]  \[Spike Required\]**

| Classification Description | Triggered at call wrap-up — when AFV resolves the caller's request, transfers to human, or call ends. We'll use existing summaries from Einstein work summaries and use Update Record action to stamp on voice call record \- if using Update Record is complex, please explore a simpler way to do that.  There will be 2 types of summaries \- voice call summary and case summary (Refer SA-2) which gets stored on respective records.  |
| :---- | :---- |
| **SF Objects Affected** | VoiceCall (read, update), Case, Engagement Interaction / Timeline (write) |
| **Scope (CAN do)** | Retrieve transcript from VoiceCall object via SCV API using VoiceCallId. Generate a custom AI summary using a use-case-specific prompt template (NOT the generic SCV summary). Attach summary, transcript link, and sentiment ~~score~~ to the target record. Update Engagement timeline. Must always execute — even for auto-closed cases or escalated calls. |
| **Guardrails (CANNOT do)** | Do NOT use generic SCV summary as the primary case summary — custom prompt is required per [Solution Engineer] guidance. Do NOT pass PHI/PII to the LLM prompt — Einstein Trust Layer required. Do NOT skip summary generation for escalated or auto-closed calls. Do NOT generate a summary before call intent is resolved (or transfer initiated). |
| **Open Questions** | Does AFV auto-write transcript to VoiceCall object, or requires separate SCV API call? Which object/field stores AI summary on Case? *(Description field)* Does timeline update require explicit Engagement record creation, or is it automatic? *(Explicit)* Discuss with [Engineer] (voice agent call summary). Where does this summary reside? (where will this be rendered?) |

**Actions**

| \# | Action Name | Impl. Type | Description | Input Schema | Output Schema | Rules / Conditions | Spike |
| ----- | :---- | :---- | :---- | :---- | :---- | :---- | ----- |
| **7.1** | **Retrieve Transcript from VoiceCall** *Fetches full transcript and sentiment from SCV API via VoiceCallId.* | **Flow** | Fetches full call transcript and real-time sentiment from the VoiceCall object via SCV API. Source of truth for all AI-generated content downstream in this subagent. | **voiceCallId** *String* e.g. "0MX..." **orgId** *String* e.g. "00D..." | **transcriptText** *String* e.g. "Agent: Thank you for calling. Caller: I need help with..." **transcriptAvailable** *Boolean* e.g. true **sentimentScore** *String* e.g. "Neutral" | "Satisfied" | "Frustrated" | "Angry" **callDurationSeconds** *Integer* e.g. 247 | **•** If transcriptAvailable \= false → log error, still attempt summary from partial data **•** AFV uses OpenAI for sentiment; SCV sentiment analysis availability TBD — confirm with eng **•** Spike S-04: Does AFV auto-write transcript to VoiceCall? Or separate SCV API call needed? *Spike: Does AFV auto-write transcript to VoiceCall? Which summary object?* | **Y** |
| **7.2** | **Generate Custom Call Summary** *Custom Prompt Template — use-case-specific, not generic SCV summary.* | **Prompt** | Generates a structured, use-case-specific call summary using a custom prompt template designed for Health Cloud contact center context. NOT generic free-form text. Per [Solution Engineer]: do NOT use the generic SCV summary. | **sanitizedTranscript** *String* e.g. "Caller contacted to dispute denied claim CLM-99001..." **intentCategory** *String* e.g. "Claim Dispute" **recommendedAction** *String* e.g. "CREATE\_CASE" **resolvedDuringCall** *Boolean* e.g. false | **summaryText** *String* e.g. "Call Summary: Member called to dispute denied claim (CLM-99001). Agent confirmed denial reason and initiated reprocessing. Case CASE-001234 created. No resolution during call." **keyActionsCompleted** *List\<String\>* e.g. \["Case created", "Claim dispute logged"\] | **•** PHI: Einstein Trust Layer must mask member name, DOB, SSN before LLM call **•** Custom prompt template — NOT the generic SCV summary (per [Solution Engineer]) **•** Summary fires even for escalated and auto-closed calls **•** Spike S-03: Review custom prompt design with [Engineer] *Spike: Prompt template design — discuss with [Engineer]* | **Y** |
| **7.3** | **Attach Summary & Sentiment to Record** *Writes summary and sentiment to Case, Task, or Activity record.* | **Flow** | Attaches the AI-generated call summary and sentiment score to the target record (Case, Task, or Activity). Also updates the VoiceCall record fields. | **summaryText** *String* e.g. "Call Summary: Member called to dispute..." **sentimentScore** *String* e.g. "Frustrated" **targetRecordId** *String* e.g. "500..." | "00T..." | "00U..." **targetObjectType** *String* e.g. "Case" | "Task" | "Activity" **voiceCallId** *String* e.g. "0MX..." | **attachmentStatus** *String* e.g. "SUCCESS" | "FAILURE" **updatedRecordId** *String* e.g. "500..." | **•** Confirm with eng: summary stored in Description field, related record, or custom summary field? **•** Must also update VoiceCall record to reflect final call outcome **•** Spike S-05: Which field/object stores the summary on Case? *Spike: Which field/object stores summary on Case? VoiceCall has no native summary field.* | **Y** |
| **7.4** | **Attach Transcript to Case / VoiceCall** *Links VoiceCall (with transcript) to Case record.* | **Flow** | Links the VoiceCall record (which holds full transcript) to the Case record so human agents can access the full transcript directly from the Case. VoiceCall.ActivityId links to Task natively — confirm if custom lookup needed for Case. | **voiceCallId** *String* e.g. "0MX..." **caseId** *String* e.g. "500..." **interactionId** *String* e.g. "0FT..." | **linkStatus** *String* e.g. "SUCCESS" | "FAILURE" **linkedRecordId** *String* e.g. "500..." | **•** VoiceCall.ActivityId → links to Task natively. Confirm if custom lookup needed for Case **•** If VoiceCall → Case link not OOTB: custom lookup field on VoiceCall required (per discovery doc) **•** Spike S-06: No OOTB direct relationship between VoiceCall and Case confirmed in discovery *Spike: VoiceCall ↔ Case relationship — OOTB or custom lookup required?* | **Y** |
| **7.5** | **Update Engagement Timeline** *Ensures Case/Task/Activity appear on member's Engagement timeline.* | **Flow** | Creates or updates the Engagement data model record so that the interaction, case, and associated records appear on the member's timeline component in Health Cloud UI. Spike needed to confirm if explicit creation is required. | **interactionId** *String* e.g. "0FT..." **caseId** *String (nullable)* e.g. "500..." | null **taskId** *String (nullable)* e.g. "00T..." | null **activityId** *String (nullable)* e.g. "00U..." | null **memberId** *String* e.g. "001..." | **timelineUpdated** *Boolean* e.g. true **engagementRecordId** *String* e.g. Engagement record ID | **•** Spike needed: does creating an Engagement record auto-populate timeline, or must it be explicitly triggered? **•** Connect with [Engineer] (Engagement data model owner) per PRD **•** Spike S-07 *Spike: Does timeline update auto on Engagement record creation? Discuss with [Engineer].* | **Y** |

## **\[Exist\] SA-5: Knowledge \- Member Plan  \[P0\]**  

| Classification Description | Triggered when caller intent is about a member plan and coverage inquiry. Caller needs to provide MemberId (if already not available). Leverage existing "[Answer Questions with Knowledge](https://help.salesforce.com/s/articleView?id=ai.copilot_actions_ref_answer_questions_with_knowledge.htm&type=5)" OOTB subagent.  Voice Agent will have this subagent shipped OOTB w/o data library integration.Customers will configure their own data library and for internal demo purpose, this subagent will showcase how knowledge can be integrated to answer member inquiries queries. This It should do both \- act as grounding data to support other inquiries, and directly answer member-plan-related questions. |
| :---- | :---- |
| **SF Objects Affected** | NA |
| **Scope (CAN do)** | Used for answering member plan and benefits related queries  |
| **Guardrails (CANNOT do)** | Use existing guardrails for Claims Assistant Subagent |

**Actions**

| \# | Action Name | Impl. Type | Description | Input Schema | Output Schema | Rules / Conditions | Spike |
| ----- | :---- | :---- | :---- | :---- | :---- | :---- | ----- |
| **8.1** |  |  |  |  |  |  | **N** |
| **8.2** |  |  |  |  |  |  | **N** |

## **\[Exist\] SA-6: Escalation  \[P0\]  \[AFV→SCV\]**

| Classification Description | Triggered when: (1) fails to identify/verify caller; (2) caller explicitly requests human agent; (3) sentiment (Frustrated/Angry/Urgent); (4) intent is unclear, or intent does not match existing topics; (5) existing case search fails after one-retry; (6) any place VA fails; (7) proxy caller requires human judgment; (8) external API failure. |
| :---- | :---- |
| **SF Objects Affected** | VoiceCall (read), Omni-Channel routing, ~~Screen Pop (SCV),~~ Case |
| **Scope (CAN do)** | Transfer call to human agent via Omni-Channel routing. Preserve all context: member record, partial transcript summary, any draft case/task created before escalation, escalation reason, sentiment. Pre-populate agent screen pop. SA-7 (summary/attachment) must still execute after escalation. Customers will be responsible for setting up escalation routing The VA should have the OOTB escalation topic already added BUT no escalation routing to be shipped. Documentation should guide to configure escalation  Use existing “Conversation catch up” feature to let the human agent know about the discussion happened so far  |
| **Guardrails (CANNOT do)** | Do NOT terminate the call before transferring. Do NOT create new records after escalation triggers — preserve whatever was created before. Do NOT require the human agent to re-identify the caller. If a transfer fails, inform the caller and offer a callback. Create a case for a call back. |
| **Open Questions** | ~~What exact sentiment score threshold triggers escalation (specific value)?~~ Should records created by AFV before escalation be preserved or voided? *(Yes)* Does human agent override of AI decision need to be captured for audit? *(This will be out of scope)* |

**Actions**

| \# | Action Name | Impl. Type | Description | Input Schema | Output Schema | Rules / Conditions | Spike |
| ----- | :---- | :---- | :---- | :---- | :---- | :---- | ----- |
| **8.1** | **Initiate Human Transfer via Omni-Channel** *Routes call from AFV to human agent queue via Omni-Channel.* | **Flow** | Transfers the active voice call from AFV to the appropriate human agent queue using Omni-Channel routing. Preserves VoiceCallId for full context continuity to the human agent. | **escalationReason** *String (Enum)* e.g. "CALLER\_REQUESTED" | "LOW\_SENTIMENT" | "UNRESOLVED\_INTENT" | "MULTIPLE\_CASES" | "ID\_FAILURE" | "API\_FAILURE" **targetQueue** *String* e.g. "MemberServices\_Queue" **voiceCallId** *String* e.g. "0MX..." **memberId** *String* e.g. "001..." **draftCaseId** *String (nullable)* e.g. "500..." | null | **transferStatus** *String* e.g. "SUCCESS" | "FAILURE" **assignedAgentId** *String* e.g. "005..." **queueWaitTime** *Integer (seconds)* e.g. 45 | **•** If transferStatus \= FAILURE → inform caller, offer callback (create Task) **•** SA-7 (summary \+ attachment) must execute immediately after transfer is initiated **•** Open Q: Exact sentiment threshold value needed — TBD with PM | **N** |
| **8.2** | **Populate Agent Screen Pop** *Pre-loads human agent UI with member context and transcript summary.* | **Flow** | Automatically populates the human agent's screen with member record, sentiment indicator, transcript summary, escalation reason, and any draft Case/Task created during the autonomous call. Agent must NOT need to re-identify the caller. | **memberId** *String* e.g. "001..." **memberName** *String* e.g. "Anna Liu" **sentimentScore** *String* e.g. "Frustrated" **transcriptSummary** *String* e.g. "Caller disputing denied claim CLM-99001. Escalated due to low sentiment." **draftCaseId** *String (nullable)* e.g. "500..." | null **escalationReason** *String* e.g. "LOW\_SENTIMENT" **voiceCallId** *String* e.g. "0MX..." | **screenPopDisplayed** *Boolean* e.g. true **agentContextRecordId** *String* e.g. VoiceCall or Case ID surfaced to agent | **•** Human agent must NOT need to re-identify the caller or re-read raw transcript **•** Sentiment indicator should be visually prominent in screen pop (design requirement) **•** SCV screen pop configuration required in agent setup | **N** |

## **\[Exist\] SA-7: Claims Assistant Subagent  \[P0\]**  

| Classification Description | Triggered when caller intent is about a claim inquiry. Caller needs to provide MemberId (if already not available) or ClaimId to search for a claim. |
| :---- | :---- |
| **SF Objects Affected** | Claim DMO, Claim Item DMO, Claim Participant DMO |
| **Scope (CAN do)** | Use existing scope for Claims Assistant Subagent |
| **Guardrails (CANNOT do)** | Use existing guardrails for Claims Assistant Subagent |

## **\[Exist\] SA-8: Find Prior Auth  \[P0\]** 

| Classification Description | Triggered when caller intent is about a prior auth inquiry. Caller needs to provide MemberId (if already not available) or Prior Auth to search for a prior auth. |
| :---- | :---- |
| **SF Objects Affected** | Case DMO, Care Request Item DMO, Care Request Item DMO, Care Drug Request DMO |
| **Scope (CAN do)** | Use existing scope for Prior Auth Assistant Subagent |
| **Guardrails (CANNOT do)** | Use existing guardrails for Prior Auth Assistant Subagent |

## **\[Exist\] SA-9: Provider Network Search  \[P0\]**  

| Classification Description | Triggered when caller intent is about searching a provider or finding a provider’s network status.  |
| :---- | :---- |
| **SF Objects Affected** | Healthcare Provider DMO, Healthcare Provider NPI DMO (Uses Mulesoft) |
| **Scope (CAN do)** | Use existing scope for Provider Network Search Subagent |
| **Guardrails (CANNOT do)** | Use existing guardrails for Provider Network Search Subagent |

# **Appendix: Spike Inventory**

*All items below require technical investigation and confirmation before sprint planning. Spike owners to be assigned in team sync.*

| \# | Spike Description | Subagent / Action | Linked PRD Question | Suggested Owner | Priority | Notes |
| ----- | :---- | :---- | :---- | :---- | ----- | :---- |
| **S-01** | Intent extraction confidence scoring: what threshold triggers escalation? Is multi-intent supported — can multiple cases be created for multiple issues raised in one call? | SA-2: Actions 2.1, 2.2 | *"Will we need an intent extraction confidence score? Can multiple cases be created in a call?"* | [PM] / [Architect] | **P0** | *Required before BRE flow config* |
| **S-02** | Interaction vs. Engagement Interaction object: which to use for the parent call record? Timing — created before or after VoiceCall record creation? | SA-4: Action 4.1 | *"Should we use the interaction object or engagement interaction object?" (highlighted in red in discovery doc)* | [Architect] / [Engineer] | **P0** | *Data model blocker* |
| **S-03** | Custom call summary prompt template design: structure, fields, and output format for use-case-specific case documentation. NOT the generic SCV summary. | SA-4: 4.2 · SA-7: 7.2 | *"Create a custom prompt focused on the specific use case, instead of using the general summary." — [Solution Engineer]* | [UX Designer] / [Engineer] | **P0** | *Design \+ eng joint spike* |
| **S-04** | Does AFV automatically write transcript to VoiceCall object, or requires a separate SCV API call with VoiceCallId? What is the API endpoint and response structure? | SA-7: Action 7.1 | *"Both platforms provide transcription accessible via Service Cloud APIs using the voice call ID, which must be part of the action." — [Solution Engineer] & [Engineer]* | [Architect] / Eng | **P0** | *Blocks SA-7 entirely* |
| **S-05** | Which field or related object stores the AI-generated summary on the Case record? VoiceCall object has no native summary field. | SA-7: Action 7.3 | *"Where is the call summary stored? Which object? Voice Call object doesn't have any summary fields." — [Platform Advisor]* | [Architect] / [Engineer] | **P0** | *Data model decision needed* |
| **S-06** | VoiceCall ↔ Case object relationship: no OOTB direct relationship exists. Custom lookup field on VoiceCall referencing Case (or vice versa) likely required. | SA-7: Action 7.4 | *"No out-of-the-box direct relationship between VoiceCall and Engagement Interaction objects." — Discovery doc (PDF 2, p.1)* | [Architect] / Eng | **P0** | *Custom object config required* |
| **S-07** | Engagement Timeline update: does creating an Engagement record auto-populate the member timeline component, or does explicit linking require a separate configuration step? | SA-7: Action 7.5 | *"Needs spike to determine if we need to explicitly create separate records in the Engagement data model."* | [Architect] / [Engineer] | **P0** | *Talk to [Engineer]* |
| **S-08** | Sentiment analysis availability: AFV uses OpenAI for sentiment; SCV does not currently offer real-time sentiment. When will SCV get it? Can AFV sentiment integrate with SCV-only orgs? | SA-7: 7.1 · SA-8: 8.1 | *"Sentiment analysis when AFV isn't used and when will SCV get it? Can we integrate AFV sentiment with SCV?"* | Eng / Salesforce Voice PM | **P1** | *Affects SCV-only orgs only* |
| **S-09** | Review existing SCV framework for call wrap-up to assess overlap with custom BRE flow in SA-2. Connect with [Partner SME] from KPMG (Northwell reference implementation). | SA-2, SA-4, SA-5, SA-6 | *"Yes, check SCV framework" — PRD Spikes section* | [Architect] / [Partner SME] (KPMG) | **P1** | *Reference: Northwell impl* |
| **S-10** | Follow-up case handling: create new child case linked to existing, OR update existing case with additional notes? TBD with [Product Owner] — this is gap item \#4 from Script Matrix analysis. | SA-3, SA-4 | *"If a member is following up for an existing case, should we create a new case & attach it to the existing case OR update the existing case with additional notes?" — [Platform Advisor]* | [Product Owner] (PO) | **P0** | *Gap item \#4 — pending PO decision* |

*Document Status: v1.0 Draft · April 2026 · Author: [UX Designer] Kim · For internal review with engineering and PO. All spikes and open questions must be resolved before sprint planning.*