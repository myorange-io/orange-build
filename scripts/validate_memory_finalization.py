#!/usr/bin/env python3
"""Validate mandatory, idempotent MEMORY.md final-verification recording."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "memory-finalization-expectations.json"
START_MARKER = "<!-- orange-build:final-verification -->"
END_MARKER = "<!-- /orange-build:final-verification -->"


def fail(message: str) -> None:
    raise ValueError(message)


def resolve(spec: dict) -> dict[str, object]:
    intent = spec["intent"]
    final_gate_passed = spec["final_gate_passed"]
    starts = spec["start_marker_count"]
    ends = spec["end_marker_count"]

    if intent != "implement_and_release":
        return {
            "action": "NO_FINAL_RECORD",
            "memory_required": False,
            "completion_allowed": True,
            "expected_final_blocks": 0,
        }
    if not final_gate_passed:
        return {
            "action": "NO_FINAL_RECORD",
            "memory_required": False,
            "completion_allowed": False,
            "expected_final_blocks": 0,
        }
    if not spec["memory_exists"]:
        action = "CREATE_MEMORY_WITH_FINAL_RECORD"
    elif starts == 0 and ends == 0:
        action = "APPEND_ONE_FINAL_RECORD"
    elif starts == 1 and ends == 1:
        action = "UPDATE_EXISTING_FINAL_RECORD"
    else:
        action = "NORMALIZE_TO_ONE_FINAL_RECORD"
    return {
        "action": action,
        "memory_required": True,
        "completion_allowed": True,
        "expected_final_blocks": 1,
    }


def require(text: str, snippets: tuple[str, ...], document: str) -> None:
    for snippet in snippets:
        if snippet not in text:
            fail(f"{document} is missing memory-finalization behavior: {snippet}")


def reject(text: str, snippets: tuple[str, ...], document: str) -> None:
    for snippet in snippets:
        if snippet in text:
            fail(f"{document} keeps conflicting memory behavior: {snippet}")


def validate_memory_finalization(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected_names = {
        "implement-incomplete-no-memory",
        "plan-only-complete-no-memory",
        "implement-complete-no-memory",
        "implement-complete-existing-memory-no-marker",
        "implement-complete-existing-final-record",
        "implement-complete-duplicate-final-records",
    }
    if set(fixtures) != expected_names:
        fail("memory-finalization fixture set changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures.items():
        actual = resolve(fixture["input"])
        if actual != fixture["expected"]:
            fail(f"{name}: {actual} != {fixture['expected']}")
        lines.append(
            f"PASS {name}: action={actual['action']} blocks={actual['expected_final_blocks']}"
        )

    memory = (
        ROOT / "skills" / "orange-start" / "references" / "memory-log.md"
    ).read_text(encoding="utf-8")
    require(
        memory,
        (
            "구현 완료 증거다",
            "결과를 정확히 한 번 기록한다",
            START_MARKER,
            END_MARKER,
            "marker 블록이 이미 하나 있으면 새 항목을 append하지 않고",
            "시작 marker와 종료 marker가 각각 정확히 한 개인지 확인",
            "완료 게이트는 FAIL",
        ),
        "memory-log.md",
    )

    required_routes = {
        "orange-start/SKILL.md": ROOT / "skills" / "orange-start" / "SKILL.md",
        "verification-loop.md": ROOT
        / "skills"
        / "orange-start"
        / "references"
        / "verification-loop.md",
        "phase-verify.md": ROOT
        / "skills"
        / "orange-start"
        / "references"
        / "phase-verify.md",
        "orange-resume/SKILL.md": ROOT / "skills" / "orange-resume" / "SKILL.md",
        "README.md": ROOT / "README.md",
    }
    for name, path in required_routes.items():
        require(path.read_text(encoding="utf-8"), ("MEMORY.md", "최종 검증"), name)

    verify = required_routes["phase-verify.md"].read_text(encoding="utf-8")
    require(
        verify,
        (
            "요청 여부와 관계없이",
            "시작 marker와 종료 marker가 각각 정확히 하나",
            "기존 블록이 있으면 append하지 않고",
            "`PLAN.md`, `MEMORY.md`, 코드·테스트를 같은 최종 커밋",
        ),
        "phase-verify.md",
    )

    for name, path in required_routes.items():
        reject(
            path.read_text(encoding="utf-8"),
            (
                "`MEMORY.md`는 사용자가 과정 기록을 요청했고 별도 기록 게이트도 충족한 경우에만",
                "`MEMORY.md`와 `CASE.md`는 기본으로 만들지 않는다",
            ),
            name,
        )

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_memory_finalization()
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
