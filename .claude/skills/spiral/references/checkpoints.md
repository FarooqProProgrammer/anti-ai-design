# Slicing a target into checkpoints

Goal: an ordered list the engineer can sanity-check in about a minute. Each checkpoint:

- is **1–3 lines**: what is added, and what "done" looks like.
- adds **one concern** on top of the previous checkpoint (layout → data → interaction → edge cases → polish).
- is independently **testable** (gate 1) and, if it touches UI, **screenshot-able** (gate 2).
- is marked `ui` or `logic` (logic-only checkpoints skip gate 2).
- is small: aim for a diff an engineer can review in under 10 minutes (~50–300 changed lines).

Use 3–10 checkpoints. More than 10 means the target is too big: split it into several targets.

## checkpoints.md format

```markdown
# <Target name>
- **Mode:** migration | feature | fix
- **Reference:** <paths / Figma node URLs / ticket / bug report>
- **Branch:** spiral/<target-slug>
- **Out of scope:** <explicit exclusions>

| # | Kind | Checkpoint | Status |
|---|------|------------|--------|
| 01 | ui | Skeleton: route + static layout matching reference, placeholder data | todo |
| 02 | logic | Load orders from API via existing `useOrders` hook; loading + error states | todo |
| …  |       |            |        |

## Notes
- Deferred: <things noticed that belong to a later checkpoint or another target>
```

Status values: `todo` → `building` → `gates` → `awaiting-approval` → `done` (or `escalated`).

## Per mode

### migration (legacy code is the spec)
Read the legacy implementation first (component tree, state, API calls, navigation, analytics events, error and
empty states). Then slice:
1. Skeleton: screen exists, navigable, static layout matching the reference screenshot.
2. Real data read path.
3. One checkpoint per user interaction or mutation.
4. Edge states: empty / error / loading / permissions / offline.
5. Parity details: analytics, accessibility labels, deep links.

Record any legacy behaviour you deliberately won't port under *Out of scope*, so the engineer can veto it.

### feature (SOW / ticket + design is the spec)
Turn each acceptance criterion into at least one checkpoint "done" line. If a criterion is ambiguous, list it
under **Questions** at the top of checkpoints.md. Don't guess: the engineer answers at plan approval.
Order: data model/API contract → skeleton UI → happy path → validation/errors → secondary flows → polish.

### fix (bug or refactor)
- **Bug:** cp-01 is *always* "failing test that reproduces the bug" (gate 1 passes when the new test fails for
  the right reason and nothing else fails). cp-02 is the fix (the test goes green). Add more checkpoints only for
  related hardening.
- **Refactor:** cp-01 is "characterization tests pinning current behaviour" (they pass before any change).
  Then one checkpoint per mechanical step, each keeping all tests green. Mostly `logic`. Use `ui` only where
  rendering could change, and then the reference is `before` screenshots.
