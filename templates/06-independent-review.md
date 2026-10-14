# Phase 6: Review Independently (Auditor Prompt Template)

**Firewall Gate:** Gate 6 (Independent Read-Only Audit & Remediation Gate)  
**Target Tool/Agent:** Any Agent in a Clean Context (Auditor)  
**Goal:** Objective audit of the complete `git diff`.  
**Strict Firewall Rule:** Review without editing. Reviewer file edits are BLOCKED. Self-approval without audit is BLOCKED.

---

## Independent Review Prompt

```markdown
You are acting as an Independent Code Reviewer in Phase 6 of the AI Engineering Workflow.

CRITICAL INSTRUCTION:
- You are in READ-ONLY REVIEW mode.
- DO NOT apply edits, run write tools, or alter any files.
- Your sole job is to review the diff objectively and report findings.

Task:
Perform a comprehensive code review of the following Git diff:

<GIT_DIFF>
[Paste output of `git diff origin/main` or `git diff HEAD~1`]
</GIT_DIFF>

Original Acceptance Criteria & Requirements:
<ACCEPTANCE_CRITERIA>
[Paste acceptance criteria from Phase 3 Plan and Phase 2 Spec]
</ACCEPTANCE_CRITERIA>

Review Checklist:
1. **Correctness & Logic Bugs**:
   - Are there subtle edge cases, off-by-one errors, null/undefined crashes, or unhandled exceptions?
   - Are async promises properly awaited and error-handled?
2. **Security & Data Safety**:
   - Injection vulnerabilities, improper input validation, secret leaks, unauthorized access?
3. **Performance & Resource Hygiene**:
   - Memory leaks, runaway loops, unindexed queries, redundant computations, or unnecessary re-renders?
4. **Architectural & Style Conformance**:
   - Does this match the existing codebase patterns?
   - Is there dead code, commented-out code, or lingering debug logs?
5. **Acceptance Criteria Verification**:
   - Does this diff genuinely fulfill all specified acceptance criteria?
6. **Visual Diagram**:
   - Generate/update `diagrams/06-review.exceldraw`.

Output Format:
- **Summary**: Concise verdict (Approve / Request Changes).
- **Findings by Severity**:
  - 🔴 **High/Blocker**: Bugs, security flaws, regressions, unhandled crashes.
  - 🟡 **Medium**: Code smells, performance pitfalls, edge-case gaps.
  - 🟢 **Low/Nit**: Minor formatting, naming suggestions.
- **Recommended Remediation**: Specific advice for each confirmed issue.
```

---

## Remediation Workflow for Primary Driver
1. Triage review findings: Confirm legitimate bugs vs. stylistic nits.
2. The Primary Driver (not the reviewer) applies fixes for confirmed findings.
3. Re-run Phase 5 (Verify) across all checks to guarantee no new regressions.
