# Slop Catalog

Each tell: what it looks like → why it reads as AI-generated → what to do instead.
None of these are banned. They become slop when they appear *by default* and in *combination*. If a choice is intentional and grounded in the subject, keep it and be able to say why.

## Contents
1. Color
2. Typography
3. Layout & composition
4. Components
5. Depth, effects & motion
6. Icons & imagery
7. Copy & content
8. Responsive & mobile
9. The combination check

---

## 1. Color

**Indigo/violet/purple → blue/pink gradients** (`#6366f1`, `#8b5cf6`, `#a855f7`, `from-indigo-500 to-purple-600`)
→ The single most recognizable AI-UI signature; it's the Tailwind-demo palette.
→ Derive the accent from the subject (a bakery → warm crust brown or a jam red; a legal tool → ink and a muted oxblood). One accent, used for action and emphasis only.

**Gradient text on headlines** (`bg-clip-text text-transparent`)
→ Decorates instead of communicating; nearly every AI hero does it.
→ Make the headline strong through size, weight, typeface and contrast. If emphasis is needed, a single word in the accent color, italic, or underline treatment.

**Dark navy/black background with neon accents for no reason**
→ "Tech = dark mode + glow" shorthand.
→ Choose light/dark based on context of use. If dark, use tinted darks (warm or cool) and restrained accents.

**Pure #ffffff with gray-500 text everywhere**
→ No temperature, no brand; low-contrast gray body copy also hurts readability.
→ Tint neutrals slightly (paper, stone, bone, slate). Body text should be near-black, not mid-gray.

**Rainbow of accent colors** (each feature card a different color)
→ Feels like a template trying to be "fun".
→ One accent plus neutrals; add a second only with a job (e.g. status colors in a dashboard).

## 2. Typography

(For *choosing* fonts from the brief — signal ladder, context table, script coverage, pairing rules — see `typography.md`.)

**Inter / system-ui everywhere, one weight jump** (bold heading, regular body, same family)
→ The default of defaults.
→ Pick a pairing with character for the subject: an editorial serif, a grotesk with quirks, a mono for technical data, a condensed face for density. Inter is fine as a body face if the display face carries personality.

**Timid scale** (h1 at 48px, h2 at 36px, h3 at 24px, all bold, all centered)
→ No hierarchy drama; everything feels equally (un)important.
→ Use a real scale with big contrasts: a very large display size, tight leading (1.0–1.1) and slightly negative tracking on headlines, a calm body at 16–18px with 1.5–1.7 leading.

**Everything centered**
→ Centered multi-line text is hard to read and is the default hero pattern.
→ Left-align most text. Center only short, deliberate moments.

**ALL-CAPS eyebrow label above every section** ("FEATURES", "PRICING", "TESTIMONIALS")
→ Repeated mechanically, it's filler.
→ Use it once if it helps orientation, or replace with section numbers, a running margin note, or nothing.

## 3. Layout & composition

**The canonical slop page**: nav → centered hero (badge pill + gradient headline + subtext + two buttons) → logo strip → 3 feature cards → alternating image/text rows → testimonial cards → 3-tier pricing with "Most popular" → FAQ accordion → gradient CTA band → 4-column footer.
→ Every section the same rhythm and width; reads like a template because it is one.
→ Ask what this product's content actually is and give it the form it needs: a hero that *shows* the product or the outcome, a table, a single big number, a timeline, a long-form argument, a real photo. Cut sections that only exist because "landing pages have them".

**Three equal cards in a row** (icon, title, two lines of text)
→ The most generated component on the internet.
→ Vary weight: one large primary point + smaller supporting ones, a numbered list, a comparison table, prose with inline emphasis, or a diagram.

**Uniform spacing everywhere** (`py-20` on every section, `gap-8` on every grid)
→ No grouping, no rhythm — the eye can't find structure.
→ Tight within groups, generous between them; vary section heights; let some elements touch edges or break the grid.

**Badge pill above the hero** ("✨ New: AI-powered insights →")
→ Instant tell.
→ Only if there's a real announcement; style it as part of the system, not a glowing pill.

**Bento grid used decoratively**
→ Trendy filler when the content doesn't have bento-shaped relationships.
→ Use a bento only when tiles genuinely differ in importance and type.

## 4. Components

**Buttons**: two side-by-side ("Get Started" gradient + "Learn More" ghost), `rounded-full`, glow shadow.
→ Default pair, default labels.
→ One primary action with a specific label ("Book a tax review", "Start a 14-day trial"). Secondary as a text link if needed.

**Cards with `rounded-2xl border shadow-xl` on everything**
→ Every surface is a floating card; nothing is the background.
→ Most content doesn't need a card. Use dividers, whitespace, or background bands. Reserve cards for genuinely discrete objects.

**Pricing with "Most Popular" scaled-up middle card and checkmark lists**
→ Fine pattern, but generated verbatim it's a tell.
→ Match the actual pricing model (one price? usage-based? a table for comparing many features?).

**Testimonial cards with circular avatar, 5 stars, "Sarah J., CEO at TechCorp"**
→ Fake-looking by construction.
→ Real quotes with specifics; pull a single strong quote large; or skip testimonials.

**Dashboard: 4 KPI cards on top with "+12.5%" green pills, area chart with gradient fill, recent-activity table**
→ The generated-admin-panel layout regardless of what's being monitored.
→ Lead with the one number or list this user checks first; show comparison/context; use density appropriate to experts (tables, sparklines) rather than giant cards.

## 5. Depth, effects & motion

**Glassmorphism** (`backdrop-blur`, translucent white cards over blurred blobs)
→ Decorative depth with no meaning; also hurts contrast.
→ Pick one depth model: flat with borders, or soft single shadow, or solid color planes.

**Blurred gradient blobs / orbs in the background** (`absolute blur-3xl bg-purple-500/30`)
→ The background equivalent of the purple gradient.
→ Use texture or imagery with meaning (paper grain, a photograph, a grid that relates to the product), or nothing.

**Glow shadows** (`shadow-[0_0_40px_rgba(139,92,246,0.5)]`), gradient borders
→ Sci-fi garnish.
→ Remove; use contrast and spacing to draw attention.

**`hover:scale-105` + `transition-all` on everything; fade-up on every section; pulse/bounce on decoration**
→ Motion without purpose; feels cheap and slows the page.
→ Animate only state changes and feedback (hover color shift, focus, opening a panel). Keep durations short (150–250ms) and respect `prefers-reduced-motion`.

## 6. Icons & imagery

**Emoji as icons** (🚀 ⚡ 🔒 ✨ 📊 in feature cards, headings, buttons)
→ The cheapest possible icon decision; very common in AI output.
→ A single consistent icon set (e.g. Lucide/Phosphor stroke icons at one size/weight), or no icons — most feature points read better without them.

**Icon in a rounded gradient square** above each card title
→ Template filler.
→ Inline icon at text size, or a number, or nothing.

**Abstract 3D shapes / generic dashboard mockup / stock "team high-fiving" photos**
→ Says nothing about this product.
→ Show the real product, real output, the real place or people, or a purposeful illustration style.

## 7. Copy & content

**Hype verbs**: Unlock, Supercharge, Elevate, Empower, Revolutionize, Transform, Streamline, Unleash, Harness, Seamless(ly), Effortless(ly), Cutting-edge, Next-level, Game-changer, "Built for the future", "Take X to the next level", "All-in-one platform", "Your journey starts here".
→ Content-free; screams generated.
→ Say what it does for whom, concretely: "File your freelancer taxes in Pakistan without a spreadsheet" beats "Supercharge your financial journey".

**Triplets everywhere** ("Fast. Secure. Reliable.")
→ Rhythmic filler.
→ One specific claim with a proof point.

**Placeholder data**: John Doe, Jane Smith, Acme Inc, Lorem ipsum, $99/mo, 10,000+ happy customers, 99.9% uptime, round fake numbers.
→ Signals nobody imagined real usage.
→ Domain-plausible names, irregular realistic numbers, real feature names. If data is unknown, mark it clearly as placeholder for the user rather than inventing social proof.

**Headings that are labels** ("Features", "Why Choose Us", "How It Works")
→ Generic structure leaking into copy.
→ Headings that make a claim or answer a question.

## 8. Responsive & mobile

(Full method: `responsive.md`.)

**Desktop-first squeeze** (`max-width` media queries overriding a desktop layout; fixed `width: 1200px`)
→ The phone gets leftovers: one endless column with no priorities.
→ Write base styles for 360px and enhance with `min-width`. Decide the phone order first.

**Three cards → three stacked cards → scroll forever**
→ Cards were the desktop default; on a phone they become a wall.
→ Use a numbered list, a peeking horizontal scroller, or keep only the strongest point and link the rest.

**Hamburger hiding everything, including the main CTA**
→ The user can't see what to do next.
→ Keep the primary action visible (in the header or a sticky bottom bar). The menu holds only secondary links.

**Giant fixed hero padding / `100vh` hero on mobile**
→ The first phone screen shows a headline and nothing else; `vh` jumps as the browser bars move.
→ Use `clamp()` padding and `min-height: 100svh` only if really needed. The CTA must be visible without scrolling.

**Squashed or overflowing data tables**
→ Unreadable at 360px, or the whole page scrolls sideways.
→ Use a scroll wrapper with a sticky first column, or one card per row on small screens.

**Hover-only interactions** (menus, tooltips, reveal-on-hover cards)
→ Don't exist on touch screens.
→ Every hover needs a tap or focus equivalent. Gate hover-only polish with `@media (hover: hover)`.

**Tiny tap targets and 12–14px body text on mobile**
→ Hard to read and hard to tap.
→ Body text 16–18px, targets of 44px or more.

## 9. The combination check

Count how many of these appear together:
purple/indigo gradient · gradient text · Inter-only · centered hero with badge pill · 3 icon cards · emoji icons · glass/blur · glow · blobs · hype copy · placeholder names · uniform section padding · desktop-first layout.

- 0–2: likely fine, check they're intentional.
- 3–5: reads as template; fix the highest-visibility ones (hero, palette, type).
- 6+: it's slop; needs a point of view, not patching.

And always the **swap test**: replace the product name with an unrelated product. If nothing else needs to change, the design isn't about anything yet.
