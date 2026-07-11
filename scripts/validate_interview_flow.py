#!/usr/bin/env python3
"""Validate the no-plan interview contract documented for orange-start."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "no-plan-interview.json"
REFERENCE = ROOT / "skills" / "orange-start" / "references" / "phase-interview.md"
START = ROOT / "skills" / "orange-start" / "SKILL.md"


def fail(message: str) -> None:
    raise ValueError(message)


def validate_interview_flow(*, emit: bool = True) -> str:
    expected = json.loads(FIXTURE.read_text(encoding="utf-8"))
    reference = REFERENCE.read_text(encoding="utf-8")
    start = START.read_text(encoding="utf-8")

    if expected["max_guided_questions"] != 7:
        fail("fixture must preserve the Orange Build App seven-question limit")
    if "최대 기획 질문 수는 **7개**" not in reference:
        fail("phase-interview.md is missing the seven-question limit")
    if expected["initial_question"] not in reference:
        fail("phase-interview.md is missing the initial idea question")

    cursor = -1
    for phase_id in expected["phase_order"]:
        position = reference.find(f"`{phase_id}`", cursor + 1)
        if position < 0:
            fail(f"phase-interview.md is missing phase: {phase_id}")
        if position <= cursor:
            fail(f"phase order regressed at: {phase_id}")
        cursor = position
        question = expected["generic_questions"][phase_id]
        if question not in reference:
            fail(f"phase-interview.md is missing question for: {phase_id}")

    for kind in expected["deliverable_kinds"]:
        if f"### `{kind}`" not in reference:
            fail(f"phase-interview.md is missing deliverable kind: {kind}")

    for required in (
        "한 번에 질문은 **하나만**",
        "직전 답을 한 문장으로 요약",
        "이미 확인한 내용을 표현만 바꿔 다시 묻지 않는다",
        "선택지 2~3개",
        "source: orange-start-interview",
        "SOURCE_PLAN.md",
        expected["expected_next_reference"],
        "가정은 최대 3개",
        "대표 트리거·비트리거",
        "dry-run, 중복 실행, 재시도, 로그",
        "로딩·빈 상태·오류·성공 상태",
    ):
        if required not in reference:
            fail(f"phase-interview.md is missing behavior: {required}")

    if "phase-interview.md" not in start or "phase-plan.md" not in start:
        fail("orange-start does not route no-plan interviews into phase-plan")

    message = (
        "PASS no-plan-interview.json: phases=7 skip_covered=true "
        "source=SOURCE_PLAN.md next=phase-plan.md"
    )
    if emit:
        print(message)
    return message


if __name__ == "__main__":
    try:
        validate_interview_flow()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
