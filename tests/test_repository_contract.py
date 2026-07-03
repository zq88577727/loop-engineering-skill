from __future__ import annotations

import subprocess
import tempfile
import unittest
import shutil
import importlib.util
import json
import os
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
        report_text = (ROOT / "evals/reports/offline-eval-report.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Verdict: PASS", report_text)
        self.assertIn("vague-idea", report_text)
        self.assertIn("existing-project-continue", report_text)
        self.assertIn("premature-implementation", report_text)

    def test_ci_workflow_exists(self) -> None:
        workflow = ROOT / ".github/workflows/validate.yml"

        self.assertTrue(workflow.is_file())
        text = workflow.read_text(encoding="utf-8")
        self.assertIn("python3 scripts/validate_repo.py", text)
        self.assertIn("python3 -m unittest discover -s tests", text)

    def test_release_and_forward_test_artifacts_exist(self) -> None:
        release_notes = ROOT / "docs/releases/v0.2.1.md"
        clarify_forward_test = ROOT / "examples/forward-test-report.md"
        existing_forward_test = ROOT / "examples/forward-test-existing-project.md"
        premature_forward_test = ROOT / "examples/forward-test-premature-implementation.md"
        release_script = ROOT / "scripts/create_github_release.py"
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue(release_notes.is_file())
        self.assertTrue(clarify_forward_test.is_file())
        self.assertTrue(existing_forward_test.is_file())
        self.assertTrue(premature_forward_test.is_file())
        self.assertTrue(release_script.is_file())
        self.assertIn("--ref v0.2.1", readme)
        release_text = release_notes.read_text(encoding="utf-8")
        self.assertIn("Release Page Status", release_text)
        self.assertIn("GitHub Release page", release_text)
        self.assertIn(
            "https://github.com/zq88577727/loop-engineering-skill/releases/tag/v0.2.1",
            release_text,
        )
        self.assertIn("Published:", release_text)
        self.assertIn("PASS", clarify_forward_test.read_text(encoding="utf-8"))
        self.assertIn("PASS", existing_forward_test.read_text(encoding="utf-8"))
        self.assertIn("PASS", premature_forward_test.read_text(encoding="utf-8"))

    def test_release_script_dry_run_reports_exact_command(self) -> None:
        result = subprocess.run(
            [
                PYTHON,
                "scripts/create_github_release.py",
                "--tag",
                "v0.2.1",
                "--dry-run",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )

        payload = json.loads(result.stdout)

        self.assertEqual(payload["status"], "dry-run")
        self.assertEqual(payload["tag"], "v0.2.1")
        self.assertEqual(payload["notes_file"], "docs/releases/v0.2.1.md")
        self.assertIn("gh release create v0.2.1", payload["command"])

    def test_automated_behavior_eval_assets_exist(self) -> None:
        required = [
            "evals/README.md",
            "evals/run_offline_eval.py",
            "evals/run_live_eval.py",
            "evals/validators/validate_loop_output.py",
            "evals/scenarios/vague-idea.yaml",
            "evals/scenarios/existing-project-continue.yaml",
            "evals/scenarios/premature-implementation.yaml",
            "evals/reports/offline-eval-report.md",
            ".github/workflows/live-eval.yml",
        ]

        missing = [path for path in required if not (ROOT / path).is_file()]

        self.assertEqual(missing, [])

    def test_offline_eval_runs_without_token(self) -> None:
        env = dict(os.environ)
        env.pop("OPENAI_API_KEY", None)
        result = subprocess.run(
            [PYTHON, "evals/run_offline_eval.py"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
            env=env,
        )

        payload = json.loads(result.stdout)

        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["scenario_count"], 3)
        self.assertEqual(
            sorted(s["id"] for s in payload["scenarios"]),
            ["existing-project-continue", "premature-implementation", "vague-idea"],
        )

    def test_ci_runs_offline_eval_and_live_eval_is_manual(self) -> None:
        validate_workflow = (ROOT / ".github/workflows/validate.yml").read_text(
            encoding="utf-8"
        )
        live_workflow = (ROOT / ".github/workflows/live-eval.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("python3 evals/run_offline_eval.py", validate_workflow)
        self.assertIn("workflow_dispatch", live_workflow)
        self.assertIn("OPENAI_API_KEY", live_workflow)
        self.assertIn("python3 evals/run_live_eval.py", live_workflow)
        self.assertIn("codex exec", live_workflow)
        live_script = (ROOT / "evals/run_live_eval.py").read_text(encoding="utf-8")
        self.assertIn('"codex"', live_script)
        self.assertIn('"login"', live_script)
        self.assertIn('"status"', live_script)

    def test_live_eval_dry_run_uses_codex_exec_sandbox(self) -> None:
        result = subprocess.run(
            [PYTHON, "evals/run_live_eval.py", "--dry-run"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )

        payload = json.loads(result.stdout)

        self.assertEqual(payload["status"], "DRY_RUN")
        self.assertEqual(payload["runner"], "codex exec")
        self.assertEqual(payload["scenario_count"], 3)
        for scenario in payload["scenarios"]:
            command_list = scenario["command"]
            command = " ".join(command_list)
            self.assertEqual(command_list[0], "codex")
            self.assertIn("exec", command_list)
            self.assertIn("--sandbox workspace-write", command)
            self.assertIn("--ask-for-approval never", command)
            self.assertIn("--skip-git-repo-check", command)


if __name__ == "__main__":
    unittest.main()
