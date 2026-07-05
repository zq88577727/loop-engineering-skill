# Project Agent Instructions

Use the Loop Engineering portable workflow for vague ideas, stalled projects,
long-running tasks, and existing projects with `state/next.md`.

## Run It

1. Read `README.md`, `docs/acceptance.md`, `docs/architecture.md`, and `state/`.
2. If the request is vague, clarify before implementing.
3. Define the Project Outcome Mode: user-visible demo, business acceptance,
   loop budget, and ship/stop gate.
4. Choose one bounded loop that moves toward the demo.
5. Execute only that loop.
6. Verify the result against business acceptance, not only internal tests.
7. Update state before ending.

## Project Outcome Mode

For product, tool, demo, research-harness, or user-facing workflow work:

- Define a user-visible demo before adding harness.
- Define business acceptance in user-result terms.
- Set a loop budget, default 3 loops.
- Enforce a ship/stop gate when the budget is exhausted.
- Do not add more harness unless it directly unblocks the demo.

## Verify It

Every loop must end with:

```text
Verdict: PASS or REJECT
Evidence:
State files updated:
Next loop:
```

## Hard Constraints

- Do not implement immediately when the goal is unclear.
- Do not expand scope during a loop.
- Do not use chat memory as durable state.
- Do not mark PASS without concrete evidence.
- Do not treat internal test success as business acceptance.

## Where To Look

```text
state/next.md
state/triage.md
state/decisions.md
state/failures.md
state/inbox.md
docs/acceptance.md
docs/architecture.md
```
