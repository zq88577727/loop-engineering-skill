#!/usr/bin/env python3
"""Initialize Loop Engineering state files in a project."""

from __future__ import annotations

import argparse
from pathlib import Path


FILES = {
    "README.md": """# Project

## Goal

## Current Status

## How To Continue

Use Loop Engineering: read state files, execute one bounded loop, verify, update state.
""",
    "AGENTS.md": """# Agent Instructions

Use Loop Engineering for this project.

1. Read state before acting.
2. Restate goal, non-goals, and current loop scope.
3. Execute one bounded task.
4. Verify independently.
5. Update state files.
6. Write the next-loop entry.

Do not expand scope without writing the decision to state/inbox.md or state/decisions.md.
""",
    "docs/acceptance.md": """# Acceptance Criteria

## Project-Level Criteria

## Current Loop Criteria

## Verification Method
""",
    "docs/architecture.md": """# Architecture

## Components

## Boundaries

## Open Questions
""",
    "state/triage.md": """# Triage

## Current Goal

## Current Scope

## Priority Queue

| id | task | priority | status | next_action |
|---|---|---|---|---|

## Blockers

## Ready For Next Loop
""",
    "state/decisions.md": """# Decisions

| date | decision | reason | status |
|---|---|---|---|
""",
    "state/failures.md": """# Failures

| date | failure | cause | fix | prevention |
|---|---|---|---|---|
""",
    "state/inbox.md": """# Human Inbox

| id | question | why_human_needed | options | recommended |
|---|---|---|---|---|
""",
    "state/next.md": """# Next Loop

## Next Goal

## Entry Condition

## Task

## Verification

## Stop Condition
""",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Loop Engineering project files.")
    parser.add_argument("--target", default=".", help="Target project directory.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    skipped: list[str] = []
    for relative, content in FILES.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not args.force:
            skipped.append(relative)
            continue
        path.write_text(content, encoding="utf-8")
        created.append(relative)

    print(f"Target: {target}")
    print(f"Created: {len(created)}")
    for item in created:
        print(f"  + {item}")
    if skipped:
        print(f"Skipped existing: {len(skipped)}")
        for item in skipped:
            print(f"  = {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
