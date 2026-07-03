---
name: loop-engineering
description: Use when a user has a vague idea, early project concept, stalled project, reusable workflow, or long-running Codex task and needs to turn it into bounded loops with goals, acceptance criteria, state files, execution, independent verification, memory, and a next-loop entry.
---

# Loop Engineering

## Overview

Use Loop Engineering to turn unclear intent into a repeatable project loop:

```text
idea -> clarify -> define -> first loop -> execute -> verify -> persist state -> continue
```

Do not treat this as a request to immediately implement. First create enough clarity to define a small, verifiable loop.

## Operating Modes

Choose the mode from the user's current state.

| User state | Mode | Output |
| --- | --- | --- |
| Vague idea | Clarify | questions, assumptions, project definition |
| Defined goal but no structure | Scaffold | README, AGENTS, docs, state files |
| Existing project state | Execute loop | one bounded task, verification, state update |
| Completed iteration | Evaluate | PASS/REJECT, failures, next loop |

## Core Workflow

1. **Clarify intent.** Identify goal, user, use case, inputs, outputs, risks, non-goals, and unknowns.
2. **Separate facts from assumptions.** Label unclear points explicitly. If the user cannot answer, choose conservative defaults.
3. **Define versions.** Split the work into MVP, practical version, and long-term system.
4. **Select the first loop.** Choose the smallest loop that can produce evidence.
5. **Create state.** Use `state/triage.md`, `state/decisions.md`, `state/failures.md`, `state/inbox.md`, and `state/next.md`.
6. **Execute one bounded task.** Do not expand scope during the loop.
7. **Verify independently.** Switch to evaluator posture. Default to REJECT until evidence supports PASS.
8. **Persist outcomes.** Record completed work, decisions, failures, blockers, and the next loop entry.

For the complete 17-step method, read `references/full-workflow.md`.

## State Files

Prefer these files when starting or continuing a loop:

```text
README.md
AGENTS.md
docs/acceptance.md
docs/architecture.md
state/triage.md
state/decisions.md
state/failures.md
state/inbox.md
state/next.md
```

If the project has no loop files, offer to create them. You can run:

```bash
python3 skills/loop-engineering/scripts/init_loop_project.py --target .
```

Adjust the path if the skill is installed elsewhere.

## Verification Rules

Evaluator posture:

- Assume the output is incomplete until checked.
- Run available tests, validators, commands, renders, or file checks.
- Do not use explanation as proof.
- Write uncertain decisions to `state/inbox.md`.
- End each loop with `PASS` or `REJECT` plus evidence.

## Common Failure Patterns

- Implementing before clarifying the goal.
- Expanding the project during the first loop.
- Keeping state only in chat.
- Letting the generator approve its own work.
- Ending without a next-loop entry.
- Recording temporary reasoning instead of durable decisions.

## Useful Prompts

When the user only has a vague idea:

```text
Use Loop Engineering. Do not implement yet. Clarify the idea, label assumptions,
offer MVP/practical/long-term versions, recommend a first loop, and define
acceptance criteria before execution.
```

When the project already has state:

```text
Use Loop Engineering. Read README, AGENTS, state/triage.md, state/decisions.md,
state/failures.md, state/inbox.md, and state/next.md. Execute one bounded loop,
verify independently, update state, and write the next-loop entry.
```
