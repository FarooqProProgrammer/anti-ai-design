# Claude Code Instructions — AI Engineering Workflow

This repository adheres to a strict 6-Phase AI Engineering Workflow governed by a mandatory **Request Firewall** ([FIREWALL.md](FIREWALL.md)).

> 🛡️ **REQUEST FIREWALL PROTOCOL:**
> Every request MUST proceed through the sequential process:
> `Understand ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely`.
> - Never skip Phase 2 planning to write code immediately.
> - Never write code without explicit plan approval.
> - Never suppress or hide errors in Phase 4.
> - When asked to review in Phase 5, you are in READ-ONLY mode.

## Universal Execution Across All 6 Phases
You can execute **any or all** of the 6 phases of the workflow:

### 1. Phase 1: Understand (Code Exploration, Brainstorming & Grill-Me)
- **Mandatory Skills**: Always use **`brainstorming`** (`.claude/skills/brainstorming/`) and **`grill-me`** (`.claude/skills/grill-me/`).
- **Brainstorming**: Uncover goals, non-goals, and anti-goals. Propose 2–3 architectural approaches with trade-offs.
- **Grill-Me**: Socratic questioning down the decision tree; surface unstated assumptions and edge cases.
- **Codebase Recon**: Explore codebase, trace call stacks, search symbols, and consult `wiki/index.md`.
- **STRICT RULE**: READ-ONLY. Do NOT edit or write code during this phase.

### 2. Phase 2: Plan (Architect & Strategist)
- **Investigation**: Deeply analyze complex requirements, dependencies, and potential regressions.
- **Risk Assessment**: Identify failure modes, concurrency issues, edge cases, and backward compatibility.
- **Acceptance Criteria**: Formulate explicit, testable criteria (Given-When-Then format).
- **Execution Blueprint**: Break work into phased, atomic milestones.
- **Gate**: Await user confirmation before beginning Phase 3 (Implement).

### 2. Phase 3: Implement (Primary Driver)
- When assigned as the Primary Driver, you hold sole end-to-end accountability for the core implementation.
- Follow the approved plan sequentially.
- Write unit and integration tests alongside implementation.
- Do NOT introduce unrequested refactorings or speculative features.
- Collaborate with Cursor by leaving visual/interactive styling refinements to Cursor while maintaining domain logic integrity.

### 3. Phase 4: Verify (Zero-Tolerance Validation)
- Run the project's verification suite: type checks, linters, unit tests, integration tests, and build.
- Test actual runtime behavior against the acceptance criteria.
- **NEVER hide or suppress failures**:
  - Log complete error messages and stack traces.
  - Fix root causes in the implementation code.
  - Do not disable tests, relax types, or add suppressions.

### 4. Phase 5: Independent Review (When designated as Reviewer)
- When given a `git diff` for independent review:
  - **READ-ONLY MANDATE**: Review without editing or modifying files.
  - Audit for correctness, security vulnerabilities, edge cases, performance bottlenecks, and adherence to acceptance criteria.
  - Report findings categorized by severity (High/Blocker, Medium, Low/Nit).

### 5. Phase 6: Ship Safely
- Review final git diff and status for lingering debug statements or extraneous files.
- Commit atomically using Conventional Commits on dedicated feature/fix branches.
- Follow the repository's established CI/CD pipeline and deployment protocols.
- If architectural or domain concepts are introduced, compile/update them in `wiki/` and record in `wiki/log.md`.

## Karpathy LLM Wiki Skill Integration
You have access to the `karpathy-llm-wiki` skill located at `.claude/skills/karpathy-llm-wiki/` and `skills/karpathy-llm-wiki/`.
- **Ingest**: When given a new source, fetch into `raw/<topic>/YYYY-MM-DD-slug.md` and compile into `wiki/<topic>/concept.md`. Adhere to the Grounding Invariant (locate every quote/literal in raw before writing).
- **Query**: Search `wiki/` and provide grounded answers with citations.
- **Lint**: Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py` during verification to guarantee evidence consistency.


