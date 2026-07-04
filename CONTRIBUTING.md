# Contributing

Thanks for improving Loop Engineering Skill. The project is intentionally small:
changes should make the skill easier to install, understand, verify, or use in
real Codex sessions.

## Good contributions

- Clearer README or example wording.
- Reproducible forward-test reports.
- Validator improvements that catch real behavior regressions.
- New eval scenarios for common failure modes.
- Bug reports with exact install commands, prompts, and observed state files.

## Before opening a PR

Run the default checks:

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests
python3 evals/run_offline_eval.py
```

If you changed Python scripts, also run:

```bash
python3 -m py_compile \
  skills/loop-engineering/scripts/init_loop_project.py \
  scripts/create_github_release.py \
  scripts/validate_repo.py \
  evals/run_offline_eval.py \
  evals/run_live_eval.py \
  evals/validators/validate_loop_output.py
```

## Reporting usage feedback

The most useful feedback includes:

- Codex version or surface used.
- Install command and release tag.
- The exact user prompt.
- Files created under `state/` and `docs/`.
- Whether the agent clarified, executed, verified, and updated state.

Do not include secrets, private customer data, or API keys in issues.
