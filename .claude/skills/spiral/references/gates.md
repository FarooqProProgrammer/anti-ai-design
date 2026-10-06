# Running a checkpoint through the gates

The orchestrator is the main Claude Code session. It implements the code itself and delegates tests and reviews
to subagents, so no agent grades its own work. Paths below are relative to the target project root;
`$CP` = `.spiral/runs/<slug>/cp-NN`.

## 0. Prepare

1. Read `spiral.config.json`, `.spiral/architecture.md`, `.spiral/memory.md`, `.spiral/runs/<slug>/plan.md`, and the
   reports of the previous checkpoint (its gate-4 feedback matters most).
2. Make sure the working tree is clean and you're on `spiral/<slug>` (create it from the current branch if missing).
   If the tree is dirty with changes that aren't Spiral's, stop and ask.
3. Set the checkpoint's status to `building` in plan.md.

## 1. Behavior gate

**1a. Tests first.** Launch `spiral-test-writer` with: the checkpoint text, mode, reference pointers, `tests` config,
`memory.md`, and the list of files the previous checkpoints created. It writes or extends tests and `$CP/tests.md`.
Then run the new tests once and expect them to **fail**, because the behaviour doesn't exist yet. Tests that already pass
are fine only for characterization (refactor cp-01) or for behaviour that genuinely already exists. Note which in `tests.md`.
For bug mode cp-01, the gate *is* this: the repro test fails for the stated reason and everything else passes.

**1b. Implement** the checkpoint. Follow `architecture.md` and every rule in `memory.md`. Don't edit Spiral tests;
if you think one is wrong, write why in `gate-1.md` and re-launch the test writer with that note.

**1c. Run** `typecheck`, `lint`, then `test` (full suite, so you catch regressions). Append an attempt record to `$CP/gate-1.md`:

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
   - `figma` → Figma MCP `get_screenshot` for the node(s) in plan.md
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

1. Collect the checkpoint diff: `git diff` plus untracked files.
2. Launch **both** reviewers **in one message** (parallel, independent):
   - `spiral-reviewer-architecture`: conventions, structure, reuse, naming, layering, `architecture.md`, `memory.md`.
   - `spiral-reviewer-correctness`: logic, edge cases, error handling, security, performance, test adequacy.
   Give each: the diff, the checkpoint text, mode/reference pointers, `architecture.md`, `memory.md`. Don't give either
   one the other's output.
3. Each returns `APPROVE` or `CHANGES_REQUESTED` with numbered findings. Append both to `$CP/gate-3.md`.
4. Address **every** finding: fix it, or rebut it in one line (`R2#3 rejected: …`). Rebuttals are shown to the engineer.
5. If any code changed: re-run gate 1, gate 2 if UI was touched, then gate 3 again (fresh reviewer launches, with
   the previous findings and your responses attached so they can verify). Loop until both say `APPROVE` with no new findings.

## 4. Engineer approval gate

Present a compact summary in the chat. Never paste whole diffs:

```
cp-03 · logic · "Mark order as fulfilled; optimistic update with rollback"
Gates: behavior ✔ (2 attempts) · UI skipped · review ✔ (A: 1 round, C: 2 rounds)
Changed: src/orders/useFulfill.ts (+48), src/orders/OrderRow.tsx (+12/-3), tests/spiral/fulfill.test.tsx (+66)
Rebutted findings: C#2 "debounce clicks": the button is disabled while pending
Minor UI notes: none
Try it: pnpm dev → /orders → click "Fulfill" on any open order
```

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
didn't write): set the status to `escalated`, write the blocker at the top of the latest gate report, and stop with a
short message saying what you tried and what decision you need. Do not skip the gate, mark tests skipped, or loosen
lint rules.

## End of target

After the last checkpoint: run `commands.build` if set, then run the full gate 1 once more and update plan.md. Tell the
engineer the branch is ready for their normal PR process. Don't open the PR yourself unless asked.
