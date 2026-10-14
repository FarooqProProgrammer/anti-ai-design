# Claude Code — Universal 7-Phase Workflow Rules

You can execute **all 7 phases** of the software engineering lifecycle end-to-end:

`Understand ➔ Spec ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely`

---

## 1. Phase-by-Phase Directives

### Phase 1: Understand
- Mandatory Skills: `brainstorming` and `grill-me`.
- Clarify goals, non-goals, and anti-goals. Present 2–3 architectural options with trade-offs.
- Drill down the decision tree via Socratic questioning; surface unstated assumptions and edge cases.
- Reconnaissance: Explore code, trace dependencies, consult `wiki/index.md`.
- **Constraint:** READ-ONLY. Zero code edits.
- **Diagram:** Maintain and reference `diagrams/01-understand.exceldraw`.

### Phase 2: Spec
- Formalize functional and technical contracts (the WHAT, not the HOW).
- User journeys, behavioral invariants, state machines, and explicit non-features.
- TypeScript interfaces, database schemas, API contracts, error response envelopes.
- Latency thresholds (<50ms), security rules, concurrency safety, migration compatibility.
- Ingest external specs into `raw/` and compile in `wiki/`.
- **Constraint:** READ-ONLY on source code. Obtain human sign-off before planning.
- **Diagram:** Maintain and reference `diagrams/02-spec.exceldraw`.

### Phase 3: Plan
- Deep requirement investigation, edge case analysis, and risk mitigation matrix.
- Testable acceptance criteria in Given-When-Then format.
- Phased implementation roadmap and Primary Driver assignment.
- **Constraint:** No code is written until plan approval.
- **Diagram:** Maintain and reference `diagrams/03-plan.exceldraw`.

### Phase 4: Implement (Single Driver & Implementation Loop Gate)
- Execute the approved plan sequentially as Primary Driver.
- Write unit and integration tests alongside business logic.
- **Implementation Loop (`Implement ➔ Loop ➔ Spec ➔ Plan ➔ Implement`):**
  - If multiple sub-modules, decoupled tasks, or new domain requirements arise, break them down.
  - Run `/find-skills` (or `npx skills find <domain>`) to find and equip missing specialized capabilities.
  - Dispatch **parallel subagents** for decoupled tasks under Single Driver orchestration.
  - Invariant: Every parallel stream must follow `Spec ➔ Plan ➔ Implement` before code is committed.
- Avoid scope creep or unsolicited refactors.
- **Diagram:** Maintain and reference `diagrams/04-implement.exceldraw`.

### Phase 5: Verify (Automated Quality Gates & Evidence Completion)
- Run risk-tiered automated quality gates: Git diff sanity, TypeScript/typecheck, linters, tests, dependency/security audits, and CI build.
- Enforce stricter checks for high-risk domains: database migrations (schema idempotency & rollbacks), authentication (sessions & tokens), permissions (RBAC boundaries), and payment changes (decimal precision & idempotency).
- Zero Concealment: Fix root causes; never suppress errors.
- Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.
- Output mandatory 5-point Evidence-Based Completion Report (what changed, files changed, tests passed, what was NOT tested, remaining risks).
- **Diagram:** Maintain and reference `diagrams/05-verify.exceldraw`.

### Phase 6: Review Independently
- Fresh-context audit of the final `git diff`.
- Check correctness, security, performance, and acceptance criteria.
- **Constraint:** Review without editing. Never modify files during review.
- **Diagram:** Maintain and reference `diagrams/06-review.exceldraw`.

### Phase 7: Ship Safely
- Verify clean git status (no debug statements, no temp files).
- Commit atomically using Conventional Commits on a feature branch.
- Verify CI/CD pipeline.
- Compound newly established patterns into `wiki/` and record in `wiki/log.md`.
- **Diagram:** Maintain and reference `diagrams/07-ship.exceldraw`.
