# Spiral + Spec Kit

[Spec Kit](https://github.com/github/spec-kit) (MIT, GitHub) decides **what** to build: constitution → specify → clarify →
plan → tasks → analyze. Spiral decides **how it ships**: every task is built inside a checkpoint that must pass the four
gates. Spiral is installed into Spec Kit as an **extension** (`speckit-extension/` in this skill), so the two connect
through Spec Kit's own hooks. Nothing is forked, and `specify` upgrades keep working.

## Flow

```
/speckit-constitution      ← before hook (optional): house rules offered as candidate principles
/speckit-specify           spec.md            (git extension: feature branch NNN-name)
/speckit-clarify           resolves [NEEDS CLARIFICATION]
/speckit-plan              plan.md, research.md, data-model.md, contracts/, quickstart.md
/speckit-checklist         optional requirement-quality checklists
/speckit-tasks             tasks.md
   └─ after hook (mandatory): speckit.spiral.checkpoints → SPEC GATE + tasks → checkpoints, engineer approves
/speckit-implement
   └─ before hook (mandatory): speckit.spiral.run → every checkpoint through gates 1–4, tasks marked [X] on approval
/speckit-converge          finds unbuilt or unspecified work, appends tasks
   └─ after hook (optional): speckit.spiral.checkpoints → new checkpoints for the new tasks → /speckit-implement again
```

Spec Kit's *converge* loop and Spiral's *gate* loop nest: the feature converges against the spec, and each checkpoint
converges against its gates.

## Mode `spec`

A fourth Spiral mode, used when the target is a Spec Kit feature directory (`specs/NNN-name/`).

| Input | Comes from |
|-------|-----------|
| Target slug | the feature directory name, e.g. `003-provider-onboarding` |
| Branch | the current Spec Kit feature branch if the git extension created one; otherwise `spiral/<slug>` |
| Reference (spec) | `spec.md` user stories and acceptance scenarios, `contracts/`, `data-model.md`, `quickstart.md` |
| Technical decisions | `plan.md` + `research.md`, which bind the implementer and reviewers like `architecture.md` does |
| UI reference | Figma links or images referenced in `spec.md`, else `ui.reference` from the config |

## Rule layers with Spec Kit

`.specify/memory/constitution.md` sits **above** everything else: constitution > `.spiral/memory.md` > `.spiral/architecture.md` >
house rules. If engineer feedback at gate 4 contradicts the constitution, don't write it to memory. Flag it and suggest
`/speckit-constitution` to amend the principle (the engineer decides).

## Spec gate

Runs inside `speckit.spiral.checkpoints`, before any checkpoint is planned. It applies the `speckit-analyze` checks
(duplication, ambiguity, underspecification, constitution alignment, coverage gaps, inconsistency):
- **CRITICAL** findings block: no checkpoints until they are fixed in the spec, plan, or tasks.
- **HIGH** findings are shown; the engineer accepts or fixes them.
- Every requirement must map to at least one task, and every task to a requirement. Unmapped tasks are questions, not work.

## Tasks → checkpoints

`tasks.md` is organised by phase (Setup, Foundational, one phase per user story in priority order, Polish), with IDs `T001…`,
`[P]` parallel markers, and `[USn]` story labels. Slice it like this:

1. **Setup + Foundational** become 1–2 `logic` checkpoints (scaffolding, shared models, migrations, auth plumbing).
2. **Each user story** becomes 1–3 checkpoints in Spiral's usual order (skeleton → data → interactions → edge states), so every
   story ends independently testable, as Spec Kit intends. Never mix two stories in one checkpoint.
3. **Polish** becomes one checkpoint (or is merged into the last story's checkpoint if small).
4. **Test tasks** in `tasks.md` ("Tests for User Story N", contract/integration tests) are assigned to **`spiral-test-writer`**
   in gate 1a of their checkpoint, never to the implementer. The checkpoint lists them under `tests:`.
5. Every unchecked task ID is covered **exactly once**. Validate this and list any orphans.

`checkpoints.md` in spec mode adds a task column:

```markdown
| # | Kind | Checkpoint | Tasks | Status |
|---|------|------------|-------|--------|
| 01 | logic | Provider model, migration, repository | T001–T006 (tests: T004) | todo |
| 02 | ui | US1 skeleton: onboarding wizard steps 1–3, static | T010, T012 | todo |
| 03 | logic | US1 data: save draft + resume (AS-1.2, AS-1.3) | T011, T013–T015 (tests: T009) | todo |
```

Cite acceptance-scenario IDs (`AS-<story>.<n>`, or the scenario's text if the spec doesn't number them) so gate 1 knows
exactly what to prove.

## Gate differences in spec mode

- **Gate 1:** `spiral-test-writer` derives tests from the cited acceptance scenarios (Given/When/Then become arrange/act/assert),
  from `contracts/` (request/response shapes, status codes), and from `quickstart.md` scenarios. Write the checkpoint's test
  tasks as specified.
- **Gate 3:** both reviewers also get `plan.md`, `data-model.md`, the relevant `contracts/`, and the constitution.
  Architecture checks for deviations from plan.md's structure and decisions; correctness checks the contracts and the
  acceptance scenarios.
- **Gate 4:** on approval, mark the checkpoint's task IDs `[X]` in `tasks.md` and include `tasks.md` in the checkpoint commit.
- **End of target:** run `/speckit-converge`. If it appends tasks, its after-hook offers to plan new checkpoints; build them
  the same way. The target is done when converge reports nothing left.

## Guardrails in spec mode

During a run the hooks also protect `.specify/**` and the feature's `spec.md`, `plan.md`, `research.md`, `data-model.md`, and
`contracts/**`. The implementer may not edit the spec to match the code. If the spec is wrong, escalate; the engineer
fixes it with `/speckit-clarify` or `/speckit-plan` while the phase is `idle`. Only `tasks.md` stays writable, so approvals can tick it.

## Installing

`/spiral-init` does this, but by hand it is:

```bash
uv tool install specify-cli --force          # or: uv tool upgrade specify-cli  (always the latest release)
specify init --here --force --non-interactive --integration claude --script ps|sh --extension git
specify extension add --dev <toolkit>/.claude/skills/spiral/speckit-extension
```

Use `--script ps` on Windows and `--script sh` on macOS/Linux. `--extension git` is optional but recommended: it gives
feature branches and auto-commits around Spec Kit steps. Spiral's own commits per checkpoint are separate.
