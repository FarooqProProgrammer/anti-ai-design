---
description: "Spec gate (analyze) + turn tasks.md into an ordered Spiral checkpoint plan"
---

# Spiral: tasks → checkpoints

The current Spec Kit feature is ready to be sliced into Spiral checkpoints. Load the `spiral` skill and follow
`references/speckit.md`, sections **Spec gate** and **Tasks → checkpoints**.

1. Resolve the feature directory from `.specify/feature.json` (`feature_directory`). If it is missing, use the most recent `specs/*/`
   that has a `tasks.md`, and say which one you picked.
2. If `spiral.config.json` is missing, run the `/spiral-init` procedure now. Don't stop to send the engineer elsewhere.
3. **Spec gate:** run the `speckit-analyze` checks on spec.md / plan.md / tasks.md against the constitution. For CRITICAL issues,
   fix them yourself by invoking the relevant skill (`speckit-clarify`, `speckit-plan`) or by editing tasks.md, then re-check,
   up to 2 rounds. Only a CRITICAL issue that needs a product decision goes to the engineer. Report HIGH issues in the approval
   summary.
4. Write `.spiral/runs/<feature-dir-name>/checkpoints.md` (mode `spec`), covering every unchecked task ID exactly once. When
   invoked after `speckit-converge`, append checkpoints only for the newly added tasks and keep the existing ones.
5. If `spiral.config.json → spec.approveCheckpoints` is true (default), show the checkpoint table and ask with AskUserQuestion:
   **Approve** / **Edit** / **Split feature**, revising until approved. If it's false, record `auto-approved` in checkpoints.md.
6. Continue without handing back: if this ran inside `/spiral-ship` or `speckit-implement`, return to that flow. If it ran on its
   own after a manual `/speckit-tasks`, go straight on with the `/spiral-run <feature-dir-name> all` procedure.
