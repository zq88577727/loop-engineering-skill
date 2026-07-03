#!/usr/bin/env python3
"""Validate the Loop Engineering public skill-pack contract."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    ".github/workflows/validate.yml",
    "docs/releases/v0.2.0.md",
    "assets/loop-engineering-flow.png",
    "scripts/validate_repo.py",
    "tests/test_repository_contract.py",
    "skills/loop-engineering/SKILL.md",
    "skills/loop-engineering/agents/openai.yaml",
    "skills/loop-engineering/references/full-workflow.md",
    "skills/loop-engineering/scripts/init_loop_project.py",
    "examples/vague-idea-to-first-loop/user-prompt.md",
    "examples/vague-idea-to-first-loop/expected-agent-output.md",
    "examples/vague-idea-to-first-loop/generated-state/triage.md",
    "examples/vague-idea-to-first-loop/generated-state/decisions.md",
    "examples/vague-idea-to-first-loop/generated-state/inbox.md",
    "examples/vague-idea-to-first-loop/generated-state/next.md",
    "examples/existing-project-continue/user-prompt.md",
    "examples/existing-project-continue/expected-agent-output.md",
    "examples/forward-test-report.md",
    "examples/forward-test-existing-project.md",
    "examples/forward-test-premature-implementation.md",
    "examples/invalid-loop.md",
]

SKILL_REQUIRED_PHRASES = [
    "name: loop-engineering",
    "description:",
    "vague idea",
    "early project concept",
    "long-running Codex task",
    "references/full-workflow.md",
    "state/triage.md",
    "PASS",
    "REJECT",
]

README_REQUIRED_PHRASES = [
    "install-skill-from-github.py",
    "--repo zq88577727/loop-engineering-skill",
    "--ref v0.2.0",
    "--path skills/loop-engineering",
    "Restart Codex",
    "python3 scripts/validate_repo.py",
    "python3 -m unittest discover -s tests",
    "v0.2.0",
]

CI_REQUIRED_PHRASES = [
    "python3 scripts/validate_repo.py",
    "python3 -m unittest discover -s tests",
    "python3 -m py_compile",
    "init_loop_project.py --target",
]


def _frontmatter_errors(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return ["SKILL.md frontmatter must start with ---"]
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        return ["SKILL.md frontmatter must be closed with ---"]

    errors: list[str] = []
    lines = [line.strip() for line in frontmatter.splitlines() if line.strip()]
    keys = {line.split(":", 1)[0] for line in lines if ":" in line}
    if keys != {"name", "description"}:
        errors.append("SKILL.md frontmatter must contain only name and description")
    return errors


def _check_initializer(root: Path) -> list[str]:
    script = root / "skills/loop-engineering/scripts/init_loop_project.py"
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "smoke"
        dry = subprocess.run(
            [sys.executable, str(script), "--target", str(target), "--dry-run"],
            cwd=root,
            text=True,
            capture_output=True,
        )
        if dry.returncode != 0:
            return [f"initializer dry-run failed: {dry.stderr.strip()}"]
        if target.exists():
            return ["initializer dry-run wrote files"]

        run = subprocess.run(
            [sys.executable, str(script), "--target", str(target)],
            cwd=root,
            text=True,
            capture_output=True,
        )
        if run.returncode != 0:
            return [f"initializer smoke test failed: {run.stderr.strip()}"]
        expected = [
            "README.md",
            "AGENTS.md",
            "docs/acceptance.md",
            "docs/architecture.md",
            "state/triage.md",
            "state/decisions.md",
            "state/failures.md",
            "state/inbox.md",
            "state/next.md",
        ]
        missing = [path for path in expected if not (target / path).is_file()]
        return [f"initializer missing generated file: {path}" for path in missing]


def validate_root(root: Path) -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")
        elif path.stat().st_size == 0:
            errors.append(f"Required file is empty: {relative}")

    skill = root / "skills/loop-engineering/SKILL.md"
    if skill.is_file():
        skill_text = skill.read_text(encoding="utf-8")
        errors.extend(_frontmatter_errors(skill_text))
        errors.extend(
            [f"SKILL.md missing phrase: {p}" for p in SKILL_REQUIRED_PHRASES if p not in skill_text]
        )

    readme = root / "README.md"
    if readme.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        errors.extend([f"README.md missing phrase: {p}" for p in README_REQUIRED_PHRASES if p not in readme_text])

    ci = root / ".github/workflows/validate.yml"
    if ci.is_file():
        ci_text = ci.read_text(encoding="utf-8")
        errors.extend([f"validate.yml missing phrase: {p}" for p in CI_REQUIRED_PHRASES if p not in ci_text])

    errors.extend(_check_initializer(root))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_root(root)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
