#!/usr/bin/env python3
"""Run optional end-to-end Codex session evals for Loop Engineering."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validators.validate_loop_output import load_scenario, scenario_result


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "evals/scenarios"
REPORT = ROOT / "evals/reports/live-eval-report.md"
SKILL = ROOT / "skills/loop-engineering/SKILL.md"
WORKFLOW = ROOT / "skills/loop-engineering/references/full-workflow.md"


def codex_available(binary: str) -> bool:
    return shutil.which(binary) is not None


def has_live_auth() -> bool:
    if os.environ.get("OPENAI_API_KEY") or os.environ.get("CODEX_HOME"):
        return True
    auth = subprocess.run(
        ["codex", "login", "status"],
        text=True,
        capture_output=True,
    )
    return auth.returncode == 0


def build_prompt(scenario: dict[str, Any]) -> str:
    skill_text = SKILL.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    required_files = "\n".join(f"- {path}" for path in scenario.get("must_create", []))
    forbidden_files = "\n".join(f"- {path}" for path in scenario.get("forbidden_files", []))
    return f"""You are running an end-to-end behavior eval for the Loop Engineering skill.

Use the skill instructions below as authoritative. Work only in the current
workspace. Create or update the expected Loop Engineering state files. Do not
create implementation files unless the scenario explicitly allows them.

<loop_engineering_skill>
{skill_text}
</loop_engineering_skill>

<loop_engineering_workflow_reference>
{workflow_text}
</loop_engineering_workflow_reference>

Scenario id: {scenario["id"]}
Expected mode: {scenario.get("expected_mode", "")}
User prompt:
{scenario["prompt"]}

Required behavior:
- Run the Loop Engineering workflow for this prompt.
- Persist the result to state files under this workspace.
- Create or update every required file listed below.
- Do not create any forbidden file listed below.
- End with a concise PASS/REJECT style summary.

Required files:
{required_files}

Forbidden files:
{forbidden_files}
"""


def build_command(binary: str, workspace: Path, prompt: str, model: str | None, output_file: Path) -> list[str]:
    command = [
        binary,
        "--ask-for-approval",
        "never",
        "exec",
        "--cd",
        str(workspace),
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "--output-last-message",
        str(output_file),
        "--",
        prompt,
    ]
    if model:
        command[2:2] = ["--model", model]
    return command


def init_workspace(workspace: Path) -> None:
    (workspace / "README.md").write_text("# Live Eval Workspace\n", encoding="utf-8")


def run_scenario(scenario_path: Path, args: argparse.Namespace) -> dict[str, Any]:
    scenario = load_scenario(scenario_path)
    if args.keep_workspace:
        temp_dir = None
        workspace = Path(tempfile.mkdtemp(prefix=f"loop-live-{scenario['id']}-"))
    else:
        temp_dir = tempfile.TemporaryDirectory(prefix=f"loop-live-{scenario['id']}-")
        workspace = Path(temp_dir.name)
    init_workspace(workspace)
    output_file = workspace / "codex-final-message.txt"
    prompt = build_prompt(scenario)
    command = build_command(args.codex_binary, workspace, prompt, args.model, output_file)
    run = subprocess.run(
        command,
        cwd=workspace,
        text=True,
        capture_output=True,
        timeout=args.timeout,
    )
    errors: list[str] = []
    if run.returncode != 0:
        errors.append(f"codex exec failed with exit {run.returncode}: {run.stderr.strip()}")
    errors.extend(scenario_result(workspace, scenario)["errors"])
    if not output_file.is_file():
        errors.append("codex final message file was not created")
    status = "PASS" if not errors else "REJECT"
    if temp_dir is not None and (status == "PASS" or not args.keep_workspace):
        temp_dir.cleanup()
    return {
        "id": scenario["id"],
        "status": status,
        "errors": errors,
        "workspace": str(workspace),
    }


def scenario_paths(selected: str | None) -> list[Path]:
    paths = sorted(SCENARIO_DIR.glob("*.yaml"))
    if selected is None:
        return paths
    return [path for path in paths if path.stem == selected]


def dry_run_payload(args: argparse.Namespace) -> dict[str, Any]:
    scenarios = []
    for path in scenario_paths(args.scenario):
        scenario = load_scenario(path)
        workspace = Path("/tmp") / f"loop-live-{scenario['id']}"
        output_file = workspace / "codex-final-message.txt"
        command = build_command(
            args.codex_binary,
            workspace,
            build_prompt(scenario),
            args.model,
            output_file,
        )
        scenarios.append({"id": scenario["id"], "command": command})
    return {
        "status": "DRY_RUN",
        "runner": "codex exec",
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
    }


def write_report(payload: dict[str, Any]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Live Behavior Eval Report",
        "",
        f"- Generated: {payload['generated_at']}",
        f"- Verdict: {payload['status']}",
        f"- Runner: {payload.get('runner', 'codex exec')}",
        f"- Model: {payload.get('model', 'default')}",
        "",
        "| scenario | status | errors |",
        "|---|---|---|",
    ]
    for scenario in payload.get("scenarios", []):
        errors = "; ".join(scenario["errors"]) if scenario.get("errors") else ""
        lines.append(f"| {scenario['id']} | {scenario['status']} | {errors} |")
    lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run optional live Codex session evals.")
    parser.add_argument("--codex-binary", default=os.environ.get("CODEX_BINARY", "codex"))
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL"))
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("CODEX_LIVE_EVAL_TIMEOUT", "600")))
    parser.add_argument("--require-token", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--scenario", help="Run one scenario id instead of all scenarios.")
    parser.add_argument("--keep-workspace", action="store_true", help="Keep failed live eval workspaces for inspection.")
    args = parser.parse_args()

    if args.dry_run:
        payload = dry_run_payload(args)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if not codex_available(args.codex_binary):
        payload = {
            "status": "SKIP",
            "reason": f"{args.codex_binary!r} was not found on PATH",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "runner": "codex exec",
            "scenarios": [],
        }
        write_report(payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1 if args.require_token else 0

    if not has_live_auth():
        payload = {
            "status": "SKIP",
            "reason": "No OPENAI_API_KEY or CODEX_HOME auth context is available",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "runner": "codex exec",
            "scenarios": [],
        }
        write_report(payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1 if args.require_token else 0

    paths = scenario_paths(args.scenario)
    if not paths:
        print(json.dumps({"status": "error", "reason": "scenario-not-found"}, indent=2, sort_keys=True))
        return 1
    scenarios = [run_scenario(path, args) for path in paths]
    status = "PASS" if scenarios and all(result["status"] == "PASS" for result in scenarios) else "REJECT"
    payload = {
        "status": status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runner": "codex exec",
        "model": args.model or "default",
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
    }
    write_report(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
