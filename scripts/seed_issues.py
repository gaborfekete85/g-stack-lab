"""Seeds the lab's GitHub issues from issues/*.md, in file order.

File order matters: issue numbers must match the "Blocked by" references inside the tickets.
Idempotent: an issue whose title already exists is skipped, or has its body synced with --update.

Usage: uv run python scripts/seed_issues.py <owner/repo> [--update]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

LABELS = {
    "feature": ("1f883d", "New behaviour — built first"),
    "bug": ("d73a4a", "Something is broken — built first"),
    "refactor": ("8250df", "Same behaviour, better shape"),
    "docs": ("0969da", "Docs only"),
    "qa": ("fbca04", "Test what exists — skips Building"),
}

ISSUES_DIR = Path(__file__).resolve().parent.parent / "issues"


def gh(*args: str) -> str:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)}\n{proc.stderr}")
    return proc.stdout


def read_ticket(path: Path) -> tuple[str, str]:
    first, _, rest = path.read_text().partition("\n")
    title = re.sub(r"^#\s+", "", first).strip()
    if not first.startswith("# ") or not title:
        raise SystemExit(f'{path.name}: first line must be "# <title>"')
    return title, rest.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", help="owner/repo")
    parser.add_argument("--update", action="store_true", help="sync bodies of issues that already exist")
    args = parser.parse_args()
    repo: str = args.repo

    for name, (color, description) in LABELS.items():
        gh("label", "create", name, "-R", repo, "--color", color, "--description", description, "--force")

    existing = {
        i["title"]: i["number"]
        for i in json.loads(
            gh("issue", "list", "-R", repo, "--state", "all", "--limit", "200", "--json", "title,number")
        )
    }

    for path in sorted(ISSUES_DIR.glob("*.md")):
        title, body = read_ticket(path)
        if title in existing:
            if args.update:
                gh("issue", "edit", str(existing[title]), "-R", repo, "--body", body)
                print(f"~ {path.name} → #{existing[title]} body synced")
            else:
                print(f"= {path.name} already exists (#{existing[title]})")
            continue
        kind = m.group(1) if (m := re.search(r"\[([a-z-]+)\]", title)) else ""
        label = ["--label", kind] if kind in LABELS else []
        url = gh("issue", "create", "-R", repo, "--title", title, "--body", body, *label)
        print(f"+ {path.name} → {url.strip()}")


if __name__ == "__main__":
    main()
