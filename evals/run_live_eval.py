#!/usr/bin/env python3
"""Run optional live model behavior evals for Loop Engineering."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from validators.validate_loop_output import load_scenario


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "evals/scenarios"
REPORT = ROOT / "evals/reports/live-eval-report.md"


SYSTEM_PROMPT = """You are evaluating the loop-engineering Codex skill.
Respond as the skill should respond. Do not implement code. Include these
sections: mode, confirmed facts, assumptions, current loop, acceptance criteria,
verification method, state files to read or write."""


def response_text(data: dict[str, object]) -> str:
    if isinstance(data.get("output_text"), str):
        return str(data["output_text"])
    chunks: list[str] = []
    for item in data.get("output", []):  # type: ignore[union-attr]
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                chunks.append(str(content.get("text", "")))
    return "\n".join(chunks)


def call_openai(api_key: str, model: str, prompt: str) -> str:
    payload = json.dumps(
        {
            "model": model,
            "input": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        data = json.loads(response.read().decode("utf-8"))
    return response_text(data)


def validate_text(scenario: dict[str, object], text: str) -> list[str]:
    lower = text.lower()
    required = [
        "mode",
        "assumption",
        "current loop",
        "acceptance",
        "verification",
        "state",
    ]
    errors = [f"missing response marker: {item}" for item in required if item not in lower]
    if scenario["id"] == "premature-implementation":
        forbidden = ["package.json", "npm install", "def main", "import react"]
        errors.extend([f"premature implementation marker present: {item}" for item in forbidden if item in lower])
    return errors


def write_report(payload: dict[str, object]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Live Behavior Eval Report",
        "",
        f"- Generated: {payload['generated_at']}",
        f"- Verdict: {payload['status']}",
        f"- Model: {payload.get('model', 'not-run')}",
        "",
        "| scenario | status | errors |",
        "|---|---|---|",
    ]
    for scenario in payload.get("scenarios", []):  # type: ignore[union-attr]
        errors = "; ".join(scenario["errors"]) if scenario["errors"] else ""
        lines.append(f"| {scenario['id']} | {scenario['status']} | {errors} |")
    lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run optional live model evals.")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-5.5"))
    parser.add_argument("--require-token", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        payload = {
            "status": "SKIP",
            "reason": "OPENAI_API_KEY is not set",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "scenarios": [],
        }
        write_report(payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1 if args.require_token else 0

    results = []
    for path in sorted(SCENARIO_DIR.glob("*.yaml")):
        scenario = load_scenario(path)
        try:
            text = call_openai(api_key, args.model, str(scenario["prompt"]))
            errors = validate_text(scenario, text)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            errors = [f"live request failed: {exc}"]
        results.append(
            {
                "id": scenario["id"],
                "status": "PASS" if not errors else "REJECT",
                "errors": errors,
            }
        )

    status = "PASS" if all(result["status"] == "PASS" for result in results) else "REJECT"
    payload = {
        "status": status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "scenario_count": len(results),
        "scenarios": results,
    }
    write_report(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
