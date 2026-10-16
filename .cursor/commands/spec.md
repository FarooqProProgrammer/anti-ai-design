---
name: spec
description: Run Phase 2 (Spec) — functional and technical contracts, schemas, non-features; no source edits
---

# Cursor Command: /spec

Executes **Phase 2 (Spec)** of the AI Engineering Workflow in Cursor.

---

## Invocation in Cursor
Type `/spec [context or requirements]` in Cursor Chat or Composer.

---

## Mandatory Instructions

1. **Functional Spec**:
   - User workflows, behavioral invariants, and input/output contracts.
   - Explicit list of non-features to stop scope creep.

2. **Technical & Data Spec**:
   - Type definitions, schemas, and API contracts.
   - External dependencies ingested into `raw/` and compiled in `wiki/`.

3. **Non-Functional Guardrails**:
   - Performance budgets, security rules, and backward compatibility.

4. **Visual Diagram**:
   - Generate `diagrams/02-spec.exceldraw`.

5. **HARD RULE**:
   - **READ-ONLY on source code.** Do not output implementation code yet.
   - Await human approval before proceeding to Phase 3 (`/plan`).
