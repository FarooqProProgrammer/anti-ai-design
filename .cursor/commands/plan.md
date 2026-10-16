---
name: plan
description: Run Phase 3 (Plan) — risk matrix, acceptance criteria, implementation blueprint; await approval before code
---

# Cursor Command: /plan

Executes **Phase 3 (Plan)** of the AI Engineering Workflow in Cursor.

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
   - Generate `diagrams/03-plan.exceldraw`.

6. **HTML Plan (html-plan skill)**:
   - Read and follow `skills/html-plan/SKILL.md`.
   - Write a chart-rich aesthetic HTML plan to `plans/html/<slug>.html`, sync to `.cursor/plans/html/`.
   - When the plan document is complete, run `node skills/html-plan/scripts/serve-open.js plans/html/<slug>.html` so it opens in **Chrome** (keep server running).
   - Reviewer **annotates** in the page and clicks **Send to Cursor** → writes `.cursor/plans/inbox/<slug>-feedback.md` plus `*.annotations.md`.
   - Before Implement, read inbox/annotations and apply change/block feedback (regenerate HTML if the plan changes).

7. **HARD RULE**:
   - **No code is written until human sign-off.**
   - Await explicit user approval before starting Phase 4 (Implement).
   - Prefer inbox **approve** annotations + chat approval; treat **block** as a hard stop.

