# Phase 4: Implement (Driver & Collaboration Guidelines)

**Firewall Gate:** Gate 4 (Single Driver Execution & Implementation Discipline)  
**Applicable Tools:** Any Agent (Cursor, Claude Code, or Codex as Primary Driver)  
**Strict Firewall Rule:** Exactly one agent owns core implementation logic. Multi-driver conflict and scope creep are BLOCKED.

---

## 4A. Primary Driver Prompt (Any Agent: Cursor / Claude / Codex)

```markdown
You are the Primary Driver in Phase 4 (Implement) of the AI Engineering Workflow.

Approved Specification & Implementation Plan:
<APPROVED_PLAN>
[Insert the approved plan from Phase 3]
</APPROVED_PLAN>

Rules of Engagement:
1. You are the single agent responsible for the core implementation.
2. Implement according to the approved plan step-by-step. Do not deviate or introduce speculative code.
3. Write or update automated tests alongside implementation to satisfy all acceptance criteria.
4. Follow existing codebase patterns identified in Phase 1 (naming, error handling, formatting).
5. If UI refinement or quick interactive edits are delegated to Cursor, do not overwrite those edits without reconciling context.
6. Once implementation is complete, run Phase 5 (Verify).
```

---

## 4B. Frontend / Interactive Refinement Prompt (When collaborating)

```markdown
You are assisting in Phase 4 (Implement) strictly for interactive edits and frontend refinement.

Scope of Responsibility:
- UI component styling, layout tuning, CSS/Tailwind adjustments.
- Interactive user experience improvements and visual feedback (hover, focus, animations, loading states).
- Fast inline edits requested by the developer.

Strict Constraints:
1. Do NOT refactor core business logic, API clients, database queries, or domain types. Those are owned by the Primary Driver.
2. Maintain compatibility with existing props, interfaces, and state stores.
3. Keep changes minimal, scoped, and visually refined.
```
