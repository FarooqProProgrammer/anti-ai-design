---
type: Workflow Specification
title: Universal AI Engineering Workflow
description: Pragmatic, disciplined 7-phase lifecycle for building software with AI coding agents.
resource: file:///d:/ai%20agent/the-developer/AI_WORKFLOW.md
tags: [workflow, lifecycle, engineering, quality-gates]
timestamp: 2026-10-14
---

# Universal AI Engineering Workflow

> Sources: AI Engineering Workflow Specification, 2026-10-14
> Raw: [AI Workflow Spec](../../raw/workflow/2026-10-14-ai-workflow-spec.md)
> Updated: 2026-10-14

## Overview

A pragmatic, disciplined workflow for building software with AI coding agents (Cursor, Claude Code, Codex, and Antigravity). It keeps AI models from making wild assumptions, hacking code in a rush, hiding failing tests, or breaking existing architecture.

## The Universal 7-Phase Lifecycle

Any agent (Cursor, Claude Code, Codex, Antigravity) can run all seven phases end-to-end, or collaborate as a team:

0. **Pre-Admission: Contradiction Check**
   - Match input against `wiki/` and project documentation; check for contradictions and return any conflicts immediately.

1. **Phase 1: Understand**
   - Skills Required: `brainstorming` and `grill-me`.
   - Objective: Trace code, explore patterns, run Socratic interview, check `wiki/index.md`.
   - Rule: READ-ONLY. Zero code edits.

2. **Phase 2: Spec**
   - Objective: Formalize requirements into an unambiguous Technical & Functional Specification (the WHAT, not the HOW).
   - Rule: READ-ONLY on source code. Zero code edits.

3. **Phase 3: Plan**
   - Objective: Investigate requirements, weigh risks, write Given-When-Then tests.
   - Rule: Human sign-off required before writing code.

4. **Phase 4: Implement**
   - Objective: Write core logic, build tests, polish UI.
   - Single Driver Principle: One agent drives the main implementation. Never bounce core logic between competing agents on the fly.
   - Implementation Loop Gate: If multiple things or domain gaps arise, loop back (Implement -> Loop -> Spec -> Plan -> Implement). Use /find-skills to discover and install missing tools, and dispatch parallel agents for decoupled sub-modules under Single Driver orchestration.

5. **Phase 5: Verify**
   - Objective: Run types, linters, test suites, runtime behavior validation, and the wiki evidence audit.
   - Automated Quality Gates (Risk-Tiered): Automate Git diff sanity checks, TypeScript/typecheck, linters, tests, dependency/security checks, and CI build according to task risk.
   - Stricter Checks for High-Risk Domains:
     - Database Migrations: Test schema changes, index impact, and verify rollback scripts with zero accidental data loss.
     - Authentication: Verify session invalidation, token lifecycle, CSRF/CORS, and password/credential handling.
     - Permissions (RBAC): Run negative permission tests; verify cross-tenant boundaries and unauthorized access blocking.
     - Payment & Billing: Test currency decimal precision, idempotency key enforcement, webhook verification, and race conditions.
   - Zero Concealment: Never hide, skip, or suppress failing tests. Capture error logs and fix root causes.
   - Evidence-Based Completion Report: At the completion of every task, the agent MUST produce an evidence report before hand-off:
     1. What changed? Summary of functional and behavioral modifications.
     2. Which files changed? Exact list of files matching git status.
     3. Which tests actually passed? Proof of tests run, passing counts, and command outputs.
     4. What was NOT tested? Explicitly call out blind spots, unmocked systems, and untested edge cases.
     5. Remaining risks or manual steps? Document pending migrations, required env vars, or manual acceptance checks.

6. **Phase 6: Review Independently**
   - Objective: Fresh-context audit of final git diff.
   - Rule: Review without editing. Never modify files while in review mode.

7. **Phase 7: Ship Safely**
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
