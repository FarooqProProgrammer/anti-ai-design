# Codex Instructions — Universal AI Engineering Workflow

This codebase operates under a strict 7-Phase AI Engineering Workflow governed by a mandatory **Request Firewall** ([FIREWALL.md](FIREWALL.md)).

You are equipped to execute **any or all** of the 7 phases. Always adhere to each gate's rules and quality standards.

---

## 🛡️ Request Firewall Protocol
Every incoming request must proceed through the sequential firewall gates:
`Contradiction Check ➔ Understand ➔ Spec ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely`.

### 0. First Action: Match Request Against Wiki & Docs (Contradiction Check)
- Before accepting any request, match it against `wiki/index.md`, compiled `wiki/` articles, and project documentation.
- If the request contradicts established architecture, invariants, or ADRs:
  - 🛑 **FIREWALL BLOCKS**: Halt execution immediately.
  - Return the contradiction clearly, citing the conflicting wiki article (`wiki/<topic>/<article>.md`).
  - Await explicit user clarification.

### 1. Phase 1: Understand (Read-Only Reconnaissance)
- **Mandatory Skills:** Always apply **`brainstorming`** and **`grill-me`** before proposing solutions.
- Explore codebase, analyze dependencies, and trace data flow.
- Consult `wiki/index.md` for architectural context and existing ADRs.
- **Local Knowledge Source:** Inspect `C:\Users\farooq\.cursor\projects` (transcripts, terminals, canvases) for historical context.
- **Rule:** READ-ONLY. Zero code edits during exploration.
- **Diagram:** Maintain and reference `diagrams/01-understand.exceldraw`.

### 2. Phase 2: Spec (Functional & Technical Contracts)
- Formalize workflows, schemas, API contracts, error response envelopes, and behavioral invariants (the WHAT).
- Set latency budgets (<50ms), security rules, concurrency safety, and migration rules.
- Ingest external specs into `raw/` and compile in `wiki/`.
- **Rule:** READ-ONLY on source code. Obtain human sign-off before Phase 3 (Plan).
- **Diagram:** Maintain and reference `diagrams/02-spec.exceldraw`.

### 3. Phase 3: Plan (Architectural Blueprints)
- Investigate requirements, assess risks, and formulate testable Acceptance Criteria (Given-When-Then).
- Ingest external RFCs/documentation into `raw/` and compile in `wiki/`.
- **Gate:** Do not start coding until the plan is approved by the user.
- **Diagram:** Maintain and reference `diagrams/03-plan.exceldraw`.

### 4. Phase 4: Implement (Single Driver)
- Execute the approved plan as Primary Driver.
- Keep one agent responsible for main business logic and architecture.
- Write unit/integration tests alongside core implementation.
- Maintain consistency with existing architecture and patterns. Avoid speculative scope.
- **Diagram:** Maintain and reference `diagrams/04-implement.exceldraw`.

### 5. Phase 5: Verify (Zero Concealment)
- Run project test suites, linters, and type checkers.
- Test actual runtime behavior against acceptance criteria.
- Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.
- **Rule:** Never suppress or hide errors (`@ts-ignore`, commented tests). Fix root causes.
- **Diagram:** Maintain and reference `diagrams/05-verify.exceldraw`.

### 6. Phase 6: Review Independently (Read-Only Auditor)
- When assigned as auditor:
  - **MANDATE: Review without editing.** Do NOT write or modify files.
  - Audit for bugs, security risks, performance regressions, and acceptance criteria fulfillment.
- **Diagram:** Maintain and reference `diagrams/06-review.exceldraw`.

### 7. Phase 7: Ship Safely (Branch Hygiene & CI/CD)
- Verify diff sanity (no residual debug statements or scratch files).
- Commit with Conventional Commits on a dedicated feature branch.
- Follow CI/CD release procedures.
- Compound newly established patterns into `wiki/` and record in `wiki/log.md`.
- **Diagram:** Maintain and reference `diagrams/07-ship.exceldraw`.

---

## ✍️ Humanized Content Standard
All code comments, documentation, commit messages, and PR descriptions must be written in natural, human software engineering prose:
- Zero AI clichés or robotic buzzwords (*"delve into"*, *"tapestry"*, *"in conclusion"*, *"testament to"*, *"harnessing"*).
- Write in active voice with clear, direct explanations.
- Never write redundant comments that echo the code syntax.

---

## Karpathy LLM Wiki & Local Project Knowledge
- Maintain the Grounding Invariant: every load-bearing fact, number, date, or direct quote in `wiki/` must exist verbatim in `raw/`.
- Consult `wiki/index.md` and compiled articles in `wiki/` for domain models, architectural patterns, and system guidelines.
- Query `C:\Users\farooq\.cursor\projects` for previous agent transcripts, terminal execution records, and architectural canvases.
- Support verification by running `python skills/karpathy-llm-wiki/scripts/check_evidence.py .` when wiki files are impacted.
