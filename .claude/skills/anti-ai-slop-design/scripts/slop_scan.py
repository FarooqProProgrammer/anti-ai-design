#!/usr/bin/env python3
"""Heuristic scanner for common "AI slop" UI tells in front-end source files.

Usage:
    python slop_scan.py <file-or-dir> [more paths...] [--json]

Findings are leads, not verdicts: a flagged pattern may be an intentional choice.
The scanner cannot judge composition (layout rhythm, hierarchy, focal point) --
review those by eye using references/slop-catalog.md.
"""
import json
import os
import re
import sys

EXTS = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx",
        ".ts", ".tsx", ".vue", ".svelte", ".astro", ".mdx"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", "out",
             "coverage", ".svelte-kit", "vendor"}

SLOP_PURPLES = r"(?:#6366f1|#4f46e5|#818cf8|#8b5cf6|#7c3aed|#a78bfa|#a855f7|#9333ea|#c084fc|#d946ef|#ec4899)"

# (id, category, weight, regex, message)
RULES = [
    ("purple-gradient", "color", 3,
     re.compile(r"(?:from|via|to)-(?:indigo|violet|purple|fuchsia)-\d{2,3}", re.I),
     "Indigo/violet/purple gradient stop (Tailwind) - the classic AI palette"),
    ("purple-gradient-css", "color", 3,
     re.compile(r"gradient\([^)]*" + SLOP_PURPLES, re.I),
     "CSS gradient using the default indigo/violet/pink hexes"),
    ("slop-hex", "color", 1,
     re.compile(SLOP_PURPLES, re.I),
     "Default Tailwind indigo/violet hex used as a color"),
    ("gradient-text", "color", 3,
     re.compile(r"bg-clip-text|background-clip:\s*text|-webkit-background-clip:\s*text", re.I),
     "Gradient-filled text (usually on the hero headline)"),
    ("glassmorphism", "effects", 2,
     re.compile(r"backdrop-blur|backdrop-filter:\s*blur", re.I),
     "Glassmorphism / backdrop blur"),
    ("blob", "effects", 2,
     re.compile(r"blur-(?:2xl|3xl)|filter:\s*blur\(\s*(?:[4-9]\d|\d{3,})px", re.I),
     "Large blur - often decorative gradient blobs/orbs"),
    ("glow", "effects", 2,
     re.compile(r"shadow-\[0_0_|box-shadow:\s*0\s+0\s+\d{2,}px|drop-shadow-\[0_0_|shadow-(?:indigo|violet|purple|fuchsia)-\d", re.I),
     "Colored glow shadow"),
    ("hover-scale", "motion", 1,
     re.compile(r"hover:scale-1(?:0[2-9]|1\d)|:hover[^{]*\{[^}]*transform:\s*scale\(1\.0[2-9]", re.I),
     "Hover scale-up (often applied to everything)"),
    ("transition-all", "motion", 1,
     re.compile(r"\btransition-all\b|transition:\s*all\b", re.I),
     "transition: all - motion without a target"),
    ("decor-anim", "motion", 1,
     re.compile(r"animate-(?:pulse|bounce|ping)\b", re.I),
     "Pulse/bounce/ping animation (check it isn't decorative)"),
    ("default-font", "type", 1,
     re.compile(r"(?:font-family:\s*['\"]?|family=|['\"])(?:Inter|Roboto|Open[ +]Sans|Poppins|Montserrat|Lato)\b(?![ +-]?(?:Tight|Flex|Serif|Mono|Slab))", re.I),
     "Default font (Inter/Roboto/Open Sans/Poppins/Montserrat/Lato) - fine as body with a reason, a tell if it's the only face"),
    ("emoji", "icons", 2,
     re.compile("[\U0001F300-\U0001FAFF✨⚡✅⭐❤]"),
     "Emoji (likely used as an icon or decoration)"),
    ("hype-copy", "copy", 2,
     re.compile(r"\b(?:unlock|supercharge[ds]?|elevate|empower(?:s|ing)?|revolutioni[sz]e|unleash|harness|"
                r"seamless(?:ly)?|effortless(?:ly)?|cutting[- ]edge|next[- ]level|game[- ]changer|"
                r"all[- ]in[- ]one platform|take your \w+ to the next|built for the future|"
                r"journey starts|transform (?:your|the way))\b", re.I),
     "Hype / filler marketing copy"),
    ("placeholder", "copy", 2,
     re.compile(r"\b(?:lorem ipsum|john doe|jane doe|jane smith|acme(?: inc| corp)?|techcorp|"
                r"example\.com)\b", re.I),
     "Placeholder names/content"),
    ("hundred-vh", "responsive", 1,
     re.compile(r"(?<![\w-])h-screen\b|(?:min-)?height:\s*100vh", re.I),
     "100vh / h-screen - jumps with mobile browser bars; use 100svh/100dvh or min-height"),
    ("fixed-width", "responsive", 2,
     re.compile(r"(?<![-\w(])width:\s*(?:[5-9]\d{2}|[1-9]\d{3,})px|\bw-\[(?:[5-9]\d{2}|[1-9]\d{3,})px\]", re.I),
     "Fixed pixel width >= 500px - breaks on phones; use max-width / min() / fluid units"),
    ("zoom-disabled", "responsive", 2,
     re.compile(r"user-scalable\s*=\s*(?:no|0)|maximum-scale\s*=\s*1(?:\.0)?\b", re.I),
     "Pinch-zoom disabled in viewport meta - accessibility failure"),
    ("generic-heading", "copy", 1,
     re.compile(r">\s*(?:Why Choose Us|How It Works|Our Features|Get Started Today|Ready to get started\??)\s*<", re.I),
     "Label-style generic heading"),
]

# Density rules: flagged only when the count in a file crosses a threshold.
DENSITY = [
    ("rounded-everywhere", "components", 2,
     re.compile(r"rounded-(?:2xl|3xl|full)\b|border-radius:\s*(?:1[6-9]|[2-9]\d)px", re.I), 8,
     "Heavy rounding on many elements"),
    ("shadow-everywhere", "components", 1,
     re.compile(r"shadow-(?:xl|2xl)\b", re.I), 5,
     "Large shadows on many elements (everything is a floating card)"),
    ("centered-everywhere", "layout", 1,
     re.compile(r"\btext-center\b|text-align:\s*center", re.I), 8,
     "Lots of centered text"),
    ("three-col-grid", "layout", 1,
     re.compile(r"grid-cols-3\b|md:grid-cols-3\b|lg:grid-cols-3\b|repeat\(3,\s*1fr\)", re.I), 2,
     "Multiple 3-column grids (the 3-feature-card pattern)"),
]


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for f in files:
                    if os.path.splitext(f)[1].lower() in EXTS:
                        yield os.path.join(root, f)


def scan_file(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        return [], {"error": str(e)}
    findings = []
    for i, line in enumerate(lines, 1):
        for rid, cat, w, rx, msg in RULES:
            m = rx.search(line)
            if m:
                findings.append({"rule": rid, "category": cat, "weight": w, "line": i,
                                 "match": m.group(0), "message": msg})
    text = "\n".join(lines)
    ext = os.path.splitext(path)[1].lower()

    def file_finding(rid, w, match, msg):
        findings.append({"rule": rid, "category": "responsive", "weight": w, "line": None,
                         "match": match, "message": msg})

    if ext in (".html", ".htm") and re.search(r"<html|<head", text, re.I) \
            and not re.search(r"<meta[^>]+name=[\"']viewport", text, re.I):
        file_finding("no-viewport", 3, "no <meta name=viewport>",
                     "Missing viewport meta - page renders as a zoomed-out desktop site on phones")
    max_q = len(re.findall(r"@media[^{]*max-width", text, re.I))
    min_q = len(re.findall(r"@media[^{]*min-width", text, re.I))
    if max_q >= 2 and max_q > min_q:
        file_finding("desktop-first", 2, f"{max_q} max-width vs {min_q} min-width queries",
                     "Desktop-first media queries - write mobile base styles and enhance with min-width")
    if ext in (".html", ".htm", ".css", ".scss", ".vue", ".svelte", ".astro") \
            and re.search(r"display:\s*(?:grid|flex)|class=\"[^\"]*\b(?:grid|flex)\b", text) \
            and not re.search(r"@media|@container|\b(?:sm|md|lg|xl):|clamp\(|auto-fit|auto-fill", text, re.I):
        file_finding("no-responsive", 2, "no media/container queries, breakpoints, clamp() or auto-fit",
                     "Layout has no responsive behaviour at all")
    for rid, cat, w, rx, threshold, msg in DENSITY:
        n = len(rx.findall(text))
        if n >= threshold:
            findings.append({"rule": rid, "category": cat, "weight": w, "line": None,
                             "match": f"{n} occurrences", "message": msg})
    return findings, {}


def main(argv):
    try:  # Windows consoles default to cp1252, which can't print emoji matches
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]
    if not paths:
        print(__doc__)
        return 2
    report = {}
    for f in iter_files(paths):
        findings, err = scan_file(f)
        if findings or err:
            report[f] = {"findings": findings, **err}

    # Score: distinct rules hit (weighted), so one repeated tell doesn't dominate.
    hit = {}
    for data in report.values():
        for fd in data["findings"]:
            hit[fd["rule"]] = fd["weight"]
    score = sum(hit.values())
    distinct = len(hit)
    if distinct <= 2:
        verdict = "low - check flagged items are intentional"
    elif distinct <= 5:
        verdict = "medium - reads as template in places"
    else:
        verdict = "high - needs a design point of view, not patching"

    if as_json:
        print(json.dumps({"score": score, "distinct_tells": distinct, "verdict": verdict,
                          "files": report}, indent=2))
        return 0

    if not report:
        print("No slop tells detected by the scanner. Still review composition and copy by eye.")
        return 0
    for f, data in report.items():
        print(f"\n{f}")
        if data.get("error"):
            print(f"  ! {data['error']}")
        # Collapse repeated hits of the same rule per file.
        grouped = {}
        for fd in data["findings"]:
            grouped.setdefault(fd["rule"], []).append(fd)
        for rid, fds in sorted(grouped.items(), key=lambda kv: -kv[1][0]["weight"]):
            lines = [str(x["line"]) for x in fds if x["line"]]
            where = f"lines {', '.join(lines[:8])}{' ...' if len(lines) > 8 else ''}" if lines else fds[0]["match"]
            sample = fds[0]["match"] if lines else ""
            print(f"  [{fds[0]['category']}] {rid}: {fds[0]['message']} ({where})"
                  + (f'  e.g. "{sample}"' if sample else ""))
    print(f"\nDistinct tells: {distinct}  |  weighted score: {score}  |  slop level: {verdict}")
    print("Scanner can't judge layout rhythm, hierarchy or copy tone - review those by eye.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
