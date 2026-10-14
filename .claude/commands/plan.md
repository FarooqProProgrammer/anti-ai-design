# Command: /plan

Executes **Phase 3 (Plan)** of the AI Engineering Workflow governed by the Request Firewall ([FIREWALL.md](../../FIREWALL.md)).

---

## Usage

```bash
/plan [context from /spec or detailed requirements]
```

### Examples:
- `/plan` (uses the findings and context snapshot from `/spec`)
- `/plan Add database migrations, repository pattern, and service layer for user profiles`

---

## Execution Protocol

When `/plan` is executed, the agent MUST produce an architectural implementation plan:

1. **Requirements & Scope Boundary**:
   - In-scope requirements vs. explicit out-of-scope items (to prevent scope creep).
   - Ingest any external RFCs or documentation into `raw/` and compile into `wiki/` via `karpathy-llm-wiki`.
   - Backward compatibility and schema migration impacts.

2. **Risk & Mitigation Matrix**:
   - Call out failure modes, concurrency issues, edge cases, and performance bottlenecks.
   - Assign likelihood/impact and provide an explicit mitigation for each.

3. **Acceptance Criteria (Given-When-Then)**:
   - Concrete, testable conditions:
     ```markdown
     - [ ] AC-1: Given [precondition], When [action], Then [expected result]
     - [ ] AC-2: Error handling: Given [invalid input], Then [expected error]
     - [ ] AC-3: Performance: [Specific threshold]
     ```

4. **Phased Implementation Roadmap**:
   - Break implementation into atomic milestones (Phase 4.1, Phase 4.2, Phase 4.3).
   - Designate the Primary Driver (Cursor, Claude Code, or Codex).

5. **Visual Diagram Artifact**:
   - Generate or update `diagrams/03-plan.exceldraw` (and `.svg`) displaying milestones and acceptance gates.

6. **🛑 MANDATORY FIREWALL RULE**:
   - **No code is written until human sign-off.**
   - Output the plan and wait for user approval before moving to Phase 4 (Implement).

