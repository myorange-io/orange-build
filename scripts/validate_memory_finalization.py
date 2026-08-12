#!/usr/bin/env python3
"""Validate completion-level-aware, idempotent MEMORY.md finalization."""

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
    if spec["completion_level"] not in {"local", "shared", "real_work"}:
        fail("invalid completion level")
    if spec["intent"] != "implement":
        return {
            "action": "NO_FINAL_RECORD",
            "memory_required": False,
            "completion_allowed": True,
            "expected_final_blocks": 0,
        }
    if not spec["selected_level_gate_passed"]:
        return {
            "action": "NO_FINAL_RECORD",
            "memory_required": False,
            "completion_allowed": False,
            "expected_final_blocks": 0,
        }
    starts = spec["start_marker_count"]
    ends = spec["end_marker_count"]
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
            fail(f"{document} is missing memory behavior: {snippet}")


def validate_memory_finalization(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected_names = {
        "implement-local-incomplete-no-memory",
        "plan-only-no-memory",
        "implement-local-complete-no-memory",
        "implement-shared-existing-memory-no-marker",
        "implement-real-existing-final-record",
        "implement-complete-duplicate-final-records",
    }
    if set(fixtures) != expected_names:
        fail("memory finalization fixture set changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures.items():
        actual = resolve(fixture["input"])
        if actual != fixture["expected"]:
            fail(f"{name}: {actual} != {fixture['expected']}")
        lines.append(
            f"PASS {name}: level={fixture['input']['completion_level']} "
            f"action={actual['action']} blocks={actual['expected_final_blocks']}"
        )

    memory = (ROOT / "skills" / "orange-start" / "references" / "memory-log.md").read_text(encoding="utf-8")
    require(
        memory,
        (
            "선택한 완료 수준의 구현 완료 증거다",
            "모든 IA STEP이 `APPROVED`",
            "`local`: 로컬 핵심 흐름",
            "`shared`: 공유 URL",
            "`real_work`: 실제 자료·계정·업무 결과",
            START_MARKER,
            END_MARKER,
            "marker 블록이 이미 하나 있으면 새 항목을 append하지 않고",
            "시작 marker와 종료 marker가 각각 정확히 하나",
            "완료 수준: [local / shared / real_work]",
            "완료 게이트는 FAIL",
        ),
        "memory-log.md",
    )

    routes = {
        "orange-start/SKILL.md": ROOT / "skills" / "orange-start" / "SKILL.md",
        "verification-loop.md": ROOT / "skills" / "orange-start" / "references" / "verification-loop.md",
        "phase-verify.md": ROOT / "skills" / "orange-start" / "references" / "phase-verify.md",
        "orange-resume/SKILL.md": ROOT / "skills" / "orange-resume" / "SKILL.md",
        "README.md": ROOT / "README.md",
    }
    for name, path in routes.items():
        require(path.read_text(encoding="utf-8"), ("MEMORY.md", "완료 수준"), name)

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_memory_finalization()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
