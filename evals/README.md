# Behavior Evals

This directory contains the automated behavior eval harness for Loop
Engineering.

## Offline Eval

Run without API tokens:

```bash
python3 evals/run_offline_eval.py
```

The offline eval creates temporary workspaces, applies deterministic scenario
fixtures, validates required state files, checks expected phrases, and confirms
that premature implementation files are absent.

## Live Eval

Run manually with an OpenAI API key:

```bash
OPENAI_API_KEY=... python3 evals/run_live_eval.py --require-token
```

The live eval sends each scenario prompt to the Responses API and checks that the
response follows the Loop Engineering contract. It is intentionally not part of
default CI because public contributors should not need a token.

## Scenarios

- `vague-idea.yaml`: vague idea should clarify and scaffold state.
- `existing-project-continue.yaml`: existing state should lead to one bounded
  continuation loop.
- `premature-implementation.yaml`: pressure to code too early should be rejected
  and converted into a first-loop state plan.
