# Phase 2: Plan (Universal Prompt Template)

**Firewall Gate:** Gate 2 (Architecture, Risk & Acceptance Criteria Approval)  
**Target Tool/Agent:** Any Agent (Cursor, Claude Code, Codex, or Antigravity)  
**Goal:** Deep investigation of complex requirements, risk assessment, acceptance criteria, and phased implementation blueprint.  
**Strict Firewall Rule:** No code implementation may begin until this plan is approved. Direct coding is BLOCKED.

---

## Universal Plan Prompt

```markdown
You are acting in Phase 2 (Plan) of the AI Engineering Workflow.

Context from Phase 1 (Understand):
<UNDERSTANDING_CONTEXT>
[Insert summary/output from Phase 1, or relevant file paths and existing patterns]
</UNDERSTANDING_CONTEXT>

Task Requirements:
<REQUIREMENTS>
[Insert detailed task requirements, user stories, or problem description]
</REQUIREMENTS>

Instructions:
Investigate the requirements thoroughly and produce a structured implementation plan adhering strictly to the format below:

### 1. Requirements Breakdown & Scope Boundary
- Explicit in-scope requirements
- Explicit out-of-scope items (to prevent scope creep)
- External references / RFCs: Ingest new documentation into `raw/<topic>/` and compile into `wiki/` using the `karpathy-llm-wiki` skill.
- Backward compatibility considerations and API contract impacts

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
- **Phase 3.1 - Core/Data Model**: [Specific steps, files to touch]
- **Phase 3.2 - Business Logic & Services**: [Specific steps, files to touch]
- **Phase 3.3 - UI / Integration & Wiring**: [Specific steps, files to touch]

### 5. Verification Strategy
- Test suites to add/update (unit, integration, e2e)
- Exact verification commands to run

Wait for explicit approval before proceeding to Phase 3 (Implement).
```
