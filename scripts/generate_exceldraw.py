#!/usr/bin/env python3
"""ExcelDraw / Excalidraw diagram generator and exporter.

Generates .exceldraw, .excalidraw, and .svg diagrams for each phase of the
AI Engineering Workflow, ensuring every step has a visual diagram with a
proper description.
"""

import json
import random
from pathlib import Path


class ExcelDrawBuilder:
    def __init__(self, title="Workflow Diagram", subtitle="AI Engineering Process"):
        self.elements = []
        self._id_counter = 1
        self.title = title
        self.subtitle = subtitle

    def _next_id(self, prefix="el"):
        res = f"{prefix}_{self._id_counter}"
        self._id_counter += 1
        return res

    def add_rect(self, x, y, w, h, bg_color="#ffffff", stroke_color="#1e1e1e", stroke_width=2, roundness=3):
        el_id = self._next_id("rect")
        self.elements.append({
            "id": el_id,
            "type": "rectangle",
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke_color,
            "backgroundColor": bg_color,
            "fillStyle": "solid",
            "strokeWidth": stroke_width,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": {"type": roundness} if roundness else None,
            "seed": random.randint(100000, 999999),
            "version": 1,
            "versionNonce": 1,
            "isDeleted": False,
            "boundElements": [],
            "updated": 1
        })
        return el_id

    def add_text(self, x, y, text, font_size=16, font_family=1, text_align="start", color="#1e1e1e"):
        el_id = self._next_id("text")
        lines = text.split("\n")
        line_height = font_size * 1.3
        total_height = len(lines) * line_height
        max_len = max(len(l) for l in lines) if lines else 1
        approx_width = max_len * (font_size * 0.6)

        self.elements.append({
            "id": el_id,
            "type": "text",
            "x": x,
            "y": y,
            "width": approx_width,
            "height": total_height,
            "angle": 0,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": None,
            "seed": random.randint(100000, 999999),
            "version": 1,
            "versionNonce": 1,
            "isDeleted": False,
            "text": text,
            "fontSize": font_size,
            "fontFamily": font_family,
            "textAlign": text_align,
            "verticalAlign": "top",
            "baseline": font_size,
            "containerId": None,
            "originalText": text,
            "lineHeight": 1.3,
            "updated": 1
        })
        return el_id

    def add_arrow(self, start_x, start_y, end_x, end_y, color="#495057", stroke_width=2):
        el_id = self._next_id("arrow")
        dx = end_x - start_x
        dy = end_y - start_y
        self.elements.append({
            "id": el_id,
            "type": "arrow",
            "x": start_x,
            "y": start_y,
            "width": max(1, abs(dx)),
            "height": max(1, abs(dy)),
            "angle": 0,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": stroke_width,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": {"type": 2},
            "seed": random.randint(100000, 999999),
            "version": 1,
            "versionNonce": 1,
            "isDeleted": False,
            "points": [[0, 0], [dx, dy]],
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "updated": 1
        })
        return el_id

    def add_banner(self, x=50, y=30, w=800, h=70):
        self.add_rect(x, y, w, h, bg_color="#f8f9fa", stroke_color="#343a40", stroke_width=2, roundness=3)
        self.add_text(x + 25, y + 14, self.title, font_size=20, color="#212529")
        self.add_text(x + 25, y + 42, self.subtitle, font_size=13, color="#6c757d")

    def build_json(self):
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements,
            "appState": {
                "gridSize": None,
                "viewBackgroundColor": "#ffffff"
            },
            "files": {}
        }

    def save(self, base_path: Path):
        base_path = Path(base_path)
        base_path.parent.mkdir(parents=True, exist_ok=True)
        data = self.build_json()

        # Save .exceldraw and .excalidraw
        exceldraw_path = base_path.with_suffix(".exceldraw")
        excalidraw_path = base_path.with_suffix(".excalidraw")
        svg_path = base_path.with_suffix(".svg")

        with open(exceldraw_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        with open(excalidraw_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self._export_svg(svg_path)
        print(f"Generated: {exceldraw_path.name}, {excalidraw_path.name}, {svg_path.name}")

    def _export_svg(self, svg_path: Path):
        if not self.elements:
            return
        min_x = min(el["x"] for el in self.elements) - 30
        min_y = min(el["y"] for el in self.elements) - 30
        max_x = max(el["x"] + el.get("width", 0) for el in self.elements) + 40
        max_y = max(el["y"] + el.get("height", 0) for el in self.elements) + 40

        width = int(max_x - min_x)
        height = int(max_y - min_y)

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {width} {height}" width="{width}" height="{height}" style="background-color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">',
            '<defs>',
            '  <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#495057" /></marker>',
            '  <marker id="arrowhead-red" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#e03131" /></marker>',
            '  <marker id="arrowhead-blue" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#1971c2" /></marker>',
            '  <marker id="arrowhead-green" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#2f9e44" /></marker>',
            '</defs>'
        ]

        for el in self.elements:
            el_type = el["type"]
            if el_type == "rectangle":
                rx = 8 if el.get("roundness") else 0
                svg_parts.append(
                    f'<rect x="{el["x"]}" y="{el["y"]}" width="{el["width"]}" height="{el["height"]}" rx="{rx}" '
                    f'fill="{el["backgroundColor"]}" stroke="{el["strokeColor"]}" stroke-width="{el["strokeWidth"]}" />'
                )
            elif el_type == "text":
                lines = el["text"].split("\n")
                font_size = el["fontSize"]
                line_height = font_size * 1.3
                tx = el["x"]
                svg_parts.append(f'<text x="{tx}" y="{el["y"] + font_size}" font-size="{font_size}" fill="{el["strokeColor"]}" font-weight="{"bold" if font_size >= 16 else "normal"}">')
                for i, line in enumerate(lines):
                    dy = "0" if i == 0 else f"{line_height}px"
                    escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    svg_parts.append(f'  <tspan x="{tx}" dy="{dy}">{escaped}</tspan>')
                svg_parts.append('</text>')
            elif el_type == "arrow":
                start_x = el["x"]
                start_y = el["y"]
                end_x = start_x + el["points"][-1][0]
                end_y = start_y + el["points"][-1][1]
                marker = "arrowhead-red" if el["strokeColor"] == "#e03131" else "arrowhead-blue" if el["strokeColor"] == "#1971c2" else "arrowhead-green" if el["strokeColor"] == "#2f9e44" else "arrowhead"
                svg_parts.append(
                    f'<line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" '
                    f'stroke="{el["strokeColor"]}" stroke-width="{el["strokeWidth"]}" marker-end="url(#{marker})" />'
                )

        svg_parts.append('</svg>')
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write("\n".join(svg_parts))


# ---------------------------------------------------------------------------
# Pre-built Phase Diagram Generators (Steps 1 to 6)
# ---------------------------------------------------------------------------

def create_step1_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 1: UNDERSTAND — Socratic Reconnaissance & Brainstorming", "Firewall Gate 1 | Applicable: Any Agent (Cursor / Claude / Codex)")
    b.add_banner(w=860)

    # 3 Parallel Columns: Brainstorming, Grill-Me, Code/Wiki Recon
    col_w = 265
    y = 120
    h = 320

    # Column 1: Brainstorming
    b.add_rect(50, y, col_w, h, bg_color="#e7f5ff", stroke_color="#1971c2", stroke_width=2)
    b.add_text(65, y + 15, "1. BRAINSTORMING SKILL", font_size=15, color="#1864ab")
    b.add_text(65, y + 45, "• Uncover the 'Why'\n• Define Goals & Non-Goals\n• Surface Anti-Goals\n• Propose 2-3 Approaches:\n  - Minimal / Simple\n  - Idiomatic / Extensible\n  - High Performance\n• Trade-off Analysis", font_size=12, color="#343a40")

    # Column 2: Grill-Me
    b.add_rect(345, y, col_w, h, bg_color="#fff4e6", stroke_color="#f76707", stroke_width=2)
    b.add_text(360, y + 15, "2. GRILL-ME SKILL", font_size=15, color="#d9480f")
    b.add_text(360, y + 45, "• Socratic Technical Interview\n• Decision-tree resolution\n• Round-by-round questioning\n• Challenge assumptions:\n  - Network / DB failure\n  - Empty states & edge limits\n  - Breaking contracts\n• Zero passive nodding", font_size=12, color="#343a40")

    # Column 3: Code & Wiki Recon
    b.add_rect(640, y, col_w, h, bg_color="#f3f0ff", stroke_color="#7950f2", stroke_width=2)
    b.add_text(655, y + 15, "3. CODE & WIKI RECON", font_size=15, color="#5f3dc4")
    b.add_text(655, y + 45, "• Query wiki/index.md (ADRs)\n• Index codebase & symbols\n• Trace call graph & data flow\n• Identify existing conventions:\n  - Error handling style\n  - State & schema patterns\n  - Naming & file hierarchy\n• READ-ONLY: 0 code edits", font_size=12, color="#343a40")

    # Bottom Output Box
    b.add_arrow(180, y + h, 480, 480, color="#1971c2")
    b.add_arrow(480, y + h, 480, 480, color="#f76707")
    b.add_arrow(770, y + h, 480, 480, color="#7950f2")

    b.add_rect(50, 480, 855, 90, bg_color="#ebfbee", stroke_color="#2f9e44", stroke_width=2)
    b.add_text(70, 492, "GATE 1 DELIVERABLE: RESOLVED CONTEXT SNAPSHOT", font_size=16, color="#2b8a3e")
    b.add_text(70, 520, "Input to Phase 2: Decided architecture, answered interview edge cases, documented patterns, and boundary constraints.", font_size=12, color="#495057")

    b.save(out_dir / "01-understand")


def create_step2_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 2: PLAN — Architecture Blueprint & Acceptance Criteria", "Firewall Gate 2 | Applicable: Any Agent (Cursor / Claude / Codex)")
    b.add_banner(w=860)

    y = 120
    # Step 2 Flow: Context Input -> Risk Assessment -> Acceptance Criteria -> Approval Gate
    b.add_rect(50, y, 250, 110, bg_color="#f8f9fa", stroke_color="#495057", stroke_width=2)
    b.add_text(65, y + 15, "1. INGEST & SCOPE", font_size=15, color="#212529")
    b.add_text(65, y + 40, "• Ingest RFCs/specs into raw/\n• Compile concepts into wiki/\n• Strict scope boundaries", font_size=12, color="#495057")

    b.add_arrow(300, y + 55, 350, y + 55, color="#495057")

    b.add_rect(350, y, 250, 110, bg_color="#fff4e6", stroke_color="#f76707", stroke_width=2)
    b.add_text(365, y + 15, "2. RISK MATRIX", font_size=15, color="#d9480f")
    b.add_text(365, y + 40, "• Failure mode analysis\n• Concurrency & race hazards\n• Mitigation for each risk", font_size=12, color="#495057")

    b.add_arrow(600, y + 55, 650, y + 55, color="#f76707")

    b.add_rect(650, y, 255, 110, bg_color="#e7f5ff", stroke_color="#1971c2", stroke_width=2)
    b.add_text(665, y + 15, "3. ACCEPTANCE CRITERIA", font_size=15, color="#1864ab")
    b.add_text(665, y + 40, "• Given-When-Then criteria\n• Edge-case assertions\n• 100% testable conditions", font_size=12, color="#495057")

    # Sequential Roadmap
    b.add_arrow(775, y + 110, 775, 270, color="#1971c2")
    b.add_rect(50, 270, 855, 120, bg_color="#e6fcf5", stroke_color="#0ca678", stroke_width=2)
    b.add_text(70, 285, "4. PHASED IMPLEMENTATION ROADMAP", font_size=16, color="#087f5b")
    b.add_text(70, 315, "Milestone 3.1: Data Models & Core Schemas  ➔  Milestone 3.2: Domain Logic & Services  ➔  Milestone 3.3: UI Wiring & Refinement", font_size=12, color="#212529")
    b.add_text(70, 345, "Each milestone specifies exact files to touch, test conditions to write, and verification checkpoints.", font_size=12, color="#495057")

    # Approval Gate Banner
    b.add_arrow(480, 390, 480, 430, color="#0ca678")
    b.add_rect(150, 430, 650, 70, bg_color="#fff5f5", stroke_color="#e03131", stroke_width=2)
    b.add_text(180, 442, "🛑 GATE 2 APPROVAL CHECKPOINT", font_size=16, color="#c92a2a")
    b.add_text(180, 468, "Coding is strictly BLOCKED until engineer reviews and signs off on this plan.", font_size=12, color="#495057")

    b.save(out_dir / "02-plan")


def create_step3_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 3: IMPLEMENT — Single Driver Principle & Scoped Refinement", "Firewall Gate 3 | Applicable: Cursor, Claude Code, or Codex")
    b.add_banner(w=860)

    y = 120
    # Left: Primary Driver
    b.add_rect(50, y, 400, 260, bg_color="#e6fcf5", stroke_color="#0ca678", stroke_width=2)
    b.add_text(70, y + 18, "PRIMARY DRIVER (Single Ownership)", font_size=16, color="#087f5b")
    b.add_text(70, y + 48, "Assigned Agent: Cursor, Claude Code, or Codex\n\n• Owns core business logic & domain models\n• Drives API endpoints, schemas & state store\n• Writes unit & integration tests alongside code\n• Adheres strictly to the approved Phase 2 plan\n• Prevents context fragmentation", font_size=12, color="#343a40")

    # Right: Secondary / Frontend Refinement
    b.add_rect(490, y, 415, 260, bg_color="#e7f5ff", stroke_color="#1971c2", stroke_width=2)
    b.add_text(510, y + 18, "INTERACTIVE & FRONTEND REFINEMENT", font_size=16, color="#1864ab")
    b.add_text(510, y + 48, "Assigned Agent: Cursor (or Primary Driver)\n\n• Scoped visual tweaks: CSS, Tailwind, layouts\n• Interactive UI states: hover, focus, animations\n• Real-time inline edits requested by engineer\n• BOUNDARY: Does NOT alter core domain logic\n• Maintains contract with Primary Driver", font_size=12, color="#343a40")

    # Coordination Arrow
    b.add_arrow(450, y + 130, 490, y + 130, color="#0ca678", stroke_width=2)

    # Bottom Implementation Hygiene
    b.add_rect(50, 420, 855, 80, bg_color="#f8f9fa", stroke_color="#495057", stroke_width=2)
    b.add_text(70, 432, "IMPLEMENTATION HYGIENE PROTOCOL", font_size=15, color="#212529")
    b.add_text(70, 458, "No speculative code • No unapproved refactoring • Atomic changes matching plan milestones.", font_size=12, color="#495057")

    b.save(out_dir / "03-implement")


def create_step4_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 4: VERIFY — Zero-Concealment Quality Validation Pipeline", "Firewall Gate 4 | Applicable: Any Agent + Test Runner")
    b.add_banner(w=860)

    # 4 Check stages horizontally
    y = 120
    cw = 195
    spacing = 25

    stages = [
        ("1. TYPECHECK", "• tsc --noEmit / mypy\n• 0 type errors\n• No 'any' leaks", "#e7f5ff", "#1971c2"),
        ("2. LINTER", "• eslint / ruff / fmt\n• 0 warnings\n• Style conformance", "#fff4e6", "#f76707"),
        ("3. TEST SUITE", "• Unit & integration\n• 100% tests green\n• Edge cases covered", "#e6fcf5", "#0ca678"),
        ("4. WIKI CHECK", "• check_evidence.py\n• Verifies literals\n• 0 suspect tolerance", "#f3f0ff", "#7950f2")
    ]

    for i, (st_title, st_desc, bg, stroke) in enumerate(stages):
        sx = 50 + i * (cw + spacing)
        b.add_rect(sx, y, cw, 130, bg_color=bg, stroke_color=stroke, stroke_width=2)
        b.add_text(sx + 15, y + 15, st_title, font_size=14, color=stroke)
        b.add_text(sx + 15, y + 45, st_desc, font_size=12, color="#343a40")
        if i < len(stages) - 1:
            b.add_arrow(sx + cw, y + 65, sx + cw + spacing, y + 65, color=stroke)

    # Runtime behavior validation
    b.add_arrow(480, y + 130, 480, 290, color="#0ca678")
    b.add_rect(50, 290, 855, 80, bg_color="#fff9db", stroke_color="#f59f00", stroke_width=2)
    b.add_text(70, 305, "5. RUNTIME BEHAVIORAL VERIFICATION", font_size=15, color="#e67700")
    b.add_text(70, 332, "Test actual flow manually or via E2E • Assert outputs directly against Phase 2 Acceptance Criteria.", font_size=12, color="#343a40")

    # Failure handling protocol
    b.add_rect(50, 400, 855, 90, bg_color="#fff5f5", stroke_color="#e03131", stroke_width=2)
    b.add_text(70, 412, "🛑 ZERO CONCEALMENT PROTOCOL (FAILURES MUST BE CAPTURED)", font_size=15, color="#c92a2a")
    b.add_text(70, 440, "Never skip, comment out, or suppress failing tests • Fix root causes in implementation • Never silence linter.", font_size=12, color="#495057")

    b.save(out_dir / "04-verify")


def create_step5_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 5: REVIEW INDEPENDENTLY — Read-Only Diff Audit", "Firewall Gate 5 | Applicable: Codex, Claude Code, or Cursor (Clean Context)")
    b.add_banner(w=860)

    y = 120
    # Left: Auditor input & mandate
    b.add_rect(50, y, 380, 250, bg_color="#f3f0ff", stroke_color="#7950f2", stroke_width=2)
    b.add_text(70, y + 18, "INDEPENDENT AUDITOR", font_size=16, color="#5f3dc4")
    b.add_text(70, y + 48, "Auditor: Clean Context / Second Agent\n\n• Input: Complete git diff + Phase 2 Plan\n• STRICT MANDATE: Review without editing\n• Auditor never modifies code files\n• Evaluates logic, security & edge cases\n• Checks acceptance criteria compliance", font_size=12, color="#343a40")

    # Right: Severity Findings & Triage
    b.add_rect(470, y, 435, 250, bg_color="#f8f9fa", stroke_color="#495057", stroke_width=2)
    b.add_text(490, y + 18, "SEVERITY TRIAGE MATRIX", font_size=16, color="#212529")
    b.add_text(490, y + 48, "🔴 HIGH / BLOCKER:\n  Bugs, regressions, unhandled crashes, security leaks\n\n🟡 MEDIUM:\n  Performance pitfalls, edge case gaps, code smells\n\n🟢 LOW / NIT:\n  Minor naming, comments, stylistic suggestions", font_size=12, color="#343a40")

    # Remediation Loop
    b.add_arrow(430, y + 125, 470, y + 125, color="#7950f2", stroke_width=2)
    b.add_rect(50, 400, 855, 90, bg_color="#ffe3e3", stroke_color="#e03131", stroke_width=2)
    b.add_text(70, 412, "REMEDIATION LOOP (Primary Driver Fixes & Re-Verifies)", font_size=15, color="#c92a2a")
    b.add_text(70, 440, "Primary Driver applies confirmed fixes ➔ Re-run Phase 4 (Verify) across all checks until 100% green.", font_size=12, color="#495057")

    b.save(out_dir / "05-review")


def create_step6_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 6: SHIP SAFELY — Release Pipeline & Knowledge Compounding", "Firewall Gate 6 | Applicable: Driver Agent + Lead Engineer")
    b.add_banner(w=860)

    y = 120
    cw = 185
    spacing = 38

    steps = [
        ("1. DIFF SANITY", "• git diff & status\n• No console.log\n• No temp files\n• Clean working tree", "#f8f9fa", "#495057"),
        ("2. BRANCH & COMMIT", "• Dedicated branch\n• Never direct to main\n• Conventional commit\n• feat/fix(<scope>): ...", "#e7f5ff", "#1971c2"),
        ("3. PR & CI/CD", "• Open Pull Request\n• Green status checks\n• Automated builds pass\n• Peer sign-off", "#e6fcf5", "#0ca678"),
        ("4. COMPOUND WIKI", "• Record ADR in wiki/\n• Update wiki/index.md\n• Append wiki/log.md\n• Permanent memory", "#fff4e6", "#f76707")
    ]

    for i, (st_title, st_desc, bg, stroke) in enumerate(steps):
        sx = 50 + i * (cw + spacing)
        b.add_rect(sx, y, cw, 140, bg_color=bg, stroke_color=stroke, stroke_width=2)
        b.add_text(sx + 15, y + 15, st_title, font_size=14, color=stroke)
        b.add_text(sx + 15, y + 45, st_desc, font_size=12, color="#343a40")
        if i < len(steps) - 1:
            b.add_arrow(sx + cw, y + 70, sx + cw + spacing, y + 70, color=stroke)

    # Protected Branch Gate Callout
    b.add_rect(50, 310, 855, 90, bg_color="#fff5f5", stroke_color="#e03131", stroke_width=2)
    b.add_text(70, 322, "🛑 PRODUCTION RELEASE GATES", font_size=16, color="#c92a2a")
    b.add_text(70, 350, "Direct commits to main/master are strictly blocked • CI pipeline must be 100% green before merge.", font_size=12, color="#495057")

    # Complete lifecycle summary
    b.add_rect(50, 430, 855, 70, bg_color="#ebfbee", stroke_color="#2f9e44", stroke_width=2)
    b.add_text(70, 442, "LIFECYCLE COMPLETE: ZERO REGRESSIONS, VERIFIED EVIDENCE & COMPOUNDED KNOWLEDGE", font_size=14, color="#2b8a3e")
    b.add_text(70, 468, "Every feature shipped leaves the codebase cleaner, safer, and better documented.", font_size=12, color="#495057")

    b.save(out_dir / "06-ship")


def main():
    out_dir = Path("d:/ai agent/the-developer/diagrams")
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Generating per-step ExcelDraw diagrams in:", out_dir)
    create_step1_diagram(out_dir)
    create_step2_diagram(out_dir)
    create_step3_diagram(out_dir)
    create_step4_diagram(out_dir)
    create_step5_diagram(out_dir)
    create_step6_diagram(out_dir)
    print("All 6 phase diagrams generated successfully!")


if __name__ == "__main__":
    main()
