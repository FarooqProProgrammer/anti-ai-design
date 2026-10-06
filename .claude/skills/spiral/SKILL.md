---
name: spiral
description: Checkpoint-and-gate delivery workflow for the software house, inspired by the Shopify engineering Helix case study (shopify.engineering/helix). Use when building a client feature, migrating/rewriting an app or screen, or doing a refactor/bug fix with AI agents and you want reliable convergence instead of one big unreviewable diff. Splits a target into small ordered checkpoints; each must pass four gates (behavior tests, UI review, two adversarial code reviews, engineer approval) before it is committed; engineer feedback becomes project memory. Triggered by /spiral-init, /spiral-plan, /spiral-run, /spiral-status, or requests like "build this screen spiral-style", "migrate X with checkpoints", "run the gates".
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

## Reference-as-spec (one workflow, three modes)

Spiral does not write giant specs. It points the agents at a **reference** and keeps context small.

| Mode | Reference (the spec) | Tests come from | UI gate compares against |
|------|----------------------|-----------------|--------------------------|
| `migration` | the legacy code/screen being replaced | observed behaviour of the old code | screenshots of the old app |
| `feature` | SOW / ticket acceptance criteria + Figma frames or design PNGs | the acceptance criteria | Figma/design images |
| `fix` (refactor or bug) | the bug report / current behaviour | a failing repro test (bug) or characterization tests (refactor) | before-screenshots (regression only), or skipped |

## Files in the target project

```
spiral.config.json            # commands, screenshot method, gate settings  → references/config.md
.spiral/
  architecture.md            # the rules reviewers enforce (from templates/architecture.md)
  memory.md                  # distilled engineer feedback, newest last (from templates/memory.md)
  runs/<target-slug>/
    plan.md                  # target, mode, reference, ordered checkpoints + status
    cp-01/                   # one folder per checkpoint
      tests.md               # what the test writer added and why
      gate-1.md … gate-4.md  # each gate attempt's report (append, never overwrite)
      shots/                 # reference-*.png, candidate-*.png
```

`.spiral/runs/` is working state: commit it with the checkpoint so the history explains itself, or gitignore it if
the client repo must stay clean (`spiral.config.json → commitRunLogs`).

## Hard rules

- **Tests before code.** Gate-1 tests for a checkpoint are written by `spiral-test-writer` from the reference,
  *before* the implementer touches the code, and the implementer may not weaken or delete them to get green. If a
  test is genuinely wrong, say so in `gate-1.md` and let the test writer (not the implementer) fix it.
- **Reviewers are independent.** Launch both gate-3 reviewers in one message, give each only the diff, the
  checkpoint text, `architecture.md` and `memory.md` — never the other reviewer's output or the implementer's reasoning.
- **Every finding is addressed.** Fixed, or rejected with a one-line reason the engineer will see at gate 4. A fix
  after gate 3 re-runs gate 1 (and gate 2 if UI changed) and then gate 3 again.
- **Loop budget.** `gates.maxAttempts` (default 5) per gate per checkpoint. On exhaustion, stop and escalate to the
  engineer with the reports. Never lower the bar to get green.
- **Scope.** One checkpoint = one concern. Don't pull work forward from later checkpoints; note it in `plan.md`.
- **Commits.** Work on branch `spiral/<target-slug>`. Commit once per checkpoint, only after gate 4 (or after gate 3 in
  `batch` autonomy — see below). Never push, merge, or open a PR unless the engineer asks.

## Autonomy

`spiral.config.json → autonomy`:
- `checkpoint` (default for a new project): gate 4 after every checkpoint.
- `batch`: gates 1–3 run per checkpoint and each green checkpoint is committed; the engineer does gate 4 once over
  the whole target. Earn this after memory has stabilised (roughly: the last 3 gate-4s needed no code changes).
  `/spiral-status` suggests when to switch.

## How to run

1. `/spiral-init` once per project: detect the stack, write `spiral.config.json`, `.spiral/architecture.md`, `.spiral/memory.md`.
2. `/spiral-plan <target>`: pick the mode and reference, propose checkpoints, engineer edits/approves `plan.md`.
3. `/spiral-run [target] [cp-N|all]`: build checkpoints through the gates. Procedure in `references/gates.md`.
4. `/spiral-status [target]`: progress, gate pass rates, escalations, autonomy suggestion.

References: `references/checkpoints.md` (how to slice per mode), `references/gates.md` (exact gate procedure),
`references/config.md` (config schema + stack presets).
