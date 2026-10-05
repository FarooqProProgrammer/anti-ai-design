# Responsive, Mobile-First

Most people will meet this UI on a phone. In markets like Pakistan, India and much of Africa and Southeast Asia, that often means a mid-range Android on a slow connection. So design **for the phone first**, then let the layout *expand* for larger screens. Never start at desktop and squeeze.

Slop is often a desktop layout that collapses into one endless column: a giant centered hero, three cards stacked forever, a hamburger hiding the only CTA, and a table you can't read. Mobile-first fixes that by forcing priorities. A phone screen has room for one thing at a time, so you have to decide what that thing is.

## Contents
1. Design order
2. CSS: write mobile-first
3. Layout patterns that adapt well
4. Touch, input and the thumb zone
5. Type, images and performance
6. Content-specific patterns (tables, nav, forms, dashboards)
7. Test before handing over

---

## 1. Design order

1. **Design the 360–390px layout first.** Decide what comes first on a phone: the one claim, the one action, the one number a manager checks. That order *is* the hierarchy.
2. **Then ask what more room lets you add or rearrange:** side-by-side columns, a visible nav, a secondary panel, bigger imagery.
3. **Add breakpoints where the content breaks,** not at device names. Common landing points are about 600px, 900px and 1200px, but let the design decide.

In the design point of view, state the primary device and context, e.g. "phone, one-handed, on mobile data".

## 2. CSS: write mobile-first

- **Base styles are the mobile styles.** Enhance with `@media (min-width: …)`. Avoid `max-width` media queries for layout; they mean you designed desktop first.
- **The viewport meta is required:** `<meta name="viewport" content="width=device-width, initial-scale=1">`. Never disable zoom.
- **Use fluid values instead of breakpoint jumps:**
  - Type: `font-size: clamp(2rem, 1.2rem + 4vw, 4.5rem)`.
  - Spacing: `padding-block: clamp(48px, 8vw, 112px)`.
  - Widths: `width: min(100% - 32px, 1200px)` for containers.
- **Use grids that adapt by themselves:** `grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr))`.
- **Container queries** (`@container`) suit components that live in different-width slots (cards, sidebars).
- **Avoid fixed widths and heights:**
  - Fixed widths: no `width: 1200px` or `height: 600px` on sections; use `max-width`/`min-height`.
  - Fixed viewport heights: use `min-height: 100svh`, not `100vh`, because mobile browser bars break `vh`.
- **No horizontal page scroll, ever.** Check it at 360px. Long words, URLs and code need `overflow-wrap: anywhere`. Wide tables scroll inside their own wrapper.
- **Respect the notch and home bar:** `padding: env(safe-area-inset-*)` on fixed bars.
- **Use logical properties** (`margin-inline`, `padding-block`) so RTL scripts (Urdu, Arabic) work without rewrites.

```css
/* mobile-first skeleton */
.wrap { width: min(100% - 32px, 1200px); margin-inline: auto; }
.hero { display: grid; gap: 24px; padding-block: clamp(40px, 8vw, 112px); }
@media (min-width: 900px) { .hero { grid-template-columns: 1.2fr 1fr; align-items: center; } }
```

## 3. Layout patterns that adapt well

- **Reorder, don't just stack.** On a phone, put the primary content and action first, even if desktop shows an image on the left. Change visual order only with `order` or grid areas when DOM order still makes sense for screen readers.
- **Left-align on mobile.** Centered multi-line text is even harder to read on a narrow screen.
- **Collapse with intent:**
  - three feature cards become a numbered list or a swipeable row with a visible peek of the next item;
  - a side panel becomes a section below;
  - a comparison table becomes per-plan cards, or a sticky first column.
- **Keep generous section spacing on desktop, but tighten it on mobile.** Giant fixed padding wastes the first screen.
- **The first screen on a phone must show what this is and the main action** without scrolling.

## 4. Touch, input and the thumb zone

- **Touch targets at least 44×44px,** with at least 8px between neighbours. Links inside text can be smaller if the line height is generous.
- **Put primary actions where thumbs reach:** the full-width button at the end of content, or a sticky bottom action bar for key flows (checkout, booking, "WhatsApp us"). Keep the nav light at the top.
- **Never rely on hover:** no hover-only menus, tooltips or reveals. Every hover effect needs a tap or focus equivalent. `@media (hover: hover)` gates hover-only polish.
- **Inputs:**
  - Use the right `type` and `inputmode` (`tel`, `email`, `numeric`, `decimal`) and `autocomplete` attributes.
  - Set input font-size to 16px or more so iOS doesn't zoom on focus.
  - Keep labels visible; placeholders are not labels.
- **Gestures are an enhancement, never the only way** to do something.

## 5. Type, images and performance

- **Body text at least 16px on mobile** (17–18px is often better), line-height 1.5–1.7, measure around 60–75ch on desktop. Scale display sizes with `clamp()` so headlines don't overflow at 360px.
- **Images:**
  - Use `srcset`/`sizes` or `<picture>`, plus `loading="lazy"` below the fold and explicit `width`/`height` to prevent layout shift.
  - Use art direction with `<picture>`: a tighter crop on mobile instead of a tiny wide shot.
- **Keep the page light on mobile data:**
  - Fonts: at most 2 families and the weights you use; `display=swap`; preconnect.
  - Scripts: no heavy JS for decoration.
  - Hero media: no autoplay background video on mobile.
- **Motion:** respect `prefers-reduced-motion`, and keep animations off the critical path.

## 6. Content-specific patterns

| Content | Mobile-first approach |
|---|---|
| **Navigation** | 3–5 key links can sit visible or scroll horizontally. A menu button is fine for more, but **never hide the primary CTA** inside it. Label the menu button ("Menu"), not just ☰. |
| **Data tables** | Put the table in its own `overflow-x:auto` wrapper with a sticky first column, or turn each row into a card on small screens. Use tabular figures and right-aligned numbers. |
| **Dashboards** | Lead with the one status a user checks ("2 RNs short tonight"), then lists. KPI tiles go 2-up, not 4 squashed. Charts get a simplified mobile version or a number plus sparkline. |
| **Pricing** | Use one plan card per row with the recommended plan first, or a segmented toggle between plans. Comparison tables get a sticky plan header. |
| **Forms** | Single column, with labels above fields. Keep them short, ask only what's needed, use the correct keyboards, and put a full-width submit button at the end. |
| **Hero** | Headline that fits in about 3 lines at 360px, one sentence, one action. The image goes below or is cropped tighter, never a desktop-only background image. |
| **Modals** | On mobile, use full-screen sheets or bottom sheets with a visible close button. |

## 7. Test before handing over

- **Check the widths:** 360, 390, 768, 1024 and 1440px. With a browser tool, take screenshots at 390px and at desktop width and look at them. Without one, at least reason through each breakpoint in the CSS.
- **Check for these failures:**
  - horizontal scroll;
  - text overflowing its container;
  - tap targets under 44px;
  - CTA below the first screen on a phone;
  - unreadable tables;
  - hover-only functionality;
  - `100vh` jumps;
  - layout shift from images without dimensions.
- **Run the scanner.** It flags desktop-first `max-width` queries, a missing viewport meta, fixed pixel widths, `100vh` and disabled zoom.
