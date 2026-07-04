# Project Agent Instructions

Use the Loop Engineering portable workflow for vague ideas, stalled projects,
long-running tasks, and existing projects with `state/next.md`.

## Run It

1. Read `README.md`, `docs/acceptance.md`, `docs/architecture.md`, and `state/`.
2. If the request is vague, clarify before implementing.
3. Choose one bounded loop.
4. Execute only that loop.
5. Verify the result.
6. Update state before ending.

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
