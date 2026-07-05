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

Use Loop Engineering for this project. Treat this file as the short router, not
as the full project manual.

## Run It

- Fill in the project setup or run command here.

## Verify It

- Fill in the project validation command here.
- If no automated check exists yet, update docs/acceptance.md with manual checks.

## Project Outcome Gate

- Define the user-visible demo before adding harness.
- Define business acceptance in user-result terms.
- Set a loop budget, default 3 loops.
- At the ship/stop gate, demo, ship, or REJECT instead of creating endless next work.

## Hard Constraints

- Read state before acting.
- Restate the goal, non-goals, and current loop scope.
- Execute one bounded loop only.
- Verify independently before reporting PASS.
- Verify against business acceptance, not only internal tests.
- Update state files before stopping.
- Do not expand scope without recording the decision.
- Do not add more harness unless it directly unblocks the demo.

## Where To Look

- Current loop -> state/next.md
- Current status and priorities -> state/triage.md
- Accepted assumptions and decisions -> state/decisions.md
- Failures and prevention notes -> state/failures.md
- Human questions -> state/inbox.md
- Acceptance criteria -> docs/acceptance.md
- Architecture and boundaries -> docs/architecture.md
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
    parser.add_argument("--dry-run", action="store_true", help="Report planned files without writing.")
    args = parser.parse_args()

    target = Path(args.target).resolve()

    created: list[str] = []
    skipped: list[str] = []
    for relative, content in FILES.items():
        path = target / relative
        if path.exists() and not args.force:
            skipped.append(relative)
            continue
        if args.dry_run:
            created.append(relative)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        created.append(relative)

    print(f"Target: {target}")
    print(f"Dry run: {str(args.dry_run).lower()}")
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
