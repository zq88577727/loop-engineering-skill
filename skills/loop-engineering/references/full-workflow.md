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

## 6A. Project Outcome Mode

Use Project Outcome Mode for product, tool, demo, research-harness, or
user-facing workflow builds. The goal is project convergence, not an endless
sequence of internally valid loops.

Before implementation, define:

```markdown
## User-visible demo

## Business acceptance

## Loop budget

## Ship/stop gate

## Human gate
```

Default rule:

- `user-visible demo`: the smallest artifact a user can try, inspect, or react
  to.
- `business acceptance`: the real user outcome, not just schema validity,
  JSON fields, state updates, tests, or validator success.
- `loop budget`: at most 3 loops before demo/acceptance review.
- `ship/stop gate`: when the budget is exhausted, stop adding harness and
  either demo, ship, or REJECT with the missing evidence.
- `human gate`: irreversible, sensitive, external, or business-critical actions
  that require explicit human approval before execution.

Do not add more harness, validators, state fields, debugging layers, or
infrastructure unless they directly unblock the user-visible demo or business
acceptance within the remaining loop budget.

## 6A.1 Stop / Demo-Freeze Gate

Stop is a valid final state. Demo-Freeze is a valid final state. A user-visible
demo, handoff package, audit package, business decision checkpoint, or
`STOP / DEMO_FREEZE` state is allowed to end the loop sequence.

After STOP / DEMO_FREEZE:

- do not synthesize another Goal;
- do not create a next-loop entry unless continuation is justified;
- do not make summary/gate/policy/template, schema, validator, or debug-layer
  work the default next action;
- reject internal-harness drift after the loop budget is exhausted;
- only resume engineering when the user explicitly asks for further
  implementation and provides a new acceptance target.

Only resume engineering when the user explicitly asks for further implementation and provides a new acceptance target.

If the next candidate task only makes the harness more internally complete but
does not advance the user-visible demo or business acceptance, choose stop or
ask for explicit continuation.

Anti-pattern:

```text
Loop 1: add schema
Loop 2: add validator
Loop 3: add state gate
Loop 4: add more diagnostics
```

Preferred pattern:

```text
Loop 1: produce a fake-data user-visible demo
Loop 2: replace fake data with the smallest real input-output path
Loop 3: run business acceptance and decide ship/stop
```

## 6B. Execution Strategy

Before execution, choose the execution strategy before executing the loop.
Record the choice in the loop contract instead of asking the user to decide at
every step.

- `Single-agent`: small, sequential, or coherence-sensitive work.
- `Subagent parallelization`: 2+ independent workstreams that do not conflict
  on shared state.
- `Subagent review`: critical behavior, release, CI, eval, public docs,
  validators, or user-facing output that needs independent review.
- `No subagent`: unclear goal, undefined acceptance, or a project that needs
  convergence before expansion.

Default to `Single-agent`. Use subagents only when they reduce risk, shorten
independent work, or improve verification.

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

Use `Ready For Next Loop: no` when the project is in STOP / DEMO_FREEZE, demo,
ship, stop, handoff, or freeze state. In that case the default next action is
stop, and engineering may resume only with explicit user request and new
acceptance target.

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

Treat `state/next.md` as a candidate next step, not the highest instruction.
Before executing it, pass Project Outcome Gate and review whether it advances
the user-visible demo and business acceptance.

When the current state is STOP / DEMO_FREEZE, `state/next.md` should record
`Default next action: stop` and `Ready For Next Loop: no`. Do not turn that
state into another Goal unless the user explicitly asks for further
implementation and provides a new acceptance target.

## 10. Continue Next Loop

Prompt:

```text
Use Loop Engineering. Read README, AGENTS, state/triage.md, state/decisions.md,
state/failures.md, state/inbox.md, and state/next.md. First pass Project
Outcome Gate, review state/next.md as a candidate next step, and execute one
bounded loop only if it advances the user-visible demo and business acceptance.
End by deciding continue / demo / ship / stop. If the project is STOP /
DEMO_FREEZE, do not synthesize another Goal unless the user explicitly asks for
further implementation and gives a new acceptance target.
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
- STOP / DEMO_FREEZE is recorded when the correct next action is to stop

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
2. Pass Project Outcome Gate.
3. Treat `state/next.md` as a candidate next step, not the highest instruction.
4. Define acceptance criteria only for a loop that advances the user-visible
   demo and business acceptance.
5. Verify independently.
6. Give PASS or REJECT.
7. Update state files.
8. Decide continue / demo / ship / stop.
9. If the decision is STOP / DEMO_FREEZE, do not create another Goal.
```

## 15. Loop Quality Gate

A loop is valid when it has:

- goal
- boundary
- state
- action
- verification
- record
- next loop only when continuation is justified, or STOP / DEMO_FREEZE

Invalid signals:

- prompt only, no state
- execution without verification
- summary without file records
- no next-loop entry when continuation is justified
- another Goal after STOP / DEMO_FREEZE without explicit user continuation
- uncontrolled scope expansion
- summary/gate/policy/template work that only increases internal-harness drift
- unrecorded failures
- generator self-approval

## 16. Six-Step Short Form

```text
1. Define the goal.
2. Read the state.
3. Pass Project Outcome Gate.
4. Verify independently.
5. Persist the result.
6. Decide continue / demo / ship / stop.
7. If STOP / DEMO_FREEZE, stop instead of generating another Goal.
```

## 17. Mindset

```text
Vague phase: clarify before building.
Definition phase: choose a first loop.
Execution phase: do only this loop.
Verification phase: require evidence.
Persistence phase: write state, not just chat.
Next loop: review state/next.md as a candidate, then decide continue / demo /
ship / stop.
Stop phase: STOP / DEMO_FREEZE is valid; do not synthesize another Goal unless
the user explicitly asks for further implementation and provides a new
acceptance target.
```
