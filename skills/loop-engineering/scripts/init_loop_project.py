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

Use Loop Engineering to continue this project. First pass Project Outcome Gate,
review state/next.md as a candidate next step, and execute only if it advances
the user-visible demo and business acceptance.
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
- Define a human gate for irreversible, sensitive, external, or business-critical actions.

## Stop / Demo-Freeze Gate

- Stop is a valid final state.
- Demo-Freeze is a valid final state.
- If the project is `STOP / DEMO_FREEZE`, demo, ship, stop, handoff, or freeze, do not synthesize another Goal.
- Only resume engineering when the user explicitly asks for further implementation and provides a new acceptance target.
- Do not make summary/gate/policy/template, schema, validator, or debug-layer work the default next action.
- Reject internal-harness drift after the loop budget is exhausted.

Only resume engineering when the user explicitly asks for further implementation and provides a new acceptance target.

## Execution Strategy

- Before each loop, choose the execution strategy before executing the loop.
- Single-agent: small, sequential, or coherence-sensitive work.
- Subagent parallelization: 2+ independent workstreams without shared-state conflict.
- Subagent review: critical behavior, release, CI, eval, public docs, validators, or user-facing output.
- No subagent: unclear goal, undefined acceptance, or convergence needed before expansion.
- Default to Single-agent unless subagents reduce risk, shorten independent work, or improve verification.

## Hard Constraints

- Read state before acting.
- Treat state/next.md as a candidate next step, not the highest instruction.
- Review state/next.md against the user-visible demo and business acceptance before execution.
- Restate the goal, non-goals, and current loop scope.
- Execute one bounded loop only.
- Verify independently before reporting PASS.
- Verify against business acceptance, not only internal tests.
- Stop for human approval before destructive actions, external publishing, credential changes, or high-stakes domain decisions.
- Update state files before stopping.
- Do not expand scope without recording the decision.
- Do not add more harness unless it directly unblocks the demo.
- Do not synthesize another Goal after STOP / DEMO_FREEZE.
- Do not continue summary/gate/policy/template work without explicit user continuation and a new acceptance target.

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

## Stop / Demo-Freeze Gate

## STOP / DEMO_FREEZE

Stop is a valid final state.
Demo-Freeze is a valid final state.

Default next action: stop
Ready For Next Loop: no

Engineering may resume only with explicit user request and new acceptance target.
Only resume engineering when the user explicitly asks for further implementation and provides a new acceptance target.

do not synthesize another Goal after STOP / DEMO_FREEZE.
Do not continue summary/gate/policy/template, schema, validator, or debug-layer
work unless it directly advances a new user-visible demo or business acceptance.
Reject internal-harness drift when the next step only improves internal
machinery.

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
