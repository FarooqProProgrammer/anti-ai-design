# Multi-Agent AI Engineering Workflow

A structured, resilient framework for building software with AI coding agents (Cursor, Claude Code, Codex, and Antigravity). It enforces role segregation, quality gates, and transparent verification to prevent common AI failure modes: hallucinations, scope drift, hidden errors, and broken architectures.

> 🛡️ **MANDATORY REQUEST FIREWALL**: Every request entering this repository must pass through the **[Request Firewall](file:///d:/ai%20agent/the-developer/FIREWALL.md)**. Direct coding, skipped tests, or unreviewed diffs are strictly blocked. Every task proceeds sequentially through:
> **1. Understand** ➔ **2. Plan** ➔ **3. Implement** ➔ **4. Verify** ➔ **5. Review Independently** ➔ **6. Ship Safely**.

---

## The 6-Phase Lifecycle Diagram

> Open and edit the native drawing with your Excalidraw / ExcelDraw viewer: **[`workflow.exceldraw`](file:///d:/ai%20agent/the-developer/workflow.exceldraw)** (or **[`workflow.excalidraw`](file:///d:/ai%20agent/the-developer/workflow.excalidraw)**).

![Multi-Agent AI Engineering Workflow](workflow.svg)

---

## Agent Role Matrix

| Phase | Assigned Tool / Agent | Focus Area | Mandatory Constraint |
|---|---|---|---|
| **1. Understand** | **Cursor** + **LLM Wiki** | Code exploration, semantic search, consult compiled wiki (`wiki/`) | **Read-Only**: Zero code edits permitted. |
| **2. Plan** | **Claude Code** + **LLM Wiki** | Complex requirements, risk matrix, ingest RFCs/specs into `raw/` | No code written until plan is approved. |
| **3. Implement** | **Claude Code** or **Codex** (Primary Driver) <br> **Cursor** (Secondary) | Core logic, data modeling, backend services (Primary) <br> Frontend refinement, UI styling, interactive tweaks (Cursor) | **Single Driver Principle**: One agent owns the core implementation. |
| **4. Verify** | **Test Runner & Driver Agent** | Typechecking, linting, unit/integration suites, manual validation, wiki evidence check | **Zero Concealment**: Never hide, skip, or suppress failures. |
| **5. Review Independently** | **Codex** or **Claude Code** (Independent) | Code review of complete `git diff` for correctness, security, performance | **Review Without Editing**: Reviewer cannot modify files. |
| **6. Ship Safely** | **Driver Agent & Engineer** | Final diff inspection, conventional commits, CI/CD pipeline, compound wiki | Never commit directly to protected branches. |

---

## Directory Structure

```
the-developer/
├── FIREWALL.md                 # Mandatory Request Firewall & admission gates
├── AI_WORKFLOW.md              # Master specification & deep guidelines
├── README.md                   # Visual architecture and quick reference
├── CLAUDE.md                   # Instructions for Claude Code
├── CODEX.md                    # Instructions for Codex
├── .cursorrules                # Legacy & root Cursor rules
├── .cursor/
│   └── rules/
│       └── workflow.mdc        # Modern Cursor rule file
├── skills/
│   └── karpathy-llm-wiki/      # Karpathy-style knowledge base skill
│       ├── SKILL.md            # Skill specification & grounding invariant
│       ├── references/         # Article, raw, index, and archive templates
│       ├── scripts/            # check_evidence.py linting script
│       └── examples/           # Sample articles and logs
└── templates/
    ├── 01-understand.md        # Cursor prompt template for Phase 1
    ├── 02-plan.md              # Claude Code planning prompt for Phase 2
    ├── 03-implement.md         # Single Driver & UI refinement guidelines for Phase 3
    ├── 04-verify.md            # Verification checklist & failure handling for Phase 4
    ├── 05-independent-review.md# Review-without-editing prompt for Phase 5
    └── 06-ship-safely.md       # Pre-flight and CI/CD shipping checklist for Phase 6
```

---

## Step-by-Step Execution Guide

### Step 1: Understand (Cursor)
1. Open the project in Cursor.
2. Provide the prompt from [`templates/01-understand.md`](file:///d:/ai%20agent/the-developer/templates/01-understand.md) along with your task description.
3. Review Cursor's analysis of affected files, existing patterns, and constraints.

### Step 2: Plan (Claude Code)
1. Launch Claude Code.
2. Feed the output from Phase 1 and the prompt from [`templates/02-plan.md`](file:///d:/ai%20agent/the-developer/templates/02-plan.md).
3. Review the generated plan: check that risks, mitigations, and acceptance criteria are comprehensive.
4. Approve the plan.

### Step 3: Implement (Claude Code / Codex + Cursor)
1. Designate either **Claude Code** or **Codex** as the **Primary Driver**.
2. Supply [`templates/03-implement.md`](file:///d:/ai%20agent/the-developer/templates/03-implement.md) to the driver to execute core changes.
3. If frontend adjustments or quick interactive iterations are needed, delegate those strictly to **Cursor**.

### Step 4: Verify (Driver & Environment)
1. Execute the verification checklist from [`templates/04-verify.md`](file:///d:/ai%20agent/the-developer/templates/04-verify.md).
2. Run typechecks, linters, and unit/integration tests.
3. Validate runtime behavior against Phase 2 Acceptance Criteria.
4. Capture any failure outputs directly; fix root causes rather than hiding or bypassing tests.

### Step 5: Review Independently (Codex or Claude Code)
1. Generate the git diff (`git diff origin/main` or `git diff HEAD~1`).
2. Provide the diff and [`templates/05-independent-review.md`](file:///d:/ai%20agent/the-developer/templates/05-independent-review.md) to an independent agent instance (Codex or Claude Code).
3. Enforce the **"Review without editing"** rule.
4. Primary Driver resolves confirmed findings and re-runs Phase 4 verification.

### Step 6: Ship Safely (Driver & Engineer)
1. Complete the pre-flight checklist in [`templates/06-ship-safely.md`](file:///d:/ai%20agent/the-developer/templates/06-ship-safely.md).
2. Commit changes with conventional commit syntax on a dedicated feature/fix branch.
3. Submit a Pull Request and ensure all CI/CD checks pass prior to merging.
4. Record new architectural insights or system models in `wiki/` and log in `wiki/log.md`.

---

## Karpathy LLM Wiki Skill Integration

This repository incorporates [`skills/karpathy-llm-wiki/`](file:///d:/ai%20agent/the-developer/skills/karpathy-llm-wiki/) based on [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki).

### Quick Usage Commands
- **Ingest a new source**:
  Ask the agent: *"Ingest this specification / URL: `<url>` into the wiki"*
  - Source is saved to `raw/<topic>/YYYY-MM-DD-slug.md`.
  - Content is triaged and compiled into `wiki/<topic>/concept.md`.
- **Query the wiki**:
  Ask the agent: *"What does our wiki say about `<topic>`?"*
  - Grounded answers generated directly from compiled markdown pages with citations.
- **Lint the wiki & verify grounding**:
  ```bash
  python skills/karpathy-llm-wiki/scripts/check_evidence.py
  ```
  - Verifies that all numbers, dates, and quotes in `wiki/` exist verbatim in `raw/`.


