# Claude Code Instructions — AI Engineering Workflow

This repository adheres to a strict 6-Phase AI Engineering Workflow governed by a mandatory **Request Firewall** ([FIREWALL.md](FIREWALL.md)).

Modular rules:
- [.claude/rules/firewall.md](.claude/rules/firewall.md) — Firewall admission control, contradiction checks & blocking gates
- [.claude/rules/wiki.md](.claude/rules/wiki.md) — Karpathy LLM Wiki Grounding Invariant & procedures
- [.claude/rules/workflow.md](.claude/rules/workflow.md) — Universal 6-phase lifecycle protocol
- [.claude/rules/engineering.md](.claude/rules/engineering.md) — Engineering standards, humanized content & diagram rules

---

## 🛡️ Non-Bypassable Request Firewall Protocol
Every request MUST proceed sequentially through the firewall gates:
`Contradiction Check ➔ Understand ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely`.

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
  - Explore codebase, trace call stacks, and consult `wiki/index.md`.
  - **STRICT RULE:** READ-ONLY. Do NOT edit or write code during this phase.

- **Gate 2: Plan (Architect & Strategist)**
  - Deeply analyze complex requirements, dependencies, and potential regressions.
  - Formulate testable Acceptance Criteria (Given-When-Then format) and risk matrix.
  - Ingest external references into `raw/` and compile in `wiki/`.
  - **Gate:** Await user confirmation before beginning Phase 3 (Implement).

- **Gate 3: Implement (Single Driver)**
  - When assigned as the Primary Driver, hold sole accountability for core logic and architecture.
  - Follow the approved plan sequentially.
  - Write unit and integration tests alongside implementation.
  - Do NOT introduce unrequested refactorings or speculative features.
  - If collaborating with Cursor, handle core architecture while allowing Cursor to perform interactive/visual refinements.

- **Gate 4: Verify (Zero Concealment)**
  - Run project test runner, type checkers, and linters.
  - Test actual runtime behavior against acceptance criteria.
  - Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.
  - **Zero Concealment:** Never hide or suppress failures (`@ts-ignore`, commented tests). Fix root causes.

- **Gate 5: Review Independently (Read-Only Auditor)**
  - When given a `git diff` for independent review:
    - **READ-ONLY MANDATE:** Review without editing or modifying files.
    - Audit for correctness, security, performance, and acceptance criteria.
    - Report findings categorized by severity (High/Blocker, Medium, Low/Nit).

- **Gate 6: Ship Safely (Branch Hygiene & CI/CD)**
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

## Karpathy LLM Wiki Skill Integration
You have access to the `karpathy-llm-wiki` skill located at `.claude/skills/karpathy-llm-wiki/` and `skills/karpathy-llm-wiki/`.
- **Ingest:** When given a new source, fetch into `raw/<topic>/YYYY-MM-DD-slug.md` and compile into `wiki/<topic>/concept.md`. Adhere to the Grounding Invariant (locate every quote/literal in raw before writing).
- **Query:** Search `wiki/` and provide grounded answers with citations.
- **Lint:** Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .` during verification to guarantee evidence consistency.

---

## Diagram Artifact Standard (.exceldraw)
Every workflow phase must maintain an ExcelDraw diagram (`.exceldraw`, `.excalidraw`, `.svg`) with a clear description under `diagrams/` or repository root.
