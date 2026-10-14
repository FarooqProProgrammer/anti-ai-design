# Setup Agent Command: /setup-agent

Automated onboarding and skills configuration for AI coding agents. Run this command to discover, vet, and install top-rated agent skills from the open ecosystem ([skills.sh](https://skills.sh/)).

---

## Command Usage

```bash
# In chat or terminal:
/setup-agent
```

Or execute directly via the Skills CLI:
```bash
cmd.exe /c "npx skills add vercel-labs/skills --skill find-skills -y --copy"
cmd.exe /c "npx skills add vercel-labs/agent-skills -y --copy"
```

---

## What `/setup-agent` Does

1. **Detects Environment**: Identifies configured AI agents (Cursor, Claude Code, Codex, Antigravity).
2. **Discovers Top Skills**: Uses the `find-skills` meta-skill to search the [skills.sh](https://skills.sh) registry and leaderboards.
3. **Installs Essential Engineering Packs**:
   - `find-skills` (`vercel-labs/skills`): Search and discover skills on the fly.
   - `react-best-practices` (`vercel-labs/agent-skills`): Enterprise React/Next.js performance patterns.
   - `web-design` / `frontend-design`: Modern UI styling and UX heuristics.
   - `brainstorming` (`obra/superpowers`): Design-first intent discovery.
   - `grill-me` (`mattpocock/skills`): Relentless Socratic requirement stress-testing.
   - `karpathy-llm-wiki` (`Astro-Han/karpathy-llm-wiki`): Persistent compounding knowledge base.
4. **Synchronizes Across Directories**: Copies installed skills to `.agents/skills/`, `skills/`, and `.claude/skills/` so **every agent** has immediate access.
5. **Verifies Evidence & Integrity**: Validates installed skill schemas and runs regression tests.

