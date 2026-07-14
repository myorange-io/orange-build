#!/usr/bin/env python3
"""Validate autonomous repair and human decision routing."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "self-improvement-expectations.json"
REFERENCE = ROOT / "skills" / "orange-start" / "references" / "self-improvement-loop.md"

HUMAN_DECISIONS = {
    "scope_tradeoff",
    "cost",
    "permission_expansion",
    "destructive_change",
    "external_write",
    "account_selection",
}
AUTO_REPAIR = {"test_failure", "requirement_gap", "runtime_error"}


def fail(message: str) -> None:
    raise ValueError(message)


def resolve(spec: dict) -> dict[str, object]:
    signal = spec["signal"]
    if signal == "verified":
        return {"action": "COMPLETE", "ask_user": False}
    if signal in HUMAN_DECISIONS:
        return {"action": "HUMAN_DECISION", "ask_user": True}
    if signal not in AUTO_REPAIR:
        fail(f"unsupported signal: {signal!r}")
    if spec["real_blocker"]:
        return {"action": "HUMAN_ACTION", "ask_user": True}
    if spec["same_failure_count"] >= 2:
        return {"action": "DIAGNOSE", "ask_user": False}
    return {"action": "AUTO_REPAIR", "ask_user": False}


def validate_self_improvement(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected_names = {
        "failing-test-auto-repair",
        "requirement-gap-auto-repair",
        "ui-runtime-error-auto-repair",
        "same-failure-switches-to-diagnosis",
        "scope-tradeoff-needs-human",
        "permission-expansion-needs-human",
        "external-write-needs-human",
        "auth-blocker-needs-one-action",
        "verified-result-completes",
    }
    if set(fixtures) != expected_names:
        fail("self-improvement fixture set changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures.items():
        actual = resolve(fixture["input"])
        if actual != fixture["expected"]:
            fail(f"{name}: {actual} != {fixture['expected']}")
        lines.append(
            f"PASS {name}: action={actual['action']} ask_user={actual['ask_user']}"
        )

    reference = REFERENCE.read_text(encoding="utf-8")
    for required in (
        "최신 고성능 모델",
        "Max와 Pro는 모델명이 아니라 사용 환경의 전제다",
        "AI가 묻지 않고 고칠 것",
        "사람이 결정할 것",
        "DIAGNOSE",
        "단순히 세 번 실패했다는 이유만으로 질문하지 않는다",
        "AI가 테스트·리뷰에서 발견해 자동으로 고친 항목",
    ):
        if required not in reference:
            fail(f"self-improvement-loop.md is missing behavior: {required}")

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_self_improvement()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
