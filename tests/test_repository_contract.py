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


def load_output_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_loop_output", ROOT / "evals/validators/validate_loop_output.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load validate_loop_output.py")
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

    def test_initializer_agents_file_is_short_router_with_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            subprocess.run(
                [
                    PYTHON,
                    "skills/loop-engineering/scripts/init_loop_project.py",
                    "--target",
                    str(target),
                ],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")

        for heading in ["## Run It", "## Verify It", "## Hard Constraints", "## Where To Look"]:
            self.assertIn(heading, agents)
        for route in [
            "state/next.md",
            "state/triage.md",
            "state/decisions.md",
            "state/failures.md",
            "state/inbox.md",
            "docs/acceptance.md",
            "docs/architecture.md",
        ]:
            self.assertIn(route, agents)
        self.assertIn("Execute one bounded loop only", agents)
        self.assertLessEqual(len(agents.splitlines()), 80)

    def test_initializer_agents_file_enforces_project_outcome_convergence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            subprocess.run(
                [
                    PYTHON,
                    "skills/loop-engineering/scripts/init_loop_project.py",
                    "--target",
                    str(target),
                ],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")

        for phrase in [
            "## Project Outcome Gate",
            "user-visible demo",
            "loop budget",
            "business acceptance",
            "ship/stop",
        ]:
            self.assertIn(phrase, agents)

    def test_initializer_agents_file_includes_execution_strategy_router(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            subprocess.run(
                [
                    PYTHON,
                    "skills/loop-engineering/scripts/init_loop_project.py",
                    "--target",
                    str(target),
                ],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")

        for phrase in [
            "## Execution Strategy",
            "Single-agent",
            "Subagent parallelization",
            "Subagent review",
            "No subagent",
            "choose the execution strategy before executing the loop",
        ]:
            self.assertIn(phrase, agents)


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
        self.assertIn("harness-drift-after-demo-freeze", report_text)

    def test_ci_workflow_exists(self) -> None:
        workflow = ROOT / ".github/workflows/validate.yml"

        self.assertTrue(workflow.is_file())
        text = workflow.read_text(encoding="utf-8")
        self.assertIn("python3 scripts/validate_repo.py", text)
        self.assertIn("python3 -m unittest discover -s tests", text)

    def test_release_and_forward_test_artifacts_exist(self) -> None:
        release_notes = ROOT / "docs/releases/v0.4.1.md"
        clarify_forward_test = ROOT / "examples/forward-test-report.md"
        existing_forward_test = ROOT / "examples/forward-test-existing-project.md"
        premature_forward_test = ROOT / "examples/forward-test-premature-implementation.md"
        stale_state_forward_test = ROOT / "examples/forward-test-stale-state-rewrite.md"
        release_script = ROOT / "scripts/create_github_release.py"
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue(release_notes.is_file())
        self.assertTrue(clarify_forward_test.is_file())
        self.assertTrue(existing_forward_test.is_file())
        self.assertTrue(premature_forward_test.is_file())
        self.assertTrue(stale_state_forward_test.is_file())
        self.assertTrue(release_script.is_file())
        self.assertIn("--ref v0.4.1", readme)
        self.assertIn("Recommended stable baseline: `v0.4.1`", readme)
        release_text = release_notes.read_text(encoding="utf-8")
        self.assertIn("Release Page Status", release_text)
        self.assertIn("GitHub Release page", release_text)
        self.assertIn(
            "https://github.com/zq88577727/loop-engineering-skill/releases/tag/v0.4.1",
            release_text,
        )
        self.assertIn("Project Outcome Gate", release_text)
        self.assertIn("workflow pack", release_text)
        self.assertIn("Published:", release_text)
        self.assertIn("PASS", clarify_forward_test.read_text(encoding="utf-8"))
        self.assertIn("PASS", existing_forward_test.read_text(encoding="utf-8"))
        self.assertIn("PASS", premature_forward_test.read_text(encoding="utf-8"))
        stale_text = stale_state_forward_test.read_text(encoding="utf-8")
        for phrase in [
            "PASS",
            "state/next.md is a candidate next step, not the highest instruction",
            "Project Outcome Gate",
            "REJECT",
            "user-visible demo",
            "business acceptance",
            "rewrite the loop",
        ]:
            self.assertIn(phrase, stale_text)

    def test_release_script_dry_run_reports_exact_command(self) -> None:
        result = subprocess.run(
            [
                PYTHON,
                "scripts/create_github_release.py",
                "--tag",
                "v0.4.1",
                "--dry-run",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )

        payload = json.loads(result.stdout)

        self.assertEqual(payload["status"], "dry-run")
        self.assertEqual(payload["tag"], "v0.4.1")
        self.assertEqual(payload["notes_file"], "docs/releases/v0.4.1.md")
        self.assertIn("gh release create v0.4.1", payload["command"])

    def test_release_script_defaults_to_current_stable_release(self) -> None:
        result = subprocess.run(
            [PYTHON, "scripts/create_github_release.py", "--dry-run"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )

        payload = json.loads(result.stdout)

        self.assertEqual(payload["tag"], "v0.4.1")
        self.assertEqual(
            payload["title"],
            "v0.4.1 outcome-gated continuation guidance",
        )
        self.assertEqual(payload["notes_file"], "docs/releases/v0.4.1.md")

    def test_automated_behavior_eval_assets_exist(self) -> None:
        required = [
            "evals/README.md",
            "evals/run_offline_eval.py",
            "evals/run_live_eval.py",
            "evals/validators/validate_loop_output.py",
            "evals/scenarios/vague-idea.yaml",
            "evals/scenarios/existing-project-continue.yaml",
            "evals/scenarios/premature-implementation.yaml",
            "evals/scenarios/harness-drift-after-demo-freeze.yaml",
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
        self.assertEqual(payload["scenario_count"], 4)
        self.assertEqual(
            sorted(s["id"] for s in payload["scenarios"]),
            [
                "existing-project-continue",
                "harness-drift-after-demo-freeze",
                "premature-implementation",
                "vague-idea",
            ],
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

    def test_repository_has_exposure_basics_for_new_users(self) -> None:
        required = [
            "docs/SHOWCASE.md",
            "docs/PROMOTION.md",
            "CONTRIBUTING.md",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/usage_feedback.yml",
        ]

        missing = [path for path in required if not (ROOT / path).is_file()]

        self.assertEqual(missing, [])

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in [
            "30-second demo",
            "中文快速开始",
            "docs/SHOWCASE.md",
            "CONTRIBUTING.md",
            "Use this when",
            "Do not use this when",
        ]:
            self.assertIn(phrase, readme)

        showcase = (ROOT / "docs/SHOWCASE.md").read_text(encoding="utf-8")
        for phrase in [
            "Vague idea",
            "Install",
            "Run",
            "Expected state files",
            "PASS criteria",
        ]:
            self.assertIn(phrase, showcase)

        promotion = (ROOT / "docs/PROMOTION.md").read_text(encoding="utf-8")
        for phrase in [
            "GitHub About",
            "Suggested topics",
            "Launch post",
            "30-second demo script",
            "workflow pack",
            "Portable Prompt Pack",
            "Cursor",
            "Claude Code",
            "Gemini CLI",
            "ChatGPT",
        ]:
            self.assertIn(phrase, promotion)

    def test_portable_prompt_pack_supports_non_codex_ai_tools(self) -> None:
        required = [
            "portable/README.md",
            "portable/LOOP_ENGINEERING_PROMPT.md",
            "portable/LOOP_ENGINEERING_PROMPT.zh.md",
            "portable/AGENTS_TEMPLATE.md",
            "portable/STATE_TEMPLATE/triage.md",
            "portable/STATE_TEMPLATE/decisions.md",
            "portable/STATE_TEMPLATE/failures.md",
            "portable/STATE_TEMPLATE/inbox.md",
            "portable/STATE_TEMPLATE/next.md",
            "portable/examples/vague-idea.md",
            "portable/examples/existing-project.md",
        ]

        missing = [path for path in required if not (ROOT / path).is_file()]

        self.assertEqual(missing, [])

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in [
            "Portable Prompt Pack",
            "portable/README.md",
            "Cursor",
            "Claude Code",
            "Gemini CLI",
            "ChatGPT",
        ]:
            self.assertIn(phrase, readme)

        portable_readme = (ROOT / "portable/README.md").read_text(encoding="utf-8")
        for phrase in [
            "No Codex required",
            "Cursor",
            "Claude Code",
            "Gemini CLI",
            "ChatGPT",
            "copy",
            "STATE_TEMPLATE",
            "PASS criteria",
        ]:
            self.assertIn(phrase, portable_readme)

        prompt = (ROOT / "portable/LOOP_ENGINEERING_PROMPT.md").read_text(
            encoding="utf-8"
        )
        for phrase in [
            "Do not implement immediately",
            "Clarify",
            "Define",
            "First loop",
            "Verify",
            "Persist state",
            "state/next.md",
            "PASS or REJECT",
        ]:
            self.assertIn(phrase, prompt)

        showcase = (ROOT / "docs/SHOWCASE.md").read_text(encoding="utf-8")
        for phrase in [
            "Portable demo",
            "portable/LOOP_ENGINEERING_PROMPT.md",
            "portable/STATE_TEMPLATE",
            "No Codex required",
        ]:
            self.assertIn(phrase, showcase)

    def test_project_outcome_mode_prevents_infinite_engineering_loops(self) -> None:
        skill = (ROOT / "skills/loop-engineering/SKILL.md").read_text(encoding="utf-8")
        full_workflow = (
            ROOT / "skills/loop-engineering/references/full-workflow.md"
        ).read_text(encoding="utf-8")
        portable_prompt = (ROOT / "portable/LOOP_ENGINEERING_PROMPT.md").read_text(
            encoding="utf-8"
        )
        portable_prompt_zh = (
            ROOT / "portable/LOOP_ENGINEERING_PROMPT.zh.md"
        ).read_text(encoding="utf-8")
        portable_agents = (ROOT / "portable/AGENTS_TEMPLATE.md").read_text(
            encoding="utf-8"
        )

        for text in [skill, full_workflow, portable_prompt, portable_agents]:
            for phrase in [
                "Project Outcome Mode",
                "user-visible demo",
                "loop budget",
                "business acceptance",
                "ship/stop gate",
                "Do not add more harness",
            ]:
                self.assertIn(phrase, text)

        for phrase in [
            "项目级收敛",
            "用户可见 demo",
            "loop 上限",
            "业务验收",
            "停止继续补 harness",
        ]:
            self.assertIn(phrase, portable_prompt_zh)

    def test_stop_demo_freeze_gate_prevents_harness_drift_after_delivery(self) -> None:
        public_files = {
            "skill": ROOT / "skills/loop-engineering/SKILL.md",
            "full_workflow": ROOT / "skills/loop-engineering/references/full-workflow.md",
            "readme": ROOT / "README.md",
            "portable_prompt": ROOT / "portable/LOOP_ENGINEERING_PROMPT.md",
            "portable_prompt_zh": ROOT / "portable/LOOP_ENGINEERING_PROMPT.zh.md",
            "portable_agents": ROOT / "portable/AGENTS_TEMPLATE.md",
            "state_next_template": ROOT / "portable/STATE_TEMPLATE/next.md",
        }
        text = {
            name: path.read_text(encoding="utf-8")
            for name, path in public_files.items()
        }

        for name in [
            "skill",
            "full_workflow",
            "readme",
            "portable_prompt",
            "portable_agents",
            "state_next_template",
        ]:
            searchable_text = text[name].lower()
            for phrase in [
                "Stop / Demo-Freeze Gate",
                "STOP / DEMO_FREEZE",
                "Stop is a valid final state",
                "Demo-Freeze is a valid final state",
                "do not synthesize another Goal",
                "explicitly asks for further implementation",
                "new acceptance target",
                "summary/gate/policy/template",
                "internal-harness drift",
            ]:
                self.assertIn(phrase.lower(), searchable_text, f"{name} missing {phrase!r}")

        for phrase in [
            "Stop / Demo-Freeze Gate",
            "STOP / DEMO_FREEZE",
            "Stop 是合法终态",
            "Demo-Freeze 是合法终态",
            "不要自动生成下一批 Goal",
            "明确要求继续工程实现",
            "新的验收目标",
            "summary/gate/policy/template",
            "内部 harness 漂移",
        ]:
            self.assertIn(phrase, text["portable_prompt_zh"])

    def test_initializer_templates_default_to_stop_after_demo_freeze(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            subprocess.run(
                [
                    PYTHON,
                    "skills/loop-engineering/scripts/init_loop_project.py",
                    "--target",
                    str(target),
                ],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            next_state = (target / "state/next.md").read_text(encoding="utf-8")

        for phrase in [
            "Stop / Demo-Freeze Gate",
            "STOP / DEMO_FREEZE",
            "Stop is a valid final state",
            "Demo-Freeze is a valid final state",
            "do not synthesize another Goal",
            "explicitly asks for further implementation",
            "new acceptance target",
            "summary/gate/policy/template",
        ]:
            self.assertIn(phrase, agents)

        for phrase in [
            "STOP / DEMO_FREEZE",
            "Default next action: stop",
            "Ready For Next Loop: no",
            "Engineering may resume only with explicit user request and new acceptance target",
        ]:
            self.assertIn(phrase, next_state)

    def test_public_guidance_treats_state_next_as_candidate_not_command(self) -> None:
        public_paths = [
            "README.md",
            "docs/SHOWCASE.md",
            "docs/PROMOTION.md",
            "portable/README.md",
            "portable/STATE_TEMPLATE/next.md",
            "portable/examples/existing-project.md",
            "skills/loop-engineering/SKILL.md",
            "skills/loop-engineering/references/full-workflow.md",
            "skills/loop-engineering/scripts/init_loop_project.py",
            "portable/AGENTS_TEMPLATE.md",
            "portable/LOOP_ENGINEERING_PROMPT.md",
            "portable/LOOP_ENGINEERING_PROMPT.zh.md",
            "examples/existing-project-continue/user-prompt.md",
            "examples/existing-project-continue/expected-agent-output.md",
            "examples/forward-test-existing-project.md",
            "evals/scenarios/existing-project-continue.yaml",
        ]
        legacy_phrases = [
            "按 state/next.md 继续",
            "Read state/next.md first, execute",
            "This is the intended user habit: initialize once, then continue from state.",
            "execute the highest-priority task",
            "execute only the highest-priority next loop",
            "Choose the highest-priority ready task",
            "execute exactly one bounded next loop from `state/next.md`",
        ]

        combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in public_paths)

        for phrase in legacy_phrases:
            self.assertNotIn(phrase, combined)

        for phrase in [
            "Project Outcome Gate",
            "state/next.md is a candidate next step, not the highest instruction",
            "review state/next.md against the user-visible demo and business acceptance",
            "continue / demo / ship / stop",
        ]:
            self.assertIn(phrase, combined)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("用 Loop Engineering 继续这个项目。", readme)
        self.assertIn("先过 Project Outcome Gate", readme)
        self.assertIn("再决定是否执行 state/next.md", readme)

    def test_execution_strategy_routes_subagents_without_user_prompting_every_step(self) -> None:
        skill = (ROOT / "skills/loop-engineering/SKILL.md").read_text(encoding="utf-8")
        full_workflow = (
            ROOT / "skills/loop-engineering/references/full-workflow.md"
        ).read_text(encoding="utf-8")
        portable_prompt = (ROOT / "portable/LOOP_ENGINEERING_PROMPT.md").read_text(
            encoding="utf-8"
        )
        portable_prompt_zh = (
            ROOT / "portable/LOOP_ENGINEERING_PROMPT.zh.md"
        ).read_text(encoding="utf-8")
        portable_agents = (ROOT / "portable/AGENTS_TEMPLATE.md").read_text(
            encoding="utf-8"
        )

        for text in [skill, full_workflow, portable_prompt, portable_agents]:
            for phrase in [
                "Execution Strategy",
                "Single-agent",
                "Subagent parallelization",
                "Subagent review",
                "No subagent",
                "choose the execution strategy before executing the loop",
            ]:
                self.assertIn(phrase, text)

        for phrase in [
            "执行策略",
            "单 agent",
            "子 agent 并行",
            "子 agent 审查",
            "不使用子 agent",
            "执行 loop 前先选择执行策略",
        ]:
            self.assertIn(phrase, portable_prompt_zh)

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
        self.assertEqual(payload["scenario_count"], 4)
        for scenario in payload["scenarios"]:
            command_list = scenario["command"]
            command = " ".join(command_list)
            self.assertEqual(command_list[0], "codex")
            self.assertIn("exec", command_list)
            self.assertIn("--sandbox workspace-write", command)
            self.assertIn("--ask-for-approval never", command)
            self.assertIn("--skip-git-repo-check", command)

    def test_live_eval_dry_run_expands_model_sample_matrix(self) -> None:
        result = subprocess.run(
            [
                PYTHON,
                "evals/run_live_eval.py",
                "--dry-run",
                "--scenario",
                "premature-implementation",
                "--models",
                "default,gpt-5.5",
                "--samples",
                "2",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )

        payload = json.loads(result.stdout)

        self.assertEqual(payload["status"], "DRY_RUN")
        self.assertEqual(payload["scenario_count"], 1)
        self.assertEqual(payload["model_count"], 2)
        self.assertEqual(payload["sample_count"], 2)
        self.assertEqual(payload["run_count"], 4)
        observed = {(run["model"], run["sample"]) for run in payload["runs"]}
        self.assertEqual(
            observed,
            {
                ("default", 1),
                ("default", 2),
                ("gpt-5.5", 1),
                ("gpt-5.5", 2),
            },
        )
        model_command = next(run["command"] for run in payload["runs"] if run["model"] == "gpt-5.5")
        default_command = next(run["command"] for run in payload["runs"] if run["model"] == "default")
        self.assertIn("--model", model_command)
        self.assertIn("gpt-5.5", model_command)
        self.assertNotIn("--model", default_command)

    def test_live_eval_failure_archive_is_part_of_contract(self) -> None:
        self.assertTrue((ROOT / "evals/reports/failures/.gitkeep").is_file())
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        live_script = (ROOT / "evals/run_live_eval.py").read_text(encoding="utf-8")

        self.assertIn("evals/reports/failures/*.json", gitignore)
        self.assertIn("archive_failure", live_script)
        self.assertIn("--failure-dir", live_script)

    def test_semantic_validator_rejects_state_without_loop_contract(self) -> None:
        validator = load_output_validator()
        scenario = validator.load_scenario(ROOT / "evals/scenarios/vague-idea.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            for relative in scenario["must_create"]:
                path = workspace / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("placeholder question recommended\n", encoding="utf-8")

            errors = validator.validate_workspace(workspace, scenario)

        self.assertTrue(any("semantic contract" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
