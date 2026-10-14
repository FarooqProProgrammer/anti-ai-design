# Cursor Command: /plan

Executes **Phase 2 (Plan)** of the AI Engineering Workflow in Cursor.

---

## Invocation in Cursor
Type `/plan [context or requirements]` in Cursor Chat or Composer.

---

## Mandatory Instructions

1. **Requirements & Scope Boundary**:
   - In-scope vs. out-of-scope boundaries.
   - Ingest new RFCs/docs into `raw/` and compile in `wiki/`.

2. **Risk & Mitigation Matrix**:
   - Identify risks, concurrency bugs, and performance traps with mitigations.

3. **Acceptance Criteria**:
   - Write testable Given-When-Then acceptance criteria.

4. **Phased Roadmap**:
   - Define atomic milestones and designate the Primary Driver.

5. **Visual Diagram**:
   - Generate `diagrams/02-plan.exceldraw`.

6. **HARD RULE**:
   - **No code is written until human sign-off.**
   - Await explicit user approval before starting Phase 3 (Implement).

