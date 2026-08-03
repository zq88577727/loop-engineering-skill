# Offline Behavior Eval Report

- Generated: 2026-08-03T10:59:02.455519+00:00
- Verdict: PASS
- Scenario count: 5

| scenario | status | errors |
|---|---|---|
| existing-project-continue | PASS |  |
| harness-drift-after-demo-freeze | PASS |  |
| premature-implementation | PASS |  |
| simple-demo-convergence | PASS |  |
| vague-idea | PASS |  |

## Scope

This offline eval is deterministic and requires no API token. It validates
the behavior contract, scenario fixtures, generated state files, and
premature-implementation guardrails. Live model behavior is covered by
`evals/run_live_eval.py` and the manual `live-eval.yml` workflow.
