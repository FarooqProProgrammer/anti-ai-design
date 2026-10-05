# shadcn for every React and Vue project

**Rule:** any React or Vue project builds its UI on shadcn, and every UI component is added and maintained the way the shadcn docs prescribe.

| Stack | Library | Docs |
|---|---|---|
| React: Next.js, Vite, React Router, TanStack Start, Astro (React islands), Laravel + React | **shadcn/ui** | https://ui.shadcn.com/docs/installation |
| Vue: Vite + Vue, Nuxt, Astro (Vue islands), Laravel + Vue (Inertia) | **shadcn-vue** (the Vue port, built on Reka UI) | https://shadcn-vue.com/docs/installation |

shadcn copies component *source* into the project, so the team owns it. That makes it a good base for a distinctive design. But its **default theme** (neutral greys, default radius, Geist/Inter, stock dashboard blocks) is one of the most recognizable AI-app looks today. So the rule has two halves:
1. Use shadcn's components and conventions, exactly as documented.
2. **Always replace its default theme with the brand's tokens.**

## The official shadcn skills (React)

shadcn publishes agent skills. **In any shadcn/ui (React) project, the official `shadcn` skill must be installed and used** for everything component-related:
- adding, searching, docs lookup, updating, presets and registries;
- its Critical Rules: `FieldGroup`/`Field` forms, `gap-*` instead of `space-*`, semantic colors, `data-icon`, full `Card` composition, `Empty`/`Alert`/`Skeleton`/`Separator`/`Badge` instead of custom markup, and so on.

Install it once per project (it's already installed in this repo under `.claude/skills/shadcn` and `.claude/skills/migrate-radix-to-base`):
```bash
npx skills add shadcn/ui            # installs: shadcn, migrate-radix-to-base
npx skills update                   # keep them at the latest version
```

- **`shadcn`:** loads live project context via `npx shadcn@latest info --json` (framework, `base` radix/base, `style`, `iconLibrary`, `tailwindVersion`, `tailwindCssFile`, aliases, installed components). Invoke it whenever you touch shadcn components.
- **`migrate-radix-to-base`:** use only when the user asks to move a project from Radix UI to Base UI.
- **Vue:** the official skills cover shadcn/ui (React) only. For Vue, follow the shadcn-vue docs directly (`/websites/shadcn-vue` on Context7), applying the same principles.

**Division of labour.** The shadcn skill decides *how components are used correctly*. This skill decides *how the product looks and reads*: the brand theme, the composition, the anti-slop checks. Where the two overlap they agree: style through tokens and variants, not one-off overrides. Also follow the shadcn skill's process rules:
- never `--overwrite` without the user's approval;
- never guess a registry (ask);
- ask overwrite / partial / merge / skip before switching presets;
- after adding components, read the added files.

## Contents
1. Before you start: check the docs and the project
2. Setup (new and existing projects)
3. Adding and maintaining components
4. Theming with the brand (the anti-slop part)
5. Composition rules
6. Verify

---

## 1. Before you start: check the docs and the project

- **Read the current docs.** shadcn changes often (CLI v4, Tailwind v4, OKLCH theming, a choice of primitive libraries, project templates). Pull the installation page for the project's framework and the theming page before acting:
  - **Context7:** `/websites/ui_shadcn` (React) or `/websites/shadcn-vue` (Vue).
  - **Fallback:** WebFetch the docs URL.
  - Follow what the docs say *now*, even if it differs from this file.
- **Check the project:**
  - Is there a `components.json`? Then shadcn is already set up. Respect its `style`, `aliases` (`components`, `ui`, `lib`, `utils`, `hooks`), `iconLibrary`, `tailwind.css` path and `baseColor`.
  - Check `package.json` for versions (React, Vue, Tailwind, Next/Nuxt). Existing versions win; see the latest-versions rule in SKILL.md.
  - Look for an existing different UI kit (MUI, Chakra, Ant Design, Mantine, Vuetify, PrimeVue, Quasar, Element Plus…). **Don't add shadcn on top, or rip the other kit out, without asking.** Say so and let the user decide.
- **Use the project's package manager runner:** `npx`, `pnpm dlx`, `bunx` or `yarn dlx`, judged from the lockfile.

## 2. Setup

**React, new project:** scaffold with a template:
```bash
npx shadcn@latest init -t next        # or: vite | start | react-router | astro
```
For Laravel, create the app with `laravel new` first, then run `npx shadcn@latest init`. Use `--monorepo` for a monorepo.

**React, existing project:**
```bash
npx shadcn@latest init
```
Make sure Tailwind and the import alias (`@/*`) are configured as the framework's install guide says.

**Vue (Vite):** follow https://shadcn-vue.com/docs/installation/vite (Tailwind and path aliases first), then:
```bash
npx shadcn-vue@latest init
```

**Nuxt:**
```bash
npx nuxi@latest module add shadcn-nuxt
npx shadcn-vue@latest init
```
Follow the Nuxt install page for the module config.

Answer `init` prompts (style, base color, primitives) per the docs. The base color hardly matters, because section 4 replaces the theme anyway.

## 3. Adding and maintaining components

- **Always add components with the CLI.** Never hand-write a component that shadcn already provides.
  ```bash
  npx shadcn@latest add button card dialog sheet table tabs form input label
  npx shadcn-vue@latest add button card dialog sheet table          # Vue
  ```
- **Blocks** (`login-…`, `sidebar-…`, `dashboard-…`) are fine as a *structural* starting point via `add <block>`. Then restyle and recompose them (section 5). Never ship them looking stock.
- **Where files live:**
  - CLI-generated primitives stay in the `ui` alias folder (usually `components/ui/`).
  - The product's own components (`PricingTable`, `ShiftGapList`, `SiteHeader`) go in `components/` (or feature folders) and are **composed from** the `ui` primitives.
  - This split keeps `ui/` maintainable with the CLI.
- **Customize the right way:**
  1. **Theme tokens first** (section 4). Most of the "look" changes there, with zero component edits.
  2. **Then variants:** add a variant to the component's `cva` config (e.g. a `ledger` button variant) instead of passing piles of classes everywhere.
  3. **Edit `ui/*` source only when necessary.** Keep the edit small and leave a one-line comment saying why. Re-adding or updating a component overwrites it (the CLI asks before overwriting), so re-check edited files after any update.
- **Updating:** follow the shadcn skill's "Updating Components" flow: `add <component> --dry-run`, then `--diff <file>` per file, then merge, keeping local edits. **Never `--overwrite` without the user's explicit approval.** Read the shadcn changelog first if the CLI or the project is behind.
- **Docs for every component you touch:** run `npx shadcn@latest docs <component>` and fetch the URLs before creating, fixing or using a component.
- **Icons:** use the library set in `components.json` → `iconLibrary` (shadcn defaults to Lucide: `lucide-react` / `lucide-vue-next`). Align it with the brand's icon set. If the brand book uses Lucide, everything matches. Never mix in emoji or a second icon set.
- **Forms, data tables, charts, dark mode, toasts:** use the patterns the docs currently recommend for each. Look them up; they change. Examples: Chart (Recharts) using `--chart-1…5`, Data Table (TanStack Table), the dark-mode guide for the framework, and the current form/field components.
- **Mobile-first still applies:**
  - `Sidebar` collapses to a `Sheet` on mobile.
  - On phones, prefer `Drawer` (bottom sheet) over `Dialog` for forms and pickers (the "responsive dialog" pattern).
  - Wide `Table`s go in a horizontal scroll wrapper or become row cards.

## 4. Theming with the brand (the anti-slop part)

shadcn reads CSS variables:
- `--background`, `--foreground`, `--card`, `--popover`, `--primary`, `--secondary`, `--muted`, `--accent`, `--destructive`, `--border`, `--input`, `--ring`, `--chart-1…5`, `--sidebar-*`, and `--radius`, each with a `-foreground` pair where relevant;
- set in `:root` and `.dark`;
- mapped to Tailwind with `@theme inline` in the global CSS (`app/globals.css`, `src/index.css`, `assets/css/main.css`…).

**If a brand kit exists** (`brand/kit/`): use its **`shadcn-theme.css`**, generated by `brand_book.py kit`. It already maps brand.json into shadcn's variables (OKLCH), with a derived `.dark` block, the brand fonts and the status colors.

Following the official skill's rule, **edit the project's existing `tailwindCssFile`** (from `npx shadcn@latest info`). Don't import a new CSS file. In that file:
1. Keep shadcn's `@import "tailwindcss"`, its other imports, the `@custom-variant dark` line and the `@theme inline { --color-…: var(--…) }` block, as `init` created them.
2. **Replace** shadcn's `:root { … }` and `.dark { … }` blocks with the ones from `shadcn-theme.css`. Paste its extra `@theme inline` block (fonts and status colors) after shadcn's own.
3. Review the derived `.dark` values; dark mode is derived, not designed. Adjust them if the brand has a real dark palette.

**Presets** (`nova`, `vega`, `maia`, `lyra`, `mira`, `luma`, or preset codes) are stock looks. A preset is fine for picking the component *style* and base at `init`. But if a brand theme exists, the brand's variables and fonts must win:
- If the user applies a preset later, warn that `apply` overwrites theme and fonts.
- Re-apply the brand theme afterwards, or use `apply <code> --only …` deliberately.

**Without a kit,** set the variables by hand from the design decisions (Build step 2), never leaving the stock neutral values.

**Map meaning, not names:**
- shadcn's `--primary` is the main action color, so it gets the **brand accent**.
- shadcn's `--accent` is the subtle *hover/selected background* (menu items, ghost buttons), so it gets a **tinted surface**, not the brand accent.
- `--ring` gets the brand accent.
- `--radius` is set from the brand's radius philosophy. Sharp brands use a small value; don't keep `0.625rem` by habit.
- Fonts: set `--font-sans` (shadcn's base font) to the brand body face, and add `--font-heading` and `--font-mono`. Use `font-heading` on headings.
- Status colors: extra tokens (`--success`, `--warning`) follow the docs' pattern: define them in `:root`/`.dark` and expose them through `@theme inline` as `--color-success` etc.

## 5. Composition rules

shadcn gives you parts; the slop comes from assembling them by default. Apply `slop-catalog.md` to the composition:
- **Not everything is a `Card`.** Use cards for discrete objects only. Sections, lists and stats often read better as plain layout with rules or `Separator`s.
- **The stock dashboard** (`dashboard-…` block: 4 KPI cards with "+12.5%" badges, an area chart with gradient fill, a data table) is the admin-panel version of the 3-card hero. Lead with the user's real first question (see the slop catalog's dashboard entry).
- **`Badge`s are for status, not decoration,** and always paired with a word.
- **Buttons:** one `default` (primary) action per view. Secondary actions use `outline`, `ghost` or `link` variants.
- **No glass, glow or gradient additions** on top of shadcn components.

## 6. Verify

- Run the project's typecheck, lint and build (`tsc --noEmit`, `npm run lint`, `npm run build`, or the Nuxt/Vite equivalents) after adding or changing components.
- Run `slop_scan.py` on `components/` and the pages, ignoring CLI-generated `ui/` internals unless you edited them.
- Check at 390px and at desktop width (see `responsive.md`), in light **and** dark mode if dark mode is enabled.
- In the handover, list the shadcn components added, any `ui/` files edited and why, and the shadcn and shadcn-vue CLI versions used.
