---
name: understand
description: Run Phase 1 (Understand) — contradiction check, brainstorming, grill-me, read-only reconnaissance
---

# Cursor Command: /understand

Executes **Phase 1 (Understand)** of the AI Engineering Workflow in Cursor.

---

## Invocation in Cursor
Type `/understand <task description>` in Cursor Chat or Composer.

---

## Mandatory Instructions

1. **Contradiction Check**:
   - Query `wiki/index.md`, compiled `wiki/` articles, and `C:\Users\farooq\.cursor\projects`.
   - If the request contradicts existing architecture, HALT and return the contradiction.

2. **Brainstorming**:
   - Identify Goals, Non-Goals, Anti-Goals.
   - Present 2–3 architectural approaches with trade-offs.

3. **Grill-Me**:
   - Run Socratic technical interview on edge cases, failure modes, and unstated assumptions.

4. **Code Reconnaissance**:
   - Trace callers and callees. Note error handling and state conventions.

5. **Visual Diagram**:
   - Update `diagrams/01-understand.exceldraw`.

6. **HARD RULE**:
   - **READ-ONLY.** Zero code modifications allowed.

