#!/usr/bin/env python3
"""Render a brand guidelines book (book.html) from a brand.json spec.

Usage:
    python brand_book.py build <brand.json> <book.html> [--offline]
    python brand_book.py kit   <brand.json> <outdir>    [--offline]
        Exports everything in the book as files the app can use: tokens.css/json,
        components.css, tailwind.theme.css (Tailwind v4 @theme) + legacy tailwind.preset.js (v3),
        fonts.html, logo SVGs (currentColor + baked
        ink/reversed/accent), favicon.svg (+ PNGs if cairosvg is installed), icon SVGs +
        sprite.svg, demo.html and a README with HTML / React / Tailwind snippets.

    --offline   don't download icon SVGs at build time (icons then load from the CDN
                via CSS masks when the book is opened).

The book is styled in the brand itself (its fonts, colors, radius) and contains:
  01 Essence  02 Logo  03 Color  04 Typography  05 Iconography  06 Imagery
  07 Layout & spacing  08 Components  09 Voice & tone  10 Guardrails  11 Tokens

Computed automatically, so you don't need to:
  - RGB / HSL values, a 50-900 tint scale per color
  - WCAG contrast of every text/background pairing, with AA/AAA badges and
    printed warnings for failing pairings you marked as intended
  - Google Fonts link, CSS custom properties, tokens JSON (with copy/download buttons)
  - logo clear-space, size ladder and "don't" examples (stretch, recolor, rotate, effects,
    low contrast) - generated from your logo SVG
  - icon SVGs fetched from lucide / tabler / phosphor and inlined (stroke width applied)

Template: assets/example-brand.json  (rendered: assets/example-book.html)
Schema (all sections optional except name + colors):
{
  "name": "Brand", "tagline": "...", "version": "1.0", "date": "2026-10-05",
  "essence": {"mission": "...", "audience": "...", "traits": ["..",".."],
              "personality": {"is": ["..."], "is_not": ["..."]}, "story": "..."},
  "logo": {"wordmark_svg": "<svg ... fill='currentColor'>", "mark_svg": "<svg ...>",
           "concept": "why it looks like this", "clearspace": "1x the height of the mark's stem",
           "min_size": {"wordmark_px": 96, "mark_px": 16}},
  "colors": [{"name": "Ledger Ink", "hex": "#1d1b18",
              "role": "text | background | surface | accent | border | muted | success | warning | danger | info",
              "usage": 60, "notes": "..."}],
  "pairings": [["Ledger Ink", "Paper"]],          # optional: intended text-on-bg pairs to verify
  "typography": {
    "families": [{"name": "Spectral", "role": "display|body|mono|<lang code>",
                  "weights": [400, 600], "italic": false, "fallback": "Georgia, serif", "why": "..."}],
    "scale": [{"token": "display", "size": 64, "line": 1.05, "weight": 600, "family": "display",
               "tracking": -0.02, "sample": "..."}],
    "scripts": [{"lang": "ur", "family": "Noto Nastaliq Urdu", "dir": "rtl", "line": 2.1, "sample": "..."}],
    "rules": ["..."]
  },
  "icons": {"library": "lucide|tabler|phosphor|custom", "size": 24, "stroke": 1.5,
            "style": "...", "items": [{"name": "receipt", "label": "Invoices", "svg": "<optional custom svg>"}],
            "rules": ["..."]},
  "imagery": {"approach": "...", "do": ["..."], "dont": ["..."]},
  "layout": {"grid": "...", "max_width": 1200, "spacing": [4, 8, 12, 16, 24, 32, 48, 64, 96],
             "radius": {"sm": 2, "md": 4, "lg": 8}, "elevation": [{"name": "raised", "css": "0 1px 2px rgba(0,0,0,.08)"}],
             "rules": ["..."]},
  "voice": {"principles": [{"title": "...", "body": "..."}],
            "we_say": ["..."], "we_dont_say": ["..."]},
  "guardrails": ["..."]
}
"""
import colorsys
import html
import math
import json
import re
import sys
import urllib.parse
import urllib.request

# Icon packages: (npm package, path inside the package). URLs are pinned to the package's
# *latest* published version, looked up on the npm registry at build time (see latest_version).
ICON_PKGS = {
    "lucide": ("lucide-static", "icons/{n}.svg"),
    "tabler": ("@tabler/icons", "icons/outline/{n}.svg"),
    "phosphor": ("@phosphor-icons/core", "assets/regular/{n}.svg"),
}
_LATEST = {}
VERSIONS_USED = {}


def latest_version(pkg):
    """Latest stable version of an npm package (registry 'latest' dist-tag), cached; None if offline."""
    if pkg not in _LATEST:
        try:
            req = urllib.request.Request(f"https://registry.npmjs.org/{pkg.replace('/', '%2F')}/latest",
                                         headers={"User-Agent": "brand-book/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                _LATEST[pkg] = json.loads(r.read().decode("utf-8")).get("version")
        except Exception:
            _LATEST[pkg] = None
    return _LATEST[pkg]


def icon_url(lib, name):
    pkg, path = ICON_PKGS[lib]
    ver = latest_version(pkg)
    if ver:
        VERSIONS_USED[pkg] = ver
    return f"https://unpkg.com/{pkg}{'@' + ver if ver else ''}/{path.format(n=urllib.parse.quote(name))}"


ICON_LIBS = ICON_PKGS  # membership checks
E = lambda x: html.escape(str(x if x is not None else ""))


# ---------- color math ----------
def rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(t):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in t)


def lum(h):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(a, b, t):
    ra, rb = rgb(a), rgb(b)
    return to_hex(tuple(x + (y - x) * t for x, y in zip(ra, rb)))


def hsl(h):
    r, g, b = (v / 255 for v in rgb(h))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return f"{round(hh * 360)}° {round(s * 100)}% {round(l * 100)}%"


def oklch(h):
    """Hex -> CSS oklch() string (the color space shadcn's themes use)."""
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(v) for v in rgb(h))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    A = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    B = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    C = (A * A + B * B) ** 0.5
    H = (math.degrees(math.atan2(B, A)) + 360) % 360 if C > 1e-4 else 0
    return f"oklch({L:.3f} {C:.3f} {H:.1f})"


def tints(h):
    # 50..900 scale anchored on the color at 500
    steps = [(50, "#ffffff", .92), (100, "#ffffff", .82), (200, "#ffffff", .62), (300, "#ffffff", .42),
             (400, "#ffffff", .2), (500, None, 0), (600, "#000000", .15), (700, "#000000", .32),
             (800, "#000000", .5), (900, "#000000", .66)]
    return [(k, h if t is None else mix(h, t, f)) for k, t, f in steps]


def grade(r):
    return "AAA" if r >= 7 else "AA" if r >= 4.5 else "AA large" if r >= 3 else "Fail"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ---------- icons ----------
def fetch_icon(lib, name, stroke):
    url = icon_url(lib, name)
    req = urllib.request.Request(url, headers={"User-Agent": "brand-book/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        svg = r.read().decode("utf-8")
    svg = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", svg, flags=re.S).strip()
    svg = re.sub(r'\s(width|height|class)="[^"]*"', "", svg, count=3)
    if stroke and lib in ("lucide", "tabler"):
        svg = re.sub(r'stroke-width="[^"]*"', f'stroke-width="{stroke}"', svg)
    return svg


def prep_svg(svg):
    """Make an author-supplied SVG scale with CSS: drop fixed width/height on the root."""
    if not svg:
        return ""
    rx = r"(<svg\b[^>]*?)\s(?:width|height)=\"[^\"]*\""
    return re.sub(rx, r"\1", re.sub(rx, r"\1", svg, count=1), count=1)


# ---------- build ----------
def build(spec, offline=False, ctx_only=False):
    name = spec.get("name", "Brand")
    colors = spec.get("colors", [])
    if not colors:
        raise SystemExit("error: brand.json needs at least one color")

    def by_role(*roles, default=None):
        for c in colors:
            rs = [r.strip() for r in str(c.get("role", "")).lower().replace(",", "|").split("|")]
            if any(r in rs for r in roles):
                return c["hex"]
        return default

    ink = by_role("text", "ink", default="#1a1a1a")
    bg = by_role("background", "paper", "bg", default="#ffffff")
    accent = by_role("accent", "primary", "brand", default=ink)
    surface = by_role("surface", default=mix(bg, ink, .035))
    border = by_role("border", "rule", default=mix(bg, ink, .16))
    muted = by_role("muted", default=mix(ink, bg, .42))
    on_accent = bg if contrast(bg, accent) >= contrast(ink, accent) else ink

    typo = spec.get("typography", {})
    fams = typo.get("families", [])
    fam_by_role = {f.get("role"): f for f in fams}

    def stack(role, fallback):
        f = fam_by_role.get(role)
        return f'"{f["name"]}", {f.get("fallback", fallback)}' if f else fallback

    f_display = stack("display", "Georgia, serif")
    f_body = stack("body", "system-ui, sans-serif")
    f_mono = stack("mono", "ui-monospace, SFMono-Regular, Menlo, monospace")

    families_q = []
    for f in fams + [{"name": s["family"], "weights": [400, 700]} for s in typo.get("scripts", [])
                     if s.get("family") and s["family"] not in [x["name"] for x in fams]]:
        ws = sorted(set(f.get("weights", [400])))
        fam = f["name"].replace(" ", "+")
        if f.get("italic"):
            families_q.append(f"family={fam}:ital,wght@" + ";".join([f"0,{w}" for w in ws] + [f"1,{w}" for w in ws]))
        else:
            families_q.append(f"family={fam}:wght@" + ";".join(map(str, ws)))
    fonts_href = ("https://fonts.googleapis.com/css2?" + "&".join(families_q) + "&display=swap") if families_q else ""

    lay = spec.get("layout", {})
    spacing = lay.get("spacing", [4, 8, 12, 16, 24, 32, 48, 64, 96])
    radius = lay.get("radius", {"sm": 2, "md": 4, "lg": 8})
    elevation = lay.get("elevation", [{"name": "flat", "css": "none"}])
    r_md = radius.get("md", list(radius.values())[0] if radius else 4)

    # ---- tokens ----
    css_vars = [f"  --color-{slug(c['name'])}: {c['hex']};" for c in colors]
    css_vars += [f"  --color-bg: {bg};", f"  --color-text: {ink};", f"  --color-accent: {accent};",
                 f"  --color-on-accent: {on_accent};", f"  --color-surface: {surface};",
                 f"  --color-border: {border};", f"  --color-muted: {muted};",
                 f"  --font-display: {f_display};", f"  --font-body: {f_body};", f"  --font-mono: {f_mono};"]
    css_vars += [f"  --space-{i + 1}: {v}px;" for i, v in enumerate(spacing)]
    css_vars += [f"  --radius-{k}: {v}px;" for k, v in radius.items()]
    css_vars += [f"  --shadow-{slug(e['name'])}: {e['css']};" for e in elevation]
    for s in typo.get("scale", []):
        css_vars.append(f"  --text-{slug(s['token'])}: {s['size']}px;")
    tokens_css = ":root {\n" + "\n".join(css_vars) + "\n}"
    if fonts_href:
        tokens_css = f"/* Fonts: <link rel=\"stylesheet\" href=\"{fonts_href}\"> */\n" + tokens_css
    tokens_json = json.dumps({
        "color": {slug(c["name"]): {"value": c["hex"], "role": c.get("role", "")} for c in colors},
        "font": {r: f["name"] for r, f in fam_by_role.items()},
        "fontSize": {slug(s["token"]): s["size"] for s in typo.get("scale", [])},
        "space": spacing, "radius": radius,
        "shadow": {slug(e["name"]): e["css"] for e in elevation},
    }, indent=2)
    if ctx_only:
        return dict(name=name, colors=colors, ink=ink, bg=bg, accent=accent, on_accent=on_accent,
                    surface=surface, border=border, muted=muted, fonts_href=fonts_href,
                    tokens_css=tokens_css, tokens_json=tokens_json, fam_by_role=fam_by_role,
                    spacing=spacing, radius=radius, elevation=elevation, typo=typo)

    sections = []
    nav = []

    def section(key, num, title, body, lede=""):
        nav.append(f'<a href="#{key}"><span>{num}</span>{E(title)}</a>')
        sections.append(f'<section id="{key}" class="sec"><header class="sh"><span class="num">{num}</span>'
                        f'<h2>{E(title)}</h2>{f"<p class=lede>{E(lede)}</p>" if lede else ""}</header>{body}</section>')

    def ul(items, cls=""):
        return f'<ul class="{cls}">' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>" if items else ""

    # 01 Essence
    es = spec.get("essence", {})
    if es:
        p = es.get("personality", {})
        traits = "".join(f'<span class="trait">{E(t)}</span>' for t in es.get("traits", []))
        body = f"""
<div class="cols2">
  <div>{f'<p class="big">{E(es.get("mission"))}</p>' if es.get("mission") else ''}
       {f'<p>{E(es.get("story"))}</p>' if es.get("story") else ''}
       {f'<p class="meta"><b>Audience.</b> {E(es.get("audience"))}</p>' if es.get("audience") else ''}
       <div class="traits">{traits}</div></div>
  <div class="isnot">
    {f'<div><h4>We are</h4>{ul(p.get("is", []), "ticks")}</div>' if p.get("is") else ''}
    {f'<div><h4>We are not</h4>{ul(p.get("is_not", []), "crosses")}</div>' if p.get("is_not") else ''}
  </div>
</div>"""
        section("essence", "01", "Brand essence", body)

    # 02 Logo
    lg = spec.get("logo", {})
    word, mark = prep_svg(lg.get("wordmark_svg")), prep_svg(lg.get("mark_svg"))
    primary = word or mark
    if primary:
        ms = lg.get("min_size", {})
        sizes = "".join(f'<figure class="sz"><div class="appicon" style="width:{s}px;height:{s}px">{mark or primary}</div>'
                        f'<figcaption>{s}px</figcaption></figure>' for s in (16, 24, 32, 48, 64, 128)) if mark else ""
        donts = [
            ("Don't stretch or squash", "transform:scaleX(1.45)", ""),
            ("Don't recolor outside the palette", "", "color:#ff2bd6"),
            ("Don't rotate", "transform:rotate(-12deg)", ""),
            ("Don't add gradients, glows or shadows", "filter:drop-shadow(0 0 10px #7c3aed) drop-shadow(0 6px 6px rgba(0,0,0,.4))", "color:#8b5cf6"),
            ("Don't place on low-contrast backgrounds", "", f"color:{mix(accent, bg, .25)};background:{accent}"),
            ("Don't outline or box the wordmark", "outline:3px solid currentColor;outline-offset:6px;border-radius:999px", ""),
        ]
        dont_html = "".join(f'<figure class="dont"><div class="tile" style="{tile_style}"><div class="lg" style="{logo_style}">{primary}</div></div>'
                            f'<figcaption><b>✕</b> {E(t)}</figcaption></figure>' for t, logo_style, tile_style in donts)
        body = f"""
{f'<p class="big">{E(lg.get("concept"))}</p>' if lg.get("concept") else ''}
<div class="logo-row">
  <figure class="tile hero-tile" style="background:{bg};color:{ink}"><div class="lg big-lg">{primary}</div><figcaption>Primary · on {E(bg)}</figcaption></figure>
  <figure class="tile hero-tile" style="background:{ink};color:{bg}"><div class="lg big-lg">{primary}</div><figcaption style="color:{bg}">Reversed · on {E(ink)}</figcaption></figure>
  <figure class="tile hero-tile" style="background:{accent};color:{on_accent}"><div class="lg big-lg">{primary}</div><figcaption style="color:{on_accent}">On accent · {E(accent)}</figcaption></figure>
</div>
{f'<h3>Wordmark &amp; mark</h3><div class="logo-pair"><figure class="tile"><div class="lg">{word}</div><figcaption>Wordmark — default</figcaption></figure><figure class="tile"><div class="lg mk">{mark}</div><figcaption>Mark — small spaces, favicon, avatar</figcaption></figure></div>' if word and mark else ''}
<h3>Clear space &amp; minimum size</h3>
<div class="cols2">
  <figure class="tile clear"><div class="cs"><div class="lg">{primary}</div></div><figcaption>Keep clear space of {E(lg.get("clearspace", "the height of the mark"))} on all sides.</figcaption></figure>
  <div><p class="meta">Minimum sizes: wordmark {E(ms.get("wordmark_px", 96))}px wide · mark {E(ms.get("mark_px", 16))}px.</p>
  {f'<div class="sizes">{sizes}</div>' if sizes else ''}</div>
</div>
<h3>Misuse</h3>
<div class="donts">{dont_html}</div>"""
        section("logo", "02", "Logo", body, "Logos use currentColor, so they follow the text color of their container.")

    # 03 Color
    total_use = sum(c.get("usage", 0) for c in colors) or 1
    prop = "".join(f'<span style="flex:{c.get("usage", 0) or 0.5};background:{c["hex"]}" title="{E(c["name"])} {c.get("usage", 0)}%"></span>' for c in colors)
    swatches = []
    for c in colors:
        h = c["hex"]
        best = "#ffffff" if contrast("#ffffff", h) >= contrast("#000000", h) else "#000000"
        scale = "".join(f'<span style="background:{t};color:{"#fff" if contrast("#fff", t) >= contrast("#000", t) else "#000"}">{k}</span>' for k, t in tints(h))
        r_, g_, b_ = rgb(h)
        swatches.append(f"""
<article class="sw">
  <div class="chip" style="background:{h};color:{best}"><b>{E(c['name'])}</b><span>{E(c.get('role', ''))}</span></div>
  <dl><div><dt>HEX</dt><dd><button class="cp" data-copy="{E(h)}">{E(h.upper())}</button></dd></div>
      <div><dt>RGB</dt><dd>{r_} {g_} {b_}</dd></div><div><dt>HSL</dt><dd>{hsl(h)}</dd></div>
      <div><dt>Use</dt><dd>{c.get('usage', '–')}%</dd></div>
      <div><dt>vs white</dt><dd>{contrast(h, '#ffffff'):.1f}:1</dd></div><div><dt>vs black</dt><dd>{contrast(h, '#000000'):.1f}:1</dd></div></dl>
  {f'<p class="note">{E(c.get("notes"))}</p>' if c.get('notes') else ''}
  <div class="scale">{scale}</div>
</article>""")
    # pairing matrix: text-ish colors vs background-ish colors
    textish = [c for c in colors if not re.search(r"background|paper|surface", str(c.get("role", "")), re.I)] or colors
    bgish = [c for c in colors if re.search(r"background|paper|surface|accent|primary", str(c.get("role", "")), re.I)] or colors
    head = "".join(f'<th style="background:{b["hex"]};color:{ink if contrast(ink, b["hex"]) > contrast(bg, b["hex"]) else bg}">{E(b["name"])}</th>' for b in bgish)
    rows = []
    for t in textish:
        cells = []
        for b in bgish:
            if t is b:
                cells.append('<td class="na">—</td>')
                continue
            r = contrast(t["hex"], b["hex"])
            g = grade(r)
            cells.append(f'<td style="background:{b["hex"]};color:{t["hex"]}"><b>Aa</b> <span class="g g-{slug(g)}">{r:.1f} {g}</span></td>')
        rows.append(f'<tr><th>{E(t["name"])}</th>{"".join(cells)}</tr>')
    warnings = []
    named = {c["name"]: c["hex"] for c in colors}
    for pair in spec.get("pairings", []):
        a, b = pair[0], pair[1]
        if a in named and b in named and contrast(named[a], named[b]) < 4.5:
            warnings.append(f"{a} on {b}: {contrast(named[a], named[b]):.2f}:1 — below AA for body text (use for large text/graphics only)")
    body = f"""
<div class="prop" aria-label="Color proportions">{prop}</div>
<p class="meta">Proportion bar shows intended usage across a typical screen (total {total_use}%).</p>
<div class="swatches">{''.join(swatches)}</div>
<h3>Accessible pairings</h3>
<p class="meta">Text color (rows) on background (columns). Body text needs AA (4.5:1); large text and icons need 3:1.</p>
<div class="tbl"><table class="pairs"><thead><tr><th></th>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>
{('<div class="warnbox"><b>Check these intended pairings:</b>' + ul(warnings) + '</div>') if warnings else ''}"""
    section("color", "03", "Color", body, "One accent, tinted neutrals, status colors only where they carry meaning.")

    # 04 Typography
    if typo:
        fam_cards = "".join(f"""
<article class="fam"><div class="spec" style="font-family:'{E(f['name'])}',{E(f.get('fallback', 'sans-serif'))}">Aa</div>
<div><h4>{E(f['name'])}</h4><p class="meta">{E(f.get('role', ''))} · weights {', '.join(map(str, f.get('weights', [400])))}</p>
<p>{E(f.get('why', ''))}</p>
<p class="glyphs" style="font-family:'{E(f['name'])}',{E(f.get('fallback', 'sans-serif'))}">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789 ₨ $ € % &amp; @ ( ) ?</p></div></article>""" for f in fams)
        fam_map = {"display": "var(--font-display)", "body": "var(--font-body)", "mono": "var(--font-mono)"}
        scale_rows = "".join(f"""
<div class="ts"><div class="ts-meta"><b>{E(s['token'])}</b><span>{s['size']}px / {s.get('line', 1.4)} · {s.get('weight', 400)}{f" · {s['tracking']}em" if s.get('tracking') else ''}</span></div>
<div class="ts-sample" style="font-family:{fam_map.get(s.get('family', 'body'), 'var(--font-body)')};font-size:{s['size']}px;line-height:{s.get('line', 1.4)};font-weight:{s.get('weight', 400)};letter-spacing:{s.get('tracking', 0)}em">{E(s.get('sample', name))}</div></div>""" for s in typo.get("scale", []))
        scripts = "".join(f"""
<div class="ts"><div class="ts-meta"><b>{E(s.get('lang', ''))}</b><span>{E(s.get('family', ''))}</span></div>
<div class="ts-sample" lang="{E(s.get('lang', ''))}" dir="{E(s.get('dir', 'auto'))}" style="font-family:'{E(s.get('family', ''))}',serif;font-size:{s.get('size', 28)}px;line-height:{s.get('line', 1.8)}">{E(s.get('sample', ''))}</div></div>""" for s in typo.get("scripts", []))
        body = f"""
<div class="fams">{fam_cards}</div>
{f'<h3>Type scale</h3><div class="scale-list">{scale_rows}</div>' if scale_rows else ''}
{f'<h3>Other scripts</h3><div class="scale-list">{scripts}</div>' if scripts else ''}
{f'<h3>Rules</h3>{ul(typo.get("rules", []), "ticks")}' if typo.get('rules') else ''}"""
        section("type", "04", "Typography", body)

    # 05 Iconography
    ic = spec.get("icons", {})
    if ic.get("items"):
        lib = ic.get("library", "lucide")
        size = ic.get("size", 24)
        stroke = ic.get("stroke")
        cells = []
        for it in ic["items"]:
            svg = prep_svg(it.get("svg", ""))
            if not svg and lib in ICON_LIBS and not offline:
                try:
                    svg = fetch_icon(lib, it["name"], stroke)
                except Exception as ex:  # network / 404: fall back to CSS mask
                    print(f"  icon '{it['name']}' not inlined ({type(ex).__name__}); using CDN mask", file=sys.stderr)
            if svg:
                glyph = f'<span class="ic" style="width:{size}px;height:{size}px">{svg}</span>'
            elif lib in ICON_LIBS:
                u = icon_url(lib, it["name"])
                glyph = f'<span class="ic mask" style="width:{size}px;height:{size}px;-webkit-mask-image:url({u});mask-image:url({u})"></span>'
            else:
                glyph = '<span class="ic missing">?</span>'
            cells.append(f'<figure class="icell">{glyph}<figcaption><b>{E(it.get("label", it["name"]))}</b><code>{E(it["name"])}</code></figcaption></figure>')
        first = cells[0].split("<figcaption>")[0].replace('<figure class="icell">', "") if cells else ""
        sizes = "".join(f'<div class="isz"><div style="transform:scale({s / size});transform-origin:center">{first}</div><span>{s}px</span></div>' for s in (16, 20, 24, 32)) if first else ""
        body = f"""
<p class="meta">Library: <b>{E(lib)}</b>{f' ({E(ICON_PKGS[lib][0])}@{E(VERSIONS_USED[ICON_PKGS[lib][0]])}, latest at build)' if lib in ICON_PKGS and ICON_PKGS[lib][0] in VERSIONS_USED else ''} · grid {size}px{f' · stroke {stroke}px' if stroke else ''}. {E(ic.get('style', ''))}</p>
<div class="icons">{''.join(cells)}</div>
<div class="cols2"><div><h3>Sizes</h3><div class="isizes">{sizes}</div></div>
<div><h3>Color</h3><div class="icolors">
  <span style="color:{ink}">{first}</span><span style="color:{muted}">{first}</span><span style="color:{accent}">{first}</span>
  <span style="background:{accent};color:{on_accent}">{first}</span></div></div></div>
{f'<h3>Rules</h3>{ul(ic.get("rules", []), "ticks")}' if ic.get('rules') else ''}"""
        section("icons", "05", "Iconography", body)

    # 06 Imagery
    im = spec.get("imagery", {})
    if im:
        body = f"""{f'<p class="big">{E(im.get("approach"))}</p>' if im.get('approach') else ''}
<div class="cols2"><div class="do"><h4>Do</h4>{ul(im.get('do', []), 'ticks')}</div><div class="dontl"><h4>Don't</h4>{ul(im.get('dont', []), 'crosses')}</div></div>"""
        section("imagery", "06", "Imagery", body)

    # 07 Layout & spacing
    sp = "".join(f'<div class="sp"><span class="bar" style="width:{v}px"></span><code>--space-{i + 1}</code><span>{v}px</span></div>' for i, v in enumerate(spacing))
    rad = "".join(f'<figure class="rad"><div style="border-radius:{v}px"></div><figcaption>{E(k)} · {v}px</figcaption></figure>' for k, v in radius.items())
    elv = "".join(f'<figure class="rad"><div style="box-shadow:{E(e["css"])};border-radius:{r_md}px"></div><figcaption>{E(e["name"])}</figcaption></figure>' for e in elevation)
    body = f"""{f'<p class="big">{E(lay.get("grid"))}</p>' if lay.get('grid') else ''}
<div class="cols2"><div><h3>Spacing scale</h3><div class="spacing">{sp}</div></div>
<div><h3>Radius</h3><div class="rads">{rad}</div><h3>Elevation</h3><div class="rads">{elv}</div></div></div>
{f'<h3>Rules</h3>{ul(lay.get("rules", []), "ticks")}' if lay.get('rules') else ''}"""
    section("layout", "07", "Layout & spacing", body)

    # 08 Components (rendered from tokens)
    status = [(c["name"], c["hex"]) for c in colors if re.search(r"success|warning|danger|error|info", str(c.get("role", "")), re.I)]
    badges = "".join(f'<span class="badge" style="color:{h};border-color:{h};background:{mix(h, bg, .9)}">{E(n)}</span>' for n, h in status)
    body = f"""
<div class="comp-grid">
  <figure class="tile comp"><div class="row"><button class="btn primary">Book a review</button><button class="btn secondary">See fees</button><a class="btn link" href="#components">Learn how it works →</a></div><figcaption>Buttons — one primary action per view; secondary as outline or link.</figcaption></figure>
  <figure class="tile comp"><label class="field"><span>Email</span><input type="email" placeholder="you@example.com"></label><figcaption>Input — visible label, 1px border, accent focus ring.</figcaption></figure>
  <figure class="tile comp"><article class="card"><h4>{E(name)}</h4><p>Cards only for discrete objects — not every block of content.</p><a href="#components">Open →</a></article><figcaption>Card</figcaption></figure>
  <figure class="tile comp"><table class="dt"><thead><tr><th>Item</th><th class="n">Amount</th></tr></thead><tbody><tr><td>Line one</td><td class="n">12,400</td></tr><tr><td>Line two</td><td class="n">3,150</td></tr><tr><td><b>Total</b></td><td class="n"><b>15,550</b></td></tr></tbody></table><figcaption>Table — tabular figures, right-aligned numbers, ruled rows.</figcaption></figure>
  {f'<figure class="tile comp"><div class="row">{badges}</div><figcaption>Status — color always paired with a word.</figcaption></figure>' if badges else ''}
</div>"""
    section("components", "08", "Components", body, "Rendered live from the tokens below.")

    # 09 Voice
    vo = spec.get("voice", {})
    if vo:
        pr = "".join(f'<article class="pr"><h4>{E(p.get("title"))}</h4><p>{E(p.get("body"))}</p></article>' for p in vo.get("principles", []))
        body = f"""<div class="prs">{pr}</div>
<div class="cols2"><div class="do"><h4>We say</h4>{ul(vo.get('we_say', []), 'ticks')}</div><div class="dontl"><h4>We don't say</h4>{ul(vo.get('we_dont_say', []), 'crosses')}</div></div>"""
        section("voice", "09", "Voice & tone", body)

    # 10 Guardrails
    gr = spec.get("guardrails") or []
    body = ul(gr, "crosses") + '<p class="meta">Audit any new page with <code>scripts/slop_scan.py</code> and the swap test before shipping.</p>'
    section("guardrails", "10", "Guardrails", body, "What keeps this brand from drifting back into generic AI defaults.")

    # 11 Tokens
    body = f"""
<div class="tokbar"><button class="btn secondary" data-copy-target="tok-css">Copy CSS</button><button class="btn secondary" data-download="tok-css" data-name="tokens.css">Download tokens.css</button>
<button class="btn secondary" data-copy-target="tok-json">Copy JSON</button><button class="btn secondary" data-download="tok-json" data-name="tokens.json">Download tokens.json</button></div>
<pre id="tok-css">{E(tokens_css)}</pre><pre id="tok-json">{E(tokens_json)}</pre>"""
    section("tokens", "11", "Design tokens", body)

    head_font = f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="{E(fonts_href)}">' if fonts_href else ""
    css = (CSS.replace("$TOKENS", tokens_css.split("*/\n")[-1])
           .replace("$RMD", str(r_md)))
    first_ic = ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(name)} Brand Book</title>{head_font}<style>{css}</style></head>
<body>
<aside class="nav"><div class="navlogo">{mark or primary or E(name)}</div><nav>{''.join(nav)}</nav></aside>
<main>
<header class="cover">
  <div class="cover-logo">{primary or ''}</div>
  <h1>{E(name)}</h1>{f'<p class="tagline">{E(spec.get("tagline"))}</p>' if spec.get('tagline') else ''}
  <p class="meta">Brand guidelines · v{E(spec.get('version', '1.0'))}{f' · {E(spec.get("date"))}' if spec.get('date') else ''}</p>
</header>
{''.join(sections)}
<footer class="foot">{E(name)} brand book · generated from brand.json</footer>
</main>
<script>{JS}</script>{first_ic}
</body></html>"""


CSS = """
$TOKENS
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--color-bg);color:var(--color-text);font:16px/1.6 var(--font-body);font-variant-numeric:tabular-nums}
.nav{position:fixed;inset:0 auto 0 0;width:220px;padding:28px 20px;border-right:1px solid var(--color-border);background:var(--color-bg);overflow:auto}
.navlogo{height:40px;margin-bottom:28px;color:var(--color-text)}.navlogo svg{height:100%;width:auto;max-width:100%}
.nav nav{display:grid;gap:2px}
.nav a{display:flex;gap:10px;padding:6px 8px;color:var(--color-text);text-decoration:none;font-size:14px;border-radius:var(--radius-sm,2px)}
.nav a span{font-family:var(--font-mono);color:var(--color-muted);font-size:12px;padding-top:2px}
.nav a:hover{background:var(--color-surface)}
main{margin-left:220px;padding:0 48px 80px;max-width:1240px}
.cover{min-height:70vh;display:flex;flex-direction:column;justify-content:flex-end;padding:64px 0 48px;border-bottom:2px solid var(--color-text)}
.cover-logo{color:var(--color-accent);height:72px;margin-bottom:auto}.cover-logo svg{height:100%;width:auto;max-width:100%}
.cover h1{font:600 clamp(48px,8vw,112px)/.95 var(--font-display);letter-spacing:-.02em;margin:48px 0 12px}
.tagline{font:400 clamp(20px,2.4vw,28px)/1.3 var(--font-display);margin:0 0 16px;max-width:30ch}
.sec{padding:72px 0 24px;border-bottom:1px solid var(--color-border)}
.sh{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;align-items:baseline;margin-bottom:28px}
.num{font:500 14px var(--font-mono);color:var(--color-accent)}
.sh h2{font:600 clamp(30px,4vw,44px)/1.05 var(--font-display);margin:0;letter-spacing:-.01em}
.lede{grid-column:2;margin:0;color:var(--color-muted);max-width:60ch}
h3{font:600 20px/1.2 var(--font-display);margin:40px 0 14px}
h4{font:600 16px/1.3 var(--font-body);margin:0 0 8px}
.big{font:400 clamp(20px,2.2vw,26px)/1.35 var(--font-display);max-width:38ch;margin:0 0 20px}
.meta{color:var(--color-muted);font-size:14px}
code,pre{font-family:var(--font-mono);font-size:13px}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:32px}
ul.ticks,ul.crosses{list-style:none;padding:0;margin:0;display:grid;gap:6px}
ul.ticks li,ul.crosses li{padding-left:24px;position:relative}
ul.ticks li::before{content:"✓";position:absolute;left:0;color:var(--color-accent);font-weight:700}
ul.crosses li::before{content:"✕";position:absolute;left:0;color:var(--color-muted);font-weight:700}
.traits{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.trait{border:1px solid var(--color-text);padding:4px 12px;font-size:14px;border-radius:var(--radius-sm,2px)}
.isnot{display:grid;gap:24px}
.tile{margin:0;border:1px solid var(--color-border);padding:24px;border-radius:$RMDpx;display:flex;flex-direction:column;gap:12px}
.tile figcaption{font-size:13px;color:var(--color-muted)}
.lg{color:inherit;height:48px}.lg svg{height:100%;width:auto;max-width:100%;display:block}
.big-lg{height:64px;margin:32px auto}
.lg.mk{height:64px}
.logo-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.hero-tile{min-height:220px;justify-content:space-between}
.logo-pair{display:grid;grid-template-columns:2fr 1fr;gap:16px}
.cs{align-self:center;padding:28px;outline:1px dashed var(--color-accent);background:repeating-linear-gradient(45deg,transparent 0 6px,color-mix(in srgb,var(--color-accent) 10%,transparent) 6px 7px)}
.cs .lg{background:var(--color-bg)}
.sizes{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;margin-top:12px}
.sz{margin:0;display:grid;gap:6px;justify-items:center;font-size:12px;color:var(--color-muted)}
.appicon{color:var(--color-on-accent);background:var(--color-accent);border-radius:22%;padding:16%;display:grid;place-items:center}.appicon svg{width:100%;height:100%}
.donts{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.dont{margin:0}.dont .tile{height:140px;align-items:center;justify-content:center;overflow:hidden}
.dont figcaption{font-size:13px;margin-top:8px}.dont figcaption b{color:#c0392b}
.prop{display:flex;height:56px;border:1px solid var(--color-border);border-radius:$RMDpx;overflow:hidden}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin-top:20px}
.sw{border:1px solid var(--color-border);border-radius:$RMDpx;overflow:hidden;display:flex;flex-direction:column}
.chip{height:120px;padding:14px;display:flex;flex-direction:column;justify-content:flex-end}
.chip b{font:600 18px var(--font-display)}.chip span{font-size:12px;opacity:.85;text-transform:uppercase;letter-spacing:.06em}
.sw dl{display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;margin:12px 14px;font-size:13px}
.sw dt{color:var(--color-muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em}.sw dd{margin:0;font-family:var(--font-mono)}
.note{margin:0 14px 12px;font-size:13px;color:var(--color-muted)}
.scale{display:grid;grid-template-columns:repeat(10,1fr);margin-top:auto}
.scale span{font:10px var(--font-mono);padding:10px 0;text-align:center}
.cp{font:inherit;background:none;border:0;padding:0;color:inherit;cursor:copy;text-decoration:underline dotted}
.tbl{overflow-x:auto}
.pairs{border-collapse:collapse;width:100%;font-size:13px}
.pairs th,.pairs td{padding:10px;border:1px solid var(--color-border);text-align:left;white-space:nowrap}
.pairs td b{font:600 20px var(--font-display);margin-right:6px}
.pairs td.na{color:var(--color-muted);text-align:center}
.g{font:11px var(--font-mono);padding:1px 6px;border-radius:999px;background:rgba(255,255,255,.85);color:#111}
.g-fail{background:#c0392b;color:#fff}.g-aa-large{background:#e3a008;color:#111}
.warnbox{margin-top:16px;border-left:4px solid #c0392b;padding:12px 16px;background:var(--color-surface)}
.fams{display:grid;gap:16px}
.fam{display:grid;grid-template-columns:160px 1fr;gap:24px;border:1px solid var(--color-border);border-radius:$RMDpx;padding:24px}
.spec{font-size:112px;line-height:1;color:var(--color-accent)}
.glyphs{font-size:18px;line-height:1.5;margin:0;word-break:break-all}
.scale-list{display:grid;border-top:1px solid var(--color-border)}
.ts{display:grid;grid-template-columns:180px 1fr;gap:24px;padding:18px 0;border-bottom:1px solid var(--color-border);align-items:baseline}
.ts-meta{display:grid;font-size:13px}.ts-meta span{color:var(--color-muted);font-family:var(--font-mono);font-size:12px}
.ts-sample{overflow-wrap:anywhere}
.icons{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:1px;background:var(--color-border);border:1px solid var(--color-border);margin-top:16px}
.icell{margin:0;background:var(--color-bg);padding:22px 12px;display:grid;justify-items:center;gap:10px;text-align:center}
.icell figcaption{display:grid;font-size:13px}.icell code{color:var(--color-muted);font-size:11px}
.ic{display:inline-grid;place-items:center;color:currentColor}.ic svg{width:100%;height:100%}
.ic.mask{background:currentColor;-webkit-mask-size:contain;mask-size:contain;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-position:center;mask-position:center}
.isizes{display:flex;gap:24px;align-items:center}
.isz{display:grid;justify-items:center;gap:8px;font-size:12px;color:var(--color-muted)}
.icolors{display:flex;gap:12px}.icolors>span{display:grid;place-items:center;width:56px;height:56px;border:1px solid var(--color-border);border-radius:$RMDpx}
.do,.dontl{border-top:3px solid var(--color-accent);padding-top:14px}.dontl{border-top-color:var(--color-muted)}
.spacing{display:grid;gap:8px}
.sp{display:grid;grid-template-columns:100px 90px 1fr;gap:12px;align-items:center;font-size:13px}
.sp .bar{height:14px;background:var(--color-accent);display:block;max-width:100px}
.sp code{color:var(--color-muted)}
.rads{display:flex;gap:16px;flex-wrap:wrap}
.rad{margin:0;display:grid;gap:8px;font-size:12px;color:var(--color-muted)}
.rad div{width:88px;height:64px;background:var(--color-surface);border:1px solid var(--color-border)}
.comp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
.comp .row{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.btn{font:600 15px var(--font-body);padding:11px 18px;border-radius:$RMDpx;border:1px solid transparent;cursor:pointer;text-decoration:none;display:inline-block}
.btn.primary{background:var(--color-accent);color:var(--color-on-accent)}
.btn.primary:hover{background:color-mix(in srgb,var(--color-accent) 88%,black)}
.btn.secondary{background:transparent;color:var(--color-text);border-color:var(--color-text)}
.btn.link{color:var(--color-accent);padding-inline:0}
.btn:focus-visible,input:focus-visible{outline:2px solid var(--color-accent);outline-offset:2px}
.field{display:grid;gap:6px;font-size:14px;font-weight:600}
.field input{font:16px var(--font-body);padding:10px 12px;border:1px solid var(--color-border);border-radius:$RMDpx;background:var(--color-bg);color:var(--color-text)}
.card{border:1px solid var(--color-border);border-radius:$RMDpx;padding:18px}.card p{margin:0 0 8px;font-size:14px}.card a{color:var(--color-accent)}
.dt{border-collapse:collapse;width:100%;font-size:14px}.dt th{text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--color-muted);border-bottom:2px solid var(--color-text);padding:6px 0}
.dt td{border-bottom:1px solid var(--color-border);padding:8px 0}.dt .n{text-align:right;font-family:var(--font-mono)}
.badge{font-size:13px;padding:2px 10px;border:1px solid;border-radius:999px}
.prs{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin-bottom:28px}
.pr{border-left:3px solid var(--color-accent);padding:4px 0 4px 16px}.pr p{margin:0;font-size:15px}
.tokbar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
pre{background:var(--color-surface);border:1px solid var(--color-border);padding:16px;overflow:auto;border-radius:$RMDpx;max-height:420px}
.foot{padding:32px 0;color:var(--color-muted);font-size:13px}
@media (max-width:960px){
  .nav{position:sticky;top:0;width:auto;inset:auto;border-right:0;border-bottom:1px solid var(--color-border);padding:10px 16px;z-index:5;display:flex;gap:16px;align-items:center}
  .navlogo{height:28px;margin:0;flex:none}.nav nav{display:flex;overflow-x:auto;gap:4px}.nav a{white-space:nowrap}
  main{margin-left:0;padding:0 16px 64px}
  .cols2,.logo-row,.logo-pair{grid-template-columns:1fr}.donts{grid-template-columns:1fr 1fr}
  .fam{grid-template-columns:1fr}.spec{font-size:80px}.ts{grid-template-columns:1fr;gap:6px}
}
@media print{.nav,.tokbar{display:none}main{margin:0;padding:0}.sec{break-inside:avoid-page}}
"""

JS = """
function flash(b,t){const o=b.textContent;b.textContent=t;setTimeout(()=>b.textContent=o,1600)}
async function copy(text,b){try{await navigator.clipboard.writeText(text)}catch(e){const t=document.createElement('textarea');t.value=text;document.body.appendChild(t);t.select();try{document.execCommand('copy')}catch(_){}t.remove()}flash(b,'Copied')}
document.addEventListener('click',e=>{
  const b=e.target.closest('[data-copy],[data-copy-target],[data-download]');if(!b)return;
  if(b.dataset.copy)copy(b.dataset.copy,b);
  else if(b.dataset.copyTarget)copy(document.getElementById(b.dataset.copyTarget).textContent,b);
  else{const txt=document.getElementById(b.dataset.download).textContent;const a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([txt],{type:'text/plain'}));a.download=b.dataset.name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}
});
"""

# ---------- kit export: everything in the book as files the app can use ----------
COMPONENTS_CSS = """/* Brand components - built on tokens.css. Load tokens.css first. */
body { background: var(--color-bg); color: var(--color-text); font-family: var(--font-body); font-variant-numeric: tabular-nums; }
h1, h2, h3 { font-family: var(--font-display); text-wrap: balance; }

.btn { font: 600 15px/1 var(--font-body); padding: 12px 18px; border-radius: var(--radius-md); border: 1px solid transparent;
       cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; transition: background-color .15s, color .15s; }
.btn-primary { background: var(--color-accent); color: var(--color-on-accent); }
.btn-primary:hover { background: color-mix(in srgb, var(--color-accent) 88%, black); }
.btn-secondary { background: transparent; color: var(--color-text); border-color: var(--color-text); }
.btn-secondary:hover { background: var(--color-surface); }
.btn-link { color: var(--color-accent); padding-inline: 0; }
.btn:focus-visible, .field input:focus-visible, .field select:focus-visible, .field textarea:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }

.field { display: grid; gap: 6px; font-size: 14px; font-weight: 600; }
.field input, .field select, .field textarea { font: 16px var(--font-body); padding: 10px 12px; border: 1px solid var(--color-border);
       border-radius: var(--radius-md); background: var(--color-bg); color: var(--color-text); }
.field .hint { font-weight: 400; color: var(--color-muted); }

.card { border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-5, 24px); background: var(--color-bg); }
.band { background: var(--color-surface); }

.table { border-collapse: collapse; width: 100%; }
.table th { text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: .06em; color: var(--color-muted);
       border-bottom: 2px solid var(--color-text); padding: 8px 0; }
.table td { border-bottom: 1px solid var(--color-border); padding: 10px 0; }
.table .num { text-align: right; font-family: var(--font-mono); }

.badge { display: inline-block; font-size: 13px; padding: 2px 10px; border: 1px solid currentColor; border-radius: 999px; }
$BADGES
.icon { width: 1.25em; height: 1.25em; display: inline-block; vertical-align: -0.2em; flex: none; }
.logo { height: 40px; width: auto; color: var(--color-text); }
.logo-mark { height: 32px; width: 32px; color: var(--color-accent); }

@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
"""

README = """# {name} - brand kit

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
| `favicon.svg` | Mark on an accent tile. Link with `<link rel="icon" href="/favicon.svg" type="image/svg+xml">`. {png_note} |
| `icons/*.svg`, `icons/sprite.svg` | The brand's icon set ({icon_lib}); sprite symbols are `#i-<name>`. |
| `demo.html` | A small page using everything above - open it to check the kit works. |

## Plain HTML
```html
<!-- in <head> -->
{fonts_tag}
<link rel="stylesheet" href="brand/tokens.css">
<link rel="stylesheet" href="brand/components.css">
<link rel="icon" href="brand/favicon.svg" type="image/svg+xml">

<!-- logo (inline SVG so it follows color) -->
<a href="/" class="logo" aria-label="{name}"><!-- paste logo/wordmark.svg here --></a>

<!-- icon from the sprite -->
<svg class="icon" aria-hidden="true"><use href="brand/icons/sprite.svg#i-{first_icon}"></use></svg>

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
export const Icon = ({{ name, ...p }}) => (
  <svg className="icon" aria-hidden="true" {{...p}}><use href={{`/brand/icons/sprite.svg#i-${{name}}`}} /></svg>
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

Legacy Tailwind v3 only: `module.exports = {{ presets: [require("./brand/tailwind.preset.js")] }}` + import `tokens.css`.

## Versions
Built against the latest stable releases at export time: {versions}. Check for newer versions
before starting a new project (`npm view <package> version`); in an existing project, keep the
versions it already uses unless you decide to upgrade.

## Rules that the files can't enforce
See `book.html`: one accent, tabular figures for money, icons always beside labels, no emoji,
voice "we say / we don't say", and the guardrails section.
"""


def _svg_inner(svg):
    m = re.search(r"<svg\b([^>]*)>(.*)</svg>", svg, re.S)
    if not m:
        return None, "", ""
    attrs, inner = m.group(1), m.group(2)
    vb = re.search(r'viewBox=["\']([^"\']+)["\']', attrs)
    return (vb.group(1) if vb else "0 0 24 24"), attrs, inner


def _bake(svg, color):
    s = svg.replace("currentColor", color)
    if "xmlns=" not in s:
        s = s.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    return s


def kit(spec, out, offline=False):
    import os
    c = build(spec, ctx_only=True)
    os.makedirs(os.path.join(out, "logo"), exist_ok=True)
    os.makedirs(os.path.join(out, "icons"), exist_ok=True)
    w = lambda p, t: open(os.path.join(out, p), "w", encoding="utf-8").write(t)
    made = []

    # tokens
    w("tokens.css", c["tokens_css"] + "\n"); w("tokens.json", c["tokens_json"] + "\n"); made += ["tokens.css", "tokens.json"]

    # components
    status = [(slug(x["name"]), x["hex"]) for x in c["colors"] if re.search(r"success|warning|danger|error|info", str(x.get("role", "")), re.I)]
    badges = "\n".join(f".badge-{s} {{ color: {h}; background: color-mix(in srgb, {h} 10%, var(--color-bg)); }}" for s, h in status)
    w("components.css", COMPONENTS_CSS.replace("$BADGES", badges)); made.append("components.css")

    # fonts
    fonts_tag = (f'<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                 f'<link rel="stylesheet" href="{c["fonts_href"]}">') if c["fonts_href"] else "<!-- no web fonts -->"
    w("fonts.html", fonts_tag + "\n"); made.append("fonts.html")

    # Tailwind v4 (current): CSS-first @theme with real values, so it works on its own.
    named = {slug(x["name"]): x["hex"] for x in c["colors"]}
    named.update({"bg": c["bg"], "text": c["ink"], "accent": c["accent"], "on-accent": c["on_accent"],
                  "surface": c["surface"], "border": c["border"], "muted": c["muted"]})
    fb = c["fam_by_role"]
    fam_line = lambda role, fallback: (f'"{fb[role]["name"]}", {fb[role].get("fallback", fallback)}' if role in fb else fallback)
    th = ["/* Tailwind CSS v4 theme for this brand.", "   Usage (main CSS):  @import \"tailwindcss\";  @import \"./brand/tailwind.theme.css\";",
          "   Generates bg-accent, text-on-accent, border-border, font-display, text-h1, rounded-md, shadow-raised ... */", "@theme {"]
    th += [f"  --color-{k}: {v};" for k, v in named.items()]
    th += [f"  --font-display: {fam_line('display', 'Georgia, serif')};",
           f"  --font-body: {fam_line('body', 'system-ui, sans-serif')};",
           f"  --font-mono: {fam_line('mono', 'ui-monospace, monospace')};"]
    for s in c["typo"].get("scale", []):
        th.append(f"  --text-{slug(s['token'])}: {s['size'] / 16:g}rem;")
        if s.get("line"):
            th.append(f"  --text-{slug(s['token'])}--line-height: {s['line']};")
    th += [f"  --radius-{k}: {v}px;" for k, v in c["radius"].items()]
    th += [f"  --shadow-{slug(e['name'])}: {e['css']};" for e in c["elevation"]]
    th.append("}")
    w("tailwind.theme.css", "\n".join(th) + "\n"); made.append("tailwind.theme.css")

    # shadcn/ui + shadcn-vue theme: brand -> shadcn CSS variables (OKLCH), to paste into the
    # project's tailwindCssFile (replace shadcn's :root/.dark blocks). Map meaning, not names:
    # shadcn --primary = brand accent; shadcn --accent = subtle hover surface.
    def danger_hex():
        for x in c["colors"]:
            if re.search(r"danger|error|destructive", str(x.get("role", "")), re.I):
                return x["hex"]
        return "#b42318"
    ink, paper, acc, onacc = c["ink"], c["bg"], c["accent"], c["on_accent"]
    surf, bord, mut = c["surface"], c["border"], c["muted"]
    others = [x["hex"] for x in c["colors"] if x["hex"] not in (ink, paper, surf, bord, mut, acc)]
    charts = ([acc] + others + [mix(acc, paper, .45), mix(acc, ink, .4), mix(ink, paper, .5)])[:5]
    light = {
        "background": paper, "foreground": ink, "card": paper, "card-foreground": ink,
        "popover": paper, "popover-foreground": ink, "primary": acc, "primary-foreground": onacc,
        "secondary": surf, "secondary-foreground": ink, "muted": surf, "muted-foreground": mut,
        "accent": mix(surf, ink, .04), "accent-foreground": ink, "destructive": danger_hex(),
        "border": bord, "input": bord, "ring": acc,
        **{f"chart-{i + 1}": h for i, h in enumerate(charts)},
        "sidebar": surf, "sidebar-foreground": ink, "sidebar-primary": acc,
        "sidebar-primary-foreground": onacc, "sidebar-accent": mix(surf, ink, .07),
        "sidebar-accent-foreground": ink, "sidebar-border": bord, "sidebar-ring": acc,
    }
    # Derived dark mode: brand ink becomes the canvas; accent lightened until it reads on it.
    d_bg = mix(ink, "#000000", .15)
    d_card = mix(d_bg, paper, .06)
    d_acc = acc
    for t in (.15, .3, .45, .6):
        if contrast(d_acc, d_bg) >= 4.5:
            break
        d_acc = mix(acc, "#ffffff", t)
    d_onacc = d_bg if contrast(d_bg, d_acc) >= contrast(paper, d_acc) else paper
    dark = {
        "background": d_bg, "foreground": paper, "card": d_card, "card-foreground": paper,
        "popover": d_card, "popover-foreground": paper, "primary": d_acc, "primary-foreground": d_onacc,
        "secondary": mix(d_bg, paper, .12), "secondary-foreground": paper,
        "muted": mix(d_bg, paper, .12), "muted-foreground": mix(paper, d_bg, .35),
        "accent": mix(d_bg, paper, .14), "accent-foreground": paper,
        "destructive": mix(danger_hex(), "#ffffff", .25),
        "border": mix(d_bg, paper, .16), "input": mix(d_bg, paper, .2), "ring": d_acc,
        **{f"chart-{i + 1}": mix(h, "#ffffff", .2) for i, h in enumerate(charts)},
        "sidebar": d_card, "sidebar-foreground": paper, "sidebar-primary": d_acc,
        "sidebar-primary-foreground": d_onacc, "sidebar-accent": mix(d_bg, paper, .14),
        "sidebar-accent-foreground": paper, "sidebar-border": mix(d_bg, paper, .16), "sidebar-ring": d_acc,
    }
    status_tok = {}
    for x in c["colors"]:
        m = re.search(r"success|warning|info", str(x.get("role", "")), re.I)
        if m:
            status_tok[m.group(0).lower()] = x["hex"]
    rad_px = c["radius"].get("lg", c["radius"].get("md", 6))
    sh = ["/* shadcn theme for this brand - generated by brand_book.py kit.",
          "   Paste into the project's tailwindCssFile (see `npx shadcn@latest info`):",
          "   replace shadcn's :root and .dark blocks with these, and add the @theme inline block below",
          "   after shadcn's own. Keep shadcn's imports, @custom-variant dark and its @theme inline mapping.",
          "   .dark is DERIVED from the light palette - review it. */", "", ":root {",
          f"  --radius: {rad_px / 16:g}rem;"]
    sh += [f"  --{k}: {oklch(v)};" for k, v in light.items()]
    sh += [f"  --{k}: {oklch(v)};\n  --{k}-foreground: {oklch(ink if contrast(ink, v) >= contrast(paper, v) else paper)};"
           for k, v in status_tok.items()]
    sh += ["}", "", ".dark {"]
    sh += [f"  --{k}: {oklch(v)};" for k, v in dark.items()]
    sh += [f"  --{k}: {oklch(mix(v, '#ffffff', .25))};\n  --{k}-foreground: {oklch(d_bg)};" for k, v in status_tok.items()]
    sh += ["}", "", "@theme inline {",
           f"  --font-sans: {fam_line('body', 'system-ui, sans-serif')};",
           f"  --font-heading: {fam_line('display', 'Georgia, serif')};",
           f"  --font-mono: {fam_line('mono', 'ui-monospace, monospace')};"]
    sh += [f"  --color-{k}: var(--{k});\n  --color-{k}-foreground: var(--{k}-foreground);" for k in status_tok]
    sh += ["}", ""]
    w("shadcn-theme.css", "\n".join(sh)); made.append("shadcn-theme.css")

    # Tailwind v3 preset (legacy projects only; points at CSS vars so tokens.css stays the single source)
    col = {slug(x["name"]): f"var(--color-{slug(x['name'])})" for x in c["colors"]}
    col.update({k: f"var(--color-{k})" for k in ("bg", "text", "accent", "on-accent", "surface", "border", "muted")})
    preset = {"theme": {"extend": {
        "colors": col,
        "fontFamily": {k: [f"var(--font-{k})"] for k in ("display", "body", "mono")},
        "borderRadius": {k: f"var(--radius-{k})" for k in c["radius"]},
        "boxShadow": {slug(e["name"]): f"var(--shadow-{slug(e['name'])})" for e in c["elevation"]},
        "fontSize": {slug(s["token"]): f"var(--text-{slug(s['token'])})" for s in c["typo"].get("scale", [])},
    }}}
    w("tailwind.preset.js", "/** LEGACY - Tailwind CSS v3 projects only. On v4 (current) use tailwind.theme.css instead.\n"
                            " *  Requires tokens.css to be loaded. */\nmodule.exports = " + json.dumps(preset, indent=2) + ";\n")
    made.append("tailwind.preset.js")

    # logos
    lg = spec.get("logo", {})
    mark, word = prep_svg(lg.get("mark_svg", "")), prep_svg(lg.get("wordmark_svg", ""))
    variants = {"ink": c["ink"], "reversed": c["bg"], "accent": c["accent"]}
    for nm, svg in (("mark", mark), ("wordmark", word)):
        if not svg:
            continue
        w(f"logo/{nm}.svg", _bake(svg, "currentColor")); made.append(f"logo/{nm}.svg")
        for v, col_ in variants.items():
            w(f"logo/{nm}-{v}.svg", _bake(svg, col_)); made.append(f"logo/{nm}-{v}.svg")

    # favicon: mark on an accent tile
    png_note = ""
    src = mark or word
    if src:
        vb, _, inner = _svg_inner(src)
        x0, y0, vw, vh = (float(v) for v in re.split(r"[\s,]+", vb.strip()))
        s = 40 / max(vw, vh)
        tx, ty = 12 + (40 - vw * s) / 2 - x0 * s, 12 + (40 - vh * s) / 2 - y0 * s
        fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{c["accent"]}"/>'
               f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})" fill="{c["on_accent"]}">{inner.replace("currentColor", c["on_accent"])}</g></svg>')
        w("favicon.svg", fav); made.append("favicon.svg")
        try:
            import cairosvg  # optional
            for px, fn in ((32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")):
                cairosvg.svg2png(bytestring=fav.encode(), write_to=os.path.join(out, fn), output_width=px, output_height=px)
                made.append(fn)
        except Exception:
            png_note = "PNG sizes not generated (install `cairosvg`, or export favicon.svg at 32/180/512px)."

    # icons + sprite
    ic = spec.get("icons", {})
    lib, stroke = ic.get("library", "lucide"), ic.get("stroke")
    symbols, names = [], []
    for it in ic.get("items", []):
        svg = it.get("svg", "")
        if not svg and lib in ICON_LIBS and not offline:
            try:
                svg = fetch_icon(lib, it["name"], stroke)
            except Exception as ex:
                print(f"  icon '{it['name']}' skipped ({type(ex).__name__})", file=sys.stderr)
                continue
        if not svg:
            continue
        svg = _bake(prep_svg(svg), "currentColor")
        w(f"icons/{slug(it['name'])}.svg", svg); names.append(slug(it["name"]))
        vb, attrs, inner = _svg_inner(svg)
        paint = " ".join(re.findall(r'\b(?:fill|stroke|stroke-width|stroke-linecap|stroke-linejoin)="[^"]*"', attrs))
        symbols.append(f'<symbol id="i-{slug(it["name"])}" viewBox="{vb}"><g {paint}>{inner.strip()}</g></symbol>')
    if symbols:
        w("icons/sprite.svg", '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n' + "\n".join(symbols) + "\n</svg>\n")
        made += [f"icons/{n}.svg" for n in names] + ["icons/sprite.svg"]

    # demo page proving the kit works
    first = names[0] if names else ""
    sprite_inline = ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">' + "".join(symbols) + "</svg>") if symbols else ""
    icon_list = "".join(f'<li><svg class="icon" aria-hidden="true"><use href="#i-{n}"></use></svg>{E(next((i.get("label", i["name"]) for i in ic.get("items", []) if slug(i["name"]) == n), n))}</li>' for n in names)
    status_badges = "".join(f'<span class="badge badge-{s}">{E(s.replace("-", " "))}</span> ' for s, _ in status)
    demo = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(c['name'])} - kit demo</title>{fonts_tag}<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="components.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>body{{margin:0}}.wrap{{max-width:960px;margin:0 auto;padding:24px 16px}}header.top{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--color-border)}}
h1{{font-size:var(--text-h1,44px);line-height:1.08;margin:48px 0 12px}}p.lead{{font-size:19px;max-width:60ch}}.row{{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}}
ul.icons{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}ul.icons li{{display:flex;gap:10px;align-items:center}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin:24px 0}}</style></head><body>
<!-- sprite inlined so icons also work when opened from disk; on a server you can use href="icons/sprite.svg#i-name" -->
{sprite_inline}
<header class="top wrap"><a href="#" class="logo" aria-label="{E(c['name'])}">{word or mark}</a><a class="btn btn-secondary" href="#">Contact</a></header>
<main class="wrap">
<h1>{E(c['name'])}</h1><p class="lead">{E(spec.get('tagline', ''))}</p>
<div class="row"><button class="btn btn-primary">{('<svg class="icon" aria-hidden="true"><use href="#i-' + first + '"></use></svg>') if first else ''}Primary action</button><button class="btn btn-secondary">Secondary</button><a class="btn btn-link" href="#">Text link →</a></div>
<div class="grid"><div class="card"><h3>Card</h3><p>Built from components.css and tokens.css.</p>{status_badges}</div>
<label class="field">Email <input type="email" placeholder="you@example.com"><span class="hint">We reply within a day.</span></label></div>
<table class="table"><thead><tr><th>Item</th><th class="num">Amount</th></tr></thead><tbody><tr><td>Line one</td><td class="num">12,400</td></tr><tr><td><b>Total</b></td><td class="num"><b>12,400</b></td></tr></tbody></table>
<h2>Icons</h2><ul class="icons">{icon_list}</ul>
</main></body></html>"""
    w("demo.html", demo); made.append("demo.html")

    w("README.md", README.format(name=c["name"], fonts_tag=fonts_tag, first_icon=first or "name",
                                 icon_lib=lib, png_note=png_note,
                                 versions=", ".join(f"`{p}@{v}`" for p, v in VERSIONS_USED.items()) or "n/a (offline)"))
    made.append("README.md")
    return made


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    a = [x for x in sys.argv[1:] if x != "--offline"]
    if len(a) == 3 and a[0] == "kit":
        with open(a[1], encoding="utf-8") as fh:
            files = kit(json.load(fh), a[2], offline="--offline" in sys.argv)
        print(a[2])
        for f in files:
            print("  " + f)
    elif len(a) == 3 and a[0] == "build":
        with open(a[1], encoding="utf-8") as fh:
            spec = json.load(fh)
        out = build(spec, offline="--offline" in sys.argv)
        with open(a[2], "w", encoding="utf-8") as fh:
            fh.write(out)
        print(a[2])
        named = {c["name"]: c["hex"] for c in spec.get("colors", [])}
        for p in spec.get("pairings", []):
            if p[0] in named and p[1] in named:
                r = contrast(named[p[0]], named[p[1]])
                print(f"  {p[0]} on {p[1]}: {r:.2f}:1 {grade(r)}")
    else:
        print(__doc__)
        sys.exit(2)
