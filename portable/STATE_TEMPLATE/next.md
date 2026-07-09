# Next Loop

## Stop / Demo-Freeze Gate

## STOP / DEMO_FREEZE

Stop is a valid final state.
Demo-Freeze is a valid final state.

Default next action: stop
Ready For Next Loop: no

Engineering may resume only with explicit user request and new acceptance target.
Only resume engineering when the user explicitly asks for further implementation and provides a new acceptance target.

do not synthesize another Goal after STOP / DEMO_FREEZE.
Do not continue summary/gate/policy/template, schema, validator, or debug-layer
work unless it directly advances a new user-visible demo or business acceptance.
Reject internal-harness drift when the next step only improves internal
machinery.

## Objective

Define the next bounded loop.

## Acceptance Criteria

- 

## Constraints

- One loop only.
- Verify before continuing.
- Update state before ending.

## Suggested Prompt

```text
Use the Loop Engineering portable workflow to continue this project. First pass
Project Outcome Gate, review state/next.md as a candidate next step, and execute
one bounded loop only if it advances the user-visible demo and business
acceptance.
```
