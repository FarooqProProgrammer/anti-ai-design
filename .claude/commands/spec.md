# Command: /spec

Executes **Phase 2 (Spec)** of the AI Engineering Workflow governed by the Request Firewall ([FIREWALL.md](../../FIREWALL.md)).

---

## Usage

```bash
/spec [context from /understand or feature description]
```

### Examples:
- `/spec` (uses the findings and context snapshot from `/understand`)
- `/spec Define API contracts, data models, and error responses for User Authentication`

---

## Execution Protocol

When `/spec` is executed, the agent MUST produce an unambiguous Technical & Functional Specification:

1. **Functional Specification**:
   - User journeys and workflows.
   - Behavioral invariants that must always hold true.
   - Input and output contracts.
   - Explicit non-features to block scope creep.

2. **Technical & Data Specification**:
   - TypeScript interface and type signatures.
   - Database schema modifications and entity relations.
   - API endpoint request/response payloads and HTTP status codes.
   - Error response envelopes.
   - External RFCs/specs ingested into `raw/` and compiled in `wiki/`.

3. **Non-Functional Guardrails**:
   - Latency thresholds and performance budgets.
   - Security, authentication boundaries, and permissions.
   - Concurrency and race-condition safety.
   - Backward compatibility and migration rules.

4. **Visual Diagram Artifact**:
   - Generate or update `diagrams/02-spec.exceldraw` (and `.svg`).

5. **🛑 MANDATORY FIREWALL RULE**:
   - **READ-ONLY on source code.** Do NOT write implementation code.
   - Obtain human review and sign-off on the Specification before moving to Phase 3 (`/plan`).
