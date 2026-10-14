#!/usr/bin/env python3
"""Automated Verification and Evidence Collector for AI Engineering Workflow.

Performs risk-tiered automated quality checks before finishing a task:
1. Git diff & status inspection (changed files, stray debug statements, suppressions)
2. High-risk domain detection (migrations, auth, permissions, payments)
3. Wiki evidence integrity check (if wiki or raw files are modified)
4. Generates a structured 5-point Evidence-Based Completion Report template.

Usage:
  python verify_changes.py [options]

Options:
  --root DIR     Project root directory (default: current working directory)
  --check-wiki   Force check wiki evidence even if wiki/ is not modified
  --json         Output report in JSON format
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

HIGH_RISK_PATTERNS = {
    "Database Migrations": [
        r"migrations?\/",
        r"schema\.prisma$",
        r"schema\.sql$",
        r"alembic\/",
        r"\.sql$",
    ],
    "Authentication": [
        r"auth",
        r"session",
        r"jwt",
        r"token",
        r"login",
        r"password",
        r"credential",
    ],
    "Permissions & RBAC": [
        r"permission",
        r"rbac",
        r"tenant",
        r"role",
        r"authorization",
        r"acl",
    ],
    "Payment & Billing": [
        r"payment",
        r"billing",
        r"stripe",
        r"invoice",
        r"subscription",
        r"checkout",
        r"wallet",
    ],
}

DEBUG_PATTERNS = [
    (r"console\.log\(", "JavaScript/TypeScript console.log statement"),
    (r"\bdebugger\b", "JavaScript/TypeScript debugger breakpoint"),
    (r"\bimport\s+pdb\b", "Python pdb breakpoint"),
    (r"\bpdb\.set_trace\(", "Python pdb.set_trace breakpoint"),
    (r"\bbreakpoint\(", "Python breakpoint() call"),
    (r"@ts-ignore", "TypeScript type-suppression (@ts-ignore)"),
    (r"eslint-disable", "ESLint rule suppression (eslint-disable)"),
]

def run_command(cmd, cwd=None):
    """Run a shell command and return stdout, stderr, and returncode."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True,
            check=False,
        )
        return proc.stdout.strip(), proc.stderr.strip(), proc.returncode
    except Exception as e:
        return "", str(e), 1

def inspect_git_status(project_root):
    """Inspect git status to list modified, staged, untracked, and deleted files."""
    stdout, _, code = run_command("git status -s", cwd=project_root)
    if code != 0:
        return []
    
    files = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        status = line[:2].strip()
        file_path = line[2:].strip()
        # Handle rename format "R  old -> new"
        if "->" in file_path:
            file_path = file_path.split("->")[-1].strip()
        files.append((status, file_path))
    return files

def get_git_diff_patch(project_root):
    """Get the active git diff content (both staged and unstaged)."""
    unstaged_stdout, _, _ = run_command("git diff", cwd=project_root)
    staged_stdout, _, _ = run_command("git diff --staged", cwd=project_root)
    return (unstaged_stdout + "\n" + staged_stdout).strip()

def detect_high_risk_domains(changed_files):
    """Identify which high-risk domains are affected by the changed files."""
    detected = {}
    for status, fpath in changed_files:
        norm_path = fpath.replace("\\", "/").lower()
        for domain, patterns in HIGH_RISK_PATTERNS.items():
            for p in patterns:
                if re.search(p, norm_path):
                    if domain not in detected:
                        detected[domain] = []
                    detected[domain].append(fpath)
                    break
    return detected

IGNORE_EXTENSIONS = {".md", ".mdc", ".txt", ".json", ".svg", ".exceldraw", ".excalidraw", ".yml", ".yaml"}

def scan_for_debug_and_suppressions(diff_content):
    """Search added lines in git diff for stray debug statements or suppressions in source code."""
    warnings = []
    current_file = ""
    skip_file = False

    for line in diff_content.splitlines():
        if line.startswith("diff --git "):
            match = re.search(r"b/(.+)$", line)
            current_file = match.group(1) if match else ""
            ext = Path(current_file).suffix.lower()
            skip_file = ext in IGNORE_EXTENSIONS
            continue

        if skip_file:
            continue

        if line.startswith("+") and not line.startswith("+++"):
            added_content = line[1:]
            for pat, desc in DEBUG_PATTERNS:
                if re.search(pat, added_content):
                    warnings.append((desc, f"{current_file}: {added_content.strip()}"))
    return warnings

def check_wiki_evidence(project_root):
    """Run check_evidence.py if karpathy-llm-wiki skill exists."""
    script_path = project_root / "skills" / "karpathy-llm-wiki" / "scripts" / "check_evidence.py"
    if not script_path.exists():
        return True, "Wiki check script not present (skipped)."
    
    stdout, stderr, code = run_command(f"python \"{script_path}\" \"{project_root}\"", cwd=project_root)
    output = stdout + "\n" + stderr
    if "0 fidelity suspect(s), 0 evidence error(s)" in output:
        return True, "0 fidelity suspect(s), 0 evidence error(s) (Clean)"
    elif code == 0 and "evidence error" not in output.lower():
        return True, output.strip()
    else:
        return False, output.strip()

def generate_evidence_report(changed_files, high_risk_domains, debug_warnings, wiki_status):
    """Format the 5-point Evidence-Based Completion Report."""
    files_list = "\n".join(f"- `{fpath}` ({status})" for status, fpath in changed_files) or "- None (Clean working directory)"
    
    risk_summary = []
    if high_risk_domains:
        for domain, files in high_risk_domains.items():
            risk_summary.append(f"  - **{domain}**: Requires strict verification on {', '.join(files)}")
    else:
        risk_summary.append("  - No high-risk domain changes detected (Standard risk profile).")
    
    debug_summary = []
    if debug_warnings:
        for desc, snippet in debug_warnings[:5]:
            debug_summary.append(f"  - ⚠️ Found {desc}: `{snippet}`")
    else:
        debug_summary.append("  - Clean: Zero debug statements, zero `@ts-ignore`, zero `eslint-disable` detected in diff.")

    report = f"""
======================================================================
🛡️ VERIFICATION SUMMARY & QUALITY GATES REPORT
======================================================================

1. Changed Files ({len(changed_files)} detected):
{files_list}

2. High-Risk Domain Scrutiny:
{chr(10).join(risk_summary)}

3. Zero-Concealment & Debug Audit:
{chr(10).join(debug_summary)}

4. Wiki Grounding Invariant:
  - {wiki_status}

======================================================================
📋 EVIDENCE-BASED COMPLETION REPORT (Mandatory Before Declaring "Done")
======================================================================

### Evidence-Based Completion Report
1. **What changed?**:
   [Fill: Concise summary of functional behavior, architecture modifications, or bug fixes]

2. **Which files changed?**:
{chr(10).join(f"   - {fpath}" for _, fpath in changed_files) if changed_files else "   - None"}

3. **Which tests actually passed?**:
   [Fill: Exact commands executed, test count, assertions verified, and proof of green run]

4. **What was NOT tested?**:
   [Fill: Explicit declaration of unmocked systems, third-party integrations, manual edge cases, or blind spots]

5. **Remaining risks or manual steps?**:
   [Fill: Pending database migrations, required environment variables, manual lead engineer sign-offs, or rollout considerations]
======================================================================
"""
    return report

def main():
    project_root = Path(os.getcwd())
    for i, arg in enumerate(sys.argv):
        if arg == "--root" and i + 1 < len(sys.argv):
            project_root = Path(sys.argv[i + 1]).resolve()

    changed_files = inspect_git_status(project_root)
    diff_content = get_git_diff_patch(project_root)
    high_risk_domains = detect_high_risk_domains(changed_files)
    debug_warnings = scan_for_debug_and_suppressions(diff_content)

    touches_wiki = any("wiki/" in f.replace("\\", "/").lower() or "raw/" in f.replace("\\", "/").lower() for _, f in changed_files)
    if touches_wiki or "--check-wiki" in sys.argv:
        wiki_ok, wiki_msg = check_wiki_evidence(project_root)
    else:
        wiki_ok, wiki_msg = True, "Wiki files not touched (check not required)."

    report = generate_evidence_report(changed_files, high_risk_domains, debug_warnings, wiki_msg)
    print(report)

    # Return non-zero if debug suppressions or wiki error found
    if debug_warnings:
        print("⚠️ ACTION REQUIRED: Remove debug statements or suppressions before submitting for review.")
        sys.exit(1)
    if not wiki_ok:
        print("🛑 ACTION REQUIRED: Resolve wiki evidence errors before submitting for review.")
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
