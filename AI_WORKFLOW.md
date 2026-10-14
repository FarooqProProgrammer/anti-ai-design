# AI Engineering Workflow Specification

An end-to-end, multi-agent development lifecycle designed to maximize code quality, eliminate AI hallucinations, and prevent architectural regressions by enforcing role segregation and verification gates.

---

## The AI Request Firewall

> [!IMPORTANT]
> **EVERY INCOMING REQUEST MUST PASS THROUGH THE FIREWALL.**
> No agent may write or modify code directly. All user prompts, feature requests, and bug reports must be intercepted by the Request Firewall and routed sequentially through all 6 phases:
> `Understand ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely`.
> Any attempt to jump directly to coding, bypass tests, self-approve, or push unverified diffs is **BLOCKED** by the Firewall. See detailed rules in **[`FIREWALL.md`](file:///d:/ai%20agent/the-developer/FIREWALL.md)**.

---

## The 6-Phase Lifecycle Matrix

| Phase | Primary Agent / Tool | Secondary / Support | Core Objective | Quality Gate / Exit Criteria |
|---|---|---|---|---|
| **1. Understand** | **Cursor** | **LLM Wiki (Query)** | Explore relevant codebases, consult compiled wiki knowledge, identify design patterns | Documented context notes & pattern map; **zero code modifications** |
| **2. Plan** | **Claude Code** | **LLM Wiki (Ingest)** | Investigate complex requirements, ingest external RFCs/specs into wiki, generate acceptance criteria | Approved implementation plan with explicit testable criteria & risk matrix |
| **3. Implement** | **Claude Code** or **Codex** (Single Driver) | **Cursor** (Interactive & UI) | Execute main change according to plan; scoped UI refinement | Plan items completed; single agent ownership maintained; no speculative scope |
| **4. Verify** | **Project Shell / Agent** | **LLM Wiki (Lint)** | Run full test suites, typechecks, linter, runtime checks, and wiki evidence verification | 100% checks passing; all failures captured and resolved; zero hidden errors |
| **5. Review Independently** | **Codex** or **Claude Code** (Read-Only) | - | Independent audit of `git diff` without editing permissions | All high/medium severity findings remediated and re-verified |
| **6. Ship Safely** | **Driver Agent / Engineer** | **LLM Wiki (Compound)** | Atomic commit, branch push, PR review, CI pipeline validation, and wiki knowledge compounding | Clean diff, passed CI/CD checks, deployment readiness verified, wiki updated |

---

> **Visual Diagram:** View and edit the lifecycle architecture diagram in **[`workflow.exceldraw`](file:///d:/ai%20agent/the-developer/workflow.exceldraw)** (or **[`workflow.excalidraw`](file:///d:/ai%20agent/the-developer/workflow.excalidraw)** / **[`workflow.svg`](file:///d:/ai%20agent/the-developer/workflow.svg)**).

---

## Detailed Phase Specifications

### Phase 1: Understand
**Owner:** Cursor  
**Goal:** Build complete architectural awareness and map dependencies before proposing any modifications.

#### Protocols & Actions:
1. **Repository Indexing & Search**:
   - Use Cursor's codebase indexing (`@Codebase`, semantic search, symbol search) to locate relevant files, types, and schemas.
   - Trace callers and callees of affected components.
2. **Identify Existing Patterns**:
   - Note error-handling strategies (result types, exceptions, custom error classes).
   - Document state management patterns (stores, hooks, context, immutability).
   - Inspect naming conventions, module structure, and layer boundaries.
3. **Strict Constraints**:
   - **Do NOT edit code** during this phase.
   - Summarize findings into a structured context snapshot (files impacted, patterns identified, constraints).

---

### Phase 2: Plan
**Owner:** Claude Code  
**Goal:** Deeply analyze complex requirements, forecast edge cases, assess risks, and formulate an actionable implementation plan.

#### Protocols & Actions:
1. **Requirements & Scope Investigation**:
   - Ingest requirements, existing codebase context from Phase 1, and technical constraints.
   - Identify implicit requirements, breaking change potentials, and backward compatibility concerns.
2. **Risk & Mitigation Matrix**:
   - Identify performance bottlenecks, race conditions, security vulnerabilities, and API limits.
   - Propose explicit mitigations for each identified risk.
3. **Acceptance Criteria**:
   - Define concrete, testable criteria (Given-When-Then / Gherkin or bulleted test conditions).
4. **Phased Implementation Roadmap**:
   - Divide implementation into sequential, atomic milestones.
   - Define checkpoint criteria for each milestone.
5. **Gate Approval**:
   - The user or lead engineer reviews and approves the plan before execution begins.

---

### Phase 3: Implement
**Owner:** Claude Code or Codex (Primary Driver)  
**Collaborator:** Cursor (Interactive Edits & Frontend Refinement)  
**Goal:** Execute the planned changes with discipline and architectural fidelity.

#### The Single Driver Principle:
> [!IMPORTANT]
> **Exactly one agent holds primary responsibility for the main implementation.**
> Do NOT bounce core backend/business logic between multiple generative agents. This prevents context fragmentation, conflicting paradigms, and code duplication.

#### Protocols & Actions:
1. **Main Change (Claude Code or Codex)**:
   - Follow the approved plan sequentially.
   - Build unit/integration tests alongside or prior to business logic (TDD preferred).
   - Maintain consistency with patterns identified in Phase 1.
2. **Interactive & Frontend Refinement (Cursor)**:
   - Use Cursor for live UI preview iteration, styling tweaks (CSS/Tailwind), visual adjustments, and small interactive fixes.
   - Scope Cursor's role strictly to interactive edits; core business and domain logic remains with the Primary Driver.
3. **Implementation Hygiene**:
   - Do not touch unrelated files or refactor code outside the planned scope.
   - Keep diffs minimal, focused, and clean.

---

### Phase 4: Verify
**Owner:** Driver Agent / Local Environment  
**Goal:** Validate functional behavior, ensure zero regressions, and transparently log all diagnostic outputs.

#### Protocols & Actions:
1. **Automated Checks**:
   - **Type Checking**: Run compiler/typechecker (e.g., `tsc --noEmit`, `mypy`, `cargo check`).
   - **Linting & Formatting**: Run project linters (e.g., `eslint`, `flake8`, `ruff`, `prettier`).
   - **Automated Tests**: Execute unit, integration, and end-to-end test suites.
2. **Behavioral Runtime Verification**:
   - Test the actual behavior against the acceptance criteria defined in Phase 2.
   - Trigger edge cases, error conditions, and empty states.
3. **Failure Transparency Protocol**:
   > [!CAUTION]
   > **Never hide, bypass, suppress, or skip failing tests or type errors.**
   > - Capture the full stack trace and error message.
   > - Root-cause every failure.
   > - Fix the underlying defect, do not modify the test assertions to make failing code appear green unless the requirement itself changed.

---

### Phase 5: Review Independently
**Owner:** Codex or Claude Code (Independent Auditor)  
**Goal:** Fresh-context, objective code review of the final Git diff without editing permissions.

#### Protocols & Actions:
1. **Reviewer Segregation**:
   - The reviewer agent must be initialized with a clean context or be a separate model/agent instance from the implementation driver.
2. **Strict Read-Only Instruction**:
   - Prompt instructions: *"You are an independent code auditor. Review this git diff for correctness, performance, edge cases, and security vulnerabilities. DO NOT edit or modify files."*
3. **Review Evaluation Criteria**:
   - **Correctness & Logic**: Any off-by-one errors, null/undefined hazards, unhandled promise rejections?
   - **Security**: Any injection vectors, unauthorized access, secrets leaked, unsafe deserialization?
   - **Performance**: Any unnecessary allocations, N+1 queries, memory leaks, unoptimized re-renders?
   - **Acceptance Criteria Check**: Does the diff satisfy all criteria defined in Phase 2?
4. **Remediation Loop**:
   - Triage feedback: classify into blocker, fix, or false-positive.
   - Primary driver implements confirmed fixes.
   - Re-run Phase 4 (Verify) on the updated diff.

---

### Phase 6: Ship Safely
**Owner:** Driver Agent & Engineer  
**Goal:** Package, commit, and deploy changes adhering to repository hygiene and CI/CD protocols.

#### Protocols & Actions:
1. **Final Diff Inspection**:
   - Run `git diff` and `git status` to ensure no temporary files, debug statements (`console.log`, `print`, `debugger`), or unintended changes are staged.
2. **Branch Management**:
   - Ensure commits are made on the designated feature or hotfix branch (`feature/...`, `fix/...`), never directly to protected branches (`main`, `master`).
3. **Atomic Conventional Commits**:
   - Use standard conventional commit format:
     `feat(scope): concise description of feature`
     `fix(scope): concise description of bugfix`
4. **CI/CD & Deployment**:
   - Push to remote and open a Pull Request with the implementation plan and verification proof.
   - Monitor CI pipeline until all status checks pass.
   - Adhere to the project's staging and production release gates.
5. **Knowledge Compounding**:
   - If the shipped change introduces new architectural patterns, external APIs, or domain concepts, record or update the corresponding article in `wiki/`.
   - Log the change in `wiki/log.md`.

---

## Compounding Knowledge: Karpathy LLM Wiki Subsystem

This workflow integrates the **Karpathy LLM Wiki** (`skills/karpathy-llm-wiki/`) to prevent amnesia and eliminate repeated exploratory research.

### Core Architecture
- **`raw/` (Immutable Source Material)**: Primary sources, RFCs, API references, meeting notes, articles, and incident logs. Agents read but never modify.
- **`wiki/` (Compiled Knowledge)**: Synthesized markdown articles maintained by LLM agents.
  - `wiki/index.md`: Global table of contents linking all concepts.
  - `wiki/log.md`: Append-only operation log.
- **`skills/karpathy-llm-wiki/`**: The schema and verification scripts (`check_evidence.py`).

### Workflow Operations Across the 6 Phases
1. **Querying (Phase 1: Understand)**:
   - Before exploring raw code, check `wiki/index.md` or search `wiki/<topic>/` for existing domain models, business rules, and technical decisions.
2. **Ingestion & Compilation (Phase 2: Plan)**:
   - When researching external dependencies, algorithms, or complex requirements, fetch the source into `raw/` and compile a clean article in `wiki/`.
   - Maintain the **Grounding Invariant**: every specific number, date, and quote in `wiki/` must exist verbatim in `raw/`.
3. **Verification & Evidence Linting (Phase 4: Verify)**:
   - Run the evidence checker:
     ```bash
     python skills/karpathy-llm-wiki/scripts/check_evidence.py
     ```
   - Verifies that all citations and literal claims in `wiki/` map cleanly to immutable sources in `raw/`.
4. **Knowledge Compounding (Phase 6: Ship Safely)**:
   - Record newly established architecture decisions (ADRs) or system behavioral contracts directly into `wiki/` upon release.


