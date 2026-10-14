# Web Research & Wiki Indexing Command: /research

Use this command to research any technical topic or URL on the web, and immediately index and compile the researched source into `raw/` and `wiki/`.

---

## Usage

```bash
/research <topic or url>
```

### Examples:
- `/research Next.js 15 Server Actions best practices`
- `/research https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API`
- `/research React compiler optimization trade-offs`

---

## What `/research` Does Automatically:

1. **Searches & Fetches Web Content**:
   - Downloads the authoritative text and documentation from the web.
2. **Archives Raw Source**:
   - Saves clean, immutable markdown into `raw/<topic>/YYYY-MM-DD-<slug>.md` with URL, collected date, and published date.
3. **Compiles Grounded Knowledge Article**:
   - Writes a compiled article in `wiki/<topic>/<article>.md` citing the raw source and respecting the Grounding Invariant.
4. **Indexes Website in Project Wiki**:
   - Adds an entry directly into `wiki/index.md` so the whole team and all AI agents can query it.
   - Logs the operation in `wiki/log.md`.
5. **Verifies Evidence**:
   - Runs `python skills/karpathy-llm-wiki/scripts/check_evidence.py .` to ensure 100% evidentiary integrity.
