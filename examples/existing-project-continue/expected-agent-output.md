# Expected Agent Output

## Mode

Execute loop.

## Required First Actions

- Read the project README and AGENTS instructions.
- Read every state file named in the prompt.
- Restate current goal, non-goals, current loop scope, and blockers.

## Execution Contract

- Choose the highest-priority ready task from `state/triage.md`.
- Execute only that task.
- Use the verification method in `state/next.md` or define a concrete one before
  starting.
- Do not expand scope because a related improvement is visible.

## Completion Contract

- Report PASS or REJECT with evidence.
- Update `state/triage.md`, `state/decisions.md`, `state/failures.md`,
  `state/inbox.md`, or `state/next.md` as needed.
- End with the next-loop entry, not with a generic summary.
