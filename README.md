<div align="center">

# Loop Engineering Skill

**A Codex skill for turning vague ideas into bounded, verified project loops.**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827)](skills/loop-engineering/SKILL.md)
[![Verified](https://img.shields.io/badge/v0.2.0-public%20ready-16a34a)](#quality-gates)
[![GitHub stars](https://img.shields.io/github/stars/zq88577727/loop-engineering-skill?style=social)](https://github.com/zq88577727/loop-engineering-skill/stargazers)

Turn unclear intent into a loop that clarifies, defines, executes, verifies,
persists state, and continues with durable progress.

![Loop Engineering flow](assets/loop-engineering-flow.png)

</div>

## What This Is

Loop Engineering is a practical workflow pattern for Codex-assisted work:

```text
idea -> clarify -> define -> first loop -> execute -> verify -> persist state -> continue
```

This repository packages that pattern as an installable Codex skill. It is
designed for users who start with a rough project idea, a stalled build, or a
long-running task that needs structure before implementation.

## Why Use It

- Turns vague intent into a concrete first loop.
- Separates clarification, acceptance criteria, execution, and verification.
- Persists project state so future Codex sessions can resume from the same
  decision trail.
- Makes progress auditable through explicit PASS, REJECT, and CONTINUE gates.

## When To Use

Use this skill when the task is not yet ready for direct implementation:

- You have a product, tool, research, or automation idea but cannot give exact
  instructions yet.
- You need Codex to ask sharper questions before building.
- You want a reusable project state folder that survives across sessions.
- You want execution to be checked against acceptance criteria instead of judged
  by whether code was merely written.

## Install

Install from GitHub:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo zq88577727/loop-engineering-skill \
  --path skills/loop-engineering
```

Restart Codex after installation so the skill is discoverable.

Recommended stable baseline: `v0.2.0`.

After restart, verify activation with a natural prompt:

```text
Use Loop Engineering for this vague idea: I want a small browser extension for saving useful snippets, but I do not know the exact requirements yet.
```

Codex should classify the request as a Loop Engineering task, clarify assumptions,
define the first loop, and create or propose state files before implementation.

## Quick Start

Natural trigger examples:

```text
Use Loop Engineering for this vague idea.
```

```text
按 Loop Engineering 继续这个项目，先读取 state 文件。
```

```text
帮我把这个模糊想法变成 first loop，不要马上实现。
```

## Initialize A Project

After the skill is available in a workspace:

```bash
python3 ~/.codex/skills/loop-engineering/scripts/init_loop_project.py --target .
```

The initializer creates a lightweight project operating system:

```text
README.md
AGENTS.md
docs/acceptance.md
docs/architecture.md
state/triage.md
state/decisions.md
state/failures.md
state/inbox.md
state/next.md
```

Preview the files without writing:

```bash
python3 ~/.codex/skills/loop-engineering/scripts/init_loop_project.py --target . --dry-run
```

## Workflow Contract

Loop Engineering keeps Codex work inside a visible loop:

| Stage | Purpose | Output |
| --- | --- | --- |
| Idea | Capture the rough direction | Initial intent |
| Clarify | Ask only the questions that reduce real uncertainty | Better task boundary |
| Define | Set objective, constraints, and success criteria | Acceptance target |
| First Loop | Choose the smallest useful iteration | Executable plan |
| Execute | Build, research, write, or test | Concrete result |
| Verify | Compare result against the acceptance target | PASS or REJECT |
| Persist State | Save decisions, failures, and next actions | Durable context |
| Continue | Start the next loop from current evidence | Next iteration |

## Repository Layout

```text
.
|-- assets/
|   `-- loop-engineering-flow.png
|-- scripts/
|   `-- validate_repo.py
|-- tests/
|   `-- test_repository_contract.py
|-- examples/
|   |-- vague-idea-to-first-loop/
|   |-- existing-project-continue/
|   `-- invalid-loop.md
`-- skills/
    `-- loop-engineering/
        |-- SKILL.md
        |-- agents/
        |   `-- openai.yaml
        |-- references/
        |   `-- full-workflow.md
        `-- scripts/
            `-- init_loop_project.py
```

## Quality Gates

The repository includes CI-compatible validation, unit tests, and a smoke-testable initializer:

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests
python3 -m py_compile scripts/validate_repo.py skills/loop-engineering/scripts/init_loop_project.py
python3 skills/loop-engineering/scripts/init_loop_project.py --target /tmp/loop-engineering-smoke
```

Expected validation result:

```text
ok
```

For user-facing behavior examples, see:

- `examples/vague-idea-to-first-loop/`
- `examples/existing-project-continue/`
- `examples/invalid-loop.md`

## Design Principles

- **Bound the loop first.** Do not let vague intent become unbounded execution.
- **Verify before continuing.** Treat completion as evidence-based, not assumed.
- **Persist state deliberately.** Future sessions should inherit decisions,
  failures, and next actions without reconstructing context from memory.
- **Keep the workflow lightweight.** The skill provides structure, not a heavy
  project management system.

## License

MIT. See [LICENSE](LICENSE).
