---
description: Create a brand guidelines book (book.html) plus a ready-to-use brand kit — logo SVGs, favicon, icons + sprite, color/typography tokens, components CSS, Tailwind v4 theme. Uses the latest stable versions.
argument-hint: <brand name + what it is — or leave empty to use the current reference picks>
allowed-tools: Read, Write, Bash, WebFetch, AskUserQuestion, ToolSearch, mcp__claude_ai_Figma__get_metadata, mcp__claude_ai_Figma__get_screenshot, mcp__claude_ai_Figma__get_variable_defs, mcp__claude_ai_Figma__get_design_context, mcp__claude_ai_Figma__download_assets, mcp__claude_ai_Context7__resolve-library-id, mcp__claude_ai_Context7__query-docs
---

Create a brand book with the `anti-ai-slop-design` skill for:

> $ARGUMENTS

Follow `.claude/skills/anti-ai-slop-design/references/brand-book.md`. Read it first, and read `references/typography.md` for the fonts.

0. **Check sources first** (`references/design-sources.md`).
   - If the user gave a Figma link, check for the Figma MCP.
   - If it's connected, read `get_variable_defs` and `get_screenshot` first. Its colors, fonts, spacing, logo and icons go straight into `brand.json` and are not redesigned.
   - If it needs authentication or failed to connect, say so and ask for exported values or screenshots.
1. **Inputs.** Use whichever of these you have: the reference digest from a `/ref-board` run in this conversation, the brief, and any existing brand assets in the project (logo SVGs, colors, fonts, a tailwind config, CSS variables).
   - Existing assets win: document them, and don't redesign them.
   - If the brand name or what it is is missing, ask before going further.
2. **Logo.** If there is no logo and the direction is open, design 2–3 SVG mark concepts (one color, `currentColor`, grounded in the subject). Show them and ask the user to pick before building the book.
3. **brand.json.** Copy `.claude/skills/anti-ai-slop-design/assets/example-brand.json` to `brand/brand.json` in the project, unless the user named another location. Replace every value, and list every intended text-on-background pair in `pairings`.
4. **Build.**
   ```bash
   python .claude/skills/anti-ai-slop-design/scripts/brand_book.py build brand/brand.json brand/book.html
   ```
   Fix any intended pairing that prints below AA, then rebuild.
5. **Check.** Open the book and look at it (screenshot it if a browser tool is available): the logo at 16px, fonts loaded, icons present, components looking right.
6. **Export the kit.** This produces the files the app will use:
   ```bash
   python .claude/skills/anti-ai-slop-design/scripts/brand_book.py kit brand/brand.json brand/kit
   ```
   Open `brand/kit/demo.html` to confirm the logo, icons, fonts and components render.
7. **Report.** Give 4–6 lines on the key decisions: concept, palette, type, icons, voice. Include the paths to `book.html` and `kit/`, and one line on how to use the kit (the kit's README has the snippets). Then ask what to change, and offer to apply the kit to the app's pages.
