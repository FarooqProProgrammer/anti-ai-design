# Phase 2: Spec (Universal Prompt Template)

**Firewall Gate:** Gate 2 (Technical & Functional Specification Approval)  
**Target Tool/Agent:** Any Agent (Cursor, Claude Code, Codex, or Antigravity)  
**Goal:** Formalize requirements into an unambiguous Technical & Functional Specification (the WHAT, not the HOW).  
**Strict Firewall Rule:** READ-ONLY on source code. No implementation code may be written. Any attempt to write code during Spec is BLOCKED.

---

## Universal Spec Prompt

```markdown
You are acting in Phase 2 (Spec) of the AI Engineering Workflow.

Context from Phase 1 (Understand):
<UNDERSTANDING_CONTEXT>
[Insert summary/output from Phase 1, interview resolutions, or trade-off decisions]
</UNDERSTANDING_CONTEXT>

Task / Feature to Specify:
<TASK_DESCRIPTION>
[Insert feature request, bug description, or technical requirement]
</TASK_DESCRIPTION>

Instructions:
Translate the understanding into a comprehensive, unambiguous Technical & Functional Specification. Do NOT propose implementation tasks or timeline milestones yet (that belongs in Phase 3: Plan). Focus purely on WHAT the system must do and WHAT it must guarantee:

### 1. Functional Specification
- **User Journeys & Scenarios**: Step-by-step user interaction flows.
- **Behavioral Invariants**: Things that MUST ALWAYS be true (e.g. "A deleted project never appears in search results").
- **State Machine Transitions**: Valid states and transition triggers.
- **Explicit Non-Features**: Explicitly declare what will NOT be supported to prevent scope drift.

### 2. Technical & Contract Specification
- **Interface & Type Signatures**: Exact TypeScript types, structs, or class signatures.
- **API Endpoints & Contracts**: Request payloads, query parameters, response bodies, and HTTP status codes.
- **Database & Data Models**: Schema changes, entity fields, foreign keys, and indexes.
- **Error Contracts**: Standard error envelopes, error codes, and failure messages.
- **External Dependencies & RFCs**: Ingest external specs into `raw/<topic>/` and compile into `wiki/`.

### 3. Non-Functional Guardrails
- **Performance Budgets**: Latency thresholds (e.g., `<50ms` response), memory/compute budgets.
- **Security & Authorization**: Auth boundaries, permissions, data sanitization, and secrets handling.
- **Concurrency & Race Conditions**: Invariants under concurrent requests.
- **Backward Compatibility & Migrations**: Breaking change analysis and zero-downtime requirements.

### 4. Diagram
- Reference and update `diagrams/02-spec.exceldraw`.

Wait for human review and sign-off on the Specification before moving to Phase 3 (Plan).
```
