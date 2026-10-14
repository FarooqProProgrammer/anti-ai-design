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
║   Shortcuts, skipped phases, and unauthorized edits are BLOCKED.   ║
╚════════════════════════════════════════════════════════════════════╝
        │
   [GATE 1] ──► 1. UNDERSTAND            (Cursor: Read-Only Reconnaissance)
        │
   [GATE 2] ──► 2. PLAN                  (Claude Code: Risks & Acceptance Criteria)
        │
   [GATE 3] ──► 3. IMPLEMENT             (Single Driver: Claude/Codex + Cursor UI)
        │
   [GATE 4] ──► 4. VERIFY                (Checks, Runtime Behavior, Zero Concealment)
        │
   [GATE 5] ──► 5. REVIEW INDEPENDENTLY  (Codex/Claude: Diff Audit Without Editing)
        │
   [GATE 6] ──► 6. SHIP SAFELY           (Branch Hygiene, Conventional Commit, CI/CD)
```

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

### Gate 1: Understand (Cursor)
- **Admission Check**: Does the agent understand the affected files, call stack, and existing patterns?
- **Tool**: Cursor.
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Any attempt to write, edit, or delete source code during Phase 1.
  - 🛑 **BLOCKED**: Proceeding without consulting `wiki/index.md` or existing design patterns.
- **Exit Condition**: Documented context snapshot (files impacted, patterns detected, technical constraints).

### Gate 2: Plan (Claude Code)
- **Admission Check**: Are the requirements investigated, edge cases forecasted, and acceptance criteria testable?
- **Tool**: Claude Code.
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Starting implementation without an explicit, approved plan.
  - 🛑 **BLOCKED**: Plans lacking concrete Acceptance Criteria (Given-When-Then) or Risk Analysis.
  - 🛑 **BLOCKED**: Unresolved external RFCs/specs (must be ingested into `raw/` and compiled in `wiki/`).
- **Exit Condition**: Explicit human or lead engineer sign-off on the implementation plan.

### Gate 3: Implement (Single Driver)
- **Admission Check**: Is implementation owned by a single primary driver with scoped frontend support?
- **Tools**: Claude Code or Codex (Primary Driver); Cursor (Interactive & UI refinement only).
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Multi-driver chaos (switching core business logic ownership between different agents).
  - 🛑 **BLOCKED**: Scope creep (modifying files or abstractions outside the approved Phase 2 plan).
  - 🛑 **BLOCKED**: Cursor rewriting backend domain models, API clients, or database schemas.
- **Exit Condition**: Complete implementation satisfying the Phase 2 plan and initial unit tests.

### Gate 4: Verify (Zero-Concealment)
- **Admission Check**: Do all automated checks pass, and has actual runtime behavior been tested?
- **Tools**: Test Runner, Linter, Typechecker, and `check_evidence.py`.
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Concealed failures (commented-out tests, disabled assertions, `@ts-ignore`, `eslint-disable`).
  - 🛑 **BLOCKED**: Failing test suites, type errors, or lint warnings.
  - 🛑 **BLOCKED**: Inconsistent wiki evidence (`python skills/karpathy-llm-wiki/scripts/check_evidence.py` reports errors).
- **Exit Condition**: 100% green checks with failure logs transparently resolved at the root cause.

### Gate 5: Review Independently (Read-Only Auditor)
- **Admission Check**: Has the complete `git diff` been audited by an independent agent?
- **Tools**: Codex or Claude Code (in a clean context / independent reviewer role).
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: The reviewer agent modifying, editing, or writing code.
  - 🛑 **BLOCKED**: Skipping independent review or self-approving without fresh-context diff inspection.
  - 🛑 **BLOCKED**: Unresolved High/Blocker severity findings.
- **Exit Condition**: Review report generated; all confirmed issues resolved by Primary Driver and re-verified.

### Gate 6: Ship Safely (Branch Hygiene & CI/CD)
- **Admission Check**: Is the git diff clean, committed on the proper branch, and verified by CI/CD?
- **Tools**: Driver Agent & Lead Engineer.
- **Firewall Blocking Conditions**:
  - 🛑 **BLOCKED**: Committing directly to protected branches (`main`, `master`).
  - 🛑 **BLOCKED**: Lingering temporary debug code (`console.log`, `debugger`, `print()`) or un-tracked temp files.
  - 🛑 **BLOCKED**: Failing remote CI/CD status checks.
- **Exit Condition**: PR merged with conventional commits; new architecture models compounded into `wiki/`.

---

## Firewall Quick Reference Card

| Gate | Stage | Who Operates | What the Firewall Blocks |
|---|---|---|---|
| **Gate 1** | **Understand** | Cursor | Writing/editing code during reconnaissance |
| **Gate 2** | **Plan** | Claude Code | Coding without an approved plan & acceptance criteria |
| **Gate 3** | **Implement** | Claude / Codex (Single Driver) + Cursor (UI) | Scope creep, multiple competing core drivers |
| **Gate 4** | **Verify** | Runner & Driver | Hidden failures, suppressed errors, broken tests |
| **Gate 5** | **Review Independently** | Codex / Claude (Auditor) | Reviewer editing code, unaddressed review blockers |
| **Gate 6** | **Ship Safely** | Driver & Engineer | Committing to main, dirty diffs, failing CI pipelines |
