# Multi-Agent AI Engineering Workflow

A structured, resilient framework for building software with AI coding agents (Cursor, Claude Code, Codex, and Antigravity). It enforces role segregation, quality gates, and transparent verification to prevent common AI failure modes: hallucinations, scope drift, hidden errors, and broken architectures.

> 🛡️ **MANDATORY REQUEST FIREWALL**: Every request entering this repository must pass through the **[Request Firewall](file:///d:/ai%20agent/the-developer/FIREWALL.md)**. Direct coding, skipped tests, or unreviewed diffs are strictly blocked. Every task proceeds sequentially through:
> **1. Understand** ➔ **2. Plan** ➔ **3. Implement** ➔ **4. Verify** ➔ **5. Review Independently** ➔ **6. Ship Safely**.

---

## The 6-Phase Lifecycle Diagram

> Open and edit the native drawing with your Excalidraw / ExcelDraw viewer: **[`workflow.exceldraw`](file:///d:/ai%20agent/the-developer/workflow.exceldraw)** (or **[`workflow.excalidraw`](file:///d:/ai%20agent/the-developer/workflow.excalidraw)**).

![Multi-Agent AI Engineering Workflow](workflow.svg)

---

## Universal 6-Phase Lifecycle Matrix

> [!NOTE]
> **Universal Agent Execution**: Any agent (**Cursor**, **Claude Code**, **Codex**, or **Antigravity**) can execute all 6 phases. The process is not locked to one specific tool.

| Phase | Executing Agent | Focus Area | Mandatory Constraint |
|---|---|---|---|
| **1. Understand** | Any Agent + **Brainstorming & Grill-Me** + LLM Wiki | Socratic interview, edge-case probing, architectural trade-offs, code & wiki exploration | **Read-Only**: Zero code edits permitted. |
| **2. Plan** | Any Agent (Cursor / Claude / Codex) + LLM Wiki | Complex requirements, risk matrix, ingest RFCs/specs into `raw/` | No code written until plan is approved. |
| **3. Implement** | Primary Driver (Cursor / Claude / Codex) | Core logic, data modeling, backend services & frontend refinement | **Single Driver Principle**: One agent owns the core implementation. |
| **4. Verify** | Any Agent + Test Runner | Typechecking, linting, unit/integration suites, manual validation, wiki evidence check | **Zero Concealment**: Never hide, skip, or suppress failures. |
| **5. Review Independently** | Auditor (Clean Context / Second Agent) | Code review of complete `git diff` for correctness, security, performance | **Review Without Editing**: Reviewer cannot modify files. |
| **6. Ship Safely** | Any Agent + Engineer | Final diff inspection, conventional commits, CI/CD pipeline, compound wiki | Never commit directly to protected branches. |

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
│   ├── brainstorming/          # Design-first exploration & trade-offs skill
│   │   └── SKILL.md
│   ├── grill-me/               # Relentless Socratic interview & edge-case skill
│   │   └── SKILL.md
│   └── karpathy-llm-wiki/      # Karpathy-style knowledge base skill
│       ├── SKILL.md            # Skill specification & grounding invariant
│       ├── references/         # Article, raw, index, and archive templates
│       ├── scripts/            # check_evidence.py linting script
│       └── examples/           # Sample articles and logs
└── templates/
    ├── 01-understand.md        # Understand prompt template (Brainstorming + Grill-me)
    ├── 02-plan.md              # Claude Code planning prompt for Phase 2
    ├── 03-implement.md         # Single Driver & UI refinement guidelines for Phase 3
    ├── 04-verify.md            # Verification checklist & failure handling for Phase 4
    ├── 05-independent-review.md# Review-without-editing prompt for Phase 5
    └── 06-ship-safely.md       # Pre-flight and CI/CD shipping checklist for Phase 6
```

---

## Step-by-Step Universal Execution Guide

Every step in this workflow is **agent-universal** (executable by **Cursor**, **Claude Code**, **Codex**, or **Antigravity**). At each step, the agent must generate an **ExcelDraw diagram** (`.exceldraw` / `.excalidraw` / `.svg`) in [`diagrams/`](file:///d:/ai%20agent/the-developer/diagrams/) along with a structured description.

### Step 1: Understand (Any Agent)
1. Provide the prompt from [`templates/01-understand.md`](file:///d:/ai%20agent/the-developer/templates/01-understand.md) along with your task description.
2. The agent executes **Brainstorming** (goals/anti-goals, trade-offs) and **Grill-Me** (Socratic decision-tree questioning).
3. The agent explores the codebase (read-only) and consults `wiki/index.md`.
4. **Mandatory Visual**: Generate/update [`diagrams/01-understand.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/01-understand.exceldraw) with an architectural context and trade-off description.

### Step 2: Plan (Any Agent)
1. Feed the Phase 1 context into the prompt from [`templates/02-plan.md`](file:///d:/ai%20agent/the-developer/templates/02-plan.md).
2. The agent investigates complex requirements, builds a risk/mitigation matrix, and formulates testable Acceptance Criteria (Given-When-Then).
3. Ingest external references into `raw/` and compile into `wiki/` if needed.
4. **Mandatory Visual**: Generate [`diagrams/02-plan.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/02-plan.exceldraw) illustrating the phased roadmap and acceptance gates.
5. Engineer reviews and approves the plan before any coding begins.

### Step 3: Implement (Primary Driver)
1. Designate the **Primary Driver** (Cursor, Claude Code, or Codex) using [`templates/03-implement.md`](file:///d:/ai%20agent/the-developer/templates/03-implement.md).
2. The Primary Driver owns the core change, domain logic, and unit tests sequentially.
3. If collaborating, secondary agents focus strictly on interactive styling and frontend polish.
4. **Mandatory Visual**: Generate [`diagrams/03-implement.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/03-implement.exceldraw) detailing component wiring and module interactions.

### Step 4: Verify (Any Agent + Test Runner)
1. Execute the verification protocol from [`templates/04-verify.md`](file:///d:/ai%20agent/the-developer/templates/04-verify.md).
2. Run typechecks, linters, unit tests, integration suites, and validate actual runtime behavior.
3. Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py` if wiki files were touched.
4. **Zero Concealment**: Capture all failures explicitly; fix root causes rather than hiding or suppressing tests.
5. **Mandatory Visual**: Generate [`diagrams/04-verify.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/04-verify.exceldraw) showing check results and runtime flow validation.

### Step 5: Review Independently (Auditor Agent)
1. Generate the git diff (`git diff origin/main` or `git diff HEAD~1`).
2. Provide the diff and [`templates/05-independent-review.md`](file:///d:/ai%20agent/the-developer/templates/05-independent-review.md) to an independent agent instance or clean context.
3. Enforce the **"Review without editing"** mandate (the auditor never modifies files).
4. The Primary Driver applies confirmed fixes, and Phase 4 verification is re-run.
5. **Mandatory Visual**: Generate [`diagrams/05-review.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/05-review.exceldraw) mapping the diff review findings and remediation loop.

### Step 6: Ship Safely (Driver & Engineer)
1. Complete the pre-flight checklist in [`templates/06-ship-safely.md`](file:///d:/ai%20agent/the-developer/templates/06-ship-safely.md).
2. Commit changes with conventional commit syntax on a dedicated feature/fix branch (never direct to `main`).
3. Submit a Pull Request and verify remote CI/CD status checks.
4. Record newly established architecture decisions and domain models in `wiki/` and log in `wiki/log.md`.
5. **Mandatory Visual**: Generate [`diagrams/06-ship.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/06-ship.exceldraw) displaying the release pipeline and knowledge compounding.

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


