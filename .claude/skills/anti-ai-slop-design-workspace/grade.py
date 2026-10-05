"""Programmatic grader for anti-ai-slop-design iteration runs.
Usage: python grade.py <iteration-dir>
Writes grading.json into each <eval>/<config>/ directory.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(HERE, "..", "anti-ai-slop-design", "scripts", "slop_scan.py")
EMOJI = re.compile("[\U0001F300-\U0001FAFF✨⚡✅⭐]")
HYPE = re.compile(r"\b(unlock|supercharge|elevate|empower|revolutioni[sz]e|unleash|seamless(ly)?|effortless(ly)?|cutting[- ]edge|next[- ]level|game[- ]changer)\b", re.I)
PURPLE = re.compile(r"(from|via|to)-(indigo|violet|purple|fuchsia)-\d|gradient\([^)]*(#6366f1|#8b5cf6|#a855f7|#7c3aed|#818cf8|#c084fc)", re.I)


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def scan(p):
    if not os.path.exists(p):
        return None
    out = subprocess.run([sys.executable, SCAN, p, "--json"], capture_output=True, text=True, encoding="utf-8")
    return json.loads(out.stdout)


def chk(text, ok, ev):
    return {"text": text, "passed": bool(ok), "evidence": ev}


def strip_tags(html):
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def grade_build(out):
    p = os.path.join(out, "index.html"); h = read(p); s = scan(p)
    vis = strip_tags(h)
    dom = [w for w in ["FBR", "NTN", "filer", "Payoneer", "Wise", "Upwork", "Fiverr", "PKR", "Rs", "IRIS", "PSEB", "return"] if re.search(r"\b" + w + r"\b", vis)]
    fonts = re.findall(r"family=([A-Za-z+]+)", h)
    tells = s["distinct_tells"] if s else 99
    return [
        chk("index.html exists", bool(h), p),
        chk("Scanner finds <=3 distinct slop tells", tells <= 3, f"{tells} distinct tells" + (f": {sorted({f['rule'] for d in s['files'].values() for f in d['findings']})}" if s else "")),
        chk("No indigo/violet/purple gradient", not PURPLE.search(h), (PURPLE.search(h) or [None])[0] or "none"),
        chk("No emoji in page", not EMOJI.search(h), (EMOJI.search(h) or [None])[0] or "none"),
        chk("No hype copy words", not HYPE.search(vis), (HYPE.search(vis) or [None])[0] or "none"),
        chk("Copy uses >=3 concrete domain terms", len(dom) >= 3, ", ".join(dom)),
        chk("Uses CSS custom properties (tokens)", "--" in h and "var(--" in h, f"{h.count('var(--')} var() uses"),
        chk("Loads a display font other than Inter", any(f.split("+")[0] != "Inter" for f in fonts), ", ".join(fonts) or "no Google font"),
    ]


def grade_audit(out):
    r = read(os.path.join(out, "response.md")); lo = r.lower()
    has = lambda *ws: any(w in lo for w in ws)
    return [
        chk("Calls out purple/indigo gradient palette", has("purple", "indigo", "violet"), ""),
        chk("Calls out gradient text", has("gradient text", "bg-clip-text", "gradient headline", "gradient-filled", "clip-text"), ""),
        chk("Calls out emoji icons", has("emoji"), ""),
        chk("Calls out hype copy (e.g. Unlock/Supercharge)", has("unlock", "supercharge", "seamless", "hype", "buzzword"), ""),
        chk("Calls out the template layout / 3-card grid", has("three cards", "3 cards", "three-card", "3-card", "three feature", "template", "grid-cols-3"), ""),
        chk("Calls out placeholder/fake testimonials", has("john doe", "techcorp", "placeholder", "fake"), ""),
        chk("Gives an explicit priority / what to change first", has("first", "priority", "start with", "#1", "1."), ""),
        chk("References specific locations (lines/sections)", bool(re.search(r"line\s*\d+|lines?\s+\d+|`[^`]*class|hero|nav", lo)), ""),
        chk("Proposes a direction grounded in plants", has("soil", "leaf", "botanical", "green", "garden", "terracotta", "photo"), ""),
    ]


def grade_fix(out):
    p = os.path.join(out, "dashboard.html"); h = read(p); s = scan(p); r = read(os.path.join(out, "response.md"))
    vis = strip_tags(h).lower()
    tells = s["distinct_tells"] if s else 99
    return [
        chk("dashboard.html exists", bool(h), p),
        chk("Scanner finds <=3 distinct slop tells", tells <= 3, f"{tells} distinct tells" + (f": {sorted({f['rule'] for d in s['files'].values() for f in d['findings']})}" if s else "")),
        chk("No emoji", not EMOJI.search(h), (EMOJI.search(h) or [None])[0] or "none"),
        chk("No glassmorphism or glow", not re.search(r"backdrop-filter|backdrop-blur|box-shadow:\s*0\s+0\s+\d{2,}px", h, re.I), ""),
        chk("Surfaces coverage gaps / open shifts", any(w in vis for w in ["unfilled", "gap", "open shift", "short", "uncovered", "understaffed"]), ""),
        chk("No John Doe / Jane Smith placeholders", not re.search(r"john doe|jane smith", vis), ""),
        chk("Response summarizes what changed", len(r) > 200, f"{len(r)} chars"),
    ]


GRADERS = {"build-tax-landing": grade_build, "audit-plantly": grade_audit, "fix-shiftboard": grade_fix}

if __name__ == "__main__":
    it = sys.argv[1]
    import glob
    for ev, fn in GRADERS.items():
        for d in sorted(glob.glob(os.path.join(it, f"eval-*-{ev}", "*", "run-*"))):
            if not os.path.isdir(os.path.join(d, "outputs")):
                continue
            cfg = os.path.basename(os.path.dirname(d))
            exps = fn(os.path.join(d, "outputs"))
            passed = sum(e["passed"] for e in exps)
            g = {"expectations": exps, "summary": {"passed": passed, "failed": len(exps) - passed, "total": len(exps), "pass_rate": round(passed / len(exps), 3)}}
            json.dump(g, open(os.path.join(d, "grading.json"), "w"), indent=2)
            print(f"{ev:20} {cfg:14} {passed}/{len(exps)}")
