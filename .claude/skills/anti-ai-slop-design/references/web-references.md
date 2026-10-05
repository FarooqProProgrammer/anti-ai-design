# Reference Hunt: find, analyze, rank, let the user pick

Good design starts from looking at real work. This step collects visual references from the web, analyzes each one *visually*, scores it against the user's requirements, and has the user choose a direction before anything is built. Two things come out of it: a direction the user has agreed to, and a digest of concrete design moves to borrow, so the build is anchored in something real rather than in model defaults.

## Contents
1. When to run it
2. Write the brief (what you rank against)
3. Search
4. See the images
5. Define the modules, then analyze each reference against them
6. Score and rank
7. Build the reference board
8. Present and ask the user to pick, module by module
9. Turn the picks into a reference digest

---

## 1. When to run it

- **Run it:** the user asks for references, inspiration or a moodboard; or the work is a full page, site or app, the brief is open, and the user hasn't given any references or a design system.
- **Offer it in one line** (don't force it) when building a full page from a thin brief. For example: "Want me to pull 5–6 visual references and let you pick a direction first?"
- **Skip it:** the user supplied references, a brand guide or a design system; the task is a small component or a quick fix; or the user wants speed.

## 2. Write the brief (what you rank against)

Pull this from the user's input before searching. Ask only for what's missing *and* would change the ranking.

```
Subject:        what it is (e.g. tax consultancy for freelancers in Lahore)
Audience:       who, in what situation, on what device (default: phone first)
Traits (3):     e.g. trustworthy, precise, local
Content shape:  long reading / dense data / short marketing / app UI
Must-haves:     e.g. pricing table, WhatsApp CTA, Urdu labels, dark mode
Constraints:    stack, scripts or languages, accessibility, brand colors or fonts
Avoid:          anything the user dislikes, plus the slop tells
```

## 3. Search

Use whatever tools are available, in this order of preference. Do the Step 0 MCP check in `design-sources.md` first.

0. **The user's own Figma file**, if they gave one and Figma is connected. It's the anchor, so hunt only for what it doesn't cover.
1. **Mobbin via MCP**, if connected. Pre-check it for every hunt, not only when the user names it. Use `search_screens`, `search_sections` and `search_flows`. These are real shipped products with screenshots, which makes them the best source for app UI, sections and flows. Follow the Mobbin rules in `design-sources.md` §3: cite `mobbin_url`, show any `ai_usage_notice` word for word, download `image_url` for the board.
2. **Web search** for curated galleries of real sites. Useful sources:
   - Sites: godly.website, siteinspire.com, land-book.com, lapa.ninja, minimal.gallery, httpster.net, awwwards.com, onepagelove.com, saaslandingpage.com
   - App UI: mobbin.com, pageflows.com, screenlane
   - Typography: fontsinuse.com, typewolf.com
   - Brand identity: brandnew (underconsidered.com), behance.net (shipped case studies)
   - Also: real companies in the user's domain, or in an adjacent domain with the right *traits*. A tax firm can learn from a well-designed bank, or from a serious newspaper.
3. **A browser tool**, if available, to open pages and take screenshots directly.

Query ideas built from the brief:
- `"<domain> website design" site:land-book.com`
- `best <domain> landing pages 2026`
- `<trait> <trait> web design typography`
- `fontsinuse <domain>`
- `<competitor or admired brand> website`

Gather **8–15 candidates** across **at least 3 different directions**, for example editorial, data-forward and photographic. A shortlist of five near-identical pages gives the user no real choice.

**Be careful with Dribbble.** Many shots are concept art: unbuildable, unrealistic content, and often slop themselves (glass, gradients, fake dashboards). Prefer shipped products. If you do use a concept shot, label it as a concept.

## 4. See the images

Rank on what the reference **looks like**, not on its title or description. To get the actual pixels:

- **Mobbin and similar MCPs** return screenshots or image URLs directly.
- **Preview images:** run `python <skill>/scripts/ref_board.py fetch <page-url> <outdir>`. This saves the page's og:image or twitter:image, which is usually a hero screenshot. Then open the saved file with the Read tool to look at it.
- **Direct image URLs** from search results: download them with the same script (`fetch` accepts image URLs too).
- **A browser tool:** navigate to the page and take a screenshot.

Save everything under the session scratchpad, e.g. `<scratchpad>/refs/`.

If you can't get an image for a candidate, either drop it or mark it **"not seen — ranked on description only"**. Never present a confident visual analysis of something you didn't look at.

## 5. Define the modules, then analyze each reference against them

Users rarely want one reference wholesale. They want *this* site's hero, *that* site's type. So before analyzing, list the **modules** the user will choose for. Take them from the brief and the content shape, keeping it to 4–7.

- **Design dimensions** (almost always): Typography, Color, Layout & rhythm, Imagery.
- **Page modules** (from the must-haves and content):
  - Marketing pages: Hero, Navigation, Features/services, Pricing, Trust & proof, CTA, Footer, Forms.
  - App UI: Shell/navigation, Summary header, Tables/lists, Charts, Detail view, Empty states.

Give each module a one-line **need** that says what the brief requires from it, e.g. "Pricing: fixed fees in PKR, easy to compare on a phone". This is what each reference is judged against.

For each reference you actually looked at:

**A. Overall card**

| Field | What to note |
|---|---|
| Direction | The style in a few words ("editorial salmon paper") |
| Signature move | The one memorable idea worth borrowing |
| Borrow / Watch out | What transfers to this brief, and what doesn't |
| Slop tells | Any from the catalog (it's a reference, not a gospel) |

**B. Per-module entry** for every module this reference visibly handles:
- A **1–5 score** for how well its approach would serve *this module's need*. This is not how pretty it is in isolation.
- A **one-line note**: what it does, and what you'd take from it.
- Optionally a cropped screenshot of just that part.

If a reference doesn't show a module (for example, no pricing on the homepage), leave it out of that module. Don't guess.

Useful things to note per dimension:
- **Typography:** classification, contrast, scale drama, figures, script support.
- **Color:** proportions, e.g. "90% bone, 8% ink, 2% vermilion".
- **Layout:** grid, density, rhythm, and **how it adapts on a phone**. Look at the mobile version too: a browser screenshot at 390px, Mobbin `platform: "ios"` for app patterns, or the site's mobile layout. A reference that only works on desktop scores lower on Feasibility for a mobile-first brief.
- **Imagery:** photo, illustration, product UI or none.

## 6. Score and rank

**Overall:** score each reference 1–5 on these criteria. The board script computes the weighted total (Σ score × weight ÷ 12).

| Criterion | Weight | Question |
|---|---|---|
| Audience & context fit | 3 | Would it work for *these* users in *their* situation? |
| Trait match | 3 | Does it express the brief's three traits? |
| Content-shape match | 2 | Does its structure suit this content (data-dense, long-form, marketing)? |
| Distinctiveness | 2 | Is there a real signature move, with few slop tells? |
| Feasibility | 1 | Can it be built in the user's stack and scope, with their real content and assets? |
| Constraint fit | 1 | Scripts and languages, accessibility, brand colors and fonts |

Then **rerank for diversity**. The top 4–6 should cover distinct directions.

**Per module:** rank references by their module score, using the overall total to break ties. The top one is your **recommendation** for that module. It's normal and good for different modules to recommend different references.

## 7. Build the reference board

Always build the board for a reference hunt. It is how the user compares the options by eye.

1. Copy `assets/example-refs.json` (the template) to `<scratchpad>/refs/refs.json`. Fill in `brief`, `modules` and `refs`, with each ref's `modules` entries and image paths relative to the JSON.
2. Render it and open it in the browser:
   ```bash
   python <skill>/scripts/ref_board.py board <scratchpad>/refs/refs.json <scratchpad>/refs/board.html
   ```
   `assets/example-board.html` shows what the result looks like. The full JSON schema is in the script's docstring.

The board has three parts:
- **Overview:** every reference ranked overall, with thumbnail, scores, signature, what to borrow and what to watch out for.
- **Module by module:** for each module, every reference's approach side by side with its score and note, the top one marked *Recommended*, and a pick control. There's also a "None / decide later" option.
- **Pick bar:** a running summary of the user's picks, and a **Copy choices** button that copies them as text for the user to paste back to you.

## 8. Present and ask the user to pick, module by module

In chat, give a short summary:

**1. The overall ranking**, one line per reference:

```
#1  Financial Times (4.2) — editorial salmon paper; reads trustworthy + precise
```

**2. Per module**, the recommendation and the runner-up, with the reason:

```
Hero        → #2 Stripe (3): big claim + one action · alt #3 Linear (3): real product as hero
Typography  → #1 FT (5): serif display + sober sans, "established and careful" · alt #2 Stripe (4)
Color       → #1 FT (5): tinted paper + one accent · alt #2 Stripe (2): gradient, avoid
```

Then ask the user to choose **per module**:

- **If the harness has a structured question tool** (e.g. AskUserQuestion):
  - Ask one question per module.
  - Put the module's top 3 references as options, with the recommended one first and marked "(Recommended)". Each option's description is the note.
  - Batch up to 4 modules per call, and make several calls if there are more modules.
- **Otherwise:** point them at the board and ask them to press **Copy choices** and paste the result, or just reply in text ("hero 2, type 1, color 1…").
- **"None of these" for a module:** ask what's off for that module, and search again for that module only (once or twice at most).

Wait for the answers. Don't start building on your own recommendations: the point of this step is that the user steers.

## 9. Turn the picks into a reference digest

Write a short digest, organized by module, that feeds Build mode step 1 (point of view) and step 2 (tokens). For fonts, it's signal #3 on the typography ladder.

```
Direction:   <one sentence that reconciles the picks>
Hero:        from #2 Stripe — big single claim + one action; adapt: WhatsApp CTA, PKR example
Typography:  from #1 FT — high-contrast serif display + sober sans, tabular figures; adapt: + Noto Nastaliq Urdu
Color:       from #1 FT — tinted paper, ink, one accent ≈2%; adapt: accent from the brief, not FT salmon
Pricing:     from #2 Stripe — plain table, fine print visible
Don't copy:  logos, illustrations, photos, copy, exact layouts — take principles, not assets
```

If the picks pull in different directions (e.g. a dark tech hero with an editorial paper palette), say so and propose how to reconcile them, or ask which one leads.

Borrow **principles and proportions**, never another brand's assets or a pixel-for-pixel layout. The result should feel related to the references and still pass the swap test for the user's own product.
