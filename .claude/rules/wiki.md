# Claude Code — Karpathy LLM Wiki Rules

This repository maintains an LLM-compiled knowledge base under `wiki/` and immutable sources under `raw/` according to `skills/karpathy-llm-wiki/`.

## 1. Directory Structure
- `raw/<topic>/YYYY-MM-DD-slug.md`: Immutable source material. Read-only. Never modify existing files.
- `wiki/<topic>/<article>.md`: Compiled knowledge articles. One level of topic subdirectories only.
- `wiki/index.md`: Global index table (`Article | Summary | Updated`).
- `wiki/log.md`: Append-only operation log.

---

## 2. Grounding Invariant
> **Every load-bearing fact, number, date, and direct quote in `wiki/` must exist verbatim in the `raw/` files linked by that article's `Raw` field.**

- Locate before write: Locate literals in `raw/` before writing to `wiki/`.
- If the source states `42K`, write `42K`, not `42,000`.
- Derived values must show their components findable in `raw/`.

---

## 3. Operational Lifecycles

### Ingest
1. Fetch source into `raw/<topic>/YYYY-MM-DD-slug.md` with metadata header (`Source`, `Collected`, `Published`).
2. Triage: State disposition (`New`, `Update`, `Disputed`, or `No material`).
3. Compile into `wiki/<topic>/article.md` with metadata header (`Sources`, `Raw`, `Updated`).
4. Cascade updates to affected articles; annotate superseded claims with `> **Status: Outdated** (YYYY-MM-DD)`.
5. Update `wiki/index.md` and append to `wiki/log.md`.

### Query
1. Search `wiki/index.md` and full-text search `wiki/` using key concepts and synonyms.
2. Synthesize answers prioritizing wiki content over training knowledge. Cite using markdown links.
3. Plain queries do not write files. Only write archive pages when explicitly asked.

### Lint & Verify
- Run `python skills/karpathy-llm-wiki/scripts/check_evidence.py .`.
- Fix evidence errors immediately.
- Report fidelity suspects without modifying source facts.
- Append results to `wiki/log.md`.

---

## 4. Local Knowledge Repository (`C:\Users\farooq\.cursor\projects`)
- You are authorized to read and query `C:\Users\farooq\.cursor\projects` (especially `d-ai-agent-the-developer/` and sibling projects) for previous agent transcripts (`agent-transcripts/`), execution logs (`terminals/`), and architectural canvases.
- Compound durable insights into `raw/cursor-projects/` and `wiki/cursor-projects/`.
