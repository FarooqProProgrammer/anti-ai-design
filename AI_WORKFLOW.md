# AI Engineering Workflow

A pragmatic, disciplined workflow for building software with AI coding agents (Cursor, Claude Code, Codex, and Antigravity). It keeps AI models from making wild assumptions, hacking code in a rush, hiding failing tests, or breaking existing architecture.

---

## The AI Request Firewall

> [!IMPORTANT]
> **Every request stops at the firewall first.**
> No agent jumps straight to writing or editing code. When you give a prompt, request a feature, or report a bug, the firewall intercepts it:
> 1. **Match with Wiki & Docs First:** Take the input and check it against `wiki/index.md` and project documentation. If it contradicts established architecture, invariants, or ADRs, **halt and return the contradiction immediately**.
> 2. **Run the 7 Gates Sequentially:**
>    `Understand ➔ Spec ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely`.
>
> Skipping planning, disabling tests, self-approving, or pushing unreviewed diffs is **BLOCKED**. Details live in **[`FIREWALL.md`](file:///d:/ai%20agent/the-developer/FIREWALL.md)**.

---

## The 7-Phase Lifecycle Matrix

> [!NOTE]
> **Any agent can drive any phase:**
> This workflow isn't split into rigid silos. **Cursor**, **Claude Code**, **Codex**, or **Antigravity** can run all seven phases end-to-end, or collaborate as a team. What matters is following the gates and not cutting corners.

| Phase | Agent Role | Core Focus | Exit Criteria |
|---|---|---|---|
| **0. Pre-Admission** | Any Agent + Wiki / Docs | Match input against `wiki/` and docs; check for contradictions | Contradictions returned or input validated |
| **1. Understand** | Any Agent + **Brainstorming & Grill-Me** | Trace code, explore patterns, run Socratic interview, check `wiki/` | Context snapshot with trade-offs; **zero code edits** |
| **2. Spec** | Any Agent | Functional & technical contracts: schemas, APIs, invariants | Approved specification; **zero code edits** |
| **3. Plan** | Any Agent | Implementation blueprint, weigh risks, write Given-When-Then tests | Approved plan with acceptance criteria & risk matrix |
| **4. Implement** | **Primary Driver** (Cursor, Claude, Codex) + **Parallel Agents** | Core logic, implementation loop (`Spec➔Plan➔Impl`), `/find-skills`, parallel dispatch | Completed plan; all parallel streams integrated cleanly |
| **5. Verify** | Any Agent + Test Runner | Automated quality gates, high-risk domain checks, evidence completion report | All checks green; zero suppressed errors; evidence report filed |
| **6. Review Independently** | Auditor (Clean Context / Second Agent) | Audit final git diff with one mandate: **review without editing** | All confirmed review findings addressed & verified |
| **7. Ship Safely** | Any Agent + Engineer | Clean diff check, atomic commit, CI/CD run, compound knowledge | Clean diff, passed CI/CD, documented in `wiki/` |

---

> **Lifecycle Diagram:** View and edit the workflow diagram in **[`workflow.exceldraw`](file:///d:/ai%20agent/the-developer/workflow.exceldraw)** (or **[`workflow.excalidraw`](file:///d:/ai%20agent/the-developer/workflow.excalidraw)** / **[`workflow.svg`](file:///d:/ai%20agent/the-developer/workflow.svg)**).

---

## Phase Breakdown

### Phase 1: Understand
**Tools:** Cursor, Claude Code, Codex, or Antigravity  
**Skills:** **`brainstorming`** (`skills/brainstorming/`) & **`grill-me`** (`skills/grill-me/`)  
**Objective:** Figure out how the code actually works today and pin down the true requirements before touching a single line.

#### What to Do:
1. **Contradiction Check Against Wiki & Docs**:
   - Match the input request against `wiki/index.md` and compiled `wiki/` articles.
   - If a contradiction is detected, halt immediately and return the contradiction with links to the conflicting wiki articles before proceeding.
2. **Brainstorming (`skills/brainstorming/SKILL.md`)**:
   - Call out Goals, Non-Goals, and Anti-Goals.
   - Lay out 2–3 architectural approaches with real trade-offs (e.g. minimal vs. extensible vs. high performance).
   - Ask clarifying questions before settling on a design.
3. **Grill-Me (`skills/grill-me/SKILL.md`)**:
   - Run a Socratic technical interview.
   - Walk down the decision tree branch by branch.
   - Pressure-test edge cases, network failures, empty states, and breaking changes.
   - Don't just nod along; bring hidden assumptions out into the open.
4. **Explore the Codebase**:
   - Trace caller and callee chains across affected files.
   - Check `wiki/index.md` for earlier architecture decisions and ADRs.
   - Note down existing conventions for error handling, state, and naming.
5. **Hard Rule**:
   - **Do not write or edit code.** Gather context only.
6. **Diagram**:
   - Maintain and describe `diagrams/01-understand.exceldraw`.

---

### Phase 2: Spec
**Tools:** Cursor, Claude Code, Codex, or Antigravity  
**Objective:** Formalize requirements into an unambiguous Technical & Functional Specification (the WHAT, not the HOW).

#### What to Do:
1. **Functional Specification**:
   - Map user journeys and sequential interaction workflows.
   - Pin down behavioral invariants that must always hold true.
   - Define state machine transitions and invalid trigger handling.
   - Explicitly list non-features to stop scope creep before it starts.
2. **Technical & Contract Specification**:
   - Author TypeScript interfaces, data structs, or class signatures.
   - Specify API contracts: endpoints, payloads, HTTP status codes, and error envelopes.
   - Define database schema updates, foreign keys, and indexes.
   - Ingest external specs or RFCs into `raw/<topic>/` and compile them into `wiki/`.
3. **Non-Functional Guardrails**:
   - Set latency thresholds (e.g., `<50ms`), memory limits, and compute budgets.
   - Specify authentication boundaries, permissions, and input sanitization.
   - Ensure concurrency safety and race-condition resistance.
   - Guarantee backward compatibility and define schema migration paths.
4. **Hard Rule**:
   - **READ-ONLY on source code.** Do not write implementation code.
5. **Diagram**:
   - Maintain and describe `diagrams/02-spec.exceldraw`.

---

### Phase 3: Plan
**Tools:** Cursor, Claude Code, Codex, or Antigravity  
**Objective:** Map out how to build the approved specification, how to test it, and what could go wrong.

#### What to Do:
1. **Requirements & Scope**:
   - Pull in the approved specification from Phase 2.
   - Ingest any newly identified external RFCs or documentation into `raw/` and compile them into `wiki/` via `karpathy-llm-wiki`.
   - Call out potential breaking changes or migration headaches early.
2. **Risk & Mitigation Matrix**:
   - Identify concurrency issues, performance bottlenecks, and security gaps.
   - Write down how you will handle each one.
3. **Acceptance Criteria**:
   - Write clear, testable criteria using Given-When-Then format.
4. **Milestones**:
   - Break the task into sequential, bite-sized checkpoints.
5. **Human Sign-Off**:
   - Get explicit approval from the engineer before starting implementation.
6. **Diagram**:
   - Generate `diagrams/03-plan.exceldraw`.

---

### Phase 4: Implement
**Tools:** Cursor, Claude Code, Codex, or Antigravity  
**Objective:** Build the change cleanly, sticking strictly to the approved plan.

#### The Single Driver Principle:
> [!IMPORTANT]
> **One agent drives the main implementation.**
> Whether that driver is Cursor, Claude Code, or Codex, keep ownership of the core logic with that agent.
> - **Using Cursor alone:** Cursor writes the core logic, adds tests, and polishes the UI.
> - **Collaborating (e.g., Claude Code + Cursor):** Claude Code drives the backend and core business logic, while Cursor handles interactive UI styling and visual tweaks.
> - **Avoid chaos:** Never bounce core logic between competing agents on the fly.

#### The Implementation Loop Gate:
When an implementation phase involves multiple tasks, independent components, or missing capabilities:
1. **Decomposition Loop (`Implement ➔ Loop ➔ Spec ➔ Plan ➔ Implement`):**
   - Never write monolithic, un-specified code across multiple domain layers at once.
   - Break multi-part features into decoupled, atomic sub-features.
   - Run each sub-feature through its own mini-loop: `Spec (Contracts/Schemas) ➔ Plan (Acceptance Criteria/Roadmap) ➔ Implement`.
2. **Skill Discovery via `/find-skills`:**
   - When specialized capabilities or new domain knowledge are required (e.g., specialized testing, auth, animations, mobile, databases):
   - Invoke `/find-skills` or run `npx skills find <domain>` to search the open skills ecosystem on `skills.sh`.
   - Install verified packages via `npx skills add <package>` so agents have authoritative instructions and tools.
3. **Dispatch Parallel Agents:**
   - If sub-features are decoupled and independent (e.g. backend services vs. frontend UI vs. database migrations):
   - The Primary Driver dispatches parallel subagents to work concurrently in isolated contexts.
   - Each parallel subagent is constrained strictly to its approved sub-spec and sub-plan.
4. **Master Reconciliation:**
   - The Primary Driver reviews all parallel diffs, resolves integration points, and ensures zero drift before advancing to Phase 5 Verify.

#### What to Do:
1. **Follow the Plan**:
   - Implement step-by-step; write unit and integration tests alongside your code.
   - Keep to the patterns discovered in Phase 1 and contracts defined in Phase 2.
2. **Clean Scope**:
   - Don't rewrite unrelated code or introduce unrequested refactorings.
   - Keep the diff small, focused, and reviewable.
3. **Diagram**:
   - Generate `diagrams/04-implement.exceldraw`.

---

### Phase 5: Verify
**Tools:** Any Agent + Test Runner / Environment  
**Objective:** Prove the code actually works, catch regressions, and provide verifiable evidence.

#### What to Do:
1. **Automated Quality Gates (Risk-Tiered)**:
   - Automate Git diff sanity checks, TypeScript/typecheck, linters, tests, dependency/security checks, and CI build according to task risk.
   - Catch common regressions before independent review and deployment.
2. **Stricter Checks for High-Risk Domains**:
   - **Database Migrations:** Test schema changes, index impact, and verify rollback scripts with zero accidental data loss.
   - **Authentication:** Verify session invalidation, token lifecycle, CSRF/CORS, and password/credential handling.
   - **Permissions (RBAC):** Run negative permission tests; verify cross-tenant boundaries and unauthorized access blocking.
   - **Payment & Billing:** Test currency decimal precision, idempotency key enforcement, webhook verification, and race conditions.
3. **Zero Concealment**:
   > [!CAUTION]
   > **Never hide, skip, or suppress failing tests.**
   > - Don't comment out assertions, add `@ts-ignore`, or slap on `eslint-disable`.
   > - Capture the actual error message and stack trace.
   > - Fix the root cause in the implementation code.
4. **Evidence-Based Completion Report**:
   At the completion of every task, the agent MUST produce an evidence report before hand-off:
   - **What changed?**: Summary of functional and behavioral modifications.
   - **Which files changed?**: Exact list of files matching `git status`.
   - **Which tests actually passed?**: Proof of tests run, passing counts, and command outputs.
   - **What was NOT tested?**: Explicitly call out blind spots, unmocked systems, and untested edge cases.
   - **Remaining risks or manual steps?**: Document pending migrations, required env vars, or manual acceptance checks.
   *(Maintains a clear difference between claiming "Done" and genuinely verified work).*
5. **Diagram**:
   - Generate `diagrams/05-verify.exceldraw`.

---

### Phase 6: Review Independently
**Tools:** Codex, Claude Code, Cursor (Fresh Context), or Antigravity  
**Objective:** Fresh-context audit of the final diff without editing privileges.

#### What to Do:
1. **Fresh Context**:
   - Run the review from a clean conversation or separate model instance so you aren't biased by the coding session.
2. **Review Without Editing**:
   - Prompt: *"You are an independent auditor. Review this git diff for correctness, security, performance, and acceptance criteria. DO NOT edit or modify files."*
3. **Checklist**:
   - Logic: Off-by-one errors, null pointer traps, unhandled promises?
   - Security: Injection risks, leaked credentials, unsanitized input?
   - Performance: N+1 queries, memory leaks, needless re-renders?
   - Criteria: Did we actually deliver what was promised in Phase 2 Spec and Phase 3 Plan?
4. **Fix & Re-verify**:
   - Primary driver fixes confirmed bugs.
   - Run Phase 5 checks again on the updated diff.
5. **Diagram**:
   - Generate `diagrams/06-review.exceldraw`.

---

### Phase 7: Ship Safely
**Owner:** Driver Agent & Engineer  
**Objective:** Package, commit, and ship without surprises.

#### What to Do:
1. **Diff Hygiene**:
   - Check `git diff` and `git status` to ensure no stray `console.log`, `print()`, or temporary files made it in.
2. **Branch Discipline**:
   - Commit on a feature or bugfix branch (`feature/...`, `fix/...`), never straight to `main` or `master`.
3. **Conventional Commits**:
   - Write clear, concise commits: `feat(scope): concise description` or `fix(scope): concise description`.
4. **CI/CD**:
   - Push, open a PR with the plan and verification proof, and make sure remote CI builds pass.
5. **Compound What You Learned**:
   - If you built a new pattern or added domain rules, write or update an article in `wiki/` and log it in `wiki/log.md`.
6. **Diagram**:
   - Generate `diagrams/07-ship.exceldraw`.

---

## Humanized Content Standard

All content produced in this workspace—including code comments, docstrings, commit messages, PR descriptions, and markdown documentation—must sound like it was written by a thoughtful human software engineer:
- **No AI Clichés:** Ban empty buzzwords like "delve into", "tapestry", "in conclusion", "it's important to remember", "testament to", "harnessing", "streamlining", or "game-changer".
- **Clear Active Voice:** Write directly: "we recommend", "this function throws when...", "here's how to configure".
- **Pragmatic Comments:** Explain *why* something unusual was done, not what the syntax already shows.
- **Natural Rhythm:** Keep sentences direct, punchy, and grounded in real software engineering trade-offs.

---

## Compounding Knowledge: Karpathy LLM Wiki

To prevent knowledge amnesia and stop re-learning the same things repeatedly, the project uses the Karpathy LLM Wiki (`skills/karpathy-llm-wiki/`).

- **`raw/` (Immutable Sources)**: RFCs, upstream docs, articles, and meeting notes. Agents read these but never modify existing files.
- **`wiki/` (Compiled Articles)**: Clean markdown articles maintained by LLMs, backed by `wiki/index.md` and `wiki/log.md`.
- **The Grounding Invariant**: Every number, date, and quote in `wiki/` must exist verbatim in `raw/`.
- **Verification**: Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .` to ensure zero broken citations or fabricated facts.
