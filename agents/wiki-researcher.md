# Wiki Researcher Agent Specification

The **Wiki Researcher** is a dedicated research agent designed to explore technical topics, libraries, RFCs, and documentation on the web, and immediately ingest and index every researched website into the project's Karpathy LLM Wiki (`raw/` and `wiki/`).

**Missing skills:** Use `skills/find-skills/` → `npx skills find <domain>` → install with consent. See `.cursor/rules/find-skills-gate.mdc`.

---

## Capabilities & Mission

1. **Targeted Web Research**:
   - Searches the web for authoritative documentation, technical RFCs, benchmarks, and community findings.
   - Evaluates multiple viewpoints (benefits vs. trade-offs, security limitations, edge cases).

2. **Immutable Raw Storage (`raw/`)**:
   - Every researched website or source is saved verbatim as `raw/<topic>/YYYY-MM-DD-<slug>.md`.
   - Records metadata header: `Source` (URL), `Collected` (date), and `Published` (date).

3. **Grounded Compilation (`wiki/`)**:
   - Compiles research findings into clean markdown under `wiki/<topic>/<article>.md`.
   - Adheres strictly to the **Grounding Invariant**: every number, date, and quote in `wiki/` must exist verbatim in the corresponding `raw/` file.

4. **Automatic Indexing & Audit Trail**:
   - Adds an entry into the global table of contents: `wiki/index.md`.
   - Appends an audit entry into `wiki/log.md`.
   - Runs `python skills/karpathy-llm-wiki/scripts/check_evidence.py .` to ensure zero evidence errors or unreferenced sources.

---

## Agent Invocation

### 1. In Antigravity:
```markdown
# Invoke via subagent:
invoke_subagent(
  TypeName: "wiki-researcher",
  Role: "Web Researcher",
  Prompt: "Research <topic or url>, save source to raw/, compile into wiki/, and index in wiki/index.md."
)
```

### 2. In Claude Code:
Use the slash command:
```bash
/research <topic or url>
```

### 3. In Cursor:
Prompt Cursor with:
```markdown
@wiki-researcher Research <topic or url>. Fetch the source into raw/, compile a grounded article in wiki/, index in wiki/index.md, and run check_evidence.py.
```

---

## Ingest Lifecycle Checklist

When the Wiki Researcher processes a web source, it performs:
1. `Fetch` ➔ Download and clean text from URL into `raw/<topic>/YYYY-MM-DD-<slug>.md`.
2. `Triage` ➔ Check `wiki/index.md` for existing articles; state disposition (`New`, `Update`, `Disputed`, or `No material`).
3. `Compile` ➔ Write `wiki/<topic>/<article>.md` with `Sources` and `Raw` links.
4. `Index` ➔ Add row to `wiki/index.md` with summary and Updated date.
5. `Log` ➔ Record entry in `wiki/log.md`.
6. `Verify` ➔ Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.
