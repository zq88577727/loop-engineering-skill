# Loop Engineering Portable Prompt Pack

Use this folder when you want the Loop Engineering workflow without installing a
Codex skill. No Codex required.

The portable pack works as copy-paste instructions for AI coding tools such as:

- Cursor
- Claude Code
- Gemini CLI
- ChatGPT
- JetBrains AI or any assistant that can read project files

## What to copy

For English sessions, copy:

```text
portable/LOOP_ENGINEERING_PROMPT.md
```

For Chinese sessions, copy:

```text
portable/LOOP_ENGINEERING_PROMPT.zh.md
```

If your tool supports project instruction files, copy this file into the
project's preferred instruction location:

```text
portable/AGENTS_TEMPLATE.md
```

Then copy `portable/STATE_TEMPLATE/` into the project as `state/`.

## New project prompt

```text
Use the Loop Engineering portable workflow. Read the project files, create or
update state from portable/STATE_TEMPLATE, define one first loop, and do not
implement immediately.
```

## Existing project prompt

```text
Use the Loop Engineering portable workflow. Read state/next.md first, execute
one bounded loop only, verify against docs/acceptance.md, then update state.
```

## PASS criteria

The assistant followed the workflow only if it:

- Clarified the idea or labeled assumptions before execution.
- Defined one bounded loop with success criteria.
- Used or created `state/triage.md`, `state/decisions.md`, `state/inbox.md`,
  `state/failures.md`, and `state/next.md`.
- Verified the result with PASS or REJECT evidence.
- Updated `state/next.md` for the next session.

## Limits

This portable pack does not make every AI tool auto-load the workflow. It gives
users a tool-neutral prompt and state structure that can be pasted into most AI
coding assistants.
