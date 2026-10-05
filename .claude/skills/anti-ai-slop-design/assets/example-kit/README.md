# Khata Tax Advisory - brand kit

Generated from `brand.json` by `brand_book.py kit`. The brand book (`book.html`) documents the rules;
this folder is what you ship.

## Files
| Path | Use |
|---|---|
| `tokens.css` | CSS custom properties: colors, fonts, spacing, radius, shadows, type sizes. Load first. |
| `tokens.json` | Same tokens as data (for JS, Figma Tokens, native apps). |
| `components.css` | Buttons, fields, card, band, table, badges, icon & logo sizing - built on the tokens. |
| `tailwind.theme.css` | **Tailwind CSS v4** (current) `@theme` - `bg-accent`, `font-display`, `text-h1`, `rounded-md`, `shadow-raised`... |
| `tailwind.preset.js` | Legacy: Tailwind v3 preset, only for projects still on v3. |
| `shadcn-theme.css` | **React/Vue projects (shadcn/ui, shadcn-vue):** the brand as shadcn CSS variables (OKLCH, light + derived dark, fonts, status colors). Paste into the project's `tailwindCssFile`, replacing shadcn's `:root`/`.dark`. |
| `fonts.html` | `<link>` tags for the brand fonts. |
| `logo/*.svg` | `mark.svg`, `wordmark.svg` use `currentColor` (inline them and set `color`). `*-ink`, `*-reversed`, `*-accent` have colors baked in (for `<img>`, email, docs). |
| `favicon.svg` | Mark on an accent tile. Link with `<link rel="icon" href="/favicon.svg" type="image/svg+xml">`. PNG sizes not generated (install `cairosvg`, or export favicon.svg at 32/180/512px). |
| `icons/*.svg`, `icons/sprite.svg` | The brand's icon set (lucide); sprite symbols are `#i-<name>`. |
| `demo.html` | A small page using everything above - open it to check the kit works. |

## Plain HTML
```html
<!-- in <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:wght@400;600&family=Public+Sans:wght@400;600&family=JetBrains+Mono:wght@400;500&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap">
<link rel="stylesheet" href="brand/tokens.css">
<link rel="stylesheet" href="brand/components.css">
<link rel="icon" href="brand/favicon.svg" type="image/svg+xml">

<!-- logo (inline SVG so it follows color) -->
<a href="/" class="logo" aria-label="Khata Tax Advisory"><!-- paste logo/wordmark.svg here --></a>

<!-- icon from the sprite -->
<svg class="icon" aria-hidden="true"><use href="brand/icons/sprite.svg#i-receipt"></use></svg>

<button class="btn btn-primary">Primary action</button>
```

## React / Vue with shadcn (default for React and Vue projects)
1. Set up shadcn per its docs (`npx shadcn@latest init`, or `npx shadcn-vue@latest init` for Vue/Nuxt).
   For React, install the official agent skills: `npx skills add shadcn/ui`.
2. Open the project's global CSS (`tailwindCssFile` from `npx shadcn@latest info`), replace shadcn's
   `:root` and `.dark` blocks with those in `shadcn-theme.css`, and paste its `@theme inline` block after shadcn's.
3. Add components only with the CLI (`npx shadcn@latest add button card ...`); use `font-heading` on headings.
4. Logo, favicon and icons: as below (match `iconLibrary` in components.json to the brand's icon set).

## React / Next.js without shadcn (plain CSS)
```jsx
// app/layout.jsx (or main.jsx): import once
import "@/brand/tokens.css";
import "@/brand/components.css";

// Icon.jsx
export const Icon = ({ name, ...p }) => (
  <svg className="icon" aria-hidden="true" {...p}><use href={`/brand/icons/sprite.svg#i-${name}`} /></svg>
);
// Put sprite.svg and favicon.svg in /public/brand/. For the logo, import the SVG with SVGR
// (`import Logo from "@/brand/logo/wordmark.svg"`) or paste it into a component - keep fill="currentColor".
```

## Tailwind CSS v4 (current)
```css
/* app.css - CSS-first config, no tailwind.config.js needed */
@import "tailwindcss";
@import "./brand/tailwind.theme.css";
@import "./brand/tokens.css";      /* spacing tokens + vars used by components.css */
@import "./brand/components.css";  /* optional */
```
Then: `bg-bg text-text`, `bg-accent text-on-accent`, `border-border`, `font-display`, `text-h1`, `rounded-md`, `shadow-raised`.

Legacy Tailwind v3 only: `module.exports = { presets: [require("./brand/tailwind.preset.js")] }` + import `tokens.css`.

## Versions
Built against the latest stable releases at export time: `lucide-static@1.52.0`. Check for newer versions
before starting a new project (`npm view <package> version`); in an existing project, keep the
versions it already uses unless you decide to upgrade.

## Rules that the files can't enforce
See `book.html`: one accent, tabular figures for money, icons always beside labels, no emoji,
voice "we say / we don't say", and the guardrails section.
