#!/usr/bin/env python3

import hashlib
import json
import os
import re
import subprocess
from collections import defaultdict
from pathlib import Path


ARTIFACTS_DIR = Path(os.environ["ARTIFACTS_DIR"])
REPO_DIR = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
REPO_SLUG = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
RUN_ID = os.environ.get("GITHUB_RUN_ID", "local")

TARGET_BY_ENV = {"DEV": "develop", "UAT": "develop", "PROD": "master"}
PR_BRANCH_PREFIX = "openapi-drift"


def git(*args: str, capture_output: bool = False) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_DIR,
        check=True,
        text=True,
        capture_output=capture_output,
    )
    return result.stdout if capture_output else ""


def gh_api(method: str, path: str, payload: dict | None = None) -> dict | list:
    cmd = [
        "curl",
        "--fail",
        "--silent",
        "--show-error",
        "-X",
        method,
        "-H",
        "Accept: application/vnd.github+json",
        "-H",
        f"Authorization: Bearer {TOKEN}",
        f"https://api.github.com{path}",
    ]
    if payload is not None:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(payload)])
    result = subprocess.run(cmd, cwd=REPO_DIR, check=True, text=True, capture_output=True)
    return json.loads(result.stdout)


def sanitize_branch_component(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value)
    return value.strip("-").lower()


def load_candidates():
    grouped = defaultdict(list)
    for result_path in sorted(ARTIFACTS_DIR.glob("*/result.json")):
        record = json.loads(result_path.read_text(encoding="utf-8"))
        if not record.get("semantic_drift"):
            continue

        env = record.get("env")
        target_branch = TARGET_BY_ENV.get(env)
        if target_branch is None:
            continue

        canonical_path = result_path.parent / "apim_spec_canonical.json"
        if not canonical_path.exists():
            continue

        canonical_content = canonical_path.read_text(encoding="utf-8")
        digest = hashlib.sha256(canonical_content.encode("utf-8")).hexdigest()
        grouped[(record["file"], target_branch, digest)].append(
            {
                "env": env,
                "record": record,
                "canonical_content": canonical_content,
            }
        )
    return grouped


def ensure_base_branch(branch: str):
    git("fetch", "origin", branch)
    git("checkout", "-B", branch, f"origin/{branch}")


def open_pr_exists(head: str, base: str) -> bool:
    prs = gh_api("GET", f"/repos/{REPO_SLUG}/pulls?state=open&head={REPO_SLUG.split('/')[0]}:{head}&base={base}")
    return bool(prs)


def create_pr(head: str, base: str, title: str, body: str):
    return gh_api(
        "POST",
        f"/repos/{REPO_SLUG}/pulls",
        {"title": title, "head": head, "base": base, "body": body},
    )


def main():
    summary = []
    candidates = load_candidates()
    if not candidates:
        summary.append("No semantic drift detected; no PR created.")
        Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a", encoding="utf-8").write("\n".join(summary) + "\n")
        return

    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")

    for (file_name, target_branch, digest), entries in candidates.items():
        ensure_base_branch(target_branch)
        branch_name = f"{PR_BRANCH_PREFIX}/{target_branch}/{sanitize_branch_component(file_name.rsplit('.', 1)[0])}-{digest[:12]}"

        if open_pr_exists(branch_name, target_branch):
            summary.append(f"- `{file_name}` → `{target_branch}`: PR already open")
            continue

        git("checkout", "-B", branch_name, f"origin/{target_branch}")
        target_file = REPO_DIR / "openapi" / file_name
        target_file.write_text(entries[0]["canonical_content"], encoding="utf-8")

        diff_exit = subprocess.run(
            ["git", "diff", "--quiet", "--", str(target_file.relative_to(REPO_DIR))],
            cwd=REPO_DIR,
            check=False,
        ).returncode
        if diff_exit == 0:
            summary.append(f"- `{file_name}` → `{target_branch}`: no diff after checkout")
            continue

        git("add", str(target_file.relative_to(REPO_DIR)))
        envs = ", ".join(sorted({item["env"] for item in entries}))
        apim_names = ", ".join(sorted({item["record"].get("apim_display_name", "") for item in entries if item["record"].get("apim_display_name")}))
        apim_descriptions = "\n".join(
            f"- **{item['env']}**: {item['record'].get('apim_description') or '_No description_'}"
            for item in sorted(entries, key=lambda e: e["env"])
        )
        git("commit", "-m", f"chore: sync {file_name} from APIM\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>")
        git("push", "--force-with-lease", "origin", branch_name)

        title = f"chore: sync {file_name} from APIM to {target_branch}"
        body = (
            f"## Summary\n"
            f"- Sync `openapi/{file_name}` with APIM\n"
            f"- Source environments: {envs}\n"
            f"- Target branch: `{target_branch}`\n"
            f"- APIM display name: {apim_names or '_N/A_'}\n\n"
            f"## APIM descriptions\n{apim_descriptions}\n"
        )
        pr = create_pr(branch_name, target_branch, title, body)
        summary.append(f"- `{file_name}` → `{target_branch}`: PR #{pr['number']} created")

    Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a", encoding="utf-8").write("\n## Drift remediation PRs\n" + "\n".join(summary) + "\n")


if __name__ == "__main__":
    main()
