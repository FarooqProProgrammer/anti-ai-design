---
name: doc-prd
description: Read docs, extract meaningful info, write a PRD, and create ExcelDraw diagrams
---

# Cursor Command: /doc-prd

Runs the **doc-prd** agent: document ingest → meaningful extraction → PRD → ExcelDraw.

---

## Invocation

```text
/doc-prd <paths, URLs, or pasted brief>
```

---

## Mandatory Instructions

1. **Ingest** every named source (read-only first). Use Google Docs / WebFetch tools when available.
2. **Extract** problem, users, goals/non-goals/anti-goals, functional & non-functional requirements, journeys, constraints, risks, open questions. Label assumptions.
3. **Write PRD** to `docs/prd/YYYY-MM-DD-<slug>.md` using `templates/prd.md`. Cite sources for P0 requirements.
4. **Create ExcelDraw** at `diagrams/prd/<slug>.exceldraw` (problem → users → outcomes, scope map, primary journey). Add `.excalidraw` / `.svg` when practical via `scripts/generate_exceldraw.py` patterns.
5. **Do not** write implementation code. Hand off to `/spec` and `/plan` after sign-off.
6. **Report** PRD path, diagram paths, sources, and top open questions.
