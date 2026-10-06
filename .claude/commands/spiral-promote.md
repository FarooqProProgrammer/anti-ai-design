---
description: Promote reusable lessons from project Spiral memories into the company-wide house rules (with client details stripped), for a lead to approve.
argument-hint: [other project paths to include, space-separated]
---

Load the `spiral` skill. You are curating the company's **house rules**: lessons that should apply to every client
project. Extra projects to scan: $ARGUMENTS

1. **Find the files.** The house rules file is `spiral.config.json → houseRules` if set, otherwise `house/house-rules.md` in the
   spiral skill's directory. Collect `.spiral/memory.md` from the current project and from each path given (`<path>/.spiral/memory.md`).
   Skip missing ones and say which.
2. **Find candidates.** A project rule is a candidate if any of these hold:
   - it (or an equivalent) appears in **2+ projects**, or
   - it is clearly stack-general or taste-general (it would be right for any client on that stack), or
   - it repeats a correction the engineer had to make more than once in one project.
   Not candidates: rules about one client's domain, brand, API, or business logic, and rules that contradict another project's
   memory (list these as **conflicts** instead).
3. **Generalise and sanitise** each candidate: remove every client name, product name, domain, URL, file path specific to one
   repo, data, and identifier. If the rule makes no sense without them, it isn't a house rule. Merge with existing house rules
   instead of duplicating them; a stronger or clearer version of an existing rule replaces it.
4. **Ask** with AskUserQuestion (multiSelect) which candidates to promote. Show each as the final sanitised text plus its sources
   (project folder names are fine here; they won't be written to the file). Then list conflicts for the lead to decide on.
5. **Write** the approved rules into the right section of the house rules file with `(promoted <today>, seen in N projects)`.
   In each source project's `memory.md`, append ` → promoted to house rules <today>` to the original rule (keep it, since project
   memory still takes precedence).
6. **Don't commit.** Tell the lead the house rules live in the toolkit repo and should go through a PR so every developer gets them
   on their next pull. Show the diff of the house rules file.
