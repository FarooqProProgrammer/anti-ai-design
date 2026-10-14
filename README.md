# Multi-Agent AI Engineering Workflow

A pragmatic, battle-tested framework for building software with AI coding agents (Cursor, Claude Code, Codex, and Antigravity). It keeps AI tools from making wild assumptions, writing sloppy code in a hurry, hiding broken tests, or blowing up your architecture.

> 🛡️ **THE REQUEST FIREWALL**: Every request entering this repository stops at the **[Request Firewall](file:///d:/ai%20agent/the-developer/FIREWALL.md)** first:
> 1. **Match with Wiki & Docs First:** If the requested change contradicts existing architecture, ADRs, or wiki knowledge, the firewall blocks execution and returns the contradiction immediately.
> 2. **Sequential Quality Gates:**
>    **1. Understand** ➔ **2. Plan** ➔ **3. Implement** ➔ **4. Verify** ➔ **5. Review Independently** ➔ **6. Ship Safely**.

---

## The 6-Phase Lifecycle Diagram

> Open and edit the native drawing with your Excalidraw / ExcelDraw viewer: **[`workflow.exceldraw`](file:///d:/ai%20agent/the-developer/workflow.exceldraw)** (or **[`workflow.excalidraw`](file:///d:/ai%20agent/the-developer/workflow.excalidraw)**).

![Multi-Agent AI Engineering Workflow](workflow.svg)

---

## Universal 6-Phase Lifecycle Matrix

> [!NOTE]
> **Any agent can drive any phase:**
> This workflow isn't split into rigid silos. **Cursor**, **Claude Code**, **Codex**, or **Antigravity** can run all six phases end-to-end, or collaborate as a team. What matters is following the gates and not cutting corners.

| Phase | Who Runs It | Core Focus | Hard Constraint |
|---|---|---|---|
| **0. Pre-Admission** | Any Agent + Wiki / Docs | Match input against `wiki/` and docs; detect contradictions | Return contradiction or proceed to Phase 1. |
| **1. Understand** | Any Agent + **Brainstorming & Grill-Me** + Wiki | Socratic interview, edge cases, trade-offs, explore code & wiki | **Read-Only**: Zero code edits allowed. |
| **2. Plan** | Any Agent (Cursor / Claude / Codex) + Wiki | Real requirements, risk matrix, ingest RFCs/specs into `raw/` | No code written until human sign-off. |
| **3. Implement** | Primary Driver (Cursor / Claude / Codex) | Core logic, data models, APIs, and UI styling polish | **Single Driver**: One agent owns the core logic. |
| **4. Verify** | Any Agent + Test Runner | Typechecking, linting, unit/integration suites, wiki evidence check | **Zero Concealment**: Never hide, skip, or suppress failures. |
| **5. Review Independently** | Auditor (Clean Context / Second Agent) | Full `git diff` audit for bugs, security holes, performance | **Review Without Editing**: Reviewer cannot modify files. |
| **6. Ship Safely** | Any Agent + Engineer | Clean diff check, conventional commits, CI/CD run, compound wiki | Never commit straight to `main` or `master`. |

---

## Humanized Content Standard

All content in this project—code comments, commit messages, PR descriptions, and documentation—must read like it was written by a thoughtful, practical software engineer:
- **No AI Buzzwords:** Ban empty filler like "delve into", "tapestry", "in conclusion", "it's important to remember", "testament to", "harnessing", "streamlining", or "game-changer".
- **Direct & Active Voice:** Speak plainly: "we recommend", "this function throws when...", "here's how to configure".
- **Pragmatic Comments:** Explain *why* something unusual was done, not what the syntax already shows.
- **Natural Engineering Rhythm:** Keep sentences direct, punchy, and grounded in real-world trade-offs.

---

## Repository Rules Architecture (Agents & Wiki)

Rules derived from repository documents (`FIREWALL.md`, `AI_WORKFLOW.md`, `skills/`) and compiled into the Karpathy LLM Wiki (`wiki/`) are active across all coding assistants:

```
the-developer/
├── .cursor/
│   └── rules/
│       ├── workflow.mdc               # Universal 6-phase lifecycle protocol
│       ├── firewall-rules.mdc         # Request Firewall admission controller & contradiction check
│       ├── wiki-rules.mdc             # Karpathy LLM Wiki Grounding Invariant & evidence rules
│       └── engineering-standards.mdc  # Single Driver, zero concealment, humanized content rules
├── .cursorrules                       # Root Cursor universal agent instructions
├── .claude/
│   └── rules/
│       ├── firewall.md                # Claude Code firewall admission rules & contradiction gate
│       ├── wiki.md                    # Claude Code wiki Grounding Invariant & procedures
│       ├── workflow.md                # Claude Code 6-phase universal lifecycle
│       └── engineering.md             # Claude Code engineering, humanized prose & diagram rules
├── CLAUDE.md                          # Claude Code master instruction file
├── CODEX.md                           # Codex master universal instructions
├── raw/                               # Immutable source documents
│   └── workflow/
│       ├── 2026-10-14-ai-workflow-spec.md
│       └── 2026-10-14-firewall-spec.md
└── wiki/                              # Compiled knowledge base
    ├── index.md                       # Global knowledge index
    ├── log.md                         # Append-only operation log
    └── workflow/
        ├── universal-workflow.md      # Grounded universal workflow article
        └── request-firewall.md        # Grounded request firewall article
```

---

## Step-by-Step Universal Execution Guide

Every step in this workflow is **agent-universal** (executable by **Cursor**, **Claude Code**, **Codex**, or **Antigravity**). At each step, the agent maintains an **ExcelDraw diagram** (`.exceldraw` / `.excalidraw` / `.svg`) in [`diagrams/`](file:///d:/ai%20agent/the-developer/diagrams/) along with a clear description.

### Pre-Admission: Contradiction Check
1. The agent parses the user's prompt or requirement.
2. The agent matches the requirement against `wiki/index.md`, relevant `wiki/` articles, and project documentation.
3. If the requirement contradicts documented architecture or decisions, execution is **BLOCKED**, and the contradiction is returned immediately.

### Step 1: Understand (Any Agent)
1. Use the prompt from [`templates/01-understand.md`](file:///d:/ai%20agent/the-developer/templates/01-understand.md) with your task description.
2. The agent runs **Brainstorming** (goals/anti-goals, trade-offs) and **Grill-Me** (Socratic decision-tree questioning).
3. The agent explores the codebase (read-only) and checks `wiki/index.md`.
4. **Visual Artifact**: Update [`diagrams/01-understand.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/01-understand.exceldraw) with an architectural context and trade-off description.

### Step 2: Plan (Any Agent)
1. Feed the Phase 1 context into the prompt from [`templates/02-plan.md`](file:///d:/ai%20agent/the-developer/templates/02-plan.md).
2. The agent investigates tricky requirements, maps out risks, and writes testable Acceptance Criteria (Given-When-Then).
3. Ingest external references into `raw/` and compile into `wiki/` if needed.
4. **Visual Artifact**: Generate [`diagrams/02-plan.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/02-plan.exceldraw) illustrating milestones and acceptance gates.
5. Review and approve the plan before any coding begins.

### Step 3: Implement (Primary Driver)
1. Designate the **Primary Driver** (Cursor, Claude Code, or Codex) using [`templates/03-implement.md`](file:///d:/ai%20agent/the-developer/templates/03-implement.md).
2. The Primary Driver owns the core change, domain logic, and unit tests sequentially.
3. If collaborating, secondary agents focus strictly on interactive styling and frontend polish.
4. **Visual Artifact**: Generate [`diagrams/03-implement.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/03-implement.exceldraw) detailing component wiring and module interactions.

### Step 4: Verify (Any Agent + Test Runner)
1. Run the verification protocol from [`templates/04-verify.md`](file:///d:/ai%20agent/the-developer/templates/04-verify.md).
2. Run typechecks, linters, unit tests, integration suites, and validate actual runtime behavior.
3. Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .` if wiki files were touched.
4. **Zero Concealment**: Never hide failures. Fix root causes rather than disabling tests or assertions.
5. **Visual Artifact**: Generate [`diagrams/04-verify.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/04-verify.exceldraw) showing check results and runtime flow validation.

### Step 5: Review Independently (Auditor Agent)
1. Generate the git diff (`git diff origin/main` or `git diff HEAD~1`).
2. Provide the diff and [`templates/05-independent-review.md`](file:///d:/ai%20agent/the-developer/templates/05-independent-review.md) to an independent agent instance in a clean context.
3. Enforce the **"Review without editing"** mandate (the auditor never modifies files).
4. The Primary Driver applies confirmed fixes, and Phase 4 verification is re-run.
5. **Visual Artifact**: Generate [`diagrams/05-review.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/05-review.exceldraw) mapping the diff review findings and remediation loop.

### Step 6: Ship Safely (Driver & Engineer)
1. Complete the pre-flight checklist in [`templates/06-ship-safely.md`](file:///d:/ai%20agent/the-developer/templates/06-ship-safely.md).
2. Commit changes with conventional commit syntax on a dedicated feature/fix branch (never direct to `main`).
3. Submit a Pull Request and verify remote CI/CD status checks.
4. Record newly established architecture decisions and domain models in `wiki/` and log in `wiki/log.md`.
5. **Visual Artifact**: Generate [`diagrams/06-ship.exceldraw`](file:///d:/ai%20agent/the-developer/diagrams/06-ship.exceldraw) displaying the release pipeline and knowledge compounding.

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
  python skills/karpathy-llm-wiki/scripts/check_evidence.py .
  ```
  - Verifies that all numbers, dates, and quotes in `wiki/` exist verbatim in `raw/`.

---

## Agent Skills Ecosystem & `/setup-agent` Command

This repository uses the open [Skills CLI](https://skills.sh) standard with [`skills/find-skills/`](file:///d:/ai%20agent/the-developer/skills/find-skills/) to discover, vet, and install top-rated skills from the web.

### Command: `/setup-agent`
Run **`/setup-agent`** (documented in [`.claude/commands/setup-agent.md`](file:///d:/ai%20agent/the-developer/.claude/commands/setup-agent.md)) to automatically configure and synchronize skills across all agents.

### Discover & Install More Skills:
```bash
# Search open directory for skills by keyword or domain:
cmd.exe /c "npx skills find react"
cmd.exe /c "npx skills find testing"

# Install directly from GitHub:
cmd.exe /c "npx skills add vercel-labs/agent-skills -y --copy"
```
Installed skills are mirrored across `.agents/skills/`, `skills/`, and `.claude/skills/` so **Cursor, Claude Code, Codex, and Antigravity** can use them immediately.
