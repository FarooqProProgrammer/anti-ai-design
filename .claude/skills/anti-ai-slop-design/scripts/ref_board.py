#!/usr/bin/env python3
"""Helpers for the reference hunt (see references/web-references.md).

Usage:
    python ref_board.py fetch <page-or-image-url> <outdir> [--name NAME]
        Saves the page's og:image / twitter:image (or the image itself if the URL
        is an image) into <outdir>. Prints the saved path, or an error.

    python ref_board.py board <refs.json> <out.html>
        Renders the reference board as one HTML file:
          1. Overview  - every reference ranked overall (thumbnail, scores, notes)
          2. Modules   - for each module (hero, typography, pricing...), how every
                         reference handles it, ranked per module, with a pick control
          3. Pick bar  - the user's per-module choices + "Copy choices" button
        Starting template: assets/example-refs.json (rendered: assets/example-board.html).

refs.json schema:
{
  "brief": {"subject": "...", "audience": "...", "traits": ["..", "..", ".."],
            "content_shape": "...", "must_haves": ["..."], "constraints": ["..."]},
  "modules": [                      # what the user will pick a reference FOR
    {"key": "hero", "label": "Hero", "need": "what the brief needs from this module"}
  ],
  "refs": [
    {
      "id": 1,
      "title": "Site or screen name",
      "url": "https://...",
      "source": "land-book | mobbin | fontsinuse | ...",
      "image": "relative/or/absolute/path.png or https://...",   # optional
      "seen": true,               # false = ranked on description only
      "direction": "editorial ledger",
      "scores": {"fit": 5, "traits": 4, "content": 4, "distinct": 4, "feasible": 5, "constraints": 4},
      "signature": "numeral-led hero",
      "borrow": "ruled tables, one green accent",
      "watch_out": "stock photography",
      "notes": "type: high-contrast serif display + grotesk body; 90% bone / 2% green",
      "modules": {                # how THIS reference handles each module (omit if it has none)
        "hero": {"score": 4, "note": "giant serif numeral + one-line claim", "image": "optional crop"}
      }
    }
  ]
}
Image paths are relative to refs.json. Totals are computed here (weights 3,3,2,2,1,1,
out of 5). Per module, refs are sorted by module score; the top one is marked
"Recommended". A ref without an entry for a module is listed as "not shown".
"""
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

WEIGHTS = {"fit": 3, "traits": 3, "content": 2, "distinct": 2, "feasible": 1, "constraints": 1}
LABELS = {"fit": "Audience fit", "traits": "Traits", "content": "Content shape",
          "distinct": "Distinctive", "feasible": "Feasible", "constraints": "Constraints"}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
IMG_EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "image/gif": ".gif", "image/avif": ".avif"}


def _get(url, limit=15_000_000):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(limit), r.headers.get_content_type(), r.geturl()


def fetch(url, outdir, name=None):
    os.makedirs(outdir, exist_ok=True)
    data, ctype, final = _get(url)
    if not ctype.startswith("image/"):
        page = data.decode("utf-8", errors="replace")
        m = None
        for prop in ("og:image:secure_url", "og:image", "twitter:image", "twitter:image:src"):
            m = (re.search(r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]+content=["\']([^"\']+)' % re.escape(prop), page, re.I)
                 or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']%s["\']' % re.escape(prop), page, re.I))
            if m:
                break
        if not m:
            raise SystemExit(f"error: no og:image/twitter:image on {url} - take a screenshot with a browser tool instead")
        img_url = urllib.parse.urljoin(final, html.unescape(m.group(1)))
        data, ctype, _ = _get(img_url)
        if not ctype.startswith("image/"):
            raise SystemExit(f"error: preview URL {img_url} is not an image ({ctype})")
    base = name or re.sub(r"[^a-z0-9]+", "-", urllib.parse.urlparse(url).netloc.lower()).strip("-") or "ref"
    path = os.path.join(outdir, base + IMG_EXT.get(ctype, ".img"))
    i = 2
    while os.path.exists(path):
        path = os.path.join(outdir, f"{base}-{i}{IMG_EXT.get(ctype, '.img')}")
        i += 1
    with open(path, "wb") as fh:
        fh.write(data)
    print(path)


def total(ref):
    s = ref.get("scores", {})
    return round(sum(s.get(k, 0) * w for k, w in WEIGHTS.items()) / sum(WEIGHTS.values()), 2)


CSS = """
:root{--bg:#f4f1ea;--ink:#1d1b18;--muted:#6b665d;--rule:#d9d3c7;--accent:#1f5f4a;--accent-soft:#e3ece6;--card:#fbf9f4;--warn:#b3401f}
@media (prefers-color-scheme:dark){:root{--bg:#171614;--ink:#ece8df;--muted:#a39d91;--rule:#34312c;--accent:#6fbf9f;--accent-soft:#1f2e28;--card:#1f1d1a;--warn:#e07a5a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 ui-sans-serif,system-ui,sans-serif;padding:32px 16px 120px}
main{max-width:1180px;margin:0 auto}
h1{font:600 30px/1.1 Georgia,serif;margin:0 0 4px}
h2.sec{font:600 22px/1.2 Georgia,serif;margin:44px 0 4px;padding-top:16px;border-top:2px solid var(--ink)}
.lede{margin:0;color:var(--muted)}
.brief{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px 24px;border-block:1px solid var(--rule);padding:12px 0;margin:16px 0 8px}
dt{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}dd{margin:0 0 6px}
a{color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px;margin-top:16px}
article{background:var(--card);border:1px solid var(--rule);display:flex;flex-direction:column}
.thumb{display:block;aspect-ratio:16/10;background:var(--rule);overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.noimg{display:grid;place-items:center;height:100%;color:var(--muted);font-size:13px}
.body{padding:14px 16px 16px}
.hd{display:flex;align-items:baseline;gap:8px}
.hd h3{font-size:17px;margin:0;flex:1}
.rank{color:var(--muted);font-variant-numeric:tabular-nums}
.score{font:600 22px/1 ui-monospace,monospace;color:var(--accent)}
.dir{margin:4px 0 0;font-style:italic}
.src{margin:2px 0 10px;color:var(--muted);font-size:13px}
.warn{color:var(--warn);font-size:13px;margin:0 0 8px}
.bars{list-style:none;padding:0;margin:10px 0 0;display:grid;gap:3px;font-size:12px}
.bars li{display:grid;grid-template-columns:96px 1fr 14px;gap:8px;align-items:center}
.bars i{height:6px;background:linear-gradient(90deg,var(--accent) calc(var(--v)*20%),var(--rule) 0)}
.module{margin-top:28px}
.module>header{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px}
.module h3{font-size:18px;margin:0}
.module .need{margin:0;color:var(--muted);font-size:14px}
.opts{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:10px}
.opt{position:relative;display:flex;flex-direction:column;background:var(--card);border:1px solid var(--rule);cursor:pointer;transition:border-color .15s,box-shadow .15s}
.opt:hover{border-color:var(--muted)}
.opt:has(input:checked){border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent);background:var(--accent-soft)}
.opt input{position:absolute;top:10px;left:10px;width:18px;height:18px;accent-color:var(--accent);margin:0}
.opt input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.opt .mthumb{aspect-ratio:16/9;background:var(--rule);overflow:hidden}
.opt .mthumb img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.opt .mbody{padding:10px 12px 12px}
.opt .mt{display:flex;gap:6px;align-items:baseline;font-weight:600}
.opt .mt span:first-child{flex:1}
.opt .ms{font:600 15px ui-monospace,monospace;color:var(--accent)}
.opt p{margin:4px 0 0;font-size:13px}
.opt.absent{opacity:.55}
.badge{display:inline-block;font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);padding:0 6px;margin-top:6px}
.opt.none{justify-content:center;align-items:center;min-height:80px;color:var(--muted);font-size:14px}
.bar{position:fixed;left:0;right:0;bottom:0;background:var(--ink);color:var(--bg);padding:12px 16px}
.bar .in{max-width:1180px;margin:0 auto;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.bar .picks{flex:1;font-size:14px;min-width:0}
.bar button{font:600 14px system-ui,sans-serif;background:var(--bg);color:var(--ink);border:0;padding:10px 16px;cursor:pointer}
.bar button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.bar .count{font-variant-numeric:tabular-nums;opacity:.8;font-size:13px}
@media (max-width:560px){.bar .picks{display:none}}
"""

JS = """
const DATA = JSON.parse(document.getElementById('board-data').textContent);
const KEY = 'refboard:' + location.pathname;
const bar = document.querySelector('.bar .picks');
const count = document.querySelector('.bar .count');
function load(){try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return {}}}
function save(v){try{localStorage.setItem(KEY,JSON.stringify(v))}catch(e){}}
function picks(){const o={};document.querySelectorAll('.opts input:checked').forEach(i=>{o[i.name.slice(2)]=i.value});return o}
function label(id){const r=DATA.refs.find(r=>String(r.id)===String(id));return r?('#'+r.rank+' '+r.title):'none'}
function summary(){
  const p=picks();
  return DATA.modules.map(m=>m.label+': '+(p[m.key]?(p[m.key]==='none'?'none / decide later':label(p[m.key])):'(not picked)')).join('\\n');
}
function render(){
  const p=picks(); save(p);
  const done=DATA.modules.filter(m=>p[m.key]).length;
  count.textContent=done+' / '+DATA.modules.length+' modules picked';
  bar.textContent=DATA.modules.filter(m=>p[m.key]).map(m=>m.label+' → '+(p[m.key]==='none'?'none':label(p[m.key]))).join(' · ')||'Pick the best reference for each module below.';
}
const saved=load();
Object.entries(saved).forEach(([k,v])=>{const el=document.querySelector('input[name="m-'+k+'"][value="'+v+'"]');if(el)el.checked=true});
document.addEventListener('change',e=>{if(e.target.matches('.opts input'))render()});
document.getElementById('copy').addEventListener('click',async()=>{
  const text='My reference picks:\\n'+summary();
  const btn=document.getElementById('copy');
  try{await navigator.clipboard.writeText(text)}catch(e){
    const t=document.createElement('textarea');t.value=text;document.body.appendChild(t);t.select();
    try{document.execCommand('copy')}catch(_){}t.remove();
  }
  btn.textContent='Copied — paste it to Claude';setTimeout(()=>btn.textContent='Copy choices',2200);
});
render();
"""


def board(refs_path, out_path):
    with open(refs_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    refs = sorted(spec.get("refs", []), key=total, reverse=True)
    for i, r in enumerate(refs, 1):
        r["_rank"] = i
    modules = spec.get("modules", [])
    base = os.path.dirname(os.path.abspath(refs_path))
    out_dir = os.path.dirname(os.path.abspath(out_path))
    e = lambda x: html.escape(str(x if x is not None else ""))

    def img_src(p):
        if not p:
            return ""
        if re.match(r"https?://", p):
            return p
        ap = p if os.path.isabs(p) else os.path.join(base, p)
        return os.path.relpath(ap, out_dir).replace(os.sep, "/")

    def img_tag(p, cls):
        src = img_src(p)
        inner = f'<img src="{e(src)}" alt="" loading="lazy">' if src else '<div class="noimg">no image</div>'
        return f'<div class="{cls}">{inner}</div>'

    brief = spec.get("brief", {})
    brief_html = "".join(
        f"<div><dt>{e(k.replace('_', ' '))}</dt><dd>{e(', '.join(v) if isinstance(v, list) else v)}</dd></div>"
        for k, v in brief.items())

    # 1. Overview
    cards = []
    for r in refs:
        s = r.get("scores", {})
        bars = "".join(
            f'<li><span>{LABELS[k]}</span><i style="--v:{s.get(k, 0)}"></i><b>{s.get(k, "-")}</b></li>' for k in WEIGHTS)
        unseen = '' if r.get("seen", True) else '<p class="warn">Not seen — ranked on description only</p>'
        src = img_src(r.get("image"))
        thumb = f'<img src="{e(src)}" alt="" loading="lazy">' if src else '<div class="noimg">no image</div>'
        cards.append(f"""
<article id="ref-{e(r.get('id'))}">
  <a class="thumb" href="{e(r.get('url'))}" target="_blank" rel="noopener">{thumb}</a>
  <div class="body">
    <div class="hd"><span class="rank">#{r['_rank']}</span><h3>{e(r.get('title'))}</h3><span class="score">{total(r):.1f}</span></div>
    <p class="dir">{e(r.get('direction'))}</p>
    <p class="src">{e(r.get('source'))} · <a href="{e(r.get('url'))}" target="_blank" rel="noopener">open site</a></p>
    {unseen}
    <dl>
      <div><dt>Signature</dt><dd>{e(r.get('signature'))}</dd></div>
      <div><dt>Borrow</dt><dd>{e(r.get('borrow'))}</dd></div>
      <div><dt>Watch out</dt><dd>{e(r.get('watch_out'))}</dd></div>
      {f"<div><dt>Notes</dt><dd>{e(r.get('notes'))}</dd></div>" if r.get('notes') else ''}
    </dl>
    <ul class="bars">{bars}</ul>
  </div>
</article>""")

    # 2. Module by module
    mod_html = []
    for m in modules:
        k = m["key"]
        present = [r for r in refs if k in r.get("modules", {})]
        absent = [r for r in refs if k not in r.get("modules", {})]
        present.sort(key=lambda r: (r["modules"][k].get("score", 0), total(r)), reverse=True)
        opts = []
        for i, r in enumerate(present):
            mm = r["modules"][k]
            rec = '<span class="badge">Recommended</span>' if i == 0 else ''
            opts.append(f"""
<label class="opt">
  <input type="radio" name="m-{e(k)}" value="{e(r.get('id'))}" aria-label="{e(m.get('label'))}: {e(r.get('title'))}">
  {img_tag(mm.get('image') or r.get('image'), 'mthumb')}
  <div class="mbody">
    <div class="mt"><span>#{r['_rank']} {e(r.get('title'))}</span><span class="ms">{e(mm.get('score', '-'))}</span></div>
    <p>{e(mm.get('note'))}</p>
    {rec}
  </div>
</label>""")
        for r in absent:
            opts.append(f"""
<label class="opt absent">
  <input type="radio" name="m-{e(k)}" value="{e(r.get('id'))}" aria-label="{e(m.get('label'))}: {e(r.get('title'))}">
  <div class="mbody"><div class="mt"><span>#{r['_rank']} {e(r.get('title'))}</span></div><p>Not shown in this reference.</p></div>
</label>""")
        opts.append(f"""
<label class="opt none"><input type="radio" name="m-{e(k)}" value="none" aria-label="{e(m.get('label'))}: none">None / decide later</label>""")
        mod_html.append(f"""
<section class="module" id="mod-{e(k)}">
  <header><h3>{e(m.get('label'))}</h3><p class="need">{e(m.get('need'))}</p></header>
  <div class="opts">{''.join(opts)}</div>
</section>""")

    data = {"modules": [{"key": m["key"], "label": m.get("label", m["key"])} for m in modules],
            "refs": [{"id": r.get("id"), "title": r.get("title"), "rank": r["_rank"]} for r in refs]}
    data_json = json.dumps(data).replace("</", "<\\/")

    modules_section = f"""
<h2 class="sec">Module by module</h2>
<p class="lede">For each part of the page, pick the reference that handles it best. You can mix — e.g. hero from one, typography from another.</p>
{''.join(mod_html)}""" if modules else ""

    bar = f"""
<div class="bar" role="region" aria-label="Your picks"><div class="in">
  <div><div class="count"></div></div>
  <div class="picks"></div>
  <button id="copy" type="button">Copy choices</button>
</div></div>""" if modules else ""

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Reference Board</title>
<style>{CSS}</style></head><body><main>
<h1>Reference board</h1>
<p class="lede">Ranked against the brief.{' Pick the best reference for each module, then press “Copy choices” and paste the result to Claude.' if modules else ' Reply with the id(s) you want, or mix.'}</p>
<dl class="brief">{brief_html}</dl>
<h2 class="sec">Overview</h2>
<section class="grid">{''.join(cards)}</section>
{modules_section}
</main>
{bar}
<script type="application/json" id="board-data">{data_json}</script>
{f'<script>{JS}</script>' if modules else ''}
</body></html>"""
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(out_path)
    for r in refs:
        print(f"  #{r['_rank']}  {total(r):.1f}  [{r.get('id')}] {r.get('title')}")
    for m in modules:
        k = m["key"]
        best = max((r for r in refs if k in r.get("modules", {})),
                   key=lambda r: (r["modules"][k].get("score", 0), total(r)), default=None)
        print(f"  {m.get('label', k):<14} recommended: " + (f"#{best['_rank']} {best.get('title')}" if best else "-"))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "fetch":
        nm = a[a.index("--name") + 1] if "--name" in a else None
        try:
            fetch(a[1], a[2], nm)
        except SystemExit:
            raise
        except Exception as ex:  # network errors, 403s, timeouts
            raise SystemExit(f"error: {type(ex).__name__}: {ex}")
    elif len(a) == 3 and a[0] == "board":
        board(a[1], a[2])
    else:
        print(__doc__)
        sys.exit(2)
