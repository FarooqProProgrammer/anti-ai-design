---
description: Build Spiral checkpoints through the four gates (behavior tests, UI review, two adversarial reviewers, engineer approval) and commit each one when it passes.
argument-hint: [target-slug] [cp-NN | next | all]   (defaults: the only active target, next)
---

Load the `spiral` skill and follow `references/gates.md` exactly. Arguments: $ARGUMENTS

- Resolve the target: the given slug, or the only plan in `.spiral/runs/` whose checkpoints aren't all `done`. If there
  are several, ask which one.
- Resolve the checkpoints: `cp-NN` = just that one (earlier ones must be `done`); `next` (default) = the first one not `done`;
  `all` = every remaining checkpoint in order.
- Resume safely: if a checkpoint is `building`/`gates`, read its gate reports and `phase.log`, restore the matching phase with
  `$SPIRAL phase …`, and continue from the last incomplete gate. Don't restart from scratch. If it's `escalated`, show the
  blocker and ask how to proceed.
- Every phase change goes through `$SPIRAL` (SKILL.md → Guardrails). If a hook denies an action, treat it as a gate signal:
  fix the real problem or escalate. Never route around it.

For each checkpoint run gates 1 → 2 → 3 → 4 as specified, keeping checkpoints.md statuses and the `$CP/gate-*.md` reports
current. Subagents: `spiral-test-writer`, `spiral-ui-reviewer`, and `spiral-reviewer-architecture` +
`spiral-reviewer-correctness` (both launched in the same message).

Between gates, post one-line progress updates (e.g. "cp-02 · gate 1 attempt 2: 1 failing test, fixing empty state").
Stop and escalate on loop-budget exhaustion. Never weaken tests, lint, or review findings to get green. Whenever the run
ends (all done, one checkpoint done, escalated, or interrupted by the engineer), leave the state at `$SPIRAL phase idle`
so the guards don't affect the engineer's normal work.
