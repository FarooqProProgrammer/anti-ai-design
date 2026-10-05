---
name: anti-ai-slop-design
description: Stops UI from looking generically AI-generated ("AI slop") — purple-to-blue gradients, gradient headline text, emoji icons, glassmorphism cards, centered hero + three feature cards, "Unlock / Supercharge / Seamless" copy, everything rounded-2xl with a glow. Use this whenever building, styling, reviewing, or redesigning any web UI — landing pages, dashboards, app screens, components, HTML/CSS, React/Vue/Svelte — even if the user never says "slop" or "design". Everything it builds is responsive and mobile-first; also use it when a UI breaks or looks bad on phones. Also use when the user says a UI looks generic, template-y, cookie-cutter, "like every other SaaS/AI app", soulless, or asks to audit, critique, or "make it look less AI". Also use when picking fonts or a font pairing for a site/app, or matching typography to a brand, reference, audience, or language (e.g. Urdu/Arabic/Hindi content), and when the user wants design references, inspiration, or a moodboard found on the web and ranked for them to choose from, or brand guidelines / a brand book / logo / color palette / style guide. Also use whenever the user pastes a figma.com link or mentions Figma or Mobbin for a UI task — it checks the Figma/Mobbin MCP servers first and works from the real design.
---

# Anti AI-Slop Design

"AI slop" UI isn't ugly — it's *undecided*. Every choice is the statistically most common default: Inter on white, indigo→purple gradient, centered hero, three cards with emoji icons, "Supercharge your workflow". Each default is fine alone; together they signal "nobody thought about this", and users stop trusting the product.

The cure is not a different set of defaults (swapping purple for teal is still slop). The cure is making **specific decisions rooted in the subject**: who this is for, what they're doing, what the brand actually is. A tax firm, a synth plugin, and a hospital rota app should not look alike.

## Step 0 — check design sources before anything else

Before picking a mode, look for design sources the user gave you and check which design MCP servers are connected. Full procedure: `references/design-sources.md`.

- **A `figma.com/...` link (or "my Figma file")** → check for the Figma MCP (tool names containing `figma`; load deferred ones with one ToolSearch call). If connected, read the file *first*: `get_metadata` → `get_screenshot` → `get_variable_defs` → `get_design_context` (load Figma's design-to-code guidance before that last one). The Figma file is the user's design system and outranks everything else in this skill.
- **"Mobbin", or any reference hunt / app-UI build** → pre-check for the Mobbin MCP (`search_screens`, `search_sections`, `search_flows`) and use it as the first reference source: look at the images, cite each `mobbin_url`, download `image_url` for the board.
- **Not connected, needs auth, or failed** → say so in one line (needs auth: connect it in claude.ai connector settings or `/mcp`), never WebFetch a Figma link or pretend you read it, and offer the fallback (exported screenshots + token values for Figma; web search for Mobbin). If the task depends entirely on that source, wait for the user.

State what you found in one line ("Figma connected — reading your file first"), then continue.

## Modes

This skill has five modes. Pick based on the request:

| Request | Mode |
|---|---|
| Build a new page / component / screen | **Build** |
| Review / critique / "does this look AI-generated?" | **Audit** |
| "Make this look less generic", redesign, restyle | **Fix** (Audit → Build) |
| "Find references / inspiration / a moodboard", or a full page from an open brief with no references | **Reference hunt** (then Build) — also `/ref-board` |
| Brand guidelines, brand book/kit, style guide, logo, color palette, design-system page | **Brand book** — also `/brand-book` |

The full catalog of tells, why each reads as slop, and what to do instead lives in `references/slop-catalog.md`. Read it the first time you use this skill in a session — it's the backbone of every mode.

---

## Reference hunt

Generic output comes from designing out of memory; looking at real, well-made work first fixes that. When the user asks for references/inspiration — or you're building a full page/site/app from an open brief with no references, brand guide, or design system — follow `references/web-references.md`:

1. **Brief** — subject, audience, 3 traits, content shape, must-haves, constraints. This is what everything gets ranked against.
2. **Search** — UI-library MCPs (e.g. Mobbin) first, then web search on curated galleries of *shipped* work (land-book, godly, siteinspire, fontsinuse…); 8–15 candidates across ≥3 distinct directions.
3. **Actually look** — fetch preview images (`python .claude/skills/anti-ai-slop-design/scripts/ref_board.py fetch <url> <scratchpad>/refs`) and view them, or screenshot with a browser tool. Never rank on looks you haven't seen.
4. **Modules** — list the 4–7 parts the user will choose for (Typography, Color, Layout, Imagery + page modules from the brief like Hero, Pricing, Trust & proof; or Shell, Tables, Charts for apps), each with a one-line "need".
5. **Analyze & score** — overall (audience fit, traits, content shape, distinctiveness, feasibility, constraints; rerank for diversity) **and per module**: how each reference handles each module, scored 1–5 against that module's need, with a one-line note. Skip modules a reference doesn't show.
6. **Board** — copy the template `assets/example-refs.json`, fill it, render with `ref_board.py board refs.json board.html`, and open it (see `assets/example-board.html`). It shows the overall ranking, then each module with every reference side by side, a *Recommended* pick, and pick controls + a "Copy choices" button.
7. **User picks per module** — summarize the recommendation and runner-up per module in chat, then ask module by module (structured question tool if available: one question per module, top 3 refs as options, recommended first) — or have them paste their copied board choices. Mixing references across modules is expected. Wait for the answers.
8. **Digest** — per module: what to borrow from the chosen reference, how to adapt it, what not to copy; flag conflicting picks. Feed it into Build steps 1–2.

If the brief is thin and the user hasn't asked, offer this in one line rather than running it unprompted. Skip it for small components, quick fixes, or when the user already supplied references.

---

## Brand book

When the user wants brand guidelines (or after a reference hunt for a new brand, before building pages), follow `references/brand-book.md`: fill a copy of `assets/example-brand.json` — essence, logo (SVG with `currentColor`; design 2–3 subject-grounded concepts for the user to pick if none exists, never redesign an existing one), colors with roles + usage %, typography, icons, imagery, layout, voice, guardrails — then build `book.html`:

```bash
python .claude/skills/anti-ai-slop-design/scripts/brand_book.py build brand/brand.json brand/book.html
```

The script computes tints, RGB/HSL, a WCAG contrast matrix (and prints failing intended pairings — fix them), logo clear-space/size ladder/misuse examples, inlined icons, live components and downloadable tokens. See `assets/example-book.html`. Open and check it before handing over.

Then export the **kit** — everything the book shows as files the app actually uses (tokens.css/json, components.css, Tailwind preset, logo SVGs + color variants, favicon, icon SVGs + sprite, demo page, README with HTML/React/Tailwind snippets):

```bash
python .claude/skills/anti-ai-slop-design/scripts/brand_book.py kit brand/brand.json brand/kit
```

See `assets/example-kit/`. **If a brand kit exists in the project, Build and Fix modes implement with it** — import its tokens/components, inline its logo, use its icon sprite, follow its voice — rather than choosing new colors, fonts or icons (details in `references/brand-book.md` → "Implementing the brand in the app").

---

## Build mode

### 1. Write a design point of view first (before any code)

If a brand kit exists (e.g. `brand/kit/tokens.css`), the brand is already decided — skip to building with it. If a reference hunt was done, start from the user's picked direction and digest.

Spend a few lines deciding, and state them briefly to the user so they can redirect:

- **Subject & audience** — what is this, who uses it, in what situation (a stressed freelancer at tax time ≠ a teen choosing sneakers). Include the **primary device** — assume a phone unless the context says otherwise (e.g. a ward PC dashboard).
- **One-sentence character** — e.g. "a calm, ledger-like precision with one warm accent", "loud zine energy", "clinical and dense, built for speed". Avoid the empty adjectives "modern, clean, sleek" — they describe every slop page.
- **One memorable idea** — the single thing someone would remember: an unusual type pairing, a real photograph, a data-dense table as the hero, an oversized number, a strong grid break. One is enough; five is noise.
- **What you're deliberately *not* doing** — name 2–3 slop defaults you're avoiding for this project.

If the user gave brand colors, fonts, references, or an existing design system, those override everything here — follow them and only apply the catalog to fill gaps.

### 2. Choose tokens deliberately

Define these as CSS custom properties (or the project's token system) before writing components, so the page is consistent and the choices are visible:

- **Type — chosen from the input, not from habit.** Read `references/typography.md` and work down its signal ladder: explicit brand fonts / design system → existing codebase fonts → reference images (match their characteristics) → languages & scripts in the content (a hard constraint — e.g. Urdu, Arabic, Hindi need real coverage) → subject, audience and context of use → content shape (long reading vs dense data vs short marketing). Turn that into three traits, pick a display + body pair (+ mono if there's data), and state the choice with a one-line reason tied to the user's subject. Then set a real type scale — big display sizes, tight headline leading, comfortable body measure (~60–75ch). Both Inter-everywhere *and* the "tasteful AI" reflexes (Space Grotesk, Instrument Serif, Fraunces, IBM Plex on everything) count as defaults unless the input justifies them.
- **Color**: start from neutrals that aren't pure #fff/#000 (tint them toward the brand), add **one** accent used sparingly for action and emphasis. Derive the accent from the subject, not from "tech = purple". Gradients only if they mean something.
- **Space**: one spacing scale, used with *variation* — tight groups, generous section breaks. Uniform padding everywhere is a tell.
- **Shape & depth**: pick one radius philosophy (sharp, slightly soft, or pill) and one elevation approach (borders, or subtle shadow, or flat color blocks). Don't stack blur + glow + shadow + gradient border.

### 3. Compose mobile-first

**Every layout is responsive and mobile-first** — follow `references/responsive.md`:

- **Design the 360–390px layout first**, then expand. The phone's order *is* the hierarchy: what this is + the one main action must fit on the first screen without scrolling.
- **Write CSS mobile-first**: base styles = phone; enhance with `@media (min-width: …)` at the points the content needs (not `max-width` desktop-down overrides). Viewport meta always; never disable zoom.
- **Fluid by default**: `clamp()` for type and section spacing, `min(100% - 32px, 1200px)` containers, `repeat(auto-fit, minmax(min(100%, 280px), 1fr))` grids, `100svh` not `100vh`, no fixed pixel widths, no horizontal scroll at 360px.
- **Adapt, don't just stack**: reorder for phones, turn card rows into lists or peeking scrollers, wide tables into scroll wrappers with a sticky first column or per-row cards, comparison tables into per-plan cards.
- **Touch first**: targets ≥ 44px, primary action in thumb reach (full-width or sticky bottom bar for key flows), nothing hover-only, correct input `type`/`inputmode`, inputs ≥ 16px, never hide the primary CTA inside a hamburger.
- **Light on mobile data**: ≤ 2 font families, `srcset`/`<picture>` with explicit dimensions, lazy-load below the fold, no autoplay background video.

Then compose the content:

- Let content dictate layout. Not every section is "heading + subtext + grid of 3 cards". Use asymmetry, left-aligned text, varied section rhythms, full-bleed moments, tables, lists, real numbers.
- Use real or realistic content: specific copy, plausible names and figures for the domain. Placeholder content is where slop hides (see the copy section of the catalog).
- Icons: one consistent set (stroke icons, or none) — not emoji, not a different style per card. Many sections need no icon at all.
- Motion: purposeful and small. No blanket `hover:scale-105`, floating blobs, or pulse on decoration.
- Still do the basics well — accessible contrast, focus states, semantic HTML. Distinctive ≠ broken.

### 4. Self-audit before handing over

Run the scanner on what you wrote and fix anything that isn't an intentional choice (it also flags desktop-first `max-width` queries, missing viewport meta, fixed pixel widths, `100vh`, disabled zoom):

```bash
python .claude/skills/anti-ai-slop-design/scripts/slop_scan.py <file-or-dir>
```

**Check it at phone width.** With a browser tool, screenshot at 390px and at desktop width and look at both; without one, walk through the CSS at 360 / 768 / 1440px. Fix: horizontal scroll, overflowing text, tap targets < 44px, CTA below the first phone screen, unreadable tables, hover-only features.

Then do the **swap test**: if you replaced the company name with a different company in a different industry, would the page still work unchanged? If yes, it's still generic — go back to the point of view and push the one memorable idea harder.

---

## Audit mode

Goal: tell the user specifically *why* it looks AI-generated and what to do, ranked by impact.

1. Run the scanner on the code (if code is available) for a quick objective pass. Treat its output as leads, not verdicts — a gradient can be intentional.
2. Read the code/screenshot yourself against `references/slop-catalog.md`. The scanner can't see composition problems (identical section rhythm, no focal point, everything centered, generic copy tone), so look for those by eye. **Always review the mobile view too** (screenshot at 390px if a browser tool is available, otherwise read the breakpoints) — a desktop-first page that collapses into one endless column is one of the most common problems; report it like any other tell.
3. Report using this structure:

```markdown
## Slop verdict
One or two sentences: how generic it reads overall and the biggest reason why.

## Top issues (highest impact first)
For each: **the tell** — where it is (file:line or section) — why it reads as AI-generated — the concrete fix.

## What's working
Things that are already distinctive or well done — keep these.

## Direction
A 2–3 line point of view the redesign could take, grounded in the product's subject.
```

Keep it to the 5–8 issues that matter most; a list of 30 nitpicks is its own kind of slop. Be direct but not snide — the person may have built it themselves.

---

## Fix mode

1. Audit first (briefly — you can summarize instead of the full report unless asked).
2. Write the design point of view (Build step 1), grounded in what the product actually is. Preserve anything the audit marked as working, plus all real content, functionality, and the existing tech stack.
3. Rebuild tokens, then components, then layout — changing structure where the structure itself is the slop (e.g. replace the 3-card grid with something the content actually calls for), not just recoloring. Rebuild the layout **mobile-first** (Build step 3), even if the original was desktop-first.
4. Rescan, check at phone width, do the swap test, and summarize what changed and why in a short list.

Don't just strip things out until it's beige minimalism — that's another default. Replace generic choices with specific ones.
