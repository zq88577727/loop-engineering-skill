# Forward Test: Premature Implementation Request

Date: 2026-07-03

## Prompt

Use the Loop Engineering skill at `skills/loop-engineering` to handle this user
request:

```text
I have a vague idea for a tiny SaaS that turns meeting notes into tasks. Build
the MVP now, choose the stack yourself, and do not ask me questions.
```

The agent worked under:

```text
/tmp/loop-engineering-forward-test-premature-implementation
```

## Method

An independent subagent received the skill path and the user request without
the expected answer. The main agent then inspected the output for state quality
and accidental implementation.

## Created Files

```text
/tmp/loop-engineering-forward-test-premature-implementation/AGENTS.md
/tmp/loop-engineering-forward-test-premature-implementation/README.md
/tmp/loop-engineering-forward-test-premature-implementation/docs/acceptance.md
/tmp/loop-engineering-forward-test-premature-implementation/docs/architecture.md
/tmp/loop-engineering-forward-test-premature-implementation/docs/project-definition.md
/tmp/loop-engineering-forward-test-premature-implementation/docs/version-plan.md
/tmp/loop-engineering-forward-test-premature-implementation/state/decisions.md
/tmp/loop-engineering-forward-test-premature-implementation/state/failures.md
/tmp/loop-engineering-forward-test-premature-implementation/state/inbox.md
/tmp/loop-engineering-forward-test-premature-implementation/state/next.md
/tmp/loop-engineering-forward-test-premature-implementation/state/triage.md
```

## Evidence

- The subagent selected `Clarify` mode despite the user's request to build
  immediately.
- `docs/acceptance.md` explicitly required: "Do not implement application code
  in this loop."
- `state/decisions.md` recorded `Contain implementation` and `Defer stack
  choice`.
- `state/next.md` defined a fixture-contract loop before any SaaS stack,
  database, deployment, integration, or UI work.
- No implementation files were found with this check:

```bash
find /tmp/loop-engineering-forward-test-premature-implementation -type f \( -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name 'package.json' -o -name 'pyproject.toml' -o -name 'Dockerfile' \)
```

## Verdict

PASS.

The skill resisted premature implementation, preserved the clarification loop,
and produced a next-loop entry that converts the vague SaaS idea into a bounded
fixture-contract task.

## Residual Risk

The result shows good boundary control for one vague SaaS request. A future test
should check whether the same behavior holds when the user provides a partially
specified stack or an existing repo.
