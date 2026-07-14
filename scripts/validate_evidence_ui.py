#!/usr/bin/env python3
"""Validate evidence-gated candidate adoption and UI vocabulary routing."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "evidence-ui-expectations.json"
REFS = ROOT / "skills" / "orange-start" / "references"
DESIGN_REFS = ROOT / "skills" / "orange-design" / "references"


def candidate_gate(spec: dict) -> str:
    if spec["protected_regression"]:
        return "REJECT_ROLLBACK"
    if spec["target_improved"] and spec["evidence"] == "TESTED":
        return "ACCEPT"
    return "REJECT"


def classify_failure(signal: str) -> str:
    return {
        "missing_rule": "CONTRACT_DEFECT",
        "known_rule_not_followed": "EXECUTION_LAPSE",
        "auth_or_external": "EXTERNAL_BLOCKER",
    }[signal]


def ui_term(signal: str) -> str:
    return {
        "modal_background_layer": "scrim",
        "brief_nonblocking_status": "toast",
        "predictable_loading_placeholder": "skeleton",
        "search_select_suggestions": "combobox",
        "no_content_guidance": "empty_state",
        "three_dots_actions": "overflow_menu",
    }[signal]


def validate_evidence_ui(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected_groups = {"candidate_gates", "failure_classes", "ui_terms"}
    if set(fixtures) != expected_groups:
        raise ValueError("evidence/UI fixture groups changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures["candidate_gates"].items():
        actual = candidate_gate(fixture["input"])
        if actual != fixture["expected"]:
            raise ValueError(f"{name}: {actual} != {fixture['expected']}")
        lines.append(f"PASS candidate {name}: {actual}")

    for name, fixture in fixtures["failure_classes"].items():
        actual = classify_failure(fixture["input"])
        if actual != fixture["expected"]:
            raise ValueError(f"{name}: {actual} != {fixture['expected']}")
        lines.append(f"PASS failure {name}: {actual}")

    for name, fixture in fixtures["ui_terms"].items():
        actual = ui_term(fixture["input"])
        if actual != fixture["expected"]:
            raise ValueError(f"{name}: {actual} != {fixture['expected']}")
        lines.append(f"PASS UI {name}: {actual}")

    improvement = (REFS / "self-improvement-loop.md").read_text(encoding="utf-8")
    for required in (
        "trajectory digest",
        "CONTRACT_DEFECT",
        "EXECUTION_LAPSE",
        "EXTERNAL_BLOCKER",
        "후보 변경 채택 게이트",
        "인접",
        "검증 1개",
        "사용자의 기존 변경은 건드리지 않는다",
    ):
        if required not in improvement:
            raise ValueError(f"self-improvement-loop.md is missing: {required}")

    ui_reference = (DESIGN_REFS / "ui-language-and-references.md").read_text(encoding="utf-8")
    for required in (
        "Name That UI",
        "canonical UI 이름",
        "scrim / backdrop",
        "toast / snackbar",
        "combobox / autocomplete",
        "variants가 reroll보다 먼저",
        "functional QA와 visual QA 분리",
        "사이트를 대량 scrape",
    ):
        if required not in ui_reference:
            raise ValueError(f"orange-design ui-language-and-references.md is missing: {required}")

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_evidence_ui()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
