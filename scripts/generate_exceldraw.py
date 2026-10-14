#!/usr/bin/env python3
"""ExcelDraw / Excalidraw diagram generator and exporter.

Generates .exceldraw, .excalidraw, and .svg diagrams for all 7 phases of the
Universal AI Engineering Workflow:
1. Understand -> 2. Spec -> 3. Plan -> 4. Implement -> 5. Verify -> 6. Review -> 7. Ship
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

        self.elements.append({
            "id": el_id,
            "type": "text",
            "x": x,
            "y": y,
            "width": max_len * (font_size * 0.6),
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

    def add_banner(self, x=50, y=30, w=860, h=70):
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
                    f'<rect x="{el["x"]}" y="{el["y"]}" width="{el["width"]}" height="{el["height"]}" '
                    f'fill="{el["backgroundColor"]}" stroke="{el["strokeColor"]}" stroke-width="{el["strokeWidth"]}" rx="{rx}" />'
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
# Pre-built Phase Diagram Generators (Steps 1 to 7 + Root)
# ---------------------------------------------------------------------------

def create_root_workflow_diagram(out_path: Path):
    b = ExcelDrawBuilder("UNIVERSAL 7-PHASE AI ENGINEERING WORKFLOW", "Request Firewall Admission & Quality Gates | Agent-Universal (Cursor, Claude Code, Codex, Antigravity)")
    b.add_banner(w=1120)

    # Top admission block: Contradiction Check
    b.add_rect(50, 115, 1120, 65, bg_color="#fff9db", stroke_color="#f59f00", stroke_width=2)
    b.add_text(70, 127, "🛡️ PRE-ADMISSION: CONTRADICTION CHECK", font_size=15, color="#f08c00")
    b.add_text(70, 150, "Match input with wiki/ & docs -> If contradictory, HALT & RETURN conflict. Only proceed if consistent or clarified.", font_size=12, color="#495057")

    # 7 Sequential Phase Columns
    y = 200
    col_w = 145
    spacing = 18
    phases = [
        ("1. UNDERSTAND", "• Brainstorming\n• Grill-Me interview\n• Code exploration\n• wiki/ & cursor log\n• READ-ONLY", "#e7f5ff", "#1971c2"),
        ("2. SPEC", "• Functional Spec\n• Technical contracts\n• API & Data schemas\n• Non-functional limits\n• Sign-off WHAT", "#f3f0ff", "#7950f2"),
        ("3. PLAN", "• Risk & mitigations\n• Given-When-Then AC\n• Phased milestones\n• Single driver pick\n• Sign-off HOW", "#fff4e6", "#f76707"),
        ("4. IMPLEMENT", "• Single Driver owner\n• Loop: Spec➔Plan➔Impl\n• /find-skills for gaps\n• Dispatch parallel\n• Plan fidelity", "#e6fcf5", "#0ca678"),
        ("5. VERIFY", "• Typecheck & linters\n• Automated test run\n• Runtime validation\n• check_evidence.py\n• Zero concealment", "#ebfbee", "#2f9e44"),
        ("6. REVIEW", "• Fresh context audit\n• Final git diff check\n• Security & bugs\n• REVIEW ONLY\n• Driver fixes", "#ffe3e3", "#e03131"),
        ("7. SHIP SAFELY", "• Clean git status\n• Feature branch only\n• Conventional commit\n• CI/CD pass\n• Compound wiki/", "#f8f9fa", "#343a40")
    ]

    for i, (title, desc, bg, stroke) in enumerate(phases):
        x = 50 + i * (col_w + spacing)
        b.add_rect(x, y, col_w, 220, bg_color=bg, stroke_color=stroke, stroke_width=2)
        b.add_text(x + 10, y + 15, title, font_size=13, color=stroke)
        b.add_text(x + 10, y + 45, desc, font_size=11, color="#343a40")
        if i < len(phases) - 1:
            b.add_arrow(x + col_w, y + 110, x + col_w + spacing, y + 110, color=stroke)

    # Bottom summary block with Implementation Loop Callout
    b.add_rect(50, 440, 1120, 80, bg_color="#f8f9fa", stroke_color="#495057", stroke_width=2)
    b.add_text(70, 452, "🔄 IMPLEMENTATION LOOP GATE (Implement ➔ Loop ➔ Spec ➔ Plan ➔ Implement)", font_size=14, color="#099268")
    b.add_text(70, 477, "If multiple tasks or domain gaps emerge: /find-skills installs missing tools ➔ Dispatch parallel agents ➔ Each follows Spec ➔ Plan ➔ Implement under Single Driver.", font_size=11, color="#495057")

    b.save(out_path / "workflow")


def create_step1_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 1: UNDERSTAND — Socratic Reconnaissance & Brainstorming", "Firewall Gate 1 | Applicable: Any Agent (Cursor / Claude / Codex)")
    b.add_banner(w=860)

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
    b.add_text(655, y + 45, "• Query wiki/index.md (ADRs)\n• Check .cursor/projects context\n• Index codebase & symbols\n• Trace call graph & data flow\n• Identify existing conventions\n• READ-ONLY: 0 code edits", font_size=12, color="#343a40")

    b.add_arrow(180, y + h, 480, 480, color="#1971c2")
    b.add_arrow(480, y + h, 480, 480, color="#f76707")
    b.add_arrow(770, y + h, 480, 480, color="#7950f2")

    b.add_rect(50, 480, 855, 90, bg_color="#ebfbee", stroke_color="#2f9e44", stroke_width=2)
    b.add_text(70, 492, "GATE 1 DELIVERABLE: RESOLVED CONTEXT SNAPSHOT", font_size=16, color="#2b8a3e")
    b.add_text(70, 520, "Input to Phase 2 (Spec): Decided architectural approach, answered interview edge cases, documented patterns, and boundary constraints.", font_size=12, color="#495057")

    b.save(out_dir / "01-understand")


def create_step2_spec_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 2: SPEC — Technical & Functional Specification", "Firewall Gate 2 | Applicable: Any Agent (Cursor / Claude / Codex)")
    b.add_banner(w=860)

    col_w = 265
    y = 120
    h = 320

    # Column 1: Functional Spec
    b.add_rect(50, y, col_w, h, bg_color="#f3f0ff", stroke_color="#7950f2", stroke_width=2)
    b.add_text(65, y + 15, "1. FUNCTIONAL SPEC", font_size=15, color="#5f3dc4")
    b.add_text(65, y + 45, "• User Journeys & Workflows\n• Behavioral Invariants\n• Input / Output Contracts\n• State Machine Transitions\n• UI / UX Interactions\n• Explicit Non-Features", font_size=12, color="#343a40")

    # Column 2: Technical & Data Contracts
    b.add_rect(345, y, col_w, h, bg_color="#e7f5ff", stroke_color="#1971c2", stroke_width=2)
    b.add_text(360, y + 15, "2. DATA & API SCHEMAS", font_size=15, color="#1864ab")
    b.add_text(360, y + 45, "• TypeScript Types & Schemas\n• Database Entity Models\n• API Payloads & Status Codes\n• Error Response Formats\n• External RFCs into raw/\n• Grounded in wiki/", font_size=12, color="#343a40")

    # Column 3: Non-Functional Guardrails
    b.add_rect(640, y, col_w, h, bg_color="#fff9db", stroke_color="#f59f00", stroke_width=2)
    b.add_text(655, y + 15, "3. SYSTEM GUARDRAILS", font_size=15, color="#f08c00")
    b.add_text(655, y + 45, "• Latency & Performance Budgets\n• Security & Auth Requirements\n• Concurrency Invariants\n• Backward Compatibility\n• Breaking Change Policies\n• Rate Limits & Scaling", font_size=12, color="#343a40")

    b.add_arrow(180, y + h, 480, 480, color="#7950f2")
    b.add_arrow(480, y + h, 480, 480, color="#1971c2")
    b.add_arrow(770, y + h, 480, 480, color="#f59f00")

    b.add_rect(50, 480, 855, 90, bg_color="#ebfbee", stroke_color="#2f9e44", stroke_width=2)
    b.add_text(70, 492, "GATE 2 DELIVERABLE: APPROVED SPECIFICATION DOCUMENT (WHAT, NOT HOW)", font_size=16, color="#2b8a3e")
    b.add_text(70, 520, "Human sign-off on contracts, schemas, and invariants before planning milestones in Phase 3. READ-ONLY on source code.", font_size=12, color="#495057")

    b.save(out_dir / "02-spec")


def create_step3_plan_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 3: PLAN — Implementation Blueprint & Acceptance Criteria", "Firewall Gate 3 | Applicable: Any Agent (Cursor / Claude / Codex)")
    b.add_banner(w=860)

    y = 120
    b.add_rect(50, y, 250, 110, bg_color="#f8f9fa", stroke_color="#495057", stroke_width=2)
    b.add_text(65, y + 15, "1. SCOPE FROM SPEC", font_size=15, color="#212529")
    b.add_text(65, y + 40, "• Ingest approved Phase 2 spec\n• Confirm scope boundaries\n• Zero ambiguity on contracts", font_size=12, color="#495057")

    b.add_arrow(300, y + 55, 350, y + 55, color="#495057")

    b.add_rect(350, y, 250, 110, bg_color="#fff4e6", stroke_color="#f76707", stroke_width=2)
    b.add_text(365, y + 15, "2. RISK MATRIX", font_size=15, color="#d9480f")
    b.add_text(365, y + 40, "• Failure mode analysis\n• Concurrency & race hazards\n• Mitigation for each risk", font_size=12, color="#495057")

    b.add_arrow(600, y + 55, 650, y + 55, color="#f76707")

    b.add_rect(650, y, 255, 110, bg_color="#e7f5ff", stroke_color="#1971c2", stroke_width=2)
    b.add_text(665, y + 15, "3. ACCEPTANCE CRITERIA", font_size=15, color="#1864ab")
    b.add_text(665, y + 40, "• Given-When-Then criteria\n• Edge-case assertions\n• 100% testable conditions", font_size=12, color="#495057")

    b.add_arrow(775, y + 110, 775, 270, color="#1971c2")

    # Sequential Roadmap
    ry = 270
    b.add_rect(50, ry, 855, 120, bg_color="#f8f9fa", stroke_color="#343a40", stroke_width=2)
    b.add_text(70, ry + 15, "4. PHASED IMPLEMENTATION ROADMAP (HOW TO BUILD)", font_size=16, color="#212529")

    mw = 250
    b.add_rect(70, ry + 45, mw, 55, bg_color="#e7f5ff", stroke_color="#1971c2", stroke_width=1)
    b.add_text(80, ry + 52, "Milestone 4.1: Data Models", font_size=13, color="#1864ab")
    b.add_text(80, ry + 72, "Schemas, migrations, domain entities", font_size=11, color="#495057")

    b.add_arrow(320, ry + 72, 360, ry + 72, color="#1971c2")

    b.add_rect(360, ry + 45, mw, 55, bg_color="#fff4e6", stroke_color="#f76707", stroke_width=1)
    b.add_text(370, ry + 52, "Milestone 4.2: Core Logic", font_size=13, color="#d9480f")
    b.add_text(370, ry + 72, "Services, business rules, unit tests", font_size=11, color="#495057")

    b.add_arrow(610, ry + 72, 650, ry + 72, color="#f76707")

    b.add_rect(650, ry + 45, mw, 55, bg_color="#e6fcf5", stroke_color="#0ca678", stroke_width=1)
    b.add_text(660, ry + 52, "Milestone 4.3: UI & Wiring", font_size=13, color="#099268")
    b.add_text(660, ry + 72, "Interactive UI, styling, E2E tests", font_size=11, color="#495057")

    b.add_rect(50, 420, 855, 80, bg_color="#ebfbee", stroke_color="#2f9e44", stroke_width=2)
    b.add_text(70, 432, "GATE 3 APPROVAL CHECKPOINT (HUMAN SIGN-OFF REQUIRED)", font_size=16, color="#2b8a3e")
    b.add_text(70, 460, "Lead engineer reviews plan & risks. No code is written until sign-off is confirmed.", font_size=12, color="#495057")

    b.save(out_dir / "03-plan")


def create_step4_implement_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 4: IMPLEMENT — Single Driver, Loop Gate & Parallel Agents", "Firewall Gate 4 | Loop: Implement ➔ Spec ➔ Plan ➔ Implement | /find-skills & Parallel Dispatch")
    b.add_banner(w=860)

    y = 115
    # Row 1: Primary Driver & UI Polish
    b.add_rect(50, y, 410, 160, bg_color="#e7f5ff", stroke_color="#1971c2", stroke_width=2)
    b.add_text(70, y + 15, "PRIMARY DRIVER (Sole Logic Owner)", font_size=15, color="#1864ab")
    b.add_text(70, y + 42, "• Cursor, Claude Code, or Codex\n• Owns core business logic & domain\n• Builds unit & integration tests alongside\n• Follows approved plan sequentially\n• Prevents multi-driver context drift", font_size=12, color="#343a40")

    b.add_rect(495, y, 410, 160, bg_color="#fff4e6", stroke_color="#f76707", stroke_width=2)
    b.add_text(515, y + 15, "FRONTEND / INTERACTIVE POLISH", font_size=15, color="#d9480f")
    b.add_text(515, y + 42, "• Cursor live inline adjustments\n• Visual styling (Tailwind / CSS)\n• UI component layout & ergonomics\n• Keyboard accessibility & ARIA\n• Clean surgical diffs", font_size=12, color="#343a40")

    b.add_arrow(460, y + 80, 495, y + 80, color="#1971c2", stroke_width=2)
    b.add_arrow(495, y + 100, 460, y + 100, color="#f76707", stroke_width=2)

    # Row 2: THE IMPLEMENTATION LOOP GATE (Implement -> Loop -> Spec -> Plan -> Implement)
    ly = 295
    b.add_rect(50, ly, 855, 175, bg_color="#f3f0ff", stroke_color="#7950f2", stroke_width=2)
    b.add_text(70, ly + 14, "🔄 THE IMPLEMENTATION LOOP GATE: SUB-TASK DECOMPOSITION & PARALLEL DISPATCH", font_size=15, color="#5f3dc4")
    b.add_text(70, ly + 38, "Trigger: When implementation reveals multiple decoupled sub-modules, independent tasks, or missing skills:", font_size=12, color="#495057")

    # 3 sub-blocks in loop
    sw = 260
    b.add_rect(70, ly + 62, sw, 95, bg_color="#fff9db", stroke_color="#f59f00", stroke_width=1)
    b.add_text(80, ly + 72, "1. /find-skills DISCOVERY", font_size=13, color="#f08c00")
    b.add_text(80, ly + 94, "• npx skills find <domain>\n• Leaderboard on skills.sh\n• Equip missing tools/skills\n• Ready specialized capabilities", font_size=11, color="#495057")

    b.add_arrow(330, ly + 110, 365, ly + 110, color="#7950f2")

    b.add_rect(365, ly + 62, sw, 95, bg_color="#e6fcf5", stroke_color="#0ca678", stroke_width=1)
    b.add_text(375, ly + 72, "2. PARALLEL AGENTS", font_size=13, color="#099268")
    b.add_text(375, ly + 94, "• Dispatch parallel subagents\n• Independent work streams\n• Backend vs UI vs DB models\n• Single Driver orchestrates", font_size=11, color="#495057")

    b.add_arrow(625, ly + 110, 660, ly + 110, color="#0ca678")

    b.add_rect(660, ly + 62, sw, 95, bg_color="#e7f5ff", stroke_color="#1971c2", stroke_width=1)
    b.add_text(670, ly + 72, "3. LOOP: SPEC ➔ PLAN ➔ IMPL", font_size=13, color="#1864ab")
    b.add_text(670, ly + 94, "• Sub-Spec: contracts & schemas\n• Sub-Plan: testable criteria\n• Implement with zero drift\n• Re-integrate to Primary Driver", font_size=11, color="#495057")

    # Bottom summary
    b.add_rect(50, 490, 855, 75, bg_color="#ebfbee", stroke_color="#2f9e44", stroke_width=2)
    b.add_text(70, 502, "INVARIANT: NO PARALLEL STREAM CODE WITHOUT SPEC & PLAN APPROVAL", font_size=14, color="#2b8a3e")
    b.add_text(70, 526, "Primary Driver merges parallel streams cleanly, reviews diffs, and enforces quality gates before Phase 5 Verify.", font_size=12, color="#495057")

    b.save(out_dir / "04-implement")


def create_step5_verify_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 5: VERIFY — Zero-Concealment Validation Pipeline", "Firewall Gate 5 | Applicable: Any Agent + Test Runner / Environment")
    b.add_banner(w=860)

    y = 120
    cw = 185
    spacing = 38

    stages = [
        ("1. TYPECHECK", "• tsc --noEmit / mypy\n• Zero type errors\n• No @ts-ignore\n• Strict null safety", "#e7f5ff", "#1971c2"),
        ("2. LINT & FORMAT", "• eslint / ruff\n• Prettier / biome\n• Zero suppressed lints\n• Clean code style", "#fff4e6", "#f76707"),
        ("3. TEST RUNNER", "• Unit & integration\n• Actual runtime checks\n• Edge case coverage\n• 100% green tests", "#e6fcf5", "#0ca678"),
        ("4. WIKI EVIDENCE", "• check_evidence.py\n• 0 fidelity suspects\n• 0 evidence errors\n• Grounding intact", "#f3f0ff", "#7950f2")
    ]

    for i, (st_title, st_desc, bg, stroke) in enumerate(stages):
        sx = 50 + i * (cw + spacing)
        b.add_rect(sx, y, cw, 150, bg_color=bg, stroke_color=stroke, stroke_width=2)
        b.add_text(sx + 15, y + 15, st_title, font_size=15, color=stroke)
        b.add_text(sx + 15, y + 45, st_desc, font_size=12, color="#343a40")
        if i < len(stages) - 1:
            b.add_arrow(sx + cw, y + 75, sx + cw + spacing, y + 75, color=stroke)

    b.add_rect(50, 310, 855, 90, bg_color="#ffe3e3", stroke_color="#e03131", stroke_width=2)
    b.add_text(70, 322, "🛑 ZERO CONCEALMENT PROTOCOL", font_size=16, color="#c92a2a")
    b.add_text(70, 350, "Never disable tests, relax types, or hide errors to make code pass. Fix root causes in implementation.", font_size=12, color="#495057")

    b.add_rect(50, 420, 855, 70, bg_color="#ebfbee", stroke_color="#2f9e44", stroke_width=2)
    b.add_text(70, 432, "GATE 5 EXIT: 100% GREEN VALIDATION PROOF", font_size=15, color="#2b8a3e")
    b.add_text(70, 458, "All four checks passing cleanly. Ready for independent review.", font_size=12, color="#495057")

    b.save(out_dir / "05-verify")


def create_step6_review_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 6: REVIEW INDEPENDENTLY — Fresh-Context Diff Audit", "Firewall Gate 6 | Applicable: Auditor Agent in Clean Context")
    b.add_banner(w=860)

    y = 120
    b.add_rect(50, y, 380, 250, bg_color="#fff5f5", stroke_color="#e03131", stroke_width=2)
    b.add_text(70, y + 18, "STRICT READ-ONLY AUDITOR", font_size=16, color="#c92a2a")
    b.add_text(70, y + 48, "Mandate: Review without editing!\n• Clean context or separate agent\n• Full git diff inspection\n• Check against acceptance criteria\n• Logic & off-by-one errors\n• Security & data leakage\n• Performance bottlenecks", font_size=13, color="#343a40")

    b.add_rect(470, y, 435, 250, bg_color="#f8f9fa", stroke_color="#495057", stroke_width=2)
    b.add_text(490, y + 18, "SEVERITY TRIAGE MATRIX", font_size=16, color="#212529")
    b.add_text(490, y + 48, "🔴 HIGH / BLOCKER:\n  Bugs, regressions, unhandled crashes, security leaks\n\n🟡 MEDIUM:\n  Performance pitfalls, edge case gaps, code smells\n\n🟢 LOW / NIT:\n  Minor naming, comments, stylistic suggestions", font_size=12, color="#343a40")

    b.add_arrow(430, y + 125, 470, y + 125, color="#7950f2", stroke_width=2)
    b.add_rect(50, 400, 855, 90, bg_color="#ffe3e3", stroke_color="#e03131", stroke_width=2)
    b.add_text(70, 412, "REMEDIATION LOOP (Primary Driver Fixes & Re-Verifies)", font_size=15, color="#c92a2a")
    b.add_text(70, 440, "Primary Driver applies confirmed fixes ➔ Re-run Phase 5 (Verify) across all checks until 100% green.", font_size=12, color="#495057")

    b.save(out_dir / "06-review")


def create_step7_ship_diagram(out_dir: Path):
    b = ExcelDrawBuilder("STEP 7: SHIP SAFELY — Release Pipeline & Knowledge Compounding", "Firewall Gate 7 | Applicable: Driver Agent + Lead Engineer")
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

    b.add_rect(50, 310, 855, 90, bg_color="#fff5f5", stroke_color="#e03131", stroke_width=2)
    b.add_text(70, 322, "🛑 PRODUCTION RELEASE GATES", font_size=16, color="#c92a2a")
    b.add_text(70, 350, "Direct commits to main/master are strictly blocked • CI pipeline must be 100% green before merge.", font_size=12, color="#495057")

    b.add_rect(50, 430, 855, 70, bg_color="#ebfbee", stroke_color="#2f9e44", stroke_width=2)
    b.add_text(70, 442, "LIFECYCLE COMPLETE: ZERO REGRESSIONS, VERIFIED EVIDENCE & COMPOUNDED KNOWLEDGE", font_size=14, color="#2b8a3e")
    b.add_text(70, 468, "Every feature shipped leaves the codebase cleaner, safer, and better documented.", font_size=12, color="#495057")

    b.save(out_dir / "07-ship")


def main():
    repo_root = Path("d:/ai agent/the-developer")
    out_dir = repo_root / "diagrams"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Generating root workflow diagram...")
    create_root_workflow_diagram(repo_root)

    print("Generating per-step ExcelDraw diagrams in:", out_dir)
    create_step1_diagram(out_dir)
    create_step2_spec_diagram(out_dir)
    create_step3_plan_diagram(out_dir)
    create_step4_implement_diagram(out_dir)
    create_step5_verify_diagram(out_dir)
    create_step6_review_diagram(out_dir)
    create_step7_ship_diagram(out_dir)
    print("All 7 phase diagrams generated successfully!")


if __name__ == "__main__":
    main()
