# AI Request Firewall

> Sources: AI Request Firewall Specification, 2026-10-14
> Raw: [Firewall Spec](../../raw/workflow/2026-10-14-firewall-spec.md)
> Updated: 2026-10-14

## Overview

The Request Firewall stops shortcuts before they touch the codebase. When an AI agent gets a request, it cannot jump straight into hacking files, disable failing tests, or self-approve a pull request. Every change must clear six practical gates in order.

## Shortcut Interception

When someone prompts: "Just quickly patch this file", "Generate the code for X", or "Skip tests and push", the firewall steps in and runs the full process:
1. Understand what's actually happening in the code first.
2. Write a clear plan with testable criteria.
3. Let one agent drive the implementation.
4. Verify that tests pass and the runtime actually works.
5. Review the diff with fresh context without editing.
6. Ship safely on a clean branch.

## The Six Quality Gates

- **Gate 1: Understand**
  - Agents: Cursor, Claude Code, Codex, Antigravity.
  - Skills Required: `brainstorming` and `grill-me`.
  - BLOCKED: Editing, creating, or deleting source code during this phase.
  - BLOCKED: Skipping Brainstorming (goals, non-goals, trade-offs) or Grill-Me (Socratic decision tree questioning).
  - BLOCKED: Skipping `wiki/index.md` or existing design patterns.

- **Gate 2: Plan**
  - Agents: Cursor, Claude Code, Codex, Antigravity.
  - BLOCKED: Touching code before getting human sign-off on the plan.
  - BLOCKED: Vague plans missing testable acceptance criteria or failure modes.
  - BLOCKED: Unresolved external specs (must be fetched into `raw/` and compiled in `wiki/`).

- **Gate 3: Implement (Single Driver)**
  - Agents: Cursor, Claude Code, Codex, Antigravity.
  - BLOCKED: Bouncing core logic back and forth between different agents mid-task.
  - BLOCKED: Sneaking in unrelated refactors or out-of-scope edits.

- **Gate 4: Verify (Zero Concealment)**
  - Agents: Any agent with the project test runner.
  - BLOCKED: Concealed failures (commented-out tests, softened assertions, `@ts-ignore`, `eslint-disable`).
  - BLOCKED: Type errors, linter warnings, or failing tests.
  - BLOCKED: Inconsistent wiki evidence (python skills/karpathy-llm-wiki/scripts/check_evidence.py . reports errors).

- **Gate 5: Review Independently (Read-Only Auditor)**
  - Agents: An agent running in a fresh, clean context or a separate model.
  - BLOCKED: The reviewer making edits or rewriting code during the review.
  - BLOCKED: Self-approving or skipping independent review.
  - BLOCKED: Leaving high-severity issues or security bugs unaddressed.

- **Gate 6: Ship Safely (Branch Hygiene & CI/CD)**
  - Agents: The driver agent and the engineer.
  - BLOCKED: Committing straight to protected branches (main, master).
  - BLOCKED: Leaving behind debug statements (console.log, print(), debugger) or temporary files.
  - BLOCKED: Merging with failing remote CI checks.

## See Also

- [Universal AI Engineering Workflow](universal-workflow.md)
