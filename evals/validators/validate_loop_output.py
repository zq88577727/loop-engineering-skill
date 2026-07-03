#!/usr/bin/env python3
"""Validate Loop Engineering scenario outputs without external dependencies."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_scenario(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").lower()
    except UnicodeDecodeError:
        return ""


def _contains_any(text: str, options: list[str]) -> bool:
    return any(option.lower() in text for option in options)


def _semantic_text(workspace: Path, scenario: dict[str, Any]) -> tuple[str, dict[str, str]]:
    file_text: dict[str, str] = {}
    for relative in scenario.get("must_create", []):
        path = workspace / relative
        if path.is_file():
            file_text[relative] = _read_text(path)
    return "\n".join(file_text.values()), file_text


def _validate_semantic_contract(workspace: Path, scenario: dict[str, Any]) -> list[str]:
    contract = scenario.get("semantic_contract", {})
    if not isinstance(contract, dict) or not contract:
        return []

    errors: list[str] = []
    combined, file_text = _semantic_text(workspace, scenario)

    if contract.get("requires_loop_state"):
        required = ["current goal", "current scope", "priority queue"]
        if not all(term in combined for term in required):
            errors.append(f"{scenario['id']}: semantic contract missing loop state structure")

    if contract.get("requires_next_loop_verification"):
        next_text = file_text.get("state/next.md", "")
        if not (
            "verification" in next_text
            and "stop condition" in next_text
            and _contains_any(next_text, ["pass", "run", "check", "verify", "inspect"])
        ):
            errors.append(f"{scenario['id']}: semantic contract missing verifiable next loop")

    if contract.get("requires_human_inbox"):
        inbox_text = file_text.get("state/inbox.md", "")
        if not (
            "question" in inbox_text
            and _contains_any(inbox_text, ["recommended", "options", "why_human_needed"])
        ):
            errors.append(f"{scenario['id']}: semantic contract missing human decision point")

    if contract.get("captures_clarification_boundary"):
        if not (
            _contains_any(combined, ["clarify", "clarification"])
            and _contains_any(combined, ["not implementation", "do not implement", "no implementation"])
            and _contains_any(combined, ["acceptance criteria", "verification method"])
        ):
            errors.append(f"{scenario['id']}: semantic contract missing clarification boundary")

    if contract.get("continues_existing_state"):
        if not (
            _contains_any(combined, ["continued from state", "continue from existing", "work continued from state"])
            and "bounded loop" in combined
            and _contains_any(combined, ["verification evidence", "run the validator", "pass evidence"])
        ):
            errors.append(f"{scenario['id']}: semantic contract missing existing-state continuation")

    if contract.get("records_failure_prevention"):
        failures_text = file_text.get("state/failures.md", "")
        if not ("failure" in failures_text and "prevention" in failures_text):
            errors.append(f"{scenario['id']}: semantic contract missing failure prevention record")

    if contract.get("rejects_premature_implementation"):
        if not _contains_any(
            combined,
            [
                "no implementation",
                "not accepted for implementation",
                "coding request is rejected",
                "do not implement",
                "deferred",
                "stop before choosing stack",
            ],
        ):
            errors.append(f"{scenario['id']}: semantic contract missing premature-implementation rejection")

    return errors


def validate_workspace(workspace: Path, scenario: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for relative in scenario.get("must_create", []):
        path = workspace / relative
        if not path.is_file():
            errors.append(f"{scenario['id']}: missing required file {relative}")
        elif path.stat().st_size == 0:
            errors.append(f"{scenario['id']}: required file is empty {relative}")

    for relative, phrases in scenario.get("must_contain", {}).items():
        path = workspace / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for phrase in phrases:
            if isinstance(phrase, list):
                if not any(str(option).lower() in text for option in phrase):
                    errors.append(f"{scenario['id']}: {relative} missing one of {phrase!r}")
            elif str(phrase).lower() not in text:
                errors.append(f"{scenario['id']}: {relative} missing phrase {phrase!r}")

    for relative in scenario.get("forbidden_files", []):
        if (workspace / relative).exists():
            errors.append(f"{scenario['id']}: forbidden file exists {relative}")

    errors.extend(_validate_semantic_contract(workspace, scenario))
    return errors


def scenario_result(workspace: Path, scenario: dict[str, Any]) -> dict[str, Any]:
    errors = validate_workspace(workspace, scenario)
    return {
        "id": scenario["id"],
        "status": "PASS" if not errors else "REJECT",
        "errors": errors,
    }
