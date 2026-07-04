# Loop Engineering Showcase

This page is the shortest reproducible path for a new user. It shows how a
vague idea should become durable Loop Engineering state before implementation.

## Vague idea

```text
I want a small browser extension for saving useful snippets, but I do not know
the exact requirements yet.
```

## Install

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo zq88577727/loop-engineering-skill \
  --ref v0.3.1 \
  --path skills/loop-engineering
```

Restart Codex after installation.

## Run

Open a new Codex session in the target project and send:

```text
Use Loop Engineering for this vague idea: I want a small browser extension for
saving useful snippets, but I do not know the exact requirements yet. Do not
implement yet.
```

Codex should not start coding immediately. It should first clarify the problem,
define a bounded first loop, and create or propose state files.

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
