# Expected Agent Output

## Mode

Execute loop.

## Required First Actions

- Read the project README and AGENTS instructions.
- Read every state file named in the prompt.
- Restate current goal, non-goals, current loop scope, and blockers.

## Execution Contract

- Pass Project Outcome Gate before execution.
- Treat `state/next.md` as a candidate next step, not the highest instruction.
- Execute only if the loop advances the user-visible demo and business
  acceptance.
- Use or define a concrete verification method before starting.
- Do not expand scope because a related improvement is visible.

## Completion Contract

- Report PASS or REJECT with evidence.
- Update `state/triage.md`, `state/decisions.md`, `state/failures.md`,
  `state/inbox.md`, or `state/next.md` as needed.
- End by deciding continue / demo / ship / stop, not with a generic summary.
