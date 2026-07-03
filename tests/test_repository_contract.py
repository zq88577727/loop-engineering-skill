from __future__ import annotations

import subprocess
import tempfile
import unittest
import shutil
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = "python3"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_repo", ROOT / "scripts/validate_repo.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load validate_repo.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepositoryContractTests(unittest.TestCase):
    def run_cmd(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=ROOT,
            check=check,
            text=True,
            capture_output=True,
        )

    def test_repository_validator_passes_public_ready_contract(self) -> None:
        result = self.run_cmd(PYTHON, "scripts/validate_repo.py")

        self.assertEqual(result.stdout.strip(), "ok")

    def test_repository_validator_rejects_missing_public_ready_assets(self) -> None:
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            ignore = shutil.ignore_patterns(".git", "__pycache__")
            shutil.copytree(ROOT, target, ignore=ignore)

            (target / ".github/workflows/validate.yml").unlink()

            errors = validator.validate_root(target)

            self.assertTrue(any(".github/workflows/validate.yml" in e for e in errors))

    def test_initializer_is_idempotent_and_force_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            first = self.run_cmd(
                PYTHON,
                "skills/loop-engineering/scripts/init_loop_project.py",
                "--target",
                str(target),
            )
            self.assertIn("Created: 9", first.stdout)

            readme = target / "README.md"
            readme.write_text("# Custom\n", encoding="utf-8")

            second = self.run_cmd(
                PYTHON,
                "skills/loop-engineering/scripts/init_loop_project.py",
                "--target",
                str(target),
            )
            self.assertIn("Skipped existing: 9", second.stdout)
            self.assertEqual(readme.read_text(encoding="utf-8"), "# Custom\n")

            third = self.run_cmd(
                PYTHON,
                "skills/loop-engineering/scripts/init_loop_project.py",
                "--target",
                str(target),
                "--force",
            )
            self.assertIn("Created: 9", third.stdout)
            self.assertIn("Use Loop Engineering", readme.read_text(encoding="utf-8"))

    def test_initializer_dry_run_reports_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "dry-run-target"

            result = self.run_cmd(
                PYTHON,
                "skills/loop-engineering/scripts/init_loop_project.py",
                "--target",
                str(target),
                "--dry-run",
            )

            self.assertIn("Dry run: true", result.stdout)
            self.assertFalse(target.exists())


class PublicReadyAssetTests(unittest.TestCase):
    def test_examples_cover_new_user_and_existing_project_paths(self) -> None:
        required = [
            "examples/vague-idea-to-first-loop/user-prompt.md",
            "examples/vague-idea-to-first-loop/expected-agent-output.md",
            "examples/vague-idea-to-first-loop/generated-state/triage.md",
            "examples/vague-idea-to-first-loop/generated-state/decisions.md",
            "examples/vague-idea-to-first-loop/generated-state/inbox.md",
            "examples/vague-idea-to-first-loop/generated-state/next.md",
            "examples/existing-project-continue/user-prompt.md",
            "examples/existing-project-continue/expected-agent-output.md",
            "examples/invalid-loop.md",
        ]

        missing = [path for path in required if not (ROOT / path).is_file()]

        self.assertEqual(missing, [])

    def test_ci_workflow_exists(self) -> None:
        workflow = ROOT / ".github/workflows/validate.yml"

        self.assertTrue(workflow.is_file())
        text = workflow.read_text(encoding="utf-8")
        self.assertIn("python3 scripts/validate_repo.py", text)
        self.assertIn("python3 -m unittest discover -s tests", text)


if __name__ == "__main__":
    unittest.main()
