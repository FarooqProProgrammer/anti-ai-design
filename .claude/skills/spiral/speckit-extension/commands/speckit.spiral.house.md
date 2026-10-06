---
description: "Offer the company house rules as candidate constitution principles"
---

# Spiral: house rules → constitution candidates

Load the `spiral` skill and read the house rules (`spiral.config.json → houseRules`, else `house/house-rules.md` in the
spiral skill directory).

A constitution holds **principles**: few, durable, non-negotiable (e.g. "test-first", "accessibility is a release blocker",
"no secrets in code"). House rules are mostly more concrete conventions. For the constitution step that follows:

1. Pick only the house rules that are principle-level, and phrase each as a principle with a one-line rationale.
2. Offer them to the engineer as candidates (AskUserQuestion, multiSelect). The engineer chooses; nothing is added automatically.
3. Leave the rest in the house rules. Spiral already enforces them at gate 3, so don't copy them into the constitution.
