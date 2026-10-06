---
description: Show Spiral progress for this project: checkpoint statuses, gate attempts, escalations, memory growth, and whether autonomy can be raised.
argument-hint: [target-slug]
---

Load the `spiral` skill. Read `spiral.config.json`, `.spiral/memory.md`, and every `.spiral/runs/*/checkpoints.md` (or just $ARGUMENTS),
plus the gate reports.

Report concisely:
1. Per target: the checkpoint table (`#`, kind, title, status) and the current branch/commit for each `done` checkpoint (`git log --grep "spiral(<slug>)"`).
2. **Escalations** first, each with its blocker line and the decision needed.
3. **Gate stats** across checkpoints: average attempts per gate, the most common gate-1 failure kind, reviewer findings
   per round, and how many gate-4s requested changes.
4. **Memory:** the number of rules per section and the rules added in the last 3 checkpoints. Flag project rules that look
   general enough for the house rules (or that another project also has) and suggest `/spiral-promote`.
5. **Guardrail audit** (from each `$CP/phase.log` and the committed diffs): test re-opens (`phase tests` re-entries and
   `RELOCK` lines, with reasons), any `verify-tests FAIL`, and every `spiral-allow:` suppression currently in the code. Also report the
   current `$SPIRAL status`; if the phase isn't `idle` and no run is in progress, say so.
6. **Autonomy suggestion:** if `autonomy` is `checkpoint` and the last 3 gate-4s were approved without code changes, suggest
   switching to `batch`. If a `batch` target came back with change requests, suggest switching back.

Read-only: don't change any files.
