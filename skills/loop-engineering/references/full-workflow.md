# Loop Engineering Full Workflow

Use this reference when the user asks for the complete method, has only a vague idea, or wants to turn a project into a repeatable Codex loop.

## 1. Vague Idea

Goal: preserve unclear intent without implementing too early.

Ask for or infer:

- possible goal
- possible user
- use case
- inputs
- outputs
- risks
- questions that need human judgment

Prompt:

```text
I have a vague idea and cannot give clear requirements yet.
Use Loop Engineering. Do not implement. First split the idea into possible goals,
users, scenarios, inputs, outputs, risks, and questions that need my judgment.
```

## 2. Requirement Clarification

Goal: turn the idea into discussable project directions.

Ask questions in these groups:

- goal
- user
- input and output
- success standard
- risk boundary

If the user cannot answer, create explicit default assumptions.

Output:

```markdown
## Confirmed

## Assumptions

## Open Questions

## High-Risk Unknowns
```

## 3. Project Definition

Create `project-definition.md` or equivalent:

```markdown
# Project Definition

## Problem

## User

## Use Case

## Goal

## Non-goals

## Inputs

## Outputs

## Acceptance Criteria

## Risks

## First Loop
```

## 4. Version Split

Always split the project before implementation:

```markdown
# Version Plan

## A. MVP

## B. Practical Version

## C. Long-Term System

## Recommended First Version
```

Prefer the MVP unless the user explicitly chooses otherwise.

## 5. State Structure

Recommended project structure:

```text
README.md
AGENTS.md
docs/
  acceptance.md
  architecture.md
state/
  triage.md
  decisions.md
  failures.md
  inbox.md
  next.md
scripts/
  validate
```

Minimum structure:

```text
README.md
AGENTS.md
state/
  triage.md
  decisions.md
  failures.md
```

## 6. First Loop

Goal: produce evidence, not completeness.

The first loop should answer:

- Is the direction feasible?
- Does the smallest input-output path work?
- What is the largest uncertainty?
- What should the next loop do?

Prompt:

```text
Use project-definition.md to start the first loop. Do only the smallest
verifiable version. Do not expand scope. Verify the result and update state.
```

## 7. Execution

Before execution, state:

```text
current task:
input:
allowed changes:
forbidden changes:
expected output:
verification method:
```

Rules:

- do one bounded task
- avoid new scope
- stop on ambiguous human decisions
- keep changes tied to acceptance criteria

## 8. Independent Verification

Switch to evaluator posture.

Verification template:

```markdown
# Verification

## Target

## Method

## Commands or Checks

## Pass Criteria

## Fail Criteria

## Actual Result

## Verdict

PASS / REJECT
```

Rules:

- run what can be run
- inspect generated files
- verify behavior, not prose
- reject when evidence is missing

## 9. Persist State

Update state after every loop.

`state/triage.md`:

```markdown
# Triage

## Current Goal

## Current Scope

## Priority Queue

| id | task | priority | status | next_action |
|---|---|---|---|---|

## Blockers

## Ready For Next Loop
```

`state/decisions.md`:

```markdown
# Decisions

| date | decision | reason | status |
|---|---|---|---|
```

`state/failures.md`:

```markdown
# Failures

| date | failure | cause | fix | prevention |
|---|---|---|---|---|
```

`state/inbox.md`:

```markdown
# Human Inbox

| id | question | why_human_needed | options | recommended |
|---|---|---|---|---|
```

`state/next.md`:

```markdown
# Next Loop

## Next Goal

## Entry Condition

## Task

## Verification

## Stop Condition
```

## 10. Continue Next Loop

Prompt:

```text
Use Loop Engineering. Read README, AGENTS, state/triage.md, state/decisions.md,
state/failures.md, state/inbox.md, and state/next.md. Restate current status,
execute the highest-priority task, verify independently, update state, and write
the next-loop entry.
```

## 11. External Feedback

Use real-world feedback to update priority and risk:

- real users
- real samples
- real data
- real errors
- real environments

Record feedback as failures, decisions, or inbox questions before expanding scope.

## 12. Completion

A phase is complete only when:

- goal is met
- acceptance criteria pass
- verification evidence exists
- major failures are fixed or recorded
- decisions are durable
- README or state explains how to resume

## 13. Vague-Idea Prompt

```text
I have only a vague idea and cannot give clear requirements.

Use Loop Engineering:
1. Do not implement yet.
2. Split the idea into goals, users, scenarios, inputs, outputs, and risks.
3. Ask necessary clarification questions.
4. If I cannot answer, create labeled default assumptions.
5. Offer MVP, practical version, and long-term system.
6. Recommend a first loop.
7. Generate project definition, acceptance criteria, non-goals, and first task.
8. Implement only after the first loop is clear.
```

## 14. Existing-Project Prompt

```text
Use Loop Engineering to continue this project.

Read README, AGENTS, state/triage.md, state/decisions.md, state/failures.md,
state/inbox.md, and state/next.md.

Then:
1. Restate current goal, non-goal, phase, and loop scope.
2. Define acceptance criteria for this loop.
3. Execute the highest-priority task.
4. Verify independently.
5. Give PASS or REJECT.
6. Update state files.
7. Write the next-loop entry.
```

## 15. Loop Quality Gate

A loop is valid when it has:

- goal
- boundary
- state
- action
- verification
- record
- next loop

Invalid signals:

- prompt only, no state
- execution without verification
- summary without file records
- no next-loop entry
- uncontrolled scope expansion
- unrecorded failures
- generator self-approval

## 16. Six-Step Short Form

```text
1. Define the goal.
2. Read the state.
3. Do one bounded task.
4. Verify independently.
5. Persist the result.
6. Write the next-loop entry.
```

## 17. Mindset

```text
Vague phase: clarify before building.
Definition phase: choose a first loop.
Execution phase: do only this loop.
Verification phase: require evidence.
Persistence phase: write state, not just chat.
Next loop: continue from state, do not restart.
```
