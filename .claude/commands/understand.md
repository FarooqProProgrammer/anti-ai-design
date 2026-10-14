# Command: /understand

Executes **Phase 1 (Understand)** of the AI Engineering Workflow governed by the Request Firewall ([FIREWALL.md](../../FIREWALL.md)).

---

## Usage

```bash
/understand <feature request, bug report, or requirement>
```

### Examples:
- `/understand Add OAuth2 authentication with Google and GitHub`
- `/understand Fix race condition in web researcher wiki indexing`
- `/understand Refactor dashboard charts to use view transitions`

---

## Execution Protocol

When `/understand` is executed, the agent MUST perform:

1. **Pre-Admission Contradiction Check**:
   - Parse the input requirement.
   - Query `wiki/index.md`, relevant `wiki/` articles, and project documentation.
   - Query `C:\Users\farooq\.cursor\projects` for prior session transcripts and solutions.
   - If a contradiction with established architecture is detected, **HALT and return the contradiction immediately**.

2. **Brainstorming Protocol (`skills/brainstorming/`)**:
   - Clarify the "Why": Define Goals, Non-Goals, and Anti-Goals.
   - Propose 2–3 architectural approaches with real trade-offs (e.g. Minimal vs. Idiomatic vs. High Performance).

3. **Grill-Me Protocol (`skills/grill-me/`)**:
   - Conduct a relentless Socratic technical interview.
   - Walk down the decision tree branch-by-branch.
   - Challenge unstated assumptions, failure modes, scale limits, and edge cases.

4. **Codebase Exploration**:
   - Trace caller/callee chains across affected components.
   - Note existing conventions (error handling, state, naming).

5. **Visual Diagram Artifact**:
   - Generate or update `diagrams/01-understand.exceldraw` (and `.svg`) depicting the decision tree and trade-offs.

6. **🛑 MANDATORY FIREWALL RULE**:
   - **READ-ONLY.** Never edit, create, or delete source code during Phase 1.
