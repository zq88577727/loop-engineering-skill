# Example: Existing Project

## User prompt

```text
Use the Loop Engineering portable workflow. Read state/next.md first, execute
one bounded loop only, verify against docs/acceptance.md, then update state.
```

## Expected behavior

The assistant should:

- Read existing state before proposing work.
- Execute only the current loop.
- Verify with evidence.
- Update `state/decisions.md`, `state/failures.md`, `state/inbox.md`, and
  `state/next.md` as needed.

## PASS criteria

- The next loop is grounded in existing state.
- The assistant does not restart the project from scratch.
- The result ends with PASS or REJECT.
- `state/next.md` contains a clear continuation entry.
