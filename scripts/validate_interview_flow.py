#!/usr/bin/env python3
"""Validate the current no-plan IA interview contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "no-plan-interview.json"
REFERENCE = ROOT / "skills" / "orange-start" / "references" / "phase-interview.md"
START = ROOT / "skills" / "orange-start" / "SKILL.md"
PHASE_PLAN = ROOT / "skills" / "orange-start" / "references" / "phase-plan.md"


def fail(message: str) -> None:
    raise ValueError(message)


def validate_interview_flow(*, emit: bool = True) -> str:
    expected = json.loads(FIXTURE.read_text(encoding="utf-8"))
    reference = REFERENCE.read_text(encoding="utf-8")
    start = START.read_text(encoding="utf-8")
    phase_plan = PHASE_PLAN.read_text(encoding="utf-8")

    if expected["max_guided_questions"] != 10:
        fail("fixture must use the current ten-question ceiling")
    if "최대 기획 질문 수는 **10개**" not in reference:
        fail("phase-interview.md is missing the ten-question ceiling")
    if expected["initial_question"] not in reference:
        fail("phase-interview.md is missing the initial idea question")

    cursor = -1
    for phase_id in expected["phase_order"]:
        position = reference.find(f"`{phase_id}`", cursor + 1)
        if position <= cursor:
            fail(f"phase order regressed at {phase_id}")
        cursor = position
        if expected["generic_questions"][phase_id] not in reference:
            fail(f"phase-interview.md is missing the current question for {phase_id}")

    for kind in expected["deliverable_kinds"]:
        if f"### `{kind}`" not in reference:
            fail(f"phase-interview.md is missing deliverable kind {kind}")

    question_interface = expected["question_interface"]
    if not all(
        question_interface[key]
        for key in (
            "prefer_structured_when_available",
            "plain_conversation_fallback",
            "one_question_at_a_time",
            "recommended_first",
        )
    ):
        fail("question interface fallbacks must remain enabled")
    if (question_interface["choice_count_min"], question_interface["choice_count_max"]) != (2, 3):
        fail("question choices must remain within two to three")
    for required in (
        "한 번에 질문은 **하나만**",
        "선택지 2~3개",
        "추천안을 첫 번째",
        "구조화 질문 기능이 있으면",
        "일반 대화로 제시",
        "특정 호스트의 질문 도구 이름을 필수로 요구하지 않는다",
    ):
        if required not in reference:
            fail(f"phase-interview.md is missing question behavior: {required}")

    verification = expected["verification_scenarios"]
    template_match = re.search(r"```markdown\n(?P<body>.*?)\n```", reference, flags=re.DOTALL)
    if not template_match:
        fail("phase-interview.md is missing the SOURCE_PLAN template")
    template = template_match.group("body")
    ids = re.findall(r"^### (TEST-\d{2})\s+[—-]", template, flags=re.MULTILINE)
    if ids != verification["expected_ids"] or len(ids) != verification["expected_count"]:
        fail(f"SOURCE_PLAN template tests {ids} != {verification['expected_ids']}")
    for test_id in ids:
        start_at = template.index(f"### {test_id}")
        tail = template[start_at:]
        next_heading = re.search(r"\n### (?:TEST-|다음 개선|첫 번째 작은 완성)|\n## ", tail[1:])
        body = tail if next_heading is None else tail[: next_heading.start() + 1]
        for field in verification["required_fields"]:
            if f"- {field}:" not in body:
                fail(f"{test_id}: missing field {field}")

    task_mapping = expected["ai_skill_task_mapping"]
    if (task_mapping["task_count_min"], task_mapping["task_count_max"]) != (3, 7):
        fail("AI skill cognitive task map must stay within three to seven tasks")
    if task_mapping["reuse_phase_for_scope_confirmation"] != "ai_human_review":
        fail("AI skill scope confirmation must reuse the existing ai_human_review phase")
    if task_mapping["add_new_phase"] or not task_mapping["derive_from_existing_answers"]:
        fail("AI skill mapping must not add an interview phase")
    if not task_mapping["ask_only_when_multiple_ai_candidates"]:
        fail("AI skill scope must only add a question when candidates are genuinely distinct")
    for required in (
        "전체 업무를 3~7개의 인지 과업으로 나눈다",
        "기존 `ai_human_review` 질문을 구체화",
        task_mapping["atomic_sentence"],
        "별도 phase나 11번째 질문을",
    ):
        if required not in reference:
            fail(f"phase-interview.md is missing AI skill mapping behavior: {required}")
    for section in task_mapping["required_source_sections"]:
        if section not in template:
            fail(f"SOURCE_PLAN template is missing AI skill section {section}")
    for field in task_mapping["single_task_fields"]:
        if f"- {field}:" not in template:
            fail(f"SOURCE_PLAN template is missing single-task field {field}")
    if not task_mapping["compose_only_after_standalone_validation"]:
        fail("composition must wait until each atomic skill passes standalone validation")

    for required in (
        "## 누구의 어떤 문제인가요?",
        "## 가장 막히는 순간",
        "## 해결 방식",
        "## 추천 결과물 형태",
        "## 사용 흐름",
        "## 핵심 기능",
        "## 첫 구현의 범위",
        "## 사용할 자료",
        "## AI와 사람의 역할",
        "## 성공 기준",
        "## 실패 신호",
        "## 직접 확인할 3가지",
        "## 함께 구현할 순서",
        "## 가정 및 확인할 점",
    ):
        if required not in template:
            fail(f"SOURCE_PLAN template is missing section {required}")

    if expected["completion_levels"] != ["local", "shared", "real_work"]:
        fail("completion levels changed unexpectedly")
    for level in expected["completion_levels"]:
        if level not in reference:
            fail(f"phase-interview.md is missing completion level {level}")

    materials = (
        "용도",
        "반드시 반영할 내용",
        "그대로 유지할 요소",
        "적용 위치",
        "열린 질문",
    )
    for required in materials:
        if required not in reference:
            fail(f"phase-interview.md is missing material analysis field {required}")

    if "source: orange-start-interview" not in template:
        fail("SOURCE_PLAN template must identify the local interview source")
    if "interview_completion: skip_all" not in phase_plan:
        # phase-plan intentionally treats current local IA plans without reopening the interview.
        if "source: orange-start-interview" not in phase_plan:
            fail("phase-plan.md does not recognize current local IA plans")
    if "phase-interview.md" not in start or "phase-plan.md" not in start:
        fail("orange-start does not route no-plan interviews into phase-plan")

    message = (
        "PASS no-plan-interview.json: phases=7 max_questions=10 tests=3 "
        "choices=2..3 ai_tasks=3..7 atomic=true materials=confirmed completion_levels=3"
    )
    if emit:
        print(message)
    return message


if __name__ == "__main__":
    try:
        validate_interview_flow()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
