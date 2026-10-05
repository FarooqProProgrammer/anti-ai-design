# Choosing Fonts From the Input

Type sets the voice of a page more than anything else. Slop typography comes from picking a font *before* reading the brief. Here the order is reversed: read the input, pull out the signals, and let them pick the fonts.

## Contents
1. Read the input: the signal ladder
2. From signals to type traits
3. Starting points by context
4. Scripts and languages
5. Pairing rules
6. Reflex picks to avoid
7. Verify, then implement

---

## 1. Read the input: the signal ladder

Go down this list. A higher signal overrides the ones below it.

1. **Explicit fonts or a design system** (brand guide, Figma tokens, `tailwind.config`, existing CSS). Use them. If a brand font can't be loaded on the web (licensed, desktop-only), pick the closest web-available match by classification and proportions, and tell the user which font stands in for which.
2. **Existing codebase** (not a redesign). Keep its fonts. If you change them, say why.
3. **Reference images or URLs** ("make it look like this"). Name the *characteristics*, not the font: serif or sans; geometric, humanist, grotesk or slab; high or low stroke contrast; x-height; width (condensed or wide); weight range; case usage. Then match those characteristics. If the reference clearly uses a known face, a close free alternative is fine.
4. **Languages and scripts in the content.** This is a hard constraint, not a preference (see §4). A beautiful Latin font that falls back to the system font for Urdu or Japanese text breaks the design.
5. **Subject, audience and context of use.** Who reads this, where, and in what state of mind: a ward manager at 7am on a hospital PC, a teenager on a phone, a lawyer reading a long brief.
6. **Content shape.**
   - Long-form reading needs a comfortable text face.
   - Data-dense UI needs compact type with tabular figures and clear 1/l/I and 0/O.
   - Short marketing copy can use a display face with strong character.

## 2. From signals to type traits

Turn the signals into **three traits**, then map each trait to a type quality.

| Trait | Type qualities that express it |
|---|---|
| Trustworthy, established | Transitional or old-style serifs; restrained sans; moderate contrast |
| Precise, technical | Grotesk or neo-grotesk; mono for data; tight spacing; tabular figures |
| Warm, human, approachable | Humanist sans (open apertures); soft serifs; rounded terminals in moderation |
| Calm, clinical, legible | High-x-height sans built for legibility; generous spacing; few weights |
| Editorial, thoughtful | Text serifs with good italics; strong headline serif; real hierarchy |
| Luxurious, refined | High-contrast Didone or display serif; light weights; wide tracking on caps |
| Energetic, loud | Condensed or extended heavy sans; big sizes; tight leading |
| Playful, young | Rounded or quirky sans; bouncy display faces; chunky weights |
| Crafted, local, artisanal | Characterful serifs or slabs; slight irregularity; warm display faces |
| Raw, experimental | Mono, brutalist grotesks, unusual widths; break the rules on purpose |

For example, the tax firm for freelancers is *trustworthy + precise + local*. That suggests a sober serif or grotesk for display, a legible sans for body, tabular figures for the money, and Urdu support if the page has Urdu text.

## 3. Starting points by context

These are **starting points to adapt, not presets**. Everything listed here is on Google Fonts unless marked otherwise. Pick based on the traits, and vary between projects.

| Context | Display options | Body / UI options | Notes |
|---|---|---|---|
| Finance, legal, accounting | Source Serif 4, Newsreader, Libre Caslon Display, Schibsted Grotesk | Source Sans 3, Public Sans, Libre Franklin | Turn on tabular figures; avoid playful faces |
| Healthcare, clinical, public-service UI | Public Sans, Barlow Semi Condensed | Atkinson Hyperlegible, Public Sans, Lexend | Legibility first; large x-height; condensed only for dense labels |
| Developer tools, infra, data | Geist, Schibsted Grotesk, Martian Mono | Geist, Hanken Grotesk | Mono: Geist Mono, JetBrains Mono, Martian Mono |
| Editorial, media, long reads | Newsreader, DM Serif Display, Gloock, Playfair Display (sparingly) | Literata, Source Serif 4, Newsreader | Serif body is fine on screen at 18px+ |
| Luxury, fashion, beauty | Bodoni Moda, Cormorant Garamond, Italiana, Marcellus | Jost, Manrope | Light weights, tracked uppercase, lots of space |
| Food, hospitality, craft | Young Serif, Gloock, Caprasimo, Bricolage Grotesque | Work Sans, Figtree | Warmth; display can be quirky, body stays plain |
| Kids, education, learning | Fredoka, Baloo 2, Sniglet | Lexend, Nunito, Andika | Lexend and Andika are designed for reading ease |
| Sports, events, energy | Anton, Big Shoulders Display, Archivo (wide/condensed), Bebas Neue | Archivo, Barlow | Huge, condensed, uppercase works here |
| Government, civic, nonprofit | Public Sans, Source Serif 4 | Public Sans, Source Sans 3 | Plain and accessible beats clever |
| Creative studio, portfolio | Syne, Unbounded, Familjen Grotesk, Instrument Serif | Inter Tight, Hanken Grotesk | Licence to be weird; keep body sane |
| Consumer SaaS, startups | Bricolage Grotesque, Schibsted Grotesk, Onest, Plus Jakarta Sans | Figtree, Onest, Manrope | The category most at risk of slop; let the product's personality pick |
| Retro, brutalist, zine | Space Mono, Archivo Black, Rubik Mono One, VT323 | Space Grotesk, IBM Plex Mono | Commit fully or don't do it |

A single **superfamily** (Source, IBM Plex, Roboto Serif + Flex, Noto) is a valid choice when consistency matters more than contrast, such as dense apps or multi-script products.

## 4. Scripts and languages

If the content includes non-Latin text (headings, labels, names, a language toggle), choose fonts that **cover every script used**. Then tune the metrics, because scripts differ in height and line spacing.

| Script | Options | Notes |
|---|---|---|
| Urdu (Nastaliq) | Noto Nastaliq Urdu, Gulzar | Very tall; line-height about 2–2.2; never force it into tight Latin leading |
| Arabic, Persian (Naskh) | Noto Naskh Arabic, IBM Plex Sans Arabic, Cairo, Tajawal, Readex Pro | Use `dir="rtl"` and logical CSS properties (`margin-inline-start`) |
| Devanagari (Hindi, Marathi) | Mukta, Hind, Tiro Devanagari Hindi, Noto Sans Devanagari | Match the x-height to the Latin pair |
| Bengali | Hind Siliguri, Noto Sans Bengali, Tiro Bangla | |
| Chinese, Japanese, Korean | Noto Sans/Serif SC/TC/JP/KR, Zen Kaku Gothic, IBM Plex Sans KR | Large files; use subsets or the `text=` parameter; no faux italics |
| Cyrillic, Greek, Vietnamese | Check coverage. Good options: Manrope, Onest, PT Serif, Literata, Source families, Fira Sans | Many display faces lack these; test real strings |

Pair the non-Latin face with a Latin face of similar weight and color, and assign it per language with `:lang()`:

```css
:lang(ur) { font-family: "Noto Nastaliq Urdu", serif; line-height: 2.1; }
```

## 5. Pairing rules

- **Contrast the classification, keep the proportions similar.** A serif display with a sans body is classic. Two similar sans faces look like a mistake.
- **One family is often enough** when the type scale and weights carry the hierarchy.
- **Use at most two families, plus a mono if the page shows data or code.** Use 4–5 weights in total. Variable fonts count as one file.
- The **display face** carries the personality, so it can be strange. The **body face** carries the reading, so it should be invisible.
- **Check the italics and figures before committing.** Some display serifs have weak italics, and many sans faces have proportional-only figures.

## 6. Reflex picks to avoid

Any of these is fine for a *reason*. Picked by reflex, they are slop:

- **Classic defaults:** Inter, Roboto, Open Sans, Poppins, Montserrat or Lato as the only face.
- **The "tasteful AI" defaults:** Space Grotesk, Instrument Serif, Fraunces, DM Sans, IBM Plex everywhere, Playfair Display on every hero. These are what models reach for once told to avoid Inter, which makes them the new uniform.
- **Repeating yourself:** if you used a pairing earlier in the session for a different product, choose differently unless the brand calls for it.

A quick test: could you explain the font choice in one sentence that mentions the user's subject? ("Atkinson Hyperlegible because ward PCs are low-res and read at a glance.") If the sentence would work for any product, the choice isn't grounded yet.

## 7. Verify, then implement

Check each of these before writing components:

- [ ] Every script and character in the content renders in the chosen face. Test real strings: names, currency (₨ Rs $ €), diacritics.
- [ ] Every weight and style you use is loaded, and nothing more.
- [ ] Numbers in tables and KPIs use `font-variant-numeric: tabular-nums`.
- [ ] Body text is readable at 16px on a phone: adequate x-height, not too light.
- [ ] The fallback stack is similar in metrics. Use `size-adjust` on a fallback `@font-face` if layout shift matters.

Implementation pattern (adapt to the project's stack):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Public+Sans:wght@400;500;700&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: "Source Serif 4", Georgia, serif;
  --font-body: "Public Sans", system-ui, sans-serif;
  --font-mono: ui-monospace, "SFMono-Regular", Menlo, monospace;
}
h1, h2, h3 { font-family: var(--font-display); text-wrap: balance; }
body { font-family: var(--font-body); }
```

Tell the user the choice in one line, with the reason tied to their input, so they can redirect. For example: "Type: Source Serif 4 + Public Sans: reads like a trustworthy firm, with tabular figures for the fee table."
