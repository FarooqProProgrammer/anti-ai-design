# Claude Code Instructions — AI Engineering Workflow

This repository adheres to a strict 7-Phase AI Engineering Workflow governed by a mandatory **Request Firewall** ([FIREWALL.md](FIREWALL.md)).

Modular rules:
- [.claude/rules/firewall.md](.claude/rules/firewall.md) — Firewall admission control, contradiction checks & blocking gates
- [.claude/rules/wiki.md](.claude/rules/wiki.md) — Karpathy LLM Wiki Grounding Invariant, local cursor projects & procedures
- [.claude/rules/workflow.md](.claude/rules/workflow.md) — Universal 7-phase lifecycle protocol
- [.claude/rules/engineering.md](.claude/rules/engineering.md) — Engineering standards, humanized content & diagram rules

---

## 🛡️ Non-Bypassable Request Firewall Protocol
Every request MUST proceed sequentially through the firewall gates:
`Contradiction Check ➔ Understand ➔ Spec ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely`.

- **First Action: Match Request Against Wiki & Docs (Contradiction Check)**
  - Before accepting any request or beginning Gate 1, match it against `wiki/index.md`, compiled articles, and project documentation.
  - If the request contradicts established architecture, invariants, or ADRs:
    - 🛑 **FIREWALL BLOCKS**: Halt execution immediately.
    - **Return the contradiction** clearly to the user, citing the conflicting wiki article (`wiki/<topic>/<article>.md`).
    - Await explicit user clarification.

- **Gate 1: Understand (Read-Only Reconnaissance)**
  - Mandatory Skills: `brainstorming` (`.claude/skills/brainstorming/`) and `grill-me` (`.claude/skills/grill-me/`).
  - Uncover goals, non-goals, and anti-goals. Propose 2–3 architectural approaches with trade-offs.
  - Socratic questioning down the decision tree; challenge edge cases and surface unstated assumptions.
  - Explore codebase, trace call stacks, and consult `wiki/index.md` as well as local Cursor project knowledge (`C:\Users\farooq\.cursor\projects`).
  - **STRICT RULE:** READ-ONLY. Do NOT edit or write code during this phase.

- **Gate 2: Spec (Technical & Functional Specification)**
  - Formalize workflows, schemas, API contracts, error response envelopes, and behavioral invariants (the WHAT).
  - Set latency budgets (<50ms), security rules, concurrency safety, and migration rules.
  - Ingest external specs into `raw/` and compile in `wiki/`.
  - **STRICT RULE:** READ-ONLY on source code. Obtain human sign-off before Phase 3 (Plan).

- **Gate 3: Plan (Architect & Strategist)**
  - Deeply analyze complex requirements, dependencies, and potential regressions (the HOW).
  - Formulate testable Acceptance Criteria (Given-When-Then format) and risk matrix.
  - Ingest external references into `raw/` and compile in `wiki/`.
  - **Gate:** Await user confirmation before beginning Phase 4 (Implement).

- **Gate 4: Implement (Single Driver & Implementation Loop Gate)**
  - When assigned as the Primary Driver, hold sole accountability for core logic and architecture.
  - Follow the approved plan sequentially.
  - **Implementation Loop (`Implement ➔ Loop ➔ Spec ➔ Plan ➔ Implement`):** If multiple tasks, decoupled sub-modules, or new domain requirements arise, break them down. Use `/find-skills` (`npx skills find`) to equip missing tools, and dispatch parallel subagents under Single Driver orchestration. Each parallel stream must follow `Spec ➔ Plan ➔ Implement`.
  - Write unit and integration tests alongside implementation.
  - Do NOT introduce unrequested refactorings or speculative features.
  - If collaborating with Cursor, handle core architecture while allowing Cursor to perform interactive/visual refinements.

- **Gate 5: Verify (Zero Concealment)**
  - Run project test runner, type checkers, and linters.
  - Test actual runtime behavior against acceptance criteria.
  - Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.
  - **Zero Concealment:** Never hide or suppress failures (`@ts-ignore`, commented tests). Fix root causes.

- **Gate 6: Review Independently (Read-Only Auditor)**
  - When given a `git diff` for independent review:
    - **READ-ONLY MANDATE:** Review without editing or modifying files.
    - Audit for correctness, security, performance, and acceptance criteria.
    - Report findings categorized by severity (High/Blocker, Medium, Low/Nit).

- **Gate 7: Ship Safely (Branch Hygiene & CI/CD)**
  - Review final git diff and status for lingering debug statements or extraneous files.
  - Commit atomically using Conventional Commits on dedicated feature/fix branches.
  - Follow established CI/CD pipeline and release protocols.
  - Compound newly introduced architectural patterns into `wiki/` and record in `wiki/log.md`.

---

## ✍️ Humanized Content Standard
All generated content—including comments, PR summaries, commit messages, and documentation—must read naturally like practical human engineering prose:
- Never use robotic AI buzzwords (*"delve into"*, *"tapestry"*, *"testament to"*, *"harnessing"*, *"streamlining"*, *"game-changer"*).
- Write in active voice with clear, direct explanations.
- Never write redundant comments that merely echo code syntax.

---

## Karpathy LLM Wiki & Local Project Knowledge
You have access to the `karpathy-llm-wiki` skill located at `.claude/skills/karpathy-llm-wiki/` and `skills/karpathy-llm-wiki/`.
- **Local Cursor Knowledge Base (`C:\Users\farooq\.cursor\projects`)**: Query local project directories (especially `d-ai-agent-the-developer/` and sibling projects) for past agent transcripts, terminal execution records, and architectural canvases.
- **Ingest:** When given a new source, fetch into `raw/<topic>/YYYY-MM-DD-slug.md` and compile into `wiki/<topic>/concept.md`. Adhere to the Grounding Invariant (locate every quote/literal in raw before writing).
- **Query:** Search `wiki/` and provide grounded answers with citations.
- **Lint:** Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .` during verification to guarantee evidence consistency.

---

## Diagram Artifact Standard (.exceldraw)
Every workflow phase must maintain an ExcelDraw diagram (`.exceldraw`, `.excalidraw`, `.svg`) with a clear description under `diagrams/` or repository root.
