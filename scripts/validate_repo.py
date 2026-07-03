#!/usr/bin/env python3
"""Validate the Loop Engineering skill repository layout."""

from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "README.md",
    "LICENSE",
    "assets/loop-engineering-flow.png",
    "skills/loop-engineering/SKILL.md",
    "skills/loop-engineering/agents/openai.yaml",
    "skills/loop-engineering/references/full-workflow.md",
    "skills/loop-engineering/scripts/init_loop_project.py",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED if not (root / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"  - {path}")
        return 1

    skill = root / "skills/loop-engineering/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    required_phrases = [
        "name: loop-engineering",
        "description:",
        "references/full-workflow.md",
        "state/triage.md",
        "PASS",
        "REJECT",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in text]
    if missing_phrases:
        print("SKILL.md missing expected phrases:")
        for phrase in missing_phrases:
            print(f"  - {phrase}")
        return 1

    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
