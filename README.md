# Loop Engineering Skill

A Codex skill for turning vague ideas into bounded, verified project loops.

Loop Engineering is a workflow pattern:

```text
idea -> clarify -> define -> first loop -> execute -> verify -> persist state -> continue
```

This repository packages that pattern as an installable Codex skill.

## Install

From GitHub, after this repository is published:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo zq88577727/loop-engineering-skill \
  --path skills/loop-engineering
```

Restart Codex after installation so the skill is discoverable.

## Use

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

## Included

```text
skills/loop-engineering/SKILL.md
skills/loop-engineering/references/full-workflow.md
skills/loop-engineering/scripts/init_loop_project.py
scripts/validate_repo.py
```

## Initialize A Project

After the skill is available in a workspace:

```bash
python3 skills/loop-engineering/scripts/init_loop_project.py --target .
```

This creates:

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

## Validate

```bash
python3 scripts/validate_repo.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/loop-engineering
```
