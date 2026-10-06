---
description: End-to-end Spiral delivery. Drives Spec Kit itself (constitution → specify → clarify → plan → tasks → analyze), plans checkpoints, builds them through the four gates, and converges, stopping only at the configured human decision points.
argument-hint: <what to build — e.g. "SOW §4.2 provider onboarding, figma: <url>", "specs/003-user-auth", "bug #142 double charge">
---

Load the `spiral` skill and read `references/speckit.md` (section **Driven flow**). Target: $ARGUMENTS

You run the whole pipeline yourself, invoking each Spec Kit skill with the Skill tool (`speckit-specify`, `speckit-clarify`,
`speckit-plan`, `speckit-checklist`, `speckit-tasks`, `speckit-analyze`, `speckit-converge`, `speckit-constitution`). Never
tell the engineer to run a command that you can run. They are interrupted only at the decision points listed in
`spiral.config.json → spec` (defaults in `references/config.md`). Between stages, post a one-line progress update.

## 0. Ready the project (only what's missing)
- No `spiral.config.json`: run the `/spiral-init` procedure (with Spec Kit), batching all its questions into **one** AskUserQuestion.
- No `.specify/`, or the Spiral extension isn't registered: install them (`references/speckit.md → Installing`).
- The constitution is still the template (it contains `[PROJECT_NAME]`-style placeholders): invoke `speckit-constitution`, drafting the
  principles from `.spiral/architecture.md` and the principle-level house rules. Confirm with the engineer once, together with the spec approval below.

## 1. Route the target
- An existing `specs/NNN-name/`: resume at the first missing artifact (spec → plan → tasks → checkpoints → run).
- A **bug or refactor**, a **migration**, or a small change with a clear ticket: skip Spec Kit and go straight to `/spiral-plan`
  then `/spiral-run all` (modes `fix` / `migration` / `feature`). Spec Kit is for substantial new features.
- Otherwise, a new feature: continue in spec mode.

Run all of stage 2 with `$SPIRAL phase plan --target <slug>`, so git stays guarded while the spec files can still be written.

## 2. Spec pipeline (spec mode)
1. **Specify.** Invoke `speckit-specify` with the full feature description, including everything the engineer gave you
   (SOW text, ticket, Figma links, constraints). Execute any mandatory extension hooks it emits (e.g. the git feature branch).
2. **Clarify.** If the spec has `[NEEDS CLARIFICATION]` markers or `speckit-clarify` finds high-impact ambiguity:
   - `spec.clarify: "auto"` (default): answer each question yourself from the sources (SOW, ticket, Figma, existing code, the
     constitution, house rules, project memory), citing the source. Batch **only** the questions no source answers into one
     AskUserQuestion. Record every answer and its source in the spec's Clarifications section.
   - `"ask"`: put all of the questions to the engineer in one AskUserQuestion batch.
3. **Approve spec** (if `spec.approveSpec`): show a 10-line summary (stories with priorities, key requirements, assumptions,
   auto-answered clarifications with sources) and ask **Approve** / **Edit**. This is the one moment the engineer shapes *what*
   gets built, so keep it short and scannable.
4. **Plan.** Invoke `speckit-plan`, passing the project's real stack and `.spiral/architecture.md` conventions so the plan matches the
   codebase instead of inventing a new structure.
5. **Checklist** (if `spec.checklist`): invoke `speckit-checklist` for the configured domains and fix gaps in the spec or plan yourself.
   Ask only if a gap needs a product decision.
6. **Tasks.** Invoke `speckit-tasks`. Its mandatory after-hook runs `speckit.spiral.checkpoints`, which runs the spec gate and
   writes the checkpoints. If the hook didn't run, run that procedure yourself.
   - Spec gate CRITICAL issues: fix them yourself by re-running the relevant skill (`speckit-clarify` / `speckit-plan` / editing
     tasks), then re-check, up to 2 rounds. Escalate only if a CRITICAL issue needs a product decision.
7. **Approve checkpoints** (if `spec.approveCheckpoints`): table + AskUserQuestion, as in `/spiral-plan`.

## 3. Build
Run the `/spiral-run <slug> all` procedure (gates 1–4 per checkpoint, per `autonomy`). Don't call `speckit-implement`: Spiral's
gates are the implementation step.

## 4. Converge
When all checkpoints are `done`: `$SPIRAL phase plan`, invoke `speckit-converge`. If it appends tasks, plan checkpoints for them (same
approval rule), then go back to step 3. Repeat until converge reports nothing left or `spec.maxConvergeRounds` is reached (then
escalate with the remaining list).

## 5. Finish
`$SPIRAL phase idle --target-done`. Run `commands.build` and the full gate 1. Report: the spec dir, the branch, checkpoints and
commits, auto-answered clarifications (so the engineer can audit them), memory rules added, and anything escalated. Don't
push or open a PR unless asked.

## Stopping
Stop and wait for the engineer **only** for: a configured approval, a clarification no source answers, a gate escalation, or a
guard block you believe is wrong. Each stop asks exactly one batched question, and `/spiral-ship <slug>` resumes from where it stopped.
