# Example: Existing Project

## User prompt

```text
Use the Loop Engineering portable workflow to continue this project. First pass
Project Outcome Gate, review state/next.md as a candidate next step, and execute
one bounded loop only if it advances the user-visible demo and business
acceptance.
```

## Expected behavior

The assistant should:

- Read existing state before proposing work.
- Treat `state/next.md` as a candidate next step, not the highest instruction.
- Execute only a loop that advances the user-visible demo and business acceptance.
- Verify with evidence.
- Update `state/decisions.md`, `state/failures.md`, `state/inbox.md`, and
  `state/next.md` as needed.

## PASS criteria

- The next loop is grounded in existing state.
- The assistant does not restart the project from scratch.
- The result ends with PASS or REJECT.
- `state/next.md` contains a clear continuation entry.
