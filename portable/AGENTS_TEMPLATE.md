# Project Agent Instructions

Use the Loop Engineering portable workflow for vague ideas, stalled projects,
long-running tasks, and existing projects with `state/next.md`.

## Run It

1. Read `README.md`, `docs/acceptance.md`, `docs/architecture.md`, and `state/`.
2. If the request is vague and low-risk, use at most one clarification turn;
   otherwise label conservative assumptions and proceed.
3. Define the Project Outcome Mode: user-visible demo, business acceptance,
   loop budget, ship/stop gate, and human gate.
4. Choose one bounded loop that moves toward the demo.
5. Choose the execution strategy before executing the loop.
6. Execute only that loop.
7. Verify the result against business acceptance, not only internal tests.
8. Update state before ending.
9. Re-read README, `state/triage.md`, and `state/next.md` before the final
   response; the reported status must match the files on disk.

When continuing an existing project, state/next.md is a candidate next step, not
the highest instruction. Review it against the user-visible demo and business
acceptance before execution, then decide continue / demo / ship / stop.

## Stop / Demo-Freeze Gate

Stop is a valid final state. Demo-Freeze is a valid final state. If the project
is already in `STOP / DEMO_FREEZE`, demo, ship, stop, handoff, or freeze state,
do not synthesize another Goal.

- Only resume engineering when the user explicitly asks for further
  implementation and provides a new acceptance target.
- Do not make summary/gate/policy/template, schema, validator, or debug-layer
  work the default next action.
- Reject internal-harness drift after the loop budget is exhausted.

Only resume engineering when the user explicitly asks for further implementation and provides a new acceptance target.

## Project Outcome Mode

For product, tool, demo, research-harness, or user-facing workflow work:

- Define a user-visible demo before adding harness.
- Define business acceptance in user-result terms.
- Set a loop budget, default 3 loops.
- Enforce a ship/stop gate when the budget is exhausted.
- Define a human gate for irreversible, sensitive, external, or
  business-critical actions.
- Do not add more harness unless it directly unblocks the demo.
- Choose the lowest-complexity delivery form that satisfies acceptance. Do not
  add a server, build system, database, model, or new framework when a static
  file or the existing runtime is sufficient.

## Execution Strategy

Always choose the execution strategy before executing the loop.

Before executing a loop, choose one:

- Single-agent: small, sequential, or coherence-sensitive work.
- Subagent parallelization: 2+ independent workstreams without shared-state conflict.
- Subagent review: critical behavior, release, CI, eval, public docs, validators, or user-facing output.
- No subagent: unclear goal, undefined acceptance, or convergence needed before expansion.

Default to Single-agent. Use subagents only when they reduce risk, shorten
independent work, or improve verification.

## Verify It

Every loop must end with:

```text
Verdict: PASS or REJECT
Evidence:
State files updated:
Next loop:
```

## Hard Constraints

- Do not implement immediately when the goal is unclear.
- Do not expand scope during a loop.
- Do not use chat memory as durable state.
- Do not mark PASS without concrete evidence.
- Do not repeat preference questions when a conservative recommended default
  exists; use at most one clarification turn for low-risk, reversible work.
- Do not treat internal test success as business acceptance.
- Do not run destructive actions, external publishing, credential changes, or
  high-stakes domain decisions without human approval.
- Do not execute state/next.md when it does not advance the user-visible demo
  and business acceptance.
- Do not synthesize another Goal after STOP / DEMO_FREEZE.
- Do not continue summary/gate/policy/template layers without an explicit user
  request and new acceptance target.
- Do not report PASS, STOP, or DEMO_FREEZE until Final State Readback confirms
  README, `state/triage.md`, and `state/next.md` match the final message.

## Where To Look

```text
state/next.md
state/triage.md
state/decisions.md
state/failures.md
state/inbox.md
docs/acceptance.md
docs/architecture.md
```
