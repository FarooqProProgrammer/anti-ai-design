# AI Request Firewall Specification

> Source: FIREWALL.md
> Collected: 2026-10-14
> Published: 2026-10-14

## Overview
The Request Firewall stops shortcuts before they touch the codebase. When an AI agent gets a request, it cannot jump straight into hacking files, disable failing tests, or self-approve a pull request. Every change must clear seven practical gates in order.

## First Action: Match Request Against Wiki & Docs (Contradiction Check)
Before accepting any request or beginning Gate 1:
1. Take the input: Parse the user's prompt, requirements, or proposed changes.
2. Match with Wiki & Docs: Query wiki/index.md, search relevant wiki/ articles, and check repository documentation for existing decisions, invariants, and patterns.
3. If a Contradiction is Found:
   - FIREWALL BLOCKS: Halt execution immediately. Do NOT write code or assume intent.
   - Return the Contradiction: Present the conflict clearly to the user, citing the conflicting wiki article and the specific requirement.
   - Await Resolution: Ask whether this is an intentional architectural shift (which requires updating the wiki with a Status: Outdated or Status: Disputed block) or an error.

## Shortcut Interception
When someone prompts: "Just quickly patch this file", "Generate the code for X", or "Skip tests and push", the firewall steps in and runs the full process:
1. Understand what's actually happening in the code first.
2. Specify the exact functional and technical contracts.
3. Write a clear plan with testable criteria.
4. Let one agent drive the implementation.
5. Verify that tests pass and the runtime actually works.
6. Review the diff with fresh context without editing.
7. Ship safely on a clean branch.

## The Seven Quality Gates
Gate 1: Understand
- Agents: Cursor, Claude Code, Codex, Antigravity.
- Skills Required: brainstorming and grill-me.
- Blocking conditions:
  - BLOCKED: Proceeding when the input contradicts established wiki/ articles or project documentation without explicit resolution.
  - BLOCKED: Editing, creating, or deleting source code during this phase.
  - BLOCKED: Skipping Brainstorming (goals, non-goals, trade-offs) or Grill-Me (Socratic decision tree questioning).
  - BLOCKED: Skipping wiki/index.md or existing design patterns.

Gate 2: Spec (Technical & Functional Specification)
- Agents: Cursor, Claude Code, Codex, Antigravity.
- Blocking conditions:
  - BLOCKED: Skipping the specification to begin planning or implementation directly.
  - BLOCKED: Writing or modifying source code during this phase (READ-ONLY on source code).
  - BLOCKED: Ambiguous interface contracts, missing error states, or unspecified schema changes.

Gate 3: Plan
- Agents: Cursor, Claude Code, Codex, Antigravity.
- Blocking conditions:
  - BLOCKED: Touching code before getting human sign-off on the plan.
  - BLOCKED: Vague plans missing testable acceptance criteria or failure modes.
  - BLOCKED: Unresolved external specs (must be fetched into raw/ and compiled in wiki/).

Gate 4: Implement (Single Driver)
- Agents: Cursor, Claude Code, Codex, Antigravity.
- Blocking conditions:
  - BLOCKED: Bouncing core logic back and forth between different agents mid-task.
  - BLOCKED: Sneaking in unrelated refactors or out-of-scope edits.

Gate 5: Verify (Zero Concealment)
- Agents: Any agent with the project test runner.
- Blocking conditions:
  - BLOCKED: Concealed failures (commented-out tests, softened assertions, @ts-ignore, eslint-disable).
  - BLOCKED: Type errors, linter warnings, or failing tests.
  - BLOCKED: Inconsistent wiki evidence (python skills/karpathy-llm-wiki/scripts/check_evidence.py . reports errors).

Gate 6: Review Independently (Read-Only Auditor)
- Agents: An agent running in a fresh, clean context or a separate model.
- Blocking conditions:
  - BLOCKED: The reviewer making edits or rewriting code during the review.
  - BLOCKED: Self-approving or skipping independent review.
  - BLOCKED: Leaving high-severity issues or security bugs unaddressed.

Gate 7: Ship Safely (Branch Hygiene & CI/CD)
- Agents: The driver agent and the engineer.
- Blocking conditions:
  - BLOCKED: Committing straight to protected branches (main, master).
  - BLOCKED: Leaving behind debug statements (console.log, print(), debugger) or temporary files.
  - BLOCKED: Merging with failing remote CI checks.
