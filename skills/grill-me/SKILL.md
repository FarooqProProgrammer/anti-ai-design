---
name: grill-me
description: "A relentless Socratic technical interview to stress-test designs, plans, requirements, and edge cases before implementation. Triggers: Phase 1 Understand, grill me, interview me, stress-test requirements, challenge design."
---

# Grill-Me Skill

Use this skill during **Phase 1: Understand** to rigorously stress-test assumptions, uncover hidden edge cases, and eliminate ambiguities before advancing to Phase 2 (Plan).

## Core Directives

1. **Relentless Socratic Interrogation**:
   - Do NOT passively accept vague requirements or nod along.
   - Walk down the **decision tree** branch-by-branch, resolving prerequisites in sequential rounds.
   - Challenge hidden assumptions: *"What happens if the network drops here?"*, *"How does this scale with 100k items?"*, *"What if the user passes invalid auth tokens?"*

2. **Codebase-Grounded Inquiries**:
   - Check the codebase first. If an answer can be found in existing code, don't ask the user—cite the code and verify if the same pattern applies.
   - Point out specific existing interfaces, types, or DB models that might conflict with the proposal.

3. **Handling "I Don't Know"**:
   - If the user or developer is unsure about an architectural question, do not guess blindly.
   - Propose a small spike / prototype path or offer standard production best practices to break the deadlock.

4. **Exit Criteria**:
   - The interrogation concludes only when all load-bearing architectural choices, failure modes, and boundaries are explicitly decided.

