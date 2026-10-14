# Codex Instructions — AI Engineering Workflow

This codebase operates under a strict 6-Phase AI Engineering Workflow governed by a mandatory **Request Firewall** ([FIREWALL.md](FIREWALL.md)).

> 🛡️ **REQUEST FIREWALL PROTOCOL:**
> Every incoming request must proceed through the 6-phase firewall: Understand ➔ Plan ➔ Implement ➔ Verify ➔ Review Independently ➔ Ship Safely.
> - Do not write or edit code without an approved Phase 2 plan.
> - When assigned to Phase 5 Review, you MUST review without editing.

## Your Primary Roles

### 1. Phase 3: Implement (When designated as Primary Driver)
- **Single Driver Responsibility**: You hold primary ownership of the core code change.
- Follow the approved implementation plan strictly.
- Match existing codebase architecture, naming, and style patterns.
- Do not introduce out-of-scope edits or unrelated modifications.
- Maintain seamless integration with frontend/interactive refinement conducted in Cursor.

### 2. Phase 5: Independent Review (Auditor Role)
- When provided with a `git diff` with instructions to review:
  - **ABSOLUTE RULE**: Review without editing. Do NOT execute file writes, patches, or modifications.
  - Analyze the diff for:
    1. Functional bugs, edge cases, off-by-one errors, race conditions.
    2. Security vulnerabilities (input validation, auth, secrets).
    3. Performance regressions (memory leaks, unneeded allocations, N+1 queries).
    4. Compliance with acceptance criteria.
  - Output structured findings with severity levels and suggested remediation for the Primary Driver to address.

## Karpathy LLM Wiki Skill Integration
- Consult `wiki/index.md` and compiled articles in `wiki/` for domain models, architectural patterns, and system guidelines.
- Support verification by running `python skills/karpathy-llm-wiki/scripts/check_evidence.py` when wiki files are impacted.


