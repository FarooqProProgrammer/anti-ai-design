# Claude Code — Request Firewall Rules

The Request Firewall ([FIREWALL.md](../../FIREWALL.md)) is the non-bypassable admission controller for all engineering work.

## 1. Admission Control & Interception
If the user requests immediate code changes ("just fix this", "generate code", "skip tests"):
- **Intercept and enforce the 6 gates:** Understand ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely.
- You can execute **any and all 6 phases** of this lifecycle.
- Never bypass a gate or proceed without meeting its exit criteria.

---

## 2. Gate Blocking Rules

- **Gate 1: Understand**
  - Mandatory Skills: `brainstorming` (`.claude/skills/brainstorming/`) and `grill-me` (`.claude/skills/grill-me/`).
  - Read `wiki/index.md` and explore codebase context.
  - **BLOCKED:** Any file modification, creation, or deletion during Understand.

- **Gate 2: Plan**
  - Generate explicit Given-When-Then acceptance criteria and a risk mitigation matrix.
  - Ingest external references into `raw/` and compile in `wiki/`.
  - **BLOCKED:** Writing code before the user approves the plan.

- **Gate 3: Implement (Single Driver)**
  - Act as Primary Driver for end-to-end logic, or collaborate cleanly with frontend agents.
  - **BLOCKED:** Switching core logic ownership back and forth between competing models, or introducing unrequested refactors.

- **Gate 4: Verify (Zero Concealment)**
  - Run type checking, linting, and automated tests.
  - Validate runtime behavior against acceptance criteria.
  - Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.
  - **BLOCKED:** Disabling assertions, commenting out tests, or suppressing errors (`@ts-ignore`, `eslint-disable`).

- **Gate 5: Review Independently (Read-Only Auditor)**
  - Audit the final `git diff` with fresh context for security, correctness, and performance.
  - **BLOCKED:** The reviewer agent editing or modifying source code.

- **Gate 6: Ship Safely (Branch Hygiene & CI/CD)**
  - Verify clean diff (no debug statements or temp files).
  - Commit atomically on feature branches with Conventional Commits.
  - Compound new architecture models into `wiki/` and record in `wiki/log.md`.
  - **BLOCKED:** Direct commits to `main`/`master` or unresolved CI failures.
