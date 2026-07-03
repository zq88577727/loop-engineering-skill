#!/usr/bin/env python3
"""Run deterministic offline behavior evals for Loop Engineering."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from validators.validate_loop_output import load_scenario, scenario_result


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "evals/scenarios"
REPORT = ROOT / "evals/reports/offline-eval-report.md"
INIT_SCRIPT = ROOT / "skills/loop-engineering/scripts/init_loop_project.py"


def write_state(workspace: Path, scenario: dict[str, object]) -> None:
    simulated = scenario.get("simulated_state", {})
    if not isinstance(simulated, dict):
        raise TypeError(f"{scenario['id']}: simulated_state must be an object")
    for relative, content in simulated.items():
        path = workspace / str(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(content), encoding="utf-8")


def run_scenario(scenario_path: Path) -> dict[str, object]:
    scenario = load_scenario(scenario_path)
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / scenario["id"]
        init = subprocess.run(
            [sys.executable, str(INIT_SCRIPT), "--target", str(workspace)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if init.returncode != 0:
            return {
                "id": scenario["id"],
                "status": "REJECT",
                "errors": [f"initializer failed: {init.stderr.strip()}"],
            }
        write_state(workspace, scenario)
        return scenario_result(workspace, scenario)


def write_report(payload: dict[str, object]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Offline Behavior Eval Report",
        "",
        f"- Generated: {payload['generated_at']}",
        f"- Verdict: {payload['status']}",
        f"- Scenario count: {payload['scenario_count']}",
        "",
        "| scenario | status | errors |",
        "|---|---|---|",
    ]
    for scenario in payload["scenarios"]:  # type: ignore[index]
        errors = "; ".join(scenario["errors"]) if scenario["errors"] else ""
        lines.append(f"| {scenario['id']} | {scenario['status']} | {errors} |")
    lines.extend(
        [
            "",
            "## Scope",
            "",
            "This offline eval is deterministic and requires no API token. It validates",
            "the behavior contract, scenario fixtures, generated state files, and",
            "premature-implementation guardrails. Live model behavior is covered by",
            "`evals/run_live_eval.py` and the manual `live-eval.yml` workflow.",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    scenarios = [run_scenario(path) for path in sorted(SCENARIO_DIR.glob("*.yaml"))]
    status = "PASS" if scenarios and all(s["status"] == "PASS" for s in scenarios) else "REJECT"
    payload = {
        "status": status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
    }
    write_report(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
