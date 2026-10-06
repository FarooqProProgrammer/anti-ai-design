---
description: Set up the Spiral checkpoint-and-gate workflow in this project: detect the stack, write spiral.config.json, .spiral/architecture.md and .spiral/memory.md, and check the guardrail hooks.
argument-hint: [optional notes — e.g. "RN app, screenshots from iOS simulator"]
---

Load the `spiral` skill, then set Spiral up in the current project. Notes from the engineer: $ARGUMENTS

1. **Detect the stack.** Read the manifests (`package.json` + lockfile, `pyproject.toml`, `composer.json`,
   `build.gradle*`, `Package.swift`/`*.xcodeproj`, `pubspec.yaml`), the CI config (`.github/workflows`, etc.), and the existing
   test, lint, and typecheck setup. Use the CI commands as the source of truth for what "green" means. Check library
   docs with Context7 if a command's flags are unclear.
2. **Draft `spiral.config.json`** (plain JSON, no comments) from `references/config.md`, using the matching stack preset. Include a fast
   single-file `commands.lintFile`. Run each command once (except `dev` and `build`) to confirm it works and record its runtime.
   If one fails on a clean tree, tell the engineer: gates can't be trusted on a red baseline.
3. **Draft `.spiral/architecture.md`** from `templates/architecture.md`. Fill it from the real code: open 2–3 representative
   features and extract the conventions you actually see, citing example files. Mark anything you're unsure of with `(?)`.
   Don't invent rules. If `CLAUDE.md`, `CONTRIBUTING.md`, or ADRs exist, fold them in. Read the house rules (see SKILL.md) and
   don't restate them. Only record project-specific conventions, plus any place where this project deliberately differs from a
   house rule (say so explicitly, since project rules win).
4. **Create `.spiral/memory.md`** from `templates/memory.md` (empty sections). Add `.spiral/state.json` to `.gitignore`, and also
   `.spiral/runs/` if the engineer wants run logs kept out of the repo.
5. **Check the guardrails.** Look for the Spiral hooks in `.claude/settings.json` (project) and `~/.claude/settings.json` (user).
   If they're missing, show the two install options from `references/config.md → Installing the hooks` and ask which one to use.
   Install the chosen one (copy the scripts, merge the `hooks` block without dropping existing hooks). Then smoke-test:
   `node <hooks>/spiral.mjs status` must print state.
6. **Show** the config and architecture draft, then ask with AskUserQuestion: the UI reference source (Figma / design images /
   legacy app / none), the UI reviewer (Claude vision or Gemini CLI), the starting autonomy (recommend `checkpoint`), and
   **Spec Kit** (recommend yes for projects with substantial new features; see `references/speckit.md`). Apply the answers.
7. **Spec Kit (if chosen).** Follow `references/speckit.md → Installing`: upgrade `specify-cli` to the latest release with `uv`,
   then `specify init --here --force --non-interactive --integration claude --script <ps on Windows | sh> --extension git` (skip init
   if `.specify/` already exists), then `specify extension add --dev <spiral skill dir>/speckit-extension`. Verify the
   `speckit-spiral-*` skills exist under `.claude/skills/` and that `.specify/extensions.yml` has the Spiral hooks. Then run
   `/speckit-constitution`. Its before-hook offers house-rule principles. Keep the constitution to principles and leave the
   concrete conventions in `.spiral/architecture.md`.
8. Don't commit. Tell the engineer to review `.spiral/architecture.md` (it's the rulebook the reviewers will enforce), commit
   it themselves, and then run `/spiral-plan <target>`.
