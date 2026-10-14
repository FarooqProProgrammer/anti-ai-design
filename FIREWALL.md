# AI Request Firewall Specification

The **Request Firewall** is the mandatory admission controller and governance gatekeeper for all tasks entering the development lifecycle. No code can be edited, no test can be bypassed, and no feature can be shipped without sequentially clearing the Firewall gates.

---

## Firewall Principle & Non-Bypassable Rule

```
[ INCOMING REQUEST ]
        │
        ▼
╔════════════════════════════════════════════════════════════════════╗
║                      AI REQUEST FIREWALL                           ║
║   Every request must pass sequentially through all 6 gates.        ║
║   Any agent (Cursor / Claude / Codex) can execute all steps.       ║
║   Shortcuts, skipped phases, and unauthorized edits are BLOCKED.   ║
╚════════════════════════════════════════════════════════════════════╝
        │
   [GATE 1] ──► 1. UNDERSTAND            (Any Agent: Read-Only Reconnaissance)
        │
   [GATE 2] ──► 2. PLAN                  (Any Agent: Risks & Acceptance Criteria)
        │
   [GATE 3] ──► 3. IMPLEMENT             (Primary Driver: Core Logic & Refinement)
        │
   [GATE 4] ──► 4. VERIFY                (Checks, Runtime Behavior, Zero Concealment)
        │
   [GATE 5] ──► 5. REVIEW INDEPENDENTLY  (Auditor: Diff Audit Without Editing)
        │
   [GATE 6] ──► 6. SHIP SAFELY           (Branch Hygiene, Conventional Commit, CI/CD)
```

> [!NOTE]
> **UNIVERSAL AGENT EXECUTION POLICY:**
> This workflow does not lock tasks to a single tool. **Cursor can execute all 6 steps.** **Claude Code can execute all 6 steps.** **Codex can execute all 6 steps.** Or they can collaborate seamlessly.
> The Firewall governs the **process discipline and quality gates**, ensuring that whichever agent is active never takes shortcuts.

> [!CAUTION]
> **FIREWALL INTERCEPT RULE:**
> If a user prompts: *"Just quickly fix this file"*, *"Generate the code for X"*, or *"Skip tests and merge"*, the Firewall **intercepts and enforces the process**:
> 1. Understand the problem and codebase patterns.
> 2. Formulate a plan and acceptance criteria.
> 3. Implement with a single driver.
> 4. Verify completely.
> 5. Review independently without editing.
> 6. Ship safely.

---

## The 6 Firewall Enforcement Gates

### Gate 1: Understand
- **Applicable Agents**: Cursor, Claude Code, Codex, Antigravity.
- **Mandatory Skills**: `skills/brainstorming/` and `skills/grill-me/`.
- **Admission Check**: Does the agent understand the affected files, call stack, existing patterns, and has it interviewed the user/spec to clarify all edge cases?
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Any attempt to write, edit, or delete source code during Phase 1.
  - 🛑 **BLOCKED**: Proceeding without applying **Brainstorming** (goals/anti-goals, trade-offs) and **Grill-Me** (Socratic decision-tree questioning).
  - 🛑 **BLOCKED**: Proceeding without consulting `wiki/index.md` or existing design patterns.
- **Exit Condition**: Documented context snapshot (clarified edge cases, resolved trade-offs, files impacted, patterns detected, technical constraints).

### Gate 2: Plan
- **Applicable Agents**: Cursor, Claude Code, Codex, Antigravity.
- **Admission Check**: Are the requirements investigated, edge cases forecasted, and acceptance criteria testable?
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Starting implementation without an explicit, approved plan.
  - 🛑 **BLOCKED**: Plans lacking concrete Acceptance Criteria (Given-When-Then) or Risk Analysis.
  - 🛑 **BLOCKED**: Unresolved external RFCs/specs (must be ingested into `raw/` and compiled in `wiki/`).
- **Exit Condition**: Explicit human or lead engineer sign-off on the implementation plan.

### Gate 3: Implement (Single Driver)
- **Applicable Agents**: Cursor, Claude Code, Codex, Antigravity.
- **Admission Check**: Is implementation owned by a single primary driver (either Cursor alone, or Claude/Codex with Cursor frontend tuning)?
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Multi-driver chaos (switching core business logic ownership back and forth between competing agents during a run).
  - 🛑 **BLOCKED**: Scope creep (modifying files or abstractions outside the approved Phase 2 plan).
- **Exit Condition**: Complete implementation satisfying the Phase 2 plan and initial unit tests.

### Gate 4: Verify (Zero-Concealment)
- **Applicable Agents**: Any Agent + Test Runner / Environment.
- **Admission Check**: Do all automated checks pass, and has actual runtime behavior been tested?
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Concealed failures (commented-out tests, disabled assertions, `@ts-ignore`, `eslint-disable`).
  - 🛑 **BLOCKED**: Failing test suites, type errors, or lint warnings.
  - 🛑 **BLOCKED**: Inconsistent wiki evidence (`python skills/karpathy-llm-wiki/scripts/check_evidence.py` reports errors).
- **Exit Condition**: 100% green checks with failure logs transparently resolved at the root cause.

### Gate 5: Review Independently (Read-Only Auditor)
- **Applicable Agents**: Any Agent in a fresh/clean context (or a separate model/agent instance).
- **Admission Check**: Has the complete `git diff` been audited without editing permissions?
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: The reviewer agent modifying, editing, or writing code.
  - 🛑 **BLOCKED**: Skipping independent review or self-approving without fresh-context diff inspection.
  - 🛑 **BLOCKED**: Unresolved High/Blocker severity findings.
- **Exit Condition**: Review report generated; all confirmed issues resolved by Primary Driver and re-verified.

### Gate 6: Ship Safely (Branch Hygiene & CI/CD)
- **Applicable Agents**: Any Agent + Lead Engineer.
- **Admission Check**: Is the git diff clean, committed on the proper branch, and verified by CI/CD?
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Committing directly to protected branches (`main`, `master`).
  - 🛑 **BLOCKED**: Lingering temporary debug code (`console.log`, `debugger`, `print()`) or un-tracked temp files.
  - 🛑 **BLOCKED**: Failing remote CI/CD status checks.
- **Exit Condition**: PR merged with conventional commits; new architecture models compounded into `wiki/`.

---

## Firewall Quick Reference Card

| Gate | Stage | Who Operates | What the Firewall Blocks |
|---|---|---|---|
| **Gate 1** | **Understand** | Any Agent + Brainstorming & Grill-Me | Writing/editing code; skipping brainstorming/interview |
| **Gate 2** | **Plan** | Any Agent (Cursor / Claude / Codex) | Coding without an approved plan & acceptance criteria |
| **Gate 3** | **Implement** | Primary Driver (Cursor / Claude / Codex) | Scope creep, competing simultaneous drivers |
| **Gate 4** | **Verify** | Any Agent + Runner | Hidden failures, suppressed errors, broken tests |
| **Gate 5** | **Review Independently** | Independent Auditor (Clean Context) | Reviewer editing code, unaddressed review blockers |
| **Gate 6** | **Ship Safely** | Driver Agent & Engineer | Committing to main, dirty diffs, failing CI pipelines |

