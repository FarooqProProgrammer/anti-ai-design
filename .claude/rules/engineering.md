# Claude Code — Engineering Standards & Quality Rules

## 1. Humanized Content Rule (Mandatory)
All content generated or modified by Claude Code—including code comments, commit messages, PR descriptions, and markdown documentation—must read like it was written by an experienced human software engineer:
- **Zero AI Buzzwords:** Ban robotic filler like *"delve into"*, *"tapestry"*, *"in conclusion"*, *"it is important to remember"*, *"testament to"*, *"harnessing the power"*, *"streamlining"*, *"game-changer"*, or *"meticulously crafted"*.
- **Active, Direct Voice:** Write naturally: "we recommend", "this function throws when...", "here's how to configure".
- **Pragmatic Comments:** Never state the obvious syntax in code comments. Only explain non-obvious engineering decisions and trade-offs.
- **Natural Rhythm:** Keep sentences direct, punchy, and grounded in real-world software trade-offs.

---

## 2. Single Driver Discipline
- Keep one agent responsible for main business logic and architecture during an implementation phase.
- Prevent multi-agent churn: do not rewrite working modules between models.

---

## 3. Zero-Concealment Verification
- Do not disable tests, relax types, comment out assertions, or introduce suppressions (`@ts-ignore`, `eslint-disable`).
- Always log the complete error message and stack trace.
- Fix underlying causes in the implementation code.

---

## 4. Vercel & React Architecture Guidelines
- Minimize re-renders: derive state during rendering instead of using `useEffect`.
- Use functional updates: `setState(prev => ...)`.
- Component composition: prefer compound components and slots over boolean prop proliferation.
- Web interface guidelines: ensure keyboard accessibility, correct semantic tags, and responsive design.

---

## 5. Diagram Artifacts Standard (.exceldraw)
- Every phase requires an ExcelDraw diagram (`.exceldraw`, `.excalidraw`, `.svg`) with proper descriptions.
- Use `scripts/generate_exceldraw.py` or compatible JSON schema.

---

## 6. Commit Hygiene
- Format: `type(scope): subject`.
- Clean diffs without commented debug code or temporary files.
