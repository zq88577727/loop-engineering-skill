# Forward Test: Stale State Rewrite

Verdict: PASS

## Scenario

An existing project already has `state/next.md`, but the proposed next loop has
drifted away from the product outcome.

The user-visible demo is:

```text
Enter two drug names, return evidence-backed interaction status when possible,
and clearly explain when the system cannot give a conclusion yet.
```

The business acceptance is:

```text
A user can run one query through a visible demo path and see evidence,
limitations, and a non-overstated answer.
```

The stale `state/next.md` proposes:

```text
Add another schema snapshot for debug summaries and update validator ordering.
```

## Expected Agent Behavior

The agent must first pass Project Outcome Gate. Because `state/next.md is a
candidate next step, not the highest instruction`, the agent must review it
against the user-visible demo and business acceptance before execution.

Contract phrase: state/next.md is a candidate next step, not the highest instruction.

Expected decision:

```text
REJECT stale state/next.md. It adds more harness work but does not advance the
user-visible demo or business acceptance.
```

Expected rewritten loop:

```text
Goal: create the smallest visible query demo for two drug names.
Acceptance: demo returns evidence, limitations, and a clear cannot-conclude
message when evidence is insufficient.
Loop budget: one bounded loop.
Verification: run the demo with one positive fixture and one insufficient
evidence fixture.
Ship/stop: stop adding harness until the visible demo passes.
```

## PASS Criteria

- The agent refuses to execute stale `state/next.md` as-is.
- The agent explicitly cites Project Outcome Gate.
- The agent explains that `state/next.md` is only a candidate input.
- The rewritten loop advances the user-visible demo.
- The rewritten loop has business acceptance, loop budget, verification, and a
  ship/stop decision.
- The agent does not continue adding validator or state-structure work.

## Why This Matters

This sample guards against the old failure mode where the agent repeatedly
followed `state/next.md` even after it stopped moving the product toward a demo.
The correct behavior is to reject stale continuation and rewrite the loop.
