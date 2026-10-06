---
description: Turn a target (screen, feature, migration, bug, refactor) into an ordered Spiral checkpoint plan for the engineer to approve.
argument-hint: <target — e.g. "migrate OrdersScreen from legacy/ to app/", "SOW 4.2 provider onboarding (figma: <url>)", "bug #142 double charge">
---

Load the `spiral` skill and read `references/checkpoints.md`. Target: $ARGUMENTS

1. If `spiral.config.json` is missing, stop and tell the engineer to run `/spiral-init` first.
   If the target is a Spec Kit feature (`specs/NNN-name/` or its name) with a `tasks.md`, use `spec` mode: follow
   `references/speckit.md` (spec gate, then tasks → checkpoints) and skip to step 5. If Spec Kit is installed and the target
   is a substantial new feature with no spec yet, recommend starting with `/speckit-specify` instead of `feature` mode.
2. **Classify the mode** (`migration` | `feature` | `fix`) and **locate the reference**: the legacy files, the ticket/SOW text and
   Figma nodes, or the bug report. If the reference is missing or ambiguous, ask. The reference is the spec, so don't plan
   without one.
3. **Read the reference** directly. Don't summarise it into a long spec. Also read `.spiral/memory.md` (Process rules
   affect slicing) and look for existing code you'll extend or reuse.
4. **Write `.spiral/runs/<target-slug>/checkpoints.md`** in the format from `references/checkpoints.md`: 3–10 checkpoints, 1–3 lines each,
   each marked `ui`/`logic`, ordered by rising complexity, with *Out of scope* and *Questions* filled in.
5. **Show the checkpoint table** in chat and ask with AskUserQuestion: **Approve plan** / **Edit** (they describe the changes) /
   **Split target**. Revise until approved. Any lasting preference they express about slicing goes into memory → Process.
6. When it's approved, tell them to run `/spiral-run <target-slug>` (one checkpoint) or `/spiral-run <target-slug> all`.
