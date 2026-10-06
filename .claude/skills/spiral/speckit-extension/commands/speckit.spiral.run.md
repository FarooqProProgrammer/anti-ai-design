---
description: "Implement the feature's checkpoints through the four Spiral gates instead of free-form implementation"
---

# Spiral: gated implementation

Spiral is installed in this project, so implementation of this feature goes through Spiral's checkpoints and gates
rather than straight down `tasks.md`.

1. Resolve the feature directory from `.specify/feature.json`. Its Spiral target slug is the directory name (e.g. `003-user-auth`).
2. If `.spiral/runs/<slug>/checkpoints.md` doesn't exist, or unchecked tasks in `tasks.md` aren't covered by any checkpoint, run
   the `speckit.spiral.checkpoints` procedure first and get the plan approved.
3. Load the `spiral` skill and run the remaining checkpoints exactly as `/spiral-run <slug> all` does (`references/gates.md`,
   plus `references/speckit.md` for spec-mode inputs). Each approved checkpoint marks its task IDs `[X]` in `tasks.md`.
4. **Stop rule for the calling `/speckit-implement`:** when this hook returns, continue `/speckit-implement` only to verify
   and report. Do **not** implement any task that is still `[ ]`. Unchecked tasks remain unchecked because a checkpoint
   escalated, is awaiting approval, or the engineer paused, and they may only be built through Spiral gates. Report them and end.
