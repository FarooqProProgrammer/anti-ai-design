---
description: Set up the Spiral checkpoint-and-gate workflow in this project: detect the stack, write spiral.config.json, .spiral/architecture.md and .spiral/memory.md.
argument-hint: [optional notes — e.g. "RN app, screenshots from iOS simulator"]
---

Load the `spiral` skill, then set Spiral up in the current project. Notes from the engineer: $ARGUMENTS

1. **Detect the stack.** Read the manifests (`package.json` + lockfile, `pyproject.toml`, `composer.json`,
   `build.gradle*`, `Package.swift`/`*.xcodeproj`, `pubspec.yaml`), the CI config (`.github/workflows`, etc.), and the existing
   test, lint, and typecheck setup. Use the CI commands as the source of truth for what "green" means. Check library
   docs with Context7 if a command's flags are unclear.
2. **Draft `spiral.config.json`** from `references/config.md`, using the matching stack preset. Run each command once
   (except `dev` and `build`) to confirm it works and record its runtime. If one fails on a clean tree, tell the engineer:
   gates can't be trusted on a red baseline.
3. **Draft `.spiral/architecture.md`** from `templates/architecture.md`. Fill it from the real code: open 2–3 representative
   features and extract the conventions you actually see, citing example files. Mark anything you're unsure of with `(?)`.
   Don't invent rules. If `CLAUDE.md`, `CONTRIBUTING.md`, or ADRs exist, fold them in.
4. **Create `.spiral/memory.md`** from `templates/memory.md` (empty sections), and add `.spiral/runs/` to `.gitignore` only if
   the engineer wants run logs out of the repo.
5. **Show** the config and architecture draft, then ask with AskUserQuestion: the UI reference source (Figma / design images /
   legacy app / none), the UI reviewer (Claude vision or Gemini CLI), and the starting autonomy (recommend `checkpoint`).
   Apply the answers.
6. Don't commit. Tell the engineer to review `.spiral/architecture.md` (it's the rulebook the reviewers will enforce), commit
   it themselves, and then run `/spiral-plan <target>`.
