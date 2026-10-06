---
description: "Spec gate (analyze) + turn tasks.md into an ordered Spiral checkpoint plan for engineer approval"
---

# Spiral: tasks → checkpoints

The current Spec Kit feature is ready to be sliced into Spiral checkpoints. Load the `spiral` skill and follow
`references/speckit.md`, sections **Spec gate** and **Tasks → checkpoints**.

1. Resolve the feature directory from `.specify/feature.json` (`feature_directory`). If it is missing, use the most recent `specs/*/`
   that has a `tasks.md`, and say which one you picked.
2. If `spiral.config.json` is missing, stop and tell the engineer to run `/spiral-init` first. The tasks stay valid and this
   step can be re-run as `/speckit-spiral-checkpoints`.
3. **Spec gate:** run the `speckit-analyze` checks on spec.md / plan.md / tasks.md against the constitution. Any CRITICAL
   issue blocks: list it, recommend the fix (`/speckit-clarify`, `/speckit-plan`, or edit tasks), and stop. HIGH issues are
   shown to the engineer, who decides.
4. Write `.spiral/runs/<feature-dir-name>/checkpoints.md` (mode `spec`), covering every unchecked task ID exactly once. When
   invoked after `/speckit-converge`, append checkpoints only for the newly added tasks and keep the existing ones.
5. Show the checkpoint table and ask with AskUserQuestion: **Approve** / **Edit** / **Split feature**. Revise until approved.
6. On approval, tell the engineer that `/speckit-implement` (or `/spiral-run <feature-dir-name> all`) will now build it through
   the gates.
