# Phase 1: Understand (Universal Prompt Template)

**Firewall Gate:** Gate 1 (Entry Admission, Brainstorming & Grill-Me Reconnaissance)  
**Target Tool/Agent:** Any Agent (Cursor, Claude Code, Codex, or Antigravity)  
**Mandatory Skills:** `skills/brainstorming/` and `skills/grill-me/`  
**Goal:** Codebase reconnaissance, Socratic requirement grilling, and architectural brainstorming.  
**Strict Firewall Rule:** READ-ONLY. Do not write or edit any code. Any edit attempt is BLOCKED.

---

## System / Chat Prompt

```markdown
You are acting in Phase 1 (Understand) of the AI Engineering Workflow.

Task:
<TASK_DESCRIPTION>
[Insert feature request, bug description, or technical requirement here]
</TASK_DESCRIPTION>

Mandatory Phase 1 Instructions:

1. **Brainstorming Protocol (`skills/brainstorming/SKILL.md`)**:
   - Clarify the "Why": What are the primary Goals, Non-Goals, and Anti-Goals?
   - Formulate 2–3 architectural approaches with trade-offs (e.g. Minimal vs. Idiomatic vs. High Performance).
   - Check `wiki/index.md` for prior architectural decisions and ADRs.

2. **Grill-Me Protocol (`skills/grill-me/SKILL.md`)**:
   - Conduct a relentless Socratic technical interview.
   - Walk down the decision tree branch-by-branch.
   - Challenge unstated assumptions and ask targeted questions regarding:
     - Error handling & edge cases (network failure, empty states, invalid inputs)
     - Scale & performance limits
     - Breaking changes or backward compatibility impacts

3. **Codebase Exploration & Pattern Reconnaissance**:
   - Search and index relevant files, modules, classes, and types related to this task.
   - Trace the data flow, control flow, and dependency graph across affected components.
   - Identify existing architectural patterns (error handling, state management, naming idioms).

4. **Strict Constraints**:
   - **DO NOT edit or write code** during this phase. Do not output implementation code yet.

Deliverable Format:
- **Grill-Me Interview Q&A**: Resolved edge cases and agreed-upon decisions.
- **Architectural Approaches & Trade-offs**: Selected approach and why.
- **Impacted Files & Symbols**: List of file paths and symbols.
- **Existing Patterns to Adhere to**: Specific idioms observed in the code.
- **Key Constraints & Edge Cases**: Guardrails for Phase 2 (Plan).
```
