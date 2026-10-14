# Phase 6: Ship Safely (Checklist & Deployment Guide)

**Firewall Gate:** Gate 6 (Production Release & Knowledge Compounding Gate)  
**Target:** Driver Agent & Engineer  
**Goal:** Final sanity check, clean atomic commits, branch management, CI/CD pipeline verification, and deployment.  
**Strict Firewall Rule:** Committing to protected branches is BLOCKED. Unverified diffs are BLOCKED.

---

## Pre-Flight Checklist

```markdown
Before pushing or merging, verify every step below:

1. [ ] **Final Diff Review**:
   - Run `git status` and `git diff`.
   - Confirm NO unwanted files: `.env`, `.DS_Store`, build artifacts, temporary scratch files.
   - Confirm NO temporary debug statements: `console.log`, `debugger`, `print()`, `fmt.Println()`.
   - Confirm only files relevant to the planned feature/fix are touched.

2. [ ] **Branch Sanity**:
   - Confirm you are NOT committing directly to `main` / `master` / protected branches.
   - Feature branch format: `feat/short-description` or `fix/issue-description`.

3. [ ] **Atomic Conventional Commit(s)**:
   - Use standard conventional commit format:
     - `feat(<scope>): add support for ...`
     - `fix(<scope>): resolve crash when ...`
     - `test(<scope>): add unit tests for ...`
   - Include a concise body explaining *why* the change was made if non-trivial.

4. [ ] **Pull Request Preparation**:
   - PR Title: Follows conventional format.
   - PR Description contains:
     - Context & problem statement
     - Summary of changes
     - Acceptance criteria checklist (marked complete)
     - Test execution evidence (commands & green output)

5. [ ] **CI/CD Pipeline & Deployment Process**:
   - Push branch: `git push origin <branch-name>`
   - Monitor remote CI workflows (GitHub Actions, GitLab CI, etc.).
   - Ensure all build, test, and security scan stages turn green.
   - Follow established staging/production deployment protocols (e.g. merge approval, release tags).

6. [ ] **Knowledge Compounding (Wiki Update)**:
   - If this release introduces new architecture patterns, public API contracts, or domain models, record or update them in `wiki/<topic>/<concept>.md`.
   - Update `wiki/index.md` and log entry in `wiki/log.md`.
```

