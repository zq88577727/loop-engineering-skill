# Example: Vague Idea

## User prompt

```text
Use the Loop Engineering portable workflow. I want a small browser extension for
saving useful snippets, but I do not know the exact requirements yet. Do not
implement immediately.
```

## Expected behavior

The assistant should:

- Clarify the goal and assumptions.
- Define one first loop.
- Create or propose state files.
- Define acceptance criteria.
- Stop before coding the extension.

## Expected state

```text
state/triage.md
state/decisions.md
state/inbox.md
state/next.md
docs/acceptance.md
```

## PASS criteria

- No premature implementation.
- One bounded first loop.
- State is written or proposed.
- Verification criteria exist.
