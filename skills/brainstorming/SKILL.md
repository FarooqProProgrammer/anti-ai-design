---
name: brainstorming
description: "You MUST use this before any creative or engineering work: exploring requirements, creating features, building components, modifying behavior, or designing system architecture. Triggers: Phase 1 Understand, brainstorming, design exploration, architectural alternatives."
---

# Brainstorming Skill

Use this skill during **Phase 1: Understand** before writing plans or implementation code. It intercepts the AI's tendency to jump straight into code and ensures complete alignment on what is actually needed and why.

## Core Directives

1. **Uncover the "Why"**:
   - Don't just take the initial prompt at face value.
   - Clarify the underlying goal, user pain point, or architectural motivation.
   - Distinguish between **Goals**, **Non-Goals**, and **Anti-Goals** (what would make this a failure even if it technically works).

2. **Reconnaissance & Prior Art**:
   - Inspect existing patterns in the codebase (`@Codebase`, symbol search, call stack analysis).
   - Check `wiki/index.md` and compiled topic articles for prior architectural decisions (ADRs) and data models.
   - Examine how similar problems were solved elsewhere in the project.

3. **Explore Architectural Alternatives**:
   - Propose 2–3 viable approaches with explicit trade-offs:
     - Approach A: Minimal / Non-invasive
     - Approach B: Idiomatic / Extensible
     - Approach C: High Performance / Scalable
   - State the trade-offs (complexity, performance, backward compatibility, maintenance burden).

4. **One Question at a Time**:
   - Keep clarifying questions focused, concrete, and grounded in real codebase realities.
   - Avoid overwhelming menus of options; give a sensible default when the user asks for guidance.

