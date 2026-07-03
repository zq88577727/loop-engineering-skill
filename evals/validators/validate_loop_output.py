#!/usr/bin/env python3
"""Validate Loop Engineering scenario outputs without external dependencies."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_scenario(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
            if phrase.lower() not in text:
                errors.append(f"{scenario['id']}: {relative} missing phrase {phrase!r}")

    for relative in scenario.get("forbidden_files", []):
        if (workspace / relative).exists():
            errors.append(f"{scenario['id']}: forbidden file exists {relative}")

    return errors


def scenario_result(workspace: Path, scenario: dict[str, Any]) -> dict[str, Any]:
    errors = validate_workspace(workspace, scenario)
    return {
        "id": scenario["id"],
        "status": "PASS" if not errors else "REJECT",
        "errors": errors,
    }
