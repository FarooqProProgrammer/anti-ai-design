# Phase 3: Plan (Universal Prompt Template)

**Firewall Gate:** Gate 3 (Architecture, Risk & Acceptance Criteria Approval)  
**Target Tool/Agent:** Any Agent (Cursor, Claude Code, Codex, or Antigravity)  
**Goal:** Implementation blueprint, risk assessment, acceptance criteria, and phased milestones (the HOW).  
**Strict Firewall Rule:** No code implementation may begin until this plan is approved. Direct coding is BLOCKED.

---

## Universal Plan Prompt

```markdown
You are acting in Phase 3 (Plan) of the AI Engineering Workflow.

Context from Phase 2 (Spec):
<SPEC_CONTEXT>
[Insert approved specification document or link to Phase 2 output]
</SPEC_CONTEXT>

Instructions:
Take the approved Specification and produce a structured, phased implementation plan (the HOW to build it):

### 1. Requirements Breakdown & Scope Confirmation
- Review in-scope vs. out-of-scope items from the Phase 2 Spec.
- External references / RFCs: Ingest new documentation into `raw/<topic>/` and compile into `wiki/` using `karpathy-llm-wiki`.

### 2. Risk & Impact Analysis
Identify potential failure modes, performance bottlenecks, race conditions, edge cases, or breaking changes:
| Risk / Edge Case | Likelihood | Impact | Proposed Mitigation |
|---|---|---|---|
| [Risk description] | Low/Med/High | Low/Med/High | [Mitigation strategy] |

### 3. Acceptance Criteria (Testable & Concrete)
Formulate unambiguous criteria that can be verified automatically or manually:
- [ ] AC-1: Given [precondition], When [action], Then [expected result]
- [ ] AC-2: Error handling: Given [invalid input/state], Then [expected error response]
- [ ] AC-3: Performance/Security: [Specific constraint]

### 4. Implementation Roadmap (Phased & Atomic)
Step-by-step sequential tasks:
- **Phase 4.1 - Core & Data Models**: [Specific steps, files to touch]
- **Phase 4.2 - Business Logic & Services**: [Specific steps, files to touch]
- **Phase 4.3 - UI / Integration & Wiring**: [Specific steps, files to touch]

### 5. Single Driver Assignment
Designate the Primary Driver (Cursor, Claude Code, or Codex) responsible for core logic.

### 6. Visual Diagram
- Generate and describe `diagrams/03-plan.exceldraw`.

Wait for explicit approval before proceeding to Phase 4 (Implement).
```
