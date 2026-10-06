# Running a checkpoint through the gates

The orchestrator is the main Claude Code session. It implements the code itself and delegates tests and reviews
to subagents, so no agent grades its own work. Paths below are relative to the target project root;
`$CP` = `.spiral/runs/<slug>/cp-NN`. `$SPIRAL` = the run-state CLI (see SKILL.md → Guardrails); every phase change
below goes through it so the hooks know what is allowed.

"The rules" means all layers: constitution (if Spec Kit) > `.spiral/memory.md` > `.spiral/architecture.md` > house rules.
Pass all of them to every subagent. In `spec` mode, also apply the differences in `references/speckit.md → Gate differences`
(test sources, extra reviewer inputs, ticking `tasks.md` at approval, `/speckit-converge` at the end).

## 0. Prepare

1. Read `spiral.config.json`, the rules, `.spiral/runs/<slug>/checkpoints.md`, and the reports of the previous checkpoint (its
   gate-4 feedback matters most). If the hooks aren't registered (no Spiral entries in `.claude/settings.json` or
   `~/.claude/settings.json`), warn the engineer once: the guardrails are then only instructions.
2. Make sure the working tree is clean and you're on `spiral/<slug>` (create it from the current branch if missing).
   If the tree is dirty with changes that aren't Spiral's, stop and ask.
3. Set the checkpoint's status to `building` in checkpoints.md.

## 1. Behavior gate

**1a. Tests first.** Run `$SPIRAL phase tests --target <slug> --cp NN`, then launch `spiral-test-writer` with: the checkpoint
text, mode, reference pointers, `tests` config, the rules, and the list of files the previous checkpoints created. It writes or
extends tests and `$CP/tests.md`. Then run `$SPIRAL lock-tests` (pass the files explicitly if `tests.dir` is `colocated`).
Run the new tests once and expect them to **fail**, because the behaviour doesn't exist yet. Tests that already pass
are fine only for characterization (refactor cp-01) or for behaviour that genuinely already exists. Note which in `tests.md`.
For bug mode cp-01, the gate *is* this: the repro test fails for the stated reason and everything else passes.

**1b. Implement** the checkpoint: `$SPIRAL phase implement`, then follow the rules. Tests are now locked by the hooks.
If you think one is wrong, write why in `gate-1.md`, run `$SPIRAL phase tests --reason "<why>"`, re-launch the test writer
with that note, run `$SPIRAL lock-tests`, and return to `phase implement`.

**1c. Run** `$SPIRAL verify-tests` first (a failure here fails the gate outright and must be reported to the engineer), then
`typecheck`, `lint`, then `test` (full suite, so you catch regressions). Append an attempt record to `$CP/gate-1.md`:

```markdown
## Attempt 2 — FAIL
- typecheck: pass · lint: 1 error · tests: 41 pass / 1 fail
- failing: tests/spiral/orders.test.tsx › shows empty state when no orders
- diagnosis: empty-state branch checks `orders === null`, API returns []
- next: treat empty array as empty state
```

Loop 1b→1c until green or `maxAttempts`.

## 2. UI review gate (skip for `logic` checkpoints or when `ui.enabled` is false; record "skipped" in gate-2.md)

1. **Reference shots** into `$CP/shots/reference-<viewport>.png`:
   - `figma` → Figma MCP `get_screenshot` for the node(s) in checkpoints.md
   - `images` → copy from `ui.referenceDir`
   - `legacy-app` → capture `ui.legacyUrl` (web) or run `captureCommand` on the legacy build
   - `before` → capture from the commit before the target branch (use `git worktree`, not a checkout of the main tree)
   Reuse earlier checkpoints' reference shots when the screen state is the same.
2. **Candidate shots**: start `commands.dev` in the background if it isn't already running, then capture each viewport to
   `$CP/shots/candidate-<viewport>.png`. Use the same data and the same screen state as the reference.
3. Launch `spiral-ui-reviewer` with the shot pairs, the checkpoint text (so it knows what is *expected* to be unfinished),
   and the relevant memory rules. If `ui.reviewer` is `gemini`, the subagent shells out to the Gemini CLI instead of
   reviewing the images itself.
4. Append its findings table to `$CP/gate-2.md`. Any finding at a severity in `gates.uiBlockingSeverities` that is fixable
   in code blocks the gate. Fix it, re-run gate 1 (fast), re-capture, and re-review. `minor` findings go in the
   gate-4 summary.

## 3. Adversarial review gate

1. `$SPIRAL phase review`. Collect the checkpoint diff: `git diff` plus untracked files.
2. Launch **both** reviewers **in one message** (parallel, independent):
   - `spiral-reviewer-architecture`: conventions, structure, reuse, naming, layering, and the rules.
   - `spiral-reviewer-correctness`: logic, edge cases, error handling, security, performance, test adequacy.
   Give each: the diff, the checkpoint text, mode/reference pointers, and the rules. Don't give either one the other's
   output. Every `spiral-allow:` line in the diff must be judged by a reviewer: accepted or a finding.
3. Each returns `APPROVE` or `CHANGES_REQUESTED` with numbered findings. Append both to `$CP/gate-3.md`.
4. Address **every** finding: fix it, or rebut it in one line (`R2#3 rejected: …`). Rebuttals are shown to the engineer.
5. If any code changed (fixes happen after `$SPIRAL phase implement`): re-run gate 1, gate 2 if UI was touched, then gate 3 again (fresh reviewer launches, with
   the previous findings and your responses attached so they can verify). Loop until both say `APPROVE` with no new findings.

## 4. Engineer approval gate

Run `$SPIRAL phase approval` and present a compact summary in the chat. Never paste whole diffs:

```
cp-03 · logic · "Mark order as fulfilled; optimistic update with rollback"
Gates: behavior ✔ (2 attempts) · UI skipped · review ✔ (A: 1 round, C: 2 rounds)
Changed: src/orders/useFulfill.ts (+48), src/orders/OrderRow.tsx (+12/-3), tests/spiral/fulfill.test.tsx (+66)
Rebutted findings: C#2 "debounce clicks": the button is disabled while pending
Suppressions: src/api/client.ts:14 @ts-expect-error spiral-allow: upstream type missing `signal` (accepted by A)
Test re-opens: none   (from $CP/phase.log: any "phase tests" re-entry or RELOCK, with its reason)
Minor UI notes: none
Try it: pnpm dev → /orders → click "Fulfill" on any open order
```

After approval (or when the run stops), the next checkpoint starts with `phase tests` again. After the last one, run `$SPIRAL phase idle --target-done`.

Then use AskUserQuestion: **Approve** / **Approve with notes** / **Request changes**.

- **Request changes**: apply the requested changes, then run gates 1–3 again before asking again.
- **Any feedback** (from either Approve-with-notes or Request-changes): distil it into rules in `.spiral/memory.md` (format
  in `templates/memory.md`). Generalise ("prefer X over Y in this codebase") but keep it concrete. Merge with existing rules
  rather than duplicating them. Record the raw feedback in `$CP/gate-4.md`.
- **Approve**: mark the checkpoint `done`, commit with message `spiral(<slug>): cp-NN <checkpoint title>` (include
  `.spiral/memory.md` and, if `commitRunLogs`, `$CP/`), then continue to the next checkpoint if the run was for `all`.

In `batch` autonomy, commit after gate 3, mark `awaiting-approval`, and run gate 4 once at the end over the whole
branch (`git log` + `git diff <base>...HEAD --stat`). Feedback still goes to memory, and fixes become extra checkpoints.

## Escalation

When a gate hits `maxAttempts`, or something is truly blocked (missing API, ambiguous requirement, a flaky test you
didn't write), or a guard blocks something you believe is legitimately needed: set the status to `escalated`, write the
blocker at the top of the latest gate report, run `$SPIRAL phase idle` (so the engineer can work freely), and stop with
a short message saying what you tried and what decision you need. Do not skip the gate, mark tests skipped, loosen lint
rules, or look for another way around a guard. `/spiral-run` resumes from the reports.

## End of target

After the last checkpoint: run `commands.build` if set, then run the full gate 1 once more and update checkpoints.md. Tell the
engineer the branch is ready for their normal PR process. Don't open the PR yourself unless asked.
