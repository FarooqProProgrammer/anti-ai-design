# Codex Instructions — Universal AI Engineering Workflow

This codebase operates under a strict 6-Phase AI Engineering Workflow governed by a mandatory **Request Firewall** ([FIREWALL.md](FIREWALL.md)).

> 🛡️ **REQUEST FIREWALL PROTOCOL:**
> Every incoming request must proceed through the sequential 6-phase firewall:
> `Understand ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely`.
> You can execute **any or all** of these phases. Always adhere to each gate's rules.

---

## Universal Capabilities Across All 6 Phases

### 1. Phase 1: Understand
- Explore codebase, analyze dependencies, and trace data flow.
- Consult `wiki/index.md` for architectural context.
- **Rule:** READ-ONLY. Zero code edits during exploration.

### 2. Phase 2: Plan
- Investigate requirements, assess risks, and formulate testable Acceptance Criteria.
- Gate: Do not start coding until the plan is approved.

### 3. Phase 3: Implement
- Execute the approved plan as Primary Driver.
- Write unit/integration tests alongside core implementation.
- Maintain consistency with existing architecture and patterns.

### 4. Phase 4: Verify
- Run project test suites, linters, and type checkers.
- Test actual runtime behavior. Never suppress or hide errors.

### 5. Phase 5: Review Independently
- When assigned as auditor:
  - **MANDATE: Review without editing.** Do NOT write or modify files.
  - Audit for bugs, security risks, performance regressions, and acceptance criteria fulfillment.

### 6. Phase 6: Ship Safely
- Verify diff sanity, commit with conventional commits on a feature branch, and respect CI/CD release procedures.

---

## Karpathy LLM Wiki Skill Integration
- Consult `wiki/index.md` and compiled articles in `wiki/` for domain models, architectural patterns, and system guidelines.
- Support verification by running `python skills/karpathy-llm-wiki/scripts/check_evidence.py` when wiki files are impacted.
