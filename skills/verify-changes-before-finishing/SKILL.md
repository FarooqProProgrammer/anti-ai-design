---
name: verify-changes-before-finishing
description: "Verify all changes, run risk-tiered automated quality gates, scrutinize high-risk domains (migrations, auth, permissions, payments), enforce zero concealment, and generate an evidence-based completion report before finishing a task or declaring 'Done'. Triggers: Phase 5 Verify, finishing a task, verfy-changes-before-finesg, verify changes before finishing, pre-review checklist, pre-commit quality check."
---

# Verify Changes Before Finishing Skill

You MUST activate this skill at the end of **Phase 4: Implement** and throughout **Phase 5: Verify** before declaring any task "Done", submitting code for independent review, or committing changes to git.

This skill operationalizes **Gate 5 (Automated Quality Gates & Evidence-Based Completion)** of the Request Firewall ([FIREWALL.md](../../FIREWALL.md)). It establishes a clear, undeniable difference between claiming "Done" and *genuinely verified work*.

---

## 1. Automated Verification Script

Before any manual review, execute the automated verification utility from the project root:

```bash
python skills/verify-changes-before-finishing/scripts/verify_changes.py
```

### What the Script Checks:
1. **Working Tree & Changed Files**: Captures exact files modified, added, or deleted via `git status -s`.
2. **High-Risk Domain Detection**: Scans diffs and paths for database migrations, authentication, RBAC/permissions, and payments/billing.
3. **Debug Statements & Suppressions**: Detects stray `console.log`, `debugger`, `pdb`, `@ts-ignore`, and `eslint-disable` in added code.
4. **Wiki Evidence Check**: Runs `python skills/karpathy-llm-wiki/scripts/check_evidence.py .` if wiki or raw files are touched.
5. **Report Template**: Automatically formats the 5-point Evidence-Based Completion Report pre-populated with changed files.

---

## 2. Risk-Tiered Automated Quality Gates

Scale your verification checks to the risk profile of the task:

| Risk Tier | Scope of Changes | Required Automated Gates |
|---|---|---|
| **Tier 1: Low Risk** | Docs, markdown, comments, formatting | `git diff` sanity check, wiki evidence audit (`check_evidence.py`). |
| **Tier 2: Medium Risk** | UI components, utility functions, standard endpoints | Typecheck (`tsc --noEmit`, `mypy`), linter (`eslint`, `ruff`), unit test suites (`npm test`, `pytest`). |
| **Tier 3: High Risk** | Core business logic, external API integrations, shared utilities | Full test suites, integration tests, dependency security audit (`npm audit`, `pip-audit`), local build (`npm run build`). |
| **Tier 4: Critical Risk** | Database migrations, auth, permissions/RBAC, payments | High-risk domain scrutiny (below) + rollback verification + negative security test cases. |

---

## 3. High-Risk Domain Scrutiny

If your change touches any of the following high-risk domains, enforce stricter scrutiny before finishing:

### 1. Database Migrations
- [ ] Schema idempotency: Run migrations forward, verify, rollback, and re-apply.
- [ ] Rollback safety: Test rollback script to ensure it restores the prior state cleanly.
- [ ] Zero data loss: Confirm no unintended column truncation, table drops, or destructive operations on existing data.
- [ ] Index & performance: Verify new indexes support queries without locking production tables.

### 2. Authentication & Sessions
- [ ] Token lifecycle: Test token generation, refresh, expiration, and revocation.
- [ ] Session invalidation: Verify logout terminates sessions across all active devices/tabs.
- [ ] Credential handling: Confirm passwords and secrets are hashed (e.g. bcrypt/argon2), never logged in plain text.
- [ ] Cookie security: Ensure cookies have `HttpOnly`, `Secure`, and `SameSite` flags configured properly.

### 3. Authorization & Permissions (RBAC)
- [ ] Cross-tenant isolation: Verify tenants cannot read, modify, or infer another tenant's data.
- [ ] Negative role tests: Explicitly test that unauthorized roles (e.g. viewer, anonymous) are blocked from protected actions.
- [ ] Privilege escalation guards: Confirm users cannot grant themselves higher roles or bypass role checks via parameter tampering.

### 4. Payment & Billing
- [ ] Decimal precision: Use integer cents or arbitrary-precision decimals (e.g. `Decimal`), never floating-point arithmetic.
- [ ] Idempotency key enforcement: Test repeated checkout requests with the same key to verify charges are not duplicated.
- [ ] Webhook signature verification: Verify webhook endpoints reject forged or unsigned requests.
- [ ] Race conditions: Test concurrent checkouts or balance updates to prevent double-spending.

---

## 4. Zero-Concealment Protocol

> [!CAUTION]
> **Never hide, skip, or suppress failing tests.**
> - DO NOT comment out failing assertions or test cases.
> - DO NOT add suppressions like `@ts-ignore`, `eslint-disable`, or `# type: ignore` to mask defects.
> - Capture the actual error message and stack trace.
> - Fix the root cause in the implementation code, not in the test expectation (unless the spec genuinely changed).

---

## 5. Evidence-Based Completion Report

At the conclusion of every task, before declaring work complete or handing off to Phase 6 review, the agent MUST produce this report:

```markdown
### Evidence-Based Completion Report
1. **What changed?**:
   [Concise summary of functional modifications, architecture adjustments, or bug fixes]

2. **Which files changed?**:
   [Explicit list of modified, added, or deleted files matching git status]

3. **Which tests actually passed?**:
   [Exact commands executed, test count, assertions verified, and proof of green run]

4. **What was NOT tested?**:
   [Explicit declaration of unmocked external systems, third-party APIs, manual UI flows, or edge cases]

5. **Remaining risks or manual steps?**:
   [Pending database migrations, required environment variables, manual lead engineer sign-offs, or rollout considerations]
```

---

## Quick Reference Command
```bash
# Run verification script
python skills/verify-changes-before-finishing/scripts/verify_changes.py

# Run wiki evidence check
python skills/karpathy-llm-wiki/scripts/check_evidence.py .
```

