# AI Request Firewall

The Request Firewall stops shortcuts before they touch the codebase. When an AI agent gets a request, it cannot jump straight into hacking files, disable failing tests, or self-approve a pull request. Every change must clear seven practical gates in order.

---

## First Action: Match Request Against Wiki & Docs (Contradiction Check)

> [!IMPORTANT]
> **Always match incoming inputs against the wiki and docs first.**
> Before beginning any work or moving past admission:
> 1. **Take the input**: Parse the user's prompt, requirements, or proposed changes.
> 2. **Match with Wiki & Docs**: Query `wiki/index.md`, search relevant `wiki/` articles, and check repository documentation for existing decisions, invariants, and patterns.
> 3. **If a Contradiction is Found**:
>    - 🛑 **FIREWALL BLOCKS**: Halt execution immediately. Do NOT write code or assume intent.
>    - **Return the Contradiction**: Present the conflict clearly to the user, citing the conflicting wiki article (`wiki/<topic>/<article>.md`) and the specific requirement.
>    - **Await Resolution**: Ask whether this is an intentional architectural shift (which requires updating the wiki with a `Status: Outdated` or `Status: Disputed` block) or an error.

---

## How the Firewall Works

```
[ INCOMING REQUEST ]
        │
        ▼
╔════════════════════════════════════════════════════════════════════╗
║                      AI REQUEST FIREWALL                           ║
║   1. Match input with wiki & docs -> If contradict, RETURN error.  ║
║   2. Every change clears all seven gates sequentially.             ║
║   3. Any agent (Cursor, Claude Code, Codex, Antigravity) can drive.║
║   4. Shortcuts, blind edits, and skipped tests are BLOCKED.        ║
╚════════════════════════════════════════════════════════════════════╝
        │
   [GATE 1] ──► 1. UNDERSTAND            (Explore, Brainstorm, Grill-Me, Read-Only)
        │
   [GATE 2] ──► 2. SPEC                  (Functional & Technical Spec: WHAT to build)
        │
   [GATE 3] ──► 3. PLAN                  (Define Risks, Acceptance Criteria: HOW)
        │
   [GATE 4] ──► 4. IMPLEMENT             (Single Driver owns the core change)
        │
   [GATE 5] ──► 5. VERIFY                (Run tests, check runtime, zero concealment)
        │
   [GATE 6] ──► 6. REVIEW INDEPENDENTLY  (Fresh eyes: audit the diff without editing)
        │
   [GATE 7] ──► 7. SHIP SAFELY           (Clean diff, conventional commits, CI/CD)
```

> [!NOTE]
> **Universal Agent Execution:**
> This setup isn't tied to a single tool. **Cursor**, **Claude Code**, **Codex**, or **Antigravity** can handle every single step. Or they can team up. The firewall enforces the engineering discipline so no tool cuts corners.

> [!CAUTION]
> **Shortcut Interception:**
> When someone prompts: *"Just quickly patch this file"*, *"Generate the code for X"*, or *"Skip tests and push"*, the firewall steps in and runs the full process:
> 1. Understand what's actually happening in the code first.
> 2. Specify the exact functional and technical contracts.
> 3. Write a clear plan with testable criteria.
> 4. Let one agent drive the implementation.
> 5. Verify that tests pass and the runtime actually works.
> 6. Review the diff with fresh context without editing.
> 7. Ship safely on a clean branch.

---

## The Seven Quality Gates

### Gate 1: Understand
- **Agents:** Cursor, Claude Code, Codex, Antigravity.
- **Skills Required:** `skills/brainstorming/` and `skills/grill-me/`.
- **The Check:** Did the agent trace the affected files, check caller/callee paths, match against the wiki/docs, and ask the hard questions about edge cases?
- **What Gets Blocked:**
  - 🛑 **BLOCKED**: Proceeding when the input contradicts established `wiki/` articles or project documentation without explicit resolution.
  - 🛑 **BLOCKED**: Editing, creating, or deleting source code during this phase.
  - 🛑 **BLOCKED**: Skipping **Brainstorming** (goals, non-goals, trade-offs) or **Grill-Me** (Socratic decision tree questioning).
  - 🛑 **BLOCKED**: Skipping `wiki/index.md` or existing design patterns.
- **Exit Criteria:** A clear context snapshot with trade-offs weighed, edge cases resolved, contradictions checked, and impacted files mapped out.

### Gate 2: Spec (Technical & Functional Specification)
- **Agents:** Cursor, Claude Code, Codex, Antigravity.
- **The Check:** Are the functional workflows, data schemas, API contracts, error envelopes, and behavioral invariants unambiguously specified before planning tasks?
- **What Gets Blocked:**
  - 🛑 **BLOCKED**: Skipping the specification to begin planning or implementation directly.
  - 🛑 **BLOCKED**: Writing or modifying source code during this phase (READ-ONLY on source code).
  - 🛑 **BLOCKED**: Ambiguous interface contracts, missing error states, or unspecified schema changes.
- **Exit Criteria:** A comprehensive, human-approved Specification document (`WHAT` to build, not `HOW`).

### Gate 3: Plan
- **Agents:** Cursor, Claude Code, Codex, Antigravity.
- **The Check:** Did the agent take the approved Spec, pin down tricky implementation milestones, call out risks, and write concrete acceptance criteria (Given-When-Then)?
- **What Gets Blocked:**
  - 🛑 **BLOCKED**: Touching code before getting human sign-off on the plan.
  - 🛑 **BLOCKED**: Vague plans missing testable acceptance criteria or failure modes.
  - 🛑 **BLOCKED**: Unresolved external specs (must be fetched into `raw/` and compiled in `wiki/`).
- **Exit Criteria:** Explicit approval on the implementation plan from you or the lead engineer.

### Gate 4: Implement (Single Driver)
- **Agents:** Cursor, Claude Code, Codex, Antigravity.
- **The Check:** Does one primary driver own the implementation from start to finish?
- **What Gets Blocked:**
  - 🛑 **BLOCKED**: Bouncing core logic back and forth between different agents mid-task.
  - 🛑 **BLOCKED**: Sneaking in unrelated refactors or out-of-scope edits.
- **Exit Criteria:** Code that fulfills the approved plan and passes initial tests.

### Gate 5: Verify (Zero Concealment)
- **Agents:** Any agent with the project test runner.
- **The Check:** Do all automated checks pass, and did you test the actual behavior?
- **What Gets Blocked:**
  - 🛑 **BLOCKED**: Concealed failures (commented-out tests, softened assertions, `@ts-ignore`, `eslint-disable`).
  - 🛑 **BLOCKED**: Type errors, linter warnings, or failing tests.
  - 🛑 **BLOCKED**: Inconsistent wiki evidence (`python skills/karpathy-llm-wiki/scripts/check_evidence.py .` reports errors).
- **Exit Criteria:** 100% clean test runs, with root causes fixed instead of hidden.

### Gate 6: Review Independently (Read-Only Auditor)
- **Agents:** An agent running in a fresh, clean context or a separate model.
- **The Check:** Did fresh eyes review the entire `git diff` without editing privileges?
- **What Gets Blocked:**
  - 🛑 **BLOCKED**: The reviewer making edits or rewriting code during the review.
  - 🛑 **BLOCKED**: Self-approving or skipping independent review.
  - 🛑 **BLOCKED**: Leaving high-severity issues or security bugs unaddressed.
- **Exit Criteria:** A clear review report, with all valid findings fixed by the primary driver and re-verified.

### Gate 7: Ship Safely (Branch Hygiene & CI/CD)
- **Agents:** The driver agent and the engineer.
- **The Check:** Is the working tree clean, on a feature branch, and passing CI?
- **What Gets Blocked:**
  - 🛑 **BLOCKED**: Committing straight to protected branches (`main`, `master`).
  - 🛑 **BLOCKED**: Leaving behind debug statements (`console.log`, `print()`, `debugger`) or temporary files.
  - 🛑 **BLOCKED**: Merging with failing remote CI checks.
- **Exit Criteria:** A clean PR merged with conventional commits, with new system patterns logged in `wiki/`.

---

## Gate Summary Card

| Gate | Name | Who Runs It | What Gets Blocked |
|---|---|---|---|
| **Pre-Admission** | **Contradiction Check** | Any agent + Wiki / Docs | Unresolved contradictions against documented architecture |
| **Gate 1** | **Understand** | Any agent + Brainstorming & Grill-Me | Writing code, skipping the technical interview |
| **Gate 2** | **Spec** | Any agent (Cursor / Claude / Codex) | Coding without contract specification, ambiguous schemas |
| **Gate 3** | **Plan** | Any agent (Cursor / Claude / Codex) | Coding without an approved plan and acceptance criteria |
| **Gate 4** | **Implement** | Primary Driver | Multi-driver churn, scope creep |
| **Gate 5** | **Verify** | Any agent + test runner | Hidden failures, suppressed errors, broken tests |
| **Gate 6** | **Review Independently** | Auditor (clean context) | Reviewer editing code, unaddressed review blockers |
| **Gate 7** | **Ship Safely** | Driver & engineer | Committing to main, messy diffs, broken CI |
