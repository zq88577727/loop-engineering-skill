#!/usr/bin/env python3
"""Create the GitHub Release page for an existing tag."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_REPO = "zq88577727/loop-engineering-skill"
DEFAULT_TAG = "v0.4.2"
DEFAULT_TITLE = "v0.4.2 explicit human gate"


def build_command(repo: str, tag: str, title: str, notes_file: str) -> list[str]:
    return [
        "gh",
        "release",
        "create",
        tag,
        "--repo",
        repo,
        "--title",
        title,
        "--notes-file",
        notes_file,
    ]


def emit(payload: dict[str, object]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the GitHub Release page for a tag.")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repository in owner/name form.")
    parser.add_argument("--tag", default=DEFAULT_TAG, help="Existing git tag to release.")
    parser.add_argument("--title", default=DEFAULT_TITLE, help="GitHub Release title.")
    parser.add_argument(
        "--notes-file",
        default=f"docs/releases/{DEFAULT_TAG}.md",
        help="Markdown release notes file.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the command without running it.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    notes_path = root / args.notes_file
    command = build_command(args.repo, args.tag, args.title, args.notes_file)
    command_text = " ".join(command)

    if not notes_path.is_file():
        emit(
            {
                "status": "error",
                "reason": "notes-file-missing",
                "notes_file": args.notes_file,
            }
        )
        return 1

    if args.dry_run:
        emit(
            {
                "status": "dry-run",
                "repo": args.repo,
                "tag": args.tag,
                "title": args.title,
                "notes_file": args.notes_file,
                "command": command_text,
            }
        )
        return 0

    auth = subprocess.run(["gh", "auth", "status"], cwd=root, text=True, capture_output=True)
    if auth.returncode != 0:
        emit(
            {
                "status": "blocked",
                "reason": "gh-auth-status-failed",
                "stdout": auth.stdout,
                "stderr": auth.stderr,
                "next_action": "Run gh auth login or provide a valid GITHUB_TOKEN, then rerun this script.",
            }
        )
        return 2

    result = subprocess.run(command, cwd=root, text=True, capture_output=True)
    if result.returncode != 0:
        emit(
            {
                "status": "error",
                "reason": "gh-release-create-failed",
                "command": command_text,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        return result.returncode

    emit(
        {
            "status": "created",
            "repo": args.repo,
            "tag": args.tag,
            "stdout": result.stdout,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
