---
name: html-plan
description: >-
  Builds a visual HTML plan with charts and aesthetics, syncs it for Cursor,
  opens it in Chrome, and lets reviewers annotate the plan then send annotations
  back into Cursor-readable files. Use for /plan output, html-plan, plan preview,
  plan feedback, or when the user annotates a plan in the browser.
---

# HTML Plan

Turn a plan into browsable HTML with charts, open it in Chrome, **annotate in the browser**, and **send annotations back to Cursor**.

## When to use

- After `/plan` or Phase 3 Plan content is ready
- User asks for `html-plan`, plan preview, or visual roadmap
- Plan sections change — regenerate HTML so it stays in sync with Cursor
- User annotated a plan in Chrome — **read the returned annotation files** before Implement

## Hard rules

1. **Always sync with Cursor** — Canonical HTML: `plans/html/<slug>.html`. Mirror to `.cursor/plans/html/<slug>.html` and the local plugin `plans/html/` when present.
2. **Charts to demonstrate** — At least two Chart.js charts from real plan data (no invented metrics).
3. **Visual aesthetics** — Distinctive fonts, atmospheric background, clear hierarchy. Avoid purple-on-white AI gradients and cream+terracotta clichés.
4. **When plan complete → server + Chrome** — Run the serve script (must stay up for annotate/send-back). Prefer Node: `serve-open.js`.
5. **Annotate → send back to Cursor** — The served page must include annotation UI. **Send to Cursor** writes files the agent/Cursor can open. Do not treat the plan as approved until annotations are reviewed (or the user confirms none).

## Workflow

```
HTML Plan Progress:
- [ ] 1. Collect plan content
- [ ] 2. Write plans/html/<slug>.html from template (include {{SLUG}})
- [ ] 3. Charts + aesthetics
- [ ] 4. Sync HTML to .cursor/plans/html/
- [ ] 5. Serve + open Chrome (keep server running)
- [ ] 6. User annotates → Send to Cursor
- [ ] 7. Agent reads annotation files and applies feedback
```

### 1–4. Build and sync HTML

Same as before: fill [template.html](template.html), replace all `{{…}}` tokens including **`{{SLUG}}`** (filename without `.html`). Sync copies to `.cursor/plans/html/`.

### 5. Serve + open Chrome

```bash
node skills/html-plan/scripts/serve-open.js plans/html/<slug>.html
```

Windows:

```powershell
powershell -File skills/html-plan/scripts/serve-open.ps1 -HtmlPath "plans/html/<slug>.html"
```

Keep the server running — annotate/send-back needs `POST /api/annotations`.

### 6. Annotate and send back to Cursor

In Chrome, the reviewer can:

1. **Hover** a section to highlight it; **click** to bind the annotate panel to that section
2. **Select text** to fill the quote field
3. **Double-click** a section to focus the note box
4. **Right-click** for a context menu (comment / change / approve / block / drop pin)
5. **Alt+click** or toggle **Pin** mode, then click the plan to drop location pins (`x`/`y` page coords)
6. **Click a chart** slice/bar to quote that label
7. Drag the annotate dock by its handle
8. Click **Send to Cursor**

The local server writes (overwrite + timestamped history optional):

| File | Purpose |
|------|---------|
| `plans/html/<slug>.annotations.json` | Machine-readable annotations |
| `plans/html/<slug>.annotations.md` | Human/agent summary |
| `.cursor/plans/html/<slug>.annotations.json` | Cursor-side mirror |
| `.cursor/plans/html/<slug>.annotations.md` | Cursor-side mirror |
| `.cursor/plans/inbox/<slug>-feedback.md` | **Inbox for Cursor** — short "what changed" ping |

Payload shape (JSON):

```json
{
  "slug": "2026-10-16-example",
  "sentAt": "ISO-8601",
  "annotations": [
    {
      "id": "a1",
      "section": "Risks",
      "quote": "optional selected text",
      "note": "reviewer comment",
      "kind": "comment|change|approve|block",
      "createdAt": "ISO-8601",
      "x": 420,
      "y": 880
    }
  ]
}
```

Optional `x` / `y` are page coordinates for pins placed via Pin mode, Alt+click, or the right-click pin action.

### 7. Agent: consume feedback

When the user says they sent annotations, or before Phase 4 Implement:

1. Read `.cursor/plans/inbox/<slug>-feedback.md` and `plans/html/<slug>.annotations.md`
2. Apply **change** / **block** items to the plan (and regenerate HTML if content changes)
3. Treat **approve** as sign-off signals; **block** as hard stops
4. Confirm in chat what was applied

## Page structure (required)

1. Title + summary  
2. Scope  
3. Charts  
4. Risks  
5. Acceptance criteria  
6. Phased roadmap  
7. Open questions  
8. **Annotate panel** — notes list + Send to Cursor (from template)

## Do not

- Open `file://` only — server required for send-back  
- Skip annotation UI in the HTML  
- Ignore `.cursor/plans/inbox/*-feedback.md` when the user says they sent feedback  
- Invent chart metrics  

## Additional resources

- [template.html](template.html) — charts + annotate + send-back UI  
- [scripts/serve-open.js](scripts/serve-open.js) — static serve + `POST /api/annotations`  
- [scripts/serve-open.ps1](scripts/serve-open.ps1) — launches Node server when available  
