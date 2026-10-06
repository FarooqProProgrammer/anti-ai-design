---
name: spiral
description: Checkpoint-and-gate delivery workflow for the software house, inspired by the Shopify engineering Helix case study (shopify.engineering/helix). Use when building a client feature, migrating/rewriting an app or screen, or doing a refactor/bug fix with AI agents and you want reliable convergence instead of one big unreviewable diff. Splits a target into small ordered checkpoints; each must pass four gates (behavior tests, UI review, two adversarial code reviews, engineer approval) before it is committed; engineer feedback becomes project memory. Integrates GitHub Spec Kit as an extension (spec → plan → tasks feed checkpoints; /speckit-implement runs through the gates). Triggered by /spiral-init, /spiral-plan, /spiral-run, /spiral-status, /spiral-promote, /speckit-spiral-*, or requests like "build this screen spiral-style", "migrate X with checkpoints", "run the gates".
---

# Spiral — checkpoints, gates, memory

> "An attempt is allowed to be wrong. It is not allowed to ship until it isn't."

The agent is never expected to be right first time. It is expected to **converge**: small slices, hard gates,
loop until every gate is green, then a human signs off and the feedback is remembered.

## The three ideas

1. **Checkpoints.** A target (screen, feature, module, bug) is split into 3–10 small, ordered slices of rising
   complexity. The first slice is a skeleton; each later one adds one deliberate piece of behaviour. Each
   checkpoint is described in 1–3 lines so an engineer can review the *sequence* in a minute.
2. **Four gates.** A checkpoint is committed only when all of its gates pass:
   | # | Gate | Who | Passes when |
   |---|------|-----|-------------|
   | 1 | **Behavior** | `spiral-test-writer` writes tests from the reference *before* implementation; project commands run them | typecheck + lint + tests (new and existing) all green |
   | 2 | **UI review** | `spiral-ui-reviewer` compares reference vs. candidate screenshots | zero `blocker`/`major` findings (skipped for logic-only checkpoints) |
   | 3 | **Adversarial review** | `spiral-reviewer-architecture` + `spiral-reviewer-correctness`, run independently and in parallel | both return `APPROVE`; any fix re-runs gates 1–2 first |
   | 4 | **Engineer approval** | the human | explicit approval; their feedback is distilled into `.spiral/memory.md` |
3. **Memory.** Approved patterns and every piece of engineer feedback accumulate in `.spiral/memory.md` and are
   read at the start of every checkpoint, so later checkpoints need less supervision.

## Reference-as-spec (one workflow, four modes)

Spiral points the agents at a **reference** and keeps context small. For quick work the reference is whatever already exists.
For new client features worth specifying properly, the reference is a Spec Kit spec (`spec` mode, `references/speckit.md`).

| Mode | Reference (the spec) | Tests come from | UI gate compares against |
|------|----------------------|-----------------|--------------------------|
| `migration` | the legacy code/screen being replaced | observed behaviour of the old code | screenshots of the old app |
| `feature` | SOW / ticket acceptance criteria + Figma frames or design PNGs | the acceptance criteria | Figma/design images |
| `fix` (refactor or bug) | the bug report / current behaviour | a failing repro test (bug) or characterization tests (refactor) | before-screenshots (regression only), or skipped |
| `spec` (Spec Kit feature) | `specs/NNN-name/`: spec.md, plan.md, contracts/, data-model.md, tasks.md | acceptance scenarios + contracts + the feature's test tasks | Figma/images linked from the spec |

**Which mode for which job:** a substantial new client feature uses `spec` (the spec doubles as the client-facing requirement
record). A small feature from a clear ticket uses `feature`. Ports use `migration`. Bugs and refactors use `fix`.

## Files in the target project

```
spiral.config.json           # commands, screenshot method, gate settings  → references/config.md
.spiral/
  architecture.md            # the rules reviewers enforce (from templates/architecture.md)
  memory.md                  # distilled engineer feedback, newest last (from templates/memory.md)
  state.json                 # current phase + locked-test hashes; local only (gitignored), written by spiral.mjs
  runs/<target-slug>/        # spec mode: slug = the Spec Kit feature dir name, e.g. 003-user-auth
    checkpoints.md           # target, mode, reference, ordered checkpoints (+ task IDs in spec mode) + status
    cp-01/                   # one folder per checkpoint
      tests.md               # what the test writer added and why
      gate-1.md … gate-4.md  # each gate attempt's report (append, never overwrite)
      phase.log              # phase changes + test locks, written by spiral.mjs (audit trail)
      shots/                 # reference-*.png, candidate-*.png
```

## Layers of rules

Every checkpoint, and every test-writer and reviewer launch, reads all of them. When they conflict, the higher one wins:

0. `.specify/memory/constitution.md` (only if Spec Kit is installed): non-negotiable principles. Feedback that contradicts
   it is flagged for a `/speckit-constitution` amendment, never silently stored in memory.
1. `.spiral/memory.md`: this project's lessons from engineer feedback.
2. `.spiral/architecture.md`: this project's conventions.
3. **House rules**: company-wide taste and lessons shared by every client project. They live in `house/house-rules.md` in this
   skill's directory (override the path with `spiral.config.json → houseRules`). They grow through `/spiral-promote`, which
   generalises repeated project lessons, strips client details, and needs a lead's approval.

## Guardrails (hooks)

The rules that matter most are enforced by Claude Code hooks, not just by instructions. The hooks are in
`.claude/hooks/spiral/` and registered in `.claude/settings.json`. They do nothing unless the project has `spiral.config.json`
**and** a run is active (phase ≠ `idle`), so normal work is never affected. While a run is active they:

- **lock tests:** block edits to locked tests and to the tests dir outside the `tests` phase. Gate 1 also runs
  `verify-tests`, which compares hashes, so a shell edit that slips past the hook still fails the gate.
- **protect tooling:** block edits to lint, type, test, and CI config and to `spiral.config.json` (list in `lib.mjs`, extend it via `guard.protected`).
- **block suppressions:** block newly added `eslint-disable`, `@ts-ignore`, `noqa`, `.skip`/`.only`, and similar, unless
  the line says `spiral-allow: <reason>`. Reviewers judge those reasons.
- **block risky git:** block `git push`, `--no-verify`, `reset --hard`, `clean -f`, `rebase`, `--amend`, `merge`, and `gh pr create/merge`.
- **lint on save:** run `commands.lintFile` after each edit and feed failures straight back to Claude.

The orchestrator moves between phases with the CLI (`$SPIRAL` below means `node .claude/hooks/spiral/spiral.mjs`, or
`node ~/.claude/hooks/spiral/spiral.mjs` when Spiral is installed user-wide):

```
$SPIRAL phase tests --target <slug> --cp NN    # before launching spiral-test-writer
$SPIRAL lock-tests                             # right after it returns
$SPIRAL phase implement                        # implementer works; tests now locked
$SPIRAL verify-tests                           # first step of every gate-1 run
$SPIRAL phase review | approval                # gates 3 and 4
$SPIRAL phase idle --target-done               # target finished or run stopped
$SPIRAL phase tests --reason "<why>"           # re-opening tests in the same checkpoint (logged, shown at gate 4)
```

A blocked action is a signal to fix the real problem or escalate. Never work around a guard.

`.spiral/runs/` is working state: commit it with the checkpoint so the history explains itself, or gitignore it if
the client repo must stay clean (`spiral.config.json → commitRunLogs`).

## Hard rules

- **Tests before code.** Gate-1 tests for a checkpoint are written by `spiral-test-writer` from the reference,
  *before* the implementer touches the code, and the implementer may not weaken or delete them to get green. If a
  test is genuinely wrong, say so in `gate-1.md` and let the test writer (not the implementer) fix it.
- **Reviewers are independent.** Launch both gate-3 reviewers in one message, give each only the diff, the
  checkpoint text, `architecture.md`, `memory.md` and the house rules. Never give either one the other reviewer's output or the implementer's reasoning.
- **Every finding is addressed.** Fixed, or rejected with a one-line reason the engineer will see at gate 4. A fix
  after gate 3 re-runs gate 1 (and gate 2 if UI changed) and then gate 3 again.
- **Loop budget.** `gates.maxAttempts` (default 5) per gate per checkpoint. On exhaustion, stop and escalate to the
  engineer with the reports. Never lower the bar to get green.
- **Scope.** One checkpoint = one concern. Don't pull work forward from later checkpoints; note it in `checkpoints.md`.
- **Commits.** Work on branch `spiral/<target-slug>` (in `spec` mode, the Spec Kit feature branch if one exists). Commit once per checkpoint, only after gate 4 (or after gate 3 in
  `batch` autonomy — see below). Never push, merge, or open a PR unless the engineer asks.

## Autonomy

`spiral.config.json → autonomy`:
- `checkpoint` (default for a new project): gate 4 after every checkpoint.
- `batch`: gates 1–3 run per checkpoint and each green checkpoint is committed; the engineer does gate 4 once over
  the whole target. Earn this after memory has stabilised (roughly: the last 3 gate-4s needed no code changes).
  `/spiral-status` suggests when to switch.

## How to run

1. `/spiral-init` once per project: detect the stack, write `spiral.config.json`, `.spiral/architecture.md`, `.spiral/memory.md`.
2. `/spiral-plan <target>`: pick the mode and reference, propose checkpoints, engineer edits/approves `checkpoints.md`.
3. `/spiral-run [target] [cp-N|all]`: build checkpoints through the gates. Procedure in `references/gates.md`.
4. `/spiral-status [target]`: progress, gate pass rates, escalations, autonomy suggestion.
5. `/spiral-promote [other projects…]`: lift repeated project lessons into the house rules (lead approves).

6. **`/spiral-ship <target>`: the one-command path.** It readies the project, routes the target, **drives Spec Kit itself**
   (constitution → specify → clarify → plan → checklist → tasks → spec gate), plans checkpoints, runs the gates, and loops
   `speckit-converge` until nothing is left. It stops only at the decision points in `spiral.config.json → spec`.
   Spiral never asks the engineer to run a `/speckit-*` command; it invokes those skills itself.

References: `references/checkpoints.md` (how to slice per mode), `references/gates.md` (exact gate procedure),
`references/config.md` (config schema + stack presets + hook install), `references/speckit.md` (Spec Kit integration,
spec mode, tasks → checkpoints). The Spec Kit extension itself lives in `speckit-extension/`.
