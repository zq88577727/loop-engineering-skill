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

The live eval starts a real non-interactive Codex session with `codex exec` for
each scenario. Each session runs in a temporary workspace with
`--sandbox workspace-write` and `--ask-for-approval never`, writes actual state
files, and is then checked by `evals/validators/validate_loop_output.py`.

Preview the exact Codex commands without running a model:

```bash
python3 evals/run_live_eval.py --dry-run
```

Run one scenario while debugging:

```bash
OPENAI_API_KEY=... python3 evals/run_live_eval.py --scenario premature-implementation --require-token
```

Live eval is intentionally not part of default CI because public contributors
should not need a token or Codex auth context.

`evals/reports/live-eval-report.md` is generated locally and ignored by git
because it depends on credentials, model availability, and run time.

## Scenarios

- `vague-idea.yaml`: vague idea should clarify and scaffold state.
- `existing-project-continue.yaml`: existing state should lead to one bounded
  continuation loop.
- `premature-implementation.yaml`: pressure to code too early should be rejected
  and converted into a first-loop state plan.
