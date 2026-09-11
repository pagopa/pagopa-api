#!/usr/bin/env python3
"""
Aggregates oasdiff changelog JSON artifacts and writes a unified
Markdown drift report to $GITHUB_STEP_SUMMARY.

Expected artifact layout (produced by the drift-detector workflow):
  artifacts/
    drift-main-<file>/result.json
    drift-d-<file>/result.json
    drift-u-<file>/result.json
    drift-p-<file>/result.json

Each result.json has:
  { "file": "biz_events.json", "env": "MAIN"|"DEV"|"UAT"|"PROD",
    "branch": "master"|"develop"|"SANP...", "changes": [...oasdiff items] }

oasdiff item fields used here:
  level   : 3=ERR (breaking), 2=WARN, 1=INFO
  id      : string rule id
  text    : human-readable description
  path    : API path (may be null)
  operation: HTTP method (may be null)
  section : "paths" | "security" | "components" | ...
"""

import os
import json
import glob
from collections import defaultdict
from typing import Optional
from datetime import datetime, timezone
# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENVS = ["MAIN", "DEV", "UAT", "PROD"]
ENV_BRANCH = {
    "MAIN": "master → service main",
    "DEV":  "SANP → APIM DEV",
    "UAT":  "develop → APIM UAT",
    "PROD": "master → APIM PROD",
}

LEVEL_LABEL = {3: "Error", 2: "Warning", 1: "Info"}
LEVEL_ICON  = {3: "❌", 2: "⚠️", 1: "🔵"}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_results(artifacts_dir: str) -> dict:
    """Return {filename: {env: [changes]}} from all result.json files."""
    data: dict = defaultdict(dict)
    for path in sorted(glob.glob(f"{artifacts_dir}/*/result.json")):
        try:
            with open(path) as f:
                record = json.load(f)
            fname   = record.get("file", "unknown")
            env     = record.get("env",  "UNKNOWN").upper()
            changes = record.get("changes", [])
            if not isinstance(changes, list):
                changes = []
            data[fname][env] = changes
        except (json.JSONDecodeError, KeyError, OSError):
            pass
    return data


def status_cell(changes: Optional[list]) -> str:
    """Compact cell for the summary table."""
    if changes is None:
        return "—"
    if not changes:
        return "✅ OK"
    errors   = sum(1 for c in changes if c.get("level") == 3)
    warnings = sum(1 for c in changes if c.get("level") == 2)
    infos    = sum(1 for c in changes if c.get("level") == 1)
    if errors:
        return f"❌ {errors}E / {warnings}W / {infos}I"
    if warnings:
        return f"⚠️ {warnings}W / {infos}I"
    return f"🔵 {infos} info"


def env_header(env: str) -> str:
    return f"**{env}**<br/><sub>{ENV_BRANCH[env]}</sub>"


def format_change(c: dict) -> str:
    """Format a single oasdiff change entry as a Markdown list item."""
    icon  = LEVEL_ICON.get(c.get("level", 1), "🔵")
    rule  = c.get("id", "unknown")
    text  = c.get("text", "")
    where = ""
    if c.get("operation") and c.get("path"):
        where = f" — `{c['operation']} {c['path']}`"
    elif c.get("path"):
        where = f" — `{c['path']}`"
    elif c.get("section"):
        where = f" — `{c['section']}`"
    comment = f" _{c['comment']}_" if c.get("comment") else ""
    return f"- {icon} `{rule}`{where}: {text}{comment}"


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def build_report(files_data: dict) -> str:
    lines: list[str] = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ---- Header -----------------------------------------------------------
    lines.append(f"# 📊 API Spec Drift Report — {now}\n")

    if not files_data:
        lines.append("> ⚠️ **No comparison results found.** All comparison jobs may have failed.\n")
        return "\n".join(lines)

    # Overall status
    all_changes = [c for env_data in files_data.values() for changes in env_data.values() for c in changes]
    has_errors   = any(c.get("level") == 3 for c in all_changes)
    has_warnings = any(c.get("level") == 2 for c in all_changes)
    total_files  = len(files_data)
    total_changes = len(all_changes)

    if has_errors:
        lines.append(f"> ❌ **Breaking changes detected** — immediate review required\n")
    elif has_warnings:
        lines.append(f"> ⚠️ **Warnings detected** — review recommended\n")
    elif total_changes:
        lines.append(f"> 🔵 **Informational changes only** — no breaking changes\n")
    else:
        lines.append(f"> ✅ **All specs are aligned** — no drift detected\n")

    lines.append(f"Monitoring **{total_files}** API spec file(s) — **{total_changes}** total change(s) found across all environments.\n")

    # ---- Summary table ----------------------------------------------------
    header_cells = " | ".join(env_header(e) for e in ENVS)
    lines.append(f"| API Spec | {header_cells} |")
    lines.append(f"|----------|{'|'.join([':---:'] * len(ENVS))}|")

    for fname in sorted(files_data.keys()):
        env_data = files_data[fname]
        cells = " | ".join(status_cell(env_data.get(env)) for env in ENVS)
        lines.append(f"| `{fname}` | {cells} |")

    lines.append("")

    # ---- Detailed sections per file ---------------------------------------
    lines.append("## 🔍 Details\n")
    lines.append("_Click on a file to expand its change details._\n")

    for fname in sorted(files_data.keys()):
        env_data = files_data[fname]

        file_changes = [c for changes in env_data.values() for c in changes]
        file_errors   = sum(1 for c in file_changes if c.get("level") == 3)
        file_warnings = sum(1 for c in file_changes if c.get("level") == 2)
        file_infos    = sum(1 for c in file_changes if c.get("level") == 1)

        if file_errors:
            status_badge = "❌"
        elif file_warnings:
            status_badge = "⚠️"
        elif file_infos:
            status_badge = "🔵"
        else:
            status_badge = "✅"

        summary_counts = (
            f"{len(file_changes)} change(s): "
            f"{file_errors} error(s), {file_warnings} warning(s), {file_infos} info"
            if file_changes else "no changes"
        )

        lines.append("<details>")
        lines.append(f"<summary>{status_badge} <b>{fname}</b> &nbsp;—&nbsp; {summary_counts}</summary>")
        lines.append("")

        for env in ENVS:
            changes = env_data.get(env)
            lines.append(f"#### {env} &nbsp;<sub>({ENV_BRANCH[env]})</sub>")
            lines.append("")

            if changes is None:
                lines.append("_N/A — not configured for this environment_")
            elif not changes:
                lines.append("✅ **No changes detected** — specs are aligned")
            else:
                errors   = [c for c in changes if c.get("level") == 3]
                warnings = [c for c in changes if c.get("level") == 2]
                infos    = [c for c in changes if c.get("level") == 1]

                lines.append(
                    f"**{len(changes)} change(s):** "
                    f"{len(errors)} error(s) &nbsp;·&nbsp; "
                    f"{len(warnings)} warning(s) &nbsp;·&nbsp; "
                    f"{len(infos)} info"
                )
                lines.append("")

                for severity_label, items in [("Errors", errors), ("Warnings", warnings), ("Info", infos)]:
                    if not items:
                        continue
                    icon = LEVEL_ICON[{"Errors": 3, "Warnings": 2, "Info": 1}[severity_label]]
                    lines.append(f"**{icon} {severity_label}**")
                    lines.append("")
                    for c in items:
                        lines.append(format_change(c))
                    lines.append("")

            lines.append("")

        lines.append("</details>")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    artifacts_dir = os.environ.get("ARTIFACTS_DIR", "artifacts")
    summary_file  = os.environ.get("GITHUB_STEP_SUMMARY")

    files_data = load_results(artifacts_dir)
    report     = build_report(files_data)

    if summary_file:
        with open(summary_file, "w") as f:
            f.write(report)
        print(f"✅ Drift report written to GitHub Step Summary ({len(files_data)} file(s) processed)")
    else:
        print(report)
