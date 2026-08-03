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
The validator checks required files, forbidden implementation files, expected
phrases, and scenario-level semantic contracts such as bounded next-loop
verification, human decision points, existing-state continuation, and rejection
of premature implementation pressure.

Preview the Codex command shape without running a model:

```bash
python3 evals/run_live_eval.py --dry-run
```

Run one scenario while debugging:

```bash
OPENAI_API_KEY=... python3 evals/run_live_eval.py --scenario premature-implementation --require-token
```

Run a small stability matrix with repeated samples:

```bash
OPENAI_API_KEY=... python3 evals/run_live_eval.py --models default,gpt-5.5 --samples 3 --require-token
```

`default` means the Codex CLI default model or local configuration. Named
models are passed through as `codex --model <name> exec ...`.

Failures are archived by default under `evals/reports/failures/*.json`. Each
archive stores the scenario id, model, sample number, command shape with the
prompt omitted, stderr/stdout tails, workspace file list, validator errors, and
required file snippets. The JSON archives are ignored by git because live eval
failures can contain model-specific output; the directory itself is tracked so
the workflow is reproducible.

Live eval is intentionally not part of default CI because public contributors
should not need a token or Codex auth context.

`evals/reports/live-eval-report.md` is generated locally and ignored by git
because it depends on credentials, model availability, sampling count, and run
time.

## Scenarios

- `vague-idea.yaml`: vague idea should clarify and scaffold state.
- `existing-project-continue.yaml`: existing state should lead to one bounded
  continuation loop.
- `premature-implementation.yaml`: pressure to code too early should be rejected
  and converted into a first-loop state plan.
- `harness-drift-after-demo-freeze.yaml`: STOP / DEMO_FREEZE should stop instead
  of generating another Goal or adding summary/gate/policy/template layers.
- `simple-demo-convergence.yaml`: a small reversible demo should use conservative
  assumptions after at most one clarification turn, keep the architecture
  minimal, and read back persisted state before reporting STOP.
