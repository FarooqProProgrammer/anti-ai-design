# Phase 5: Verify (Checklist & Protocol)

**Firewall Gate:** Gate 5 (Zero-Concealment Verification & Runtime Validation)  
**Target:** Any Agent / Developer Environment  
**Goal:** Verify functional correctness, regression-free behavior, and capture all test/runtime diagnostics.  
**Strict Firewall Rule:** Zero concealment. Never skip, ignore, or suppress failures. Bypassing tests is BLOCKED.

---

## Verification Protocol

```markdown
You are executing Phase 5 (Verify) of the AI Engineering Workflow.

Context:
- Implementation is complete.
- All Acceptance Criteria from Phase 3 must be tested against the Phase 2 Spec.

Mandatory Verification Checklist:

### 1. Automated Quality Gates (Risk-Tiered)
- [ ] **Git Diff Sanity**: Inspect `git diff` for stray `console.log`, temporary scratch files, or unintended modifications.
- [ ] **Type System Check**: Run compiler/typechecker (e.g. `tsc --noEmit`, `mypy`, `cargo check`). Zero type errors permitted.
- [ ] **Linting & Code Quality**: Run linter (e.g. `eslint`, `ruff`, `prettier`). Zero unhandled warnings or formatting violations.
- [ ] **Automated Test Suites**: Run unit and integration tests (e.g. `npm test`, `pytest`, `cargo test`). 100% test pass rate required.
- [ ] **Dependency & Security Vulnerability Check**: Run package audit (`npm audit`, `pip-audit`, `cargo audit`).
- [ ] **Local Build & CI Sanity**: Verify local build succeeds (`npm run build`, `make build`) before submitting to remote CI.

### 2. High-Risk Domain Stricter Checks
If the change affects any of the following high-risk domains, enforce stricter scrutiny:
- [ ] **Database Migrations**: Verify migration schema idempotency, test rollback script, confirm zero accidental data loss or column truncation.
- [ ] **Authentication & Sessions**: Test token expiration, session invalidation, credential hashing, and cookie security flags.
- [ ] **Authorization & Permissions (RBAC)**: Test cross-tenant isolation, negative permission tests (ensure unauthorized roles are blocked), and privilege escalation guards.
- [ ] **Payment & Billing**: Verify currency decimal precision, idempotency key enforcement, webhook signature verification, and race conditions under concurrent checkouts.

### 3. Runtime Behavioral Validation
- [ ] Execute actual runtime behavior via CLI, API endpoints, or user interactions.
- [ ] Verify both "Happy Path" and "Edge/Failure Modes" against Phase 3 acceptance criteria and Phase 2 spec invariants.
- [ ] Wiki evidence check (if wiki modified): Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.

### 4. Diagram
- [ ] Maintain and describe `diagrams/05-verify.exceldraw`.

---

## Evidence-Based Completion Report (Mandatory Before Gate Exit)

At the completion of Phase 5, the agent MUST output this structured report before declaring work done:

```markdown
### Evidence-Based Completion Report
1. **What changed?**:
   [Concise summary of functional behavior, architecture modifications, or bug fixes]
2. **Which files changed?**:
   [Explicit list of modified, created, or deleted files matching git status]
3. **Which tests actually passed?**:
   [Exact commands executed, test count, assertions verified, and proof of green run]
4. **What was NOT tested?**:
   [Explicit declaration of unmocked systems, third-party integrations, manual edge cases, or blind spots]
5. **Remaining risks or manual steps?**:
   [Pending database migrations, required environment variables, manual lead engineer sign-offs, or rollout considerations]
```

---

### Failure Handling Protocol (DO NOT HIDE FAILURES):
If ANY check fails:
1. Capture and log the complete failure output, error message, and stack trace explicitly.
2. DO NOT delete, disable, or comment out failing tests.
3. DO NOT use suppressions (e.g. `@ts-ignore`, `eslint-disable`, `# type: ignore`) to hide the defect.
4. Analyze root cause: Is the failure an implementation bug, a regression, or an outdated test assumption?
5. Fix the code to address the root cause and rerun all verification steps until green.
```
