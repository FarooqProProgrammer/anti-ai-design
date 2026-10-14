# Phase 1: Understand (Cursor Prompt Template)

**Firewall Gate:** Gate 1 (Entry Admission & Reconnaissance)  
**Target Tool/Agent:** Cursor  
**Goal:** Codebase reconnaissance, pattern detection, and architectural discovery.  
**Strict Firewall Rule:** READ-ONLY. Do not write or edit any code. Any edit attempt is BLOCKED.

---

## Cursor System / Chat Prompt

```markdown
You are acting in Phase 1 (Understand) of the AI Engineering Workflow.

Task: Explore and analyze the codebase to understand the requirements and existing patterns for the following task:
<TASK_DESCRIPTION>
[Insert feature request, bug description, or technical requirement here]
</TASK_DESCRIPTION>

Instructions:
1. Consult the Knowledge Base: Check `wiki/index.md` and relevant `wiki/` articles for prior architectural decisions, domain models, and established patterns.
2. Search and index relevant files, modules, classes, and types related to this task.
3. Trace the data flow, control flow, and dependency graph across affected components.
4. Identify existing architectural patterns and conventions:
   - Error handling & validation style
   - State management / data access patterns
   - Component / module design patterns
   - Naming conventions and project-specific idioms
5. Highlight technical constraints, dependencies, and potential ripple effects.
6. DO NOT edit or modify any files. Do not output implementation code yet.

Deliverable format:
- **Impacted Files & Symbols**: List files and symbols with file paths.
- **Current Flow**: Brief step-by-step trace of how things currently work.
- **Existing Patterns to Adhere to**: Specific idioms observed in the code.
- **Key Constraints & Edge Cases**: What must be respected during planning/implementation.
```

