# Loop Engineering Showcase

This page is the shortest reproducible path for a new user. It shows how a
vague idea should become durable Loop Engineering state before implementation.

## Vague idea

```text
I want a small browser extension for saving useful snippets, but I do not know
the exact requirements yet.
```

## Codex demo

### Install

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo zq88577727/loop-engineering-skill \
  --ref v0.4.0 \
  --path skills/loop-engineering
```

Restart Codex after installation.

### Run

Open a new Codex session in the target project and send:

```text
Use Loop Engineering for this vague idea: I want a small browser extension for
saving useful snippets, but I do not know the exact requirements yet. Do not
implement yet.
```

Codex should not start coding immediately. It should first clarify the problem,
define a bounded first loop, and create or propose state files.

## Portable demo

No Codex required. Use this path for Cursor, Claude Code, Gemini CLI, ChatGPT,
JetBrains AI, or any assistant that can read project files.

1. Copy `portable/LOOP_ENGINEERING_PROMPT.md` or
   `portable/LOOP_ENGINEERING_PROMPT.zh.md` into the AI coding tool.
2. Copy `portable/STATE_TEMPLATE/` into the project as `state/`.
3. Send this prompt:

```text
Use the Loop Engineering portable workflow. Read the project files, create or
update state from portable/STATE_TEMPLATE, define one first loop, and do not
implement immediately.
```

The expected behavior is the same as the Codex demo: clarify first, define one
bounded loop, create or update state, and avoid premature implementation.

## Expected state files

The first run should create or propose files like:

```text
state/triage.md
state/decisions.md
state/inbox.md
state/next.md
docs/acceptance.md
```

Example output is tracked under
[`examples/vague-idea-to-first-loop/`](../examples/vague-idea-to-first-loop/).

## PASS criteria

Treat the demo as a pass only when all of these are true:

- The agent asks clarifying questions or labels assumptions before execution.
- The first loop has a concrete objective and success criteria.
- State is written or explicitly proposed in the canonical `state/` files.
- The response includes a verification step or acceptance gate.
- The agent avoids premature implementation.

## Continue path

For the next session, use the short continuation prompt:

```text
按 state/next.md 继续，只做一个 loop，验证后更新 state。
```

This is the intended user habit: initialize once, then continue from state.
