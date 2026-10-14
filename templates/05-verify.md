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
1. [ ] **Type System Check**:
   - Run typechecker (e.g. `npm run type-check`, `tsc --noEmit`, `mypy`, `cargo check`).
   - Zero type errors allowed.

2. [ ] **Linting & Code Quality**:
   - Run linter (e.g. `npm run lint`, `flake8`, `golangci-lint`).
   - Verify zero new lint warnings or formatting errors.

3. [ ] **Unit & Integration Tests**:
   - Run existing and new test suites (e.g. `npm test`, `pytest`, `cargo test`).
   - Verify 100% test pass rate.

4. [ ] **Runtime Behavioral Validation**:
   - Execute the actual behavior via CLI, API request, or end-to-end user flow.
   - Test both the "Happy Path" and "Edge/Failure Cases".
   - Confirm output matches each Acceptance Criterion in the Phase 3 plan.

5. [ ] **Wiki Evidence & Grounding Check (if wiki modified)**:
   - Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.
   - Confirm all citations and factual literals in `wiki/` match immutable sources in `raw/`.

6. [ ] **Visual Diagram**:
   - Generate and describe `diagrams/05-verify.exceldraw`.

---

### Failure Handling Protocol (DO NOT HIDE FAILURES):
If ANY check fails:
1. Capture and log the complete failure output, error message, and stack trace explicitly.
2. DO NOT delete, disable, or comment out failing tests.
3. DO NOT use suppressions (e.g. `@ts-ignore`, `eslint-disable`, `# type: ignore`) to hide the defect.
4. Analyze root cause: Is the failure an implementation bug, a regression, or an outdated test assumption?
5. Fix the code to address the root cause and rerun all verification steps until green.
```
