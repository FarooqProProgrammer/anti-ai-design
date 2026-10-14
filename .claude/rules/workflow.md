# Claude Code — Universal 6-Phase Workflow Rules

You can execute **all 6 phases** of the software engineering lifecycle end-to-end:

`Understand ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely`

---

## 1. Phase-by-Phase Directives

### Phase 1: Understand
- Mandatory Skills: `brainstorming` and `grill-me`.
- Clarify goals, non-goals, and anti-goals. Present 2–3 architectural options with trade-offs.
- Drill down the decision tree via Socratic questioning; surface unstated assumptions and edge cases.
- Reconnaissance: Explore code, trace dependencies, consult `wiki/index.md`.
- **Constraint:** READ-ONLY. Zero code edits.
- **Diagram:** Maintain and reference `diagrams/01-understand.exceldraw`.

### Phase 2: Plan
- Deep requirement investigation, edge case analysis, and risk mitigation matrix.
- Testable acceptance criteria in Given-When-Then format.
- Ingest external specs into `raw/` and compile in `wiki/`.
- **Constraint:** No code is written until plan approval.
- **Diagram:** Maintain and reference `diagrams/02-plan.exceldraw`.

### Phase 3: Implement
- Execute the approved plan sequentially as Primary Driver.
- Write unit and integration tests alongside business logic.
- Avoid scope creep or unsolicited refactors.
- **Diagram:** Maintain and reference `diagrams/03-implement.exceldraw`.

### Phase 4: Verify
- Run project test runner, compiler/typechecker, and linters.
- Test actual runtime behavior against acceptance criteria.
- Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.
- **Constraint:** Zero Concealment. Fix root causes; never suppress errors.
- **Diagram:** Maintain and reference `diagrams/04-verify.exceldraw`.

### Phase 5: Review Independently
- Fresh-context audit of the final `git diff`.
- Check correctness, security, performance, and acceptance criteria.
- **Constraint:** Review without editing. Never modify files during review.
- **Diagram:** Maintain and reference `diagrams/05-review.exceldraw`.

### Phase 6: Ship Safely
- Verify clean git status (no debug statements, no temp files).
- Commit atomically using Conventional Commits on a feature branch.
- Verify CI/CD pipeline.
- Compound newly established patterns into `wiki/` and record in `wiki/log.md`.
- **Diagram:** Maintain and reference `diagrams/06-ship.exceldraw`.
