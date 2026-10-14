# Universal AI Engineering Workflow

> Sources: AI Engineering Workflow Specification, 2026-10-14
> Raw: [AI Workflow Spec](../../raw/workflow/2026-10-14-ai-workflow-spec.md)
> Updated: 2026-10-14

## Overview

A pragmatic, disciplined workflow for building software with AI coding agents (Cursor, Claude Code, Codex, and Antigravity). It keeps AI models from making wild assumptions, hacking code in a rush, hiding failing tests, or breaking existing architecture.

## The Universal 6-Phase Lifecycle

Any agent (Cursor, Claude Code, Codex, Antigravity) can run all six phases end-to-end, or collaborate as a team:

1. **Phase 1: Understand**
   - Skills Required: `brainstorming` and `grill-me`.
   - Objective: Trace code, explore patterns, run Socratic interview, check `wiki/index.md`.
   - Rule: READ-ONLY. Zero code edits.

2. **Phase 2: Plan**
   - Objective: Investigate requirements, weigh risks, write Given-When-Then tests.
   - Rule: Human sign-off required before writing code.

3. **Phase 3: Implement**
   - Objective: Write core logic, build tests, polish UI.
   - Single Driver Principle: One agent drives the main implementation. Never bounce core logic between competing agents on the fly.

4. **Phase 4: Verify**
   - Objective: Run types, linters, test suites, runtime behavior validation, and the wiki evidence audit.
   - Zero Concealment: Never hide, skip, or suppress failing tests. Capture error logs and fix root causes.

5. **Phase 5: Review Independently**
   - Objective: Fresh-context audit of final git diff.
   - Rule: Review without editing. Never modify files while in review mode.

6. **Phase 6: Ship Safely**
   - Objective: Clean diff check, atomic conventional commit on feature branch, CI/CD run, compound knowledge into `wiki/`.

## Humanized Content Standard

All content produced in this workspace—including code comments, docstrings, commit messages, PR descriptions, and markdown documentation—must sound like it was written by a thoughtful human software engineer:
- No AI Clichés: Ban empty buzzwords like "delve into", "tapestry", "in conclusion", "it's important to remember", "testament to", "harnessing", "streamlining", or "game-changer".
- Clear Active Voice: Write directly: "we recommend", "this function throws when...", "here's how to configure".
- Pragmatic Comments: Explain why something unusual was done, not what the syntax already shows.
- Natural Rhythm: Keep sentences direct, punchy, and grounded in real software engineering trade-offs.

## Diagram Requirement

Every phase the agent must maintain and describe an ExcelDraw diagram (.exceldraw, .excalidraw, .svg).

## See Also

- [AI Request Firewall](request-firewall.md)
