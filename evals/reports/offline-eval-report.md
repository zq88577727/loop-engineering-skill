# Offline Behavior Eval Report

- Generated: 2026-07-16T14:27:38.919265+00:00
- Verdict: PASS
- Scenario count: 4

| scenario | status | errors |
|---|---|---|
| existing-project-continue | PASS |  |
| harness-drift-after-demo-freeze | PASS |  |
| premature-implementation | PASS |  |
| vague-idea | PASS |  |

## Scope

This offline eval is deterministic and requires no API token. It validates
the behavior contract, scenario fixtures, generated state files, and
premature-implementation guardrails. Live model behavior is covered by
`evals/run_live_eval.py` and the manual `live-eval.yml` workflow.
