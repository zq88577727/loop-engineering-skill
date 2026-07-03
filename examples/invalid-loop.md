# Invalid Loop Examples

These outputs should be treated as REJECT until corrected.

## Prompt Only, No State

The agent gives a good-looking plan but does not write or update state files.

Failure: future sessions must reconstruct context from chat.

## Execution Without Verification

The agent implements a feature and says it is complete without running checks or
recording evidence.

Failure: completion is asserted, not proven.

## Summary Without Next Loop

The agent summarizes what happened but does not write `state/next.md`.

Failure: the next session has no concrete entry condition, task, or stop
condition.

## Scope Expansion

The agent starts with one bounded task but adds unrelated features because they
seem useful.

Failure: the loop boundary is not respected.
