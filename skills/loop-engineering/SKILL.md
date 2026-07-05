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

## Project Outcome Mode

Use Project Outcome Mode whenever a loop is part of building a product, tool,
demo, research harness, or user-facing workflow. Single-loop correctness is not
enough; the project must converge toward a user-visible demo.

Before adding engineering infrastructure, define:

```text
user-visible demo:
business acceptance:
loop budget:
ship/stop gate:
```

Defaults when the user does not specify otherwise:

- `user-visible demo`: the smallest artifact a user can try or inspect.
- `business acceptance`: the real outcome the user cares about, not only schema,
  state, validator, or unit-test success.
- `loop budget`: at most 3 loops before demo/acceptance review.
- `ship/stop gate`: after the budget, stop adding harness and either demo,
  ship, or REJECT with concrete gaps.

Do not add more harness, validators, state fields, or debugging layers unless
they directly unblock the user-visible demo or business acceptance. If a loop
only improves internal machinery, explain how it moves the project closer to
the demo within the remaining loop budget.

`state/next.md` is a candidate next step, not the highest instruction. For an
existing project, review state/next.md against the user-visible demo and
business acceptance before execution. If it does not advance them, rewrite the
loop or choose continue / demo / ship / stop instead.

## Execution Strategy

Before executing a loop, choose the execution strategy before executing the loop:

- `Single-agent`: use for small, sequential, or coherence-sensitive work.
- `Subagent parallelization`: use when there are 2+ independent workstreams
  that can proceed without shared-state conflict.
- `Subagent review`: use for critical behavior, release, CI, eval, public docs,
  validators, or user-facing output that needs independent review.
- `No subagent`: use when the goal is unclear, acceptance is undefined, or the
  project needs convergence before expansion.

Default to `Single-agent`. Use subagents only when they reduce risk, shorten
independent work, or improve verification. Do not ask the user at every step;
record the chosen strategy in the loop contract and proceed.

## Required First Output

When triggered, first classify the current mode and state the loop contract before
doing task work:

```text
mode:
confirmed facts:
assumptions:
user-visible demo:
business acceptance:
loop budget:
execution strategy:
current loop:
acceptance criteria:
verification method:
state files to read or write:
ship/stop gate:
```

If the request is vague, ask only the questions that reduce real uncertainty. If
the user does not answer, proceed with labeled conservative assumptions.

## Core Workflow

1. **Clarify intent.** Identify goal, user, use case, inputs, outputs, risks, non-goals, and unknowns.
2. **Separate facts from assumptions.** Label unclear points explicitly. If the user cannot answer, choose conservative defaults.
3. **Define versions.** Split the work into MVP, practical version, and long-term system.
4. **Select the first loop.** Choose the smallest loop that can produce evidence.
5. **Create state.** Use `state/triage.md`, `state/decisions.md`, `state/failures.md`, `state/inbox.md`, and `state/next.md`.
6. **Choose execution strategy.** Decide single-agent, subagent parallelization,
   subagent review, or no subagent before execution.
7. **Execute one bounded task.** Do not expand scope during the loop.
8. **Verify independently.** Switch to evaluator posture. Default to REJECT until evidence supports PASS.
9. **Persist outcomes.** Record completed work, decisions, failures, blockers, and the next loop entry.
10. **Converge.** Track the remaining loop budget and force a demo/ship/stop
   decision instead of endlessly generating `state/next.md`.

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

Use `--dry-run` first when the user wants to preview files or when the target
directory already contains important project files.

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
- Passing internal tests while failing the business acceptance.
- Extending harness work after the loop budget is exhausted.
- Asking the user to manually decide subagent usage every loop instead of using
  the Execution Strategy rules.

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
state/failures.md, state/inbox.md, and state/next.md. First pass Project
Outcome Gate, review state/next.md as a candidate next step, execute one
bounded loop only if it advances the user-visible demo and business acceptance,
then decide continue / demo / ship / stop.
```
