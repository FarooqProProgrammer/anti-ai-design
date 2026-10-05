# Brand Book (book.html)

The brand book turns every design decision into one shareable page: essence, logo, color, typography, icons, imagery, layout, components, voice, guardrails and tokens. It's rendered by `scripts/brand_book.py` from a `brand.json` you write. The book is styled *in* the brand itself, so it doubles as a proof that the system works.

## When to make one

- The user asks for brand guidelines, a brand book, a brand or style guide, a design system page, a logo, a color palette or "brand kit".
- After a reference hunt and its digest, for a new product or company, to lock the direction before building pages.
- Before a multi-page build, so every page draws from the same tokens.

Skip it for a single component or a quick fix, or when the user already has a brand book. In that case, read theirs and follow it.

## Process

1. **Gather inputs.** Use the brief, the reference digest, typography choices (`typography.md`), and any existing brand assets.

   **Existing assets win.** Never redesign an existing logo or palette unless asked. Document it as it is, and flag accessibility problems instead of silently changing it.

2. **Copy the template.** Copy `assets/example-brand.json` to `<scratchpad or project>/brand/brand.json` and replace everything. Its schema is in the script's docstring.

3. **Fill each section using the rules below.**

4. **Build and open the book:**
   ```bash
   python .claude/skills/anti-ai-slop-design/scripts/brand_book.py build brand/brand.json brand/book.html
   ```
   The script prints the contrast of every pairing you listed in `pairings`. **Fix anything below AA (4.5:1) that's meant for body text** before showing the book. The rendered book also shows the full contrast matrix.

5. **Look at it.** Take a screenshot with the browser tool if one is available, otherwise open the file for the user. Check that:
   - the logo reads at 16px;
   - the misuse examples render;
   - the fonts loaded;
   - the icons appear.

6. **Export the kit.** The kit holds everything the book shows, as files the app can use directly:
   ```bash
   python .claude/skills/anti-ai-slop-design/scripts/brand_book.py kit brand/brand.json brand/kit
   ```

   | File | Contents |
   |---|---|
   | `tokens.css`, `tokens.json` | Colors, fonts, spacing, radius, shadows, type sizes |
   | `components.css` | `.btn-primary/secondary/link`, `.field`, `.card`, `.band`, `.table`, `.badge-*`, `.icon`, `.logo` |
   | `tailwind.theme.css` | Tailwind v4 (current) `@theme`: `bg-accent`, `font-display`, `text-h1`… |
   | `tailwind.preset.js` | Legacy Tailwind v3 preset, only for projects still on v3 |
   | `shadcn-theme.css` | Brand mapped to shadcn's variables (OKLCH, light + derived dark, fonts, status colors) for React/Vue projects |
   | `fonts.html` | Font `<link>` tags |
   | `logo/` | `mark.svg` and `wordmark.svg` (currentColor) plus baked `-ink`, `-reversed` and `-accent` variants |
   | `favicon.svg` | The favicon, plus PNGs if `cairosvg` is installed |
   | `icons/*.svg`, `icons/sprite.svg` | The icon set, individually and as a sprite |
   | `demo.html` | A page that uses all of the above |
   | `README.md` | Snippets for HTML, React/Next and Tailwind |

   Open `demo.html` to confirm everything renders.

7. **Hand it over.** Summarize the key decisions in 4–6 lines and ask what to change. Save `brand.json`, `book.html` and `kit/` where the user wants them (default: `brand/` in the project).

## Implementing the brand in the app

When building pages after a brand book exists, **use the kit; don't re-invent the design**:

- **React or Vue project:** use shadcn (see `shadcn.md`). Paste `shadcn-theme.css` into the project's `tailwindCssFile`, add components with the shadcn CLI, and use the official `shadcn` skill for React. In that case `components.css` isn't used, because shadcn's components replace it.
- **Styles (non-shadcn projects):** import `tokens.css` + `components.css` once. On Tailwind, check the project's installed version first: for v4 (current) add `@import "./brand/tailwind.theme.css"` after `@import "tailwindcss"`, and use the v3 preset only if the project is still on v3. Use the token variables and component classes, and never hard-code a hex value or font that's already a token.
- **Logo:** inline `logo/wordmark.svg` in the header (it follows `color`), and use `logo/mark.svg` where space is tight. Link `favicon.svg`.
- **Icons:** only from `icons/`, via the sprite (`<use href="…/sprite.svg#i-name">`) or the individual SVGs, always beside a label. Need an icon that isn't in the set? Add it to `brand.json` and re-export, so the set stays consistent.
- **Copy:** follow the book's voice section ("we say / we don't say").
- **Changes:** if a page needs something the system lacks (a new color, a component), extend `brand.json`, rebuild the book and the kit, and tell the user. Don't patch it ad hoc in one page.

## Section rules

### Essence
- **Mission:** one sentence about the user's customer, not about "innovation".
- **Traits:** 3–4, from the brief.
- **Personality:** "is / is not" lists that would actually rule things out. "Is not: a fintech startup" is useful; "Is not: boring" isn't.

### Logo
If the user has a logo, embed their SVG and don't redesign it. If not, design one, following these rules:

- **Ground the concept in the subject.** "A K on a double underline, the accountant's total line" beats an abstract swoosh. Write the concept in `logo.concept`.
- **Provide two lockups:**
  - `mark_svg`: a symbol that works at 16px. Simple geometry, few nodes, square viewBox.
  - `wordmark_svg`: the mark plus the name, set in or derived from the display font.
- **Use one color, via `fill="currentColor"`.** The book recolors it for light, dark and accent backgrounds and generates the size ladder and misuse examples from it. No gradients, no hard-coded colors.
- **Avoid logo slop:**
  - sparkles ✨, brains, circuit nodes, rockets, generic swooshes or orbits;
  - hexagons meaning "tech";
  - a letter in a gradient rounded square;
  - an AI "spark" or star;
  - a globe for "global";
  - a lightbulb for "ideas".
- **Text inside an SVG relies on the font being loaded.** The book loads it, but tell the user to convert text to outlines for production use (in Figma or Illustrator, "Outline stroke / Create outlines").
- **If there's no logo and the brief is open, offer 2–3 concepts first.** Render each mark small and large, and let the user pick with the same pick pattern as the reference board. Then build the book with the chosen one.

### Color
- **Roles.** Exactly one `background` and one `text`, one `accent`, plus `surface`, `border` and `muted` as needed, plus `success`, `warning`, `danger` and `info` only if the product has states.
- **Usage %.** Give each role an honest share of a typical screen. Accent around 2–8%; status colors 0% (they appear only when needed). The book draws this as a proportion bar.
- **Neutrals and accent.** Tint the neutrals toward the brand; avoid pure #fff and #000. Derive the accent from the subject (see the slop catalog's color section).
- **Pairings.** List every intended text-on-background pairing in `pairings`. The build flags anything below AA.
- **Generated for you:** the book makes the 50–900 tint scale and the RGB/HSL values, so don't hand-write them.

### Typography
Follow `typography.md` (the signal ladder, then three traits, then a pairing).
- **Families:** set each family's `role` to `display`, `body` or `mono`, with a one-line `why` tied to the brief.
- **Scale:** 6–8 steps, with real sample copy from the product, not lorem ipsum.
- **Scripts:** add every non-Latin script the product uses, with its `dir` and line height.

### Icons
- **Library:** one of lucide, tabler or phosphor. The build fetches and inlines the SVGs.
- **Custom icons:** pass custom ones as `svg` that uses currentColor.
- **Pick the icons the product needs:** its actual nouns and verbs, typically 6–12.
- **Rules:** one stroke width, one size per context, always beside a label, no emoji.

### Imagery
- **Approach:** one sentence on what the photos and illustrations are *of* and why.
- **Do / don't:** each list names concrete subjects, e.g. "Photograph the actual team", "No stock handshake photos".

### Layout & spacing
- **Spacing:** a scale with real jumps, e.g. 4 8 12 16 24 32 48 72 112.
- **Radius:** pick one philosophy (sharp, soft or pill).
- **Elevation:** at most two levels.

### Components
These are rendered automatically from the tokens: buttons, input, card, table and status badges. Check that they look right. If they don't, the tokens are wrong; fix the tokens, not the components.

### Voice & tone
- **Principles:** 3 of them, each with a short explanation.
- **"We say":** real lines from the product.
- **"We don't say":** the slop versions it replaces (hype verbs, vague claims).

### Guardrails
List 4–6 brand-specific anti-slop rules: the defaults this brand would most likely drift back into.
